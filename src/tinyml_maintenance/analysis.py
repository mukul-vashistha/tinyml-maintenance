"""EDA and unsupervised views over the synthetic fleet."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .data import feature_columns


def _write_json(value: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, default=float, allow_nan=False) + "\n")


def eda(frame: pd.DataFrame, artifact_dir: str | Path) -> dict[str, object]:
    artifact = Path(artifact_dir)
    figure_dir = artifact / "figures"
    result_dir = artifact / "results"
    figure_dir.mkdir(parents=True, exist_ok=True)

    first_positive = frame.index[frame["target_failure_within_24h"].eq(1)][0]
    machine_id = str(frame.loc[first_positive, "machine_id"])
    history = frame[frame["machine_id"].eq(machine_id)]
    position = history.index.get_loc(first_positive)
    story_rows = history.iloc[max(0, position - 3) : position + 4]
    summary = {
        "rows": len(frame),
        "machines": int(frame["machine_id"].nunique()),
        "machine_types": frame["machine_type"].value_counts().sort_index().to_dict(),
        "sites": frame["site"].value_counts().sort_index().to_dict(),
        "failure_rate": float(frame["target_failure_within_24h"].mean()),
        "missing_temperature_rate": float(frame["temperature"].isna().mean()),
        "failure_rate_by_type": frame.groupby("machine_type")["target_failure_within_24h"].mean().to_dict(),
        "failure_rate_by_site": frame.groupby("site")["target_failure_within_24h"].mean().to_dict(),
        "time_range": [str(frame["timestamp"].min()), str(frame["timestamp"].max())],
        "story_machine": {
            "machine_id": machine_id,
            "rows": [
                {
                    "timestamp": str(row.timestamp),
                    "temperature": float(row.temperature),
                    "vibration": float(row.vibration),
                    "load": float(row.load),
                    "failure_within_24h": int(row.target_failure_within_24h),
                }
                for row in story_rows.itertuples()
            ],
        },
    }
    _write_json(summary, result_dir / "eda.json")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    frame["target_failure_within_24h"].value_counts(normalize=True).sort_index().plot.bar(ax=axes[0], color=["#4c78a8", "#e45756"])
    axes[0].set(title="Near-term failure is rare", xlabel="Failure within 24h", ylabel="Share of observations")
    frame.groupby("machine_type")["target_failure_within_24h"].mean().plot.bar(ax=axes[1], color="#f2cf5b")
    axes[1].set(title="Failure rate differs by machine type", xlabel="Machine type", ylabel="Failure rate")
    fig.tight_layout()
    fig.savefig(figure_dir / "eda-failure-distribution.png", dpi=150)
    plt.close(fig)

    plot_frame = frame.sample(min(5000, len(frame)), random_state=42)
    fig, ax = plt.subplots(figsize=(7.5, 5))
    colors = np.where(plot_frame["target_failure_within_24h"].to_numpy() == 1, "#e45756", "#4c78a8")
    ax.scatter(plot_frame["vibration"], plot_frame["temperature"], c=colors, alpha=0.28, s=11)
    ax.set(title="Two sensors overlap across healthy and near-failure states", xlabel="Vibration", ylabel="Temperature")
    fig.tight_layout()
    fig.savefig(figure_dir / "eda-sensor-overlap.png", dpi=150)
    plt.close(fig)
    return summary


def unsupervised(frame: pd.DataFrame, artifact_dir: str | Path, seed: int = 42) -> dict[str, object]:
    artifact = Path(artifact_dir)
    sample = frame.sample(min(3500, len(frame)), random_state=seed).copy()
    usable = [
        column
        for column in feature_columns(sample)
        if sample[column].dtype != "object" and not column.endswith("_delta_6h")
    ]
    matrix = make_pipeline(SimpleImputer(), StandardScaler()).fit_transform(sample[usable])
    pca = PCA(n_components=2, random_state=seed)
    projected = pca.fit_transform(matrix)
    algorithms = {
        "kmeans": KMeans(n_clusters=3, n_init=10, random_state=seed).fit_predict(matrix),
        "dbscan": DBSCAN(eps=3.2, min_samples=18).fit_predict(projected),
        "gmm": GaussianMixture(n_components=3, random_state=seed).fit_predict(matrix),
    }
    latent = sample["latent_regime"].astype("category").cat.codes.to_numpy()
    results: dict[str, object] = {
        "pca_explained_variance": pca.explained_variance_ratio_.tolist(),
        "algorithms": {},
    }
    for name, labels in algorithms.items():
        valid = labels >= 0
        unique = np.unique(labels[valid])
        silhouette = float(silhouette_score(matrix[valid], labels[valid])) if len(unique) > 1 and valid.sum() > len(unique) else None
        results["algorithms"][name] = {
            "clusters": len(unique),
            "noise_rate": float((labels < 0).mean()),
            "silhouette": silhouette,
            "adjusted_rand_vs_latent_regime": float(adjusted_rand_score(latent, labels)),
        }

    result_path = artifact / "results" / "unsupervised.json"
    _write_json(results, result_path)
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2), sharex=True, sharey=True)
    for axis, (name, labels) in zip(axes, algorithms.items()):
        axis.scatter(projected[:, 0], projected[:, 1], c=labels, cmap="tab10", s=8, alpha=0.45)
        axis.set_title(name)
        axis.set_xlabel("PCA 1")
    axes[0].set_ylabel("PCA 2")
    fig.suptitle("Different clustering assumptions produce different views")
    fig.tight_layout()
    fig.savefig(artifact / "figures" / "unsupervised-views.png", dpi=150)
    plt.close(fig)
    return results
