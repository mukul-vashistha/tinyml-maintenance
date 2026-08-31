"""Reproducible supervised, regression, calibration, policy, and shift experiments."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .data import feature_columns
from .evaluation import (
    calibrate_probabilities,
    calibration_table,
    classification_metrics,
    regression_metrics,
    risk_coverage,
    select_threshold,
    slice_metrics,
)
from .modeling import (
    REGRESSION_TARGET,
    TARGET,
    classifier_pipeline,
    classifiers,
    group_split,
    naive_random_split,
    regressors,
    temporal_split,
    unseen_type_split,
)
from .policy import assign_actions


def _clean_json(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _clean_json(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_clean_json(item) for item in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        return None if not np.isfinite(value) else float(value)
    return value


def _write_json(value: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_clean_json(value), indent=2, allow_nan=False) + "\n")


def select_model(rows: list[dict[str, object]]) -> str:
    """Choose a candidate from validation evidence only."""

    return str(max(rows, key=lambda row: float(row["validation_average_precision"]))["model"])


def _fit_and_score(frame: pd.DataFrame, split: object, name: str, seed: int, false_alarm_cost: float, missed_failure_cost: float):
    features = feature_columns(frame)
    model = classifier_pipeline(split.train, classifiers(seed)[name])
    model.fit(split.train[features], split.train[TARGET])
    validation_probability = model.predict_proba(split.validation[features])[:, 1]
    test_probability = model.predict_proba(split.test[features])[:, 1]
    threshold, threshold_table = select_threshold(
        split.validation[TARGET].to_numpy(), validation_probability, false_alarm_cost, missed_failure_cost
    )
    return model, validation_probability, test_probability, threshold, threshold_table


def supervised(
    frame: pd.DataFrame,
    artifact_dir: str | Path,
    seed: int = 42,
    false_alarm_cost: float = 5,
    missed_failure_cost: float = 50,
) -> dict[str, object]:
    artifact = Path(artifact_dir)
    split = group_split(frame, seed)
    rows = []
    fitted: dict[str, tuple[object, np.ndarray, np.ndarray, float, pd.DataFrame]] = {}
    for name in classifiers(seed):
        model, val_p, test_p, threshold, threshold_table = _fit_and_score(
            frame, split, name, seed, false_alarm_cost, missed_failure_cost
        )
        fitted[name] = (model, val_p, test_p, threshold, threshold_table)
        validation_metrics = classification_metrics(split.validation[TARGET], val_p, threshold)
        rows.append(
            {
                "model": name,
                "validation_average_precision": validation_metrics["average_precision"],
                **classification_metrics(split.test[TARGET], test_p, threshold),
            }
        )

    best_name = select_model(rows)
    comparison = pd.DataFrame(rows).sort_values("validation_average_precision", ascending=False)
    regularization = {}
    for name in ("logistic", "logistic_l1", "logistic_elasticnet"):
        coefficients = fitted[name][0].named_steps["model"].coef_.ravel()
        regularization[name] = {
            "coefficients": len(coefficients),
            "nonzero_coefficients": int((np.abs(coefficients) > 1e-6).sum()),
            "l1_norm": float(np.abs(coefficients).sum()),
            "l2_norm": float(np.sqrt(np.square(coefficients).sum())),
        }
    _, validation_probability, raw_test_probability, _, _ = fitted[best_name]
    validation_machines = sorted(split.validation["machine_id"].unique())
    calibration_machines = set(validation_machines[::2])
    calibration_mask = split.validation["machine_id"].isin(calibration_machines).to_numpy()
    policy_mask = ~calibration_mask
    if split.validation.loc[calibration_mask, TARGET].nunique() < 2 or split.validation.loc[policy_mask, TARGET].nunique() < 2:
        raise ValueError("validation split lacks class coverage for separate calibration and policy selection")
    calibrated_test_probability = calibrate_probabilities(
        split.validation.loc[calibration_mask, TARGET].to_numpy(),
        validation_probability[calibration_mask],
        raw_test_probability,
        "sigmoid",
    )
    calibrated_policy_probability = calibrate_probabilities(
        split.validation.loc[calibration_mask, TARGET].to_numpy(),
        validation_probability[calibration_mask],
        validation_probability[policy_mask],
        "sigmoid",
    )
    calibrated_threshold, cost_table = select_threshold(
        split.validation.loc[policy_mask, TARGET].to_numpy(),
        calibrated_policy_probability,
        false_alarm_cost,
        missed_failure_cost,
    )
    calibrated_metrics = classification_metrics(split.test[TARGET], calibrated_test_probability, calibrated_threshold)
    calibrated_metrics["expected_cost"] = (
        calibrated_metrics["fp"] * false_alarm_cost + calibrated_metrics["fn"] * missed_failure_cost
    ) / len(split.test)
    raw_metrics = classification_metrics(split.test[TARGET], raw_test_probability, calibrated_threshold)
    slice_table = slice_metrics(split.test, calibrated_test_probability, "machine_type", calibrated_threshold)
    calibration = calibration_table(split.test[TARGET].to_numpy(), calibrated_test_probability)
    coverage = risk_coverage(split.test[TARGET].to_numpy(), calibrated_test_probability)
    actions = assign_actions(calibrated_test_probability, calibrated_threshold)

    random_model, _, random_probability, random_threshold, _ = _fit_and_score(
        frame, naive_random_split(frame, seed), "logistic", seed, false_alarm_cost, missed_failure_cost
    )
    del random_model
    random_metrics = classification_metrics(naive_random_split(frame, seed).test[TARGET], random_probability, random_threshold)

    result = {
        "primary_split": "group_by_machine",
        "best_model": best_name,
        "calibration_rows": int(calibration_mask.sum()),
        "policy_selection_rows": int(policy_mask.sum()),
        "comparison": comparison.to_dict(orient="records"),
        "regularization": regularization,
        "calibrated_threshold": calibrated_threshold,
        "raw_at_selected_threshold": raw_metrics,
        "calibrated": calibrated_metrics,
        "action_counts": pd.Series(actions).value_counts().to_dict(),
        "naive_random_logistic": random_metrics,
        "slices": slice_table.to_dict(orient="records"),
    }
    _write_json(result, artifact / "results" / "supervised.json")
    cost_table.to_csv(artifact / "results" / "thresholds.csv", index=False)
    calibration.to_csv(artifact / "results" / "calibration.csv", index=False)
    coverage.to_csv(artifact / "results" / "risk-coverage.csv", index=False)
    slice_table.to_csv(artifact / "results" / "slices.csv", index=False)

    fig, axis = plt.subplots(figsize=(8, 4.5))
    ordered = comparison.sort_values("average_precision")
    axis.barh(ordered["model"], ordered["average_precision"], color="#4c78a8")
    axis.set(title="Model comparison on held-out machines", xlabel="Average precision")
    fig.tight_layout()
    fig.savefig(artifact / "figures" / "model-comparison.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
    axes[0].plot(calibration["predicted"], calibration["observed"], marker="o")
    axes[0].plot([0, 1], [0, 1], linestyle="--", color="grey")
    axes[0].set(title="Calibration", xlabel="Predicted", ylabel="Observed")
    axes[1].plot(cost_table["threshold"], cost_table["expected_cost"])
    axes[1].axvline(calibrated_threshold, linestyle="--", color="#e45756")
    axes[1].set(title="Validation-selected policy", xlabel="Threshold", ylabel="Expected cost / row")
    axes[2].plot(coverage["coverage"], coverage["risk"])
    axes[2].set(title="Automation has a risk curve", xlabel="Coverage", ylabel="Error rate")
    fig.tight_layout()
    fig.savefig(artifact / "figures" / "calibration-policy.png", dpi=150)
    plt.close(fig)
    return result


def regression(frame: pd.DataFrame, artifact_dir: str | Path, seed: int = 42) -> dict[str, object]:
    artifact = Path(artifact_dir)
    split = group_split(frame, seed)
    features = feature_columns(frame)
    rows = []
    for name, estimator in regressors(seed).items():
        model = classifier_pipeline(split.train, estimator)
        model.fit(split.train[features], split.train[REGRESSION_TARGET])
        prediction = model.predict(split.test[features])
        rows.append({"model": name, **regression_metrics(split.test[REGRESSION_TARGET], prediction)})
    result = {"comparison": sorted(rows, key=lambda item: item["mae"])}
    _write_json(result, artifact / "results" / "regression.json")
    return result


def shifts(
    frame: pd.DataFrame,
    artifact_dir: str | Path,
    seed: int = 42,
    false_alarm_cost: float = 5,
    missed_failure_cost: float = 50,
) -> dict[str, object]:
    artifact = Path(artifact_dir)
    results = {}
    for name, split in {
        "future_time": temporal_split(frame),
        "unseen_machine_type": unseen_type_split(frame),
    }.items():
        if split.test.empty or split.train[TARGET].nunique() < 2 or split.validation[TARGET].nunique() < 2:
            results[name] = {"status": "insufficient class coverage"}
            continue
        _, _, probability, threshold, _ = _fit_and_score(
            frame, split, "logistic", seed, false_alarm_cost, missed_failure_cost
        )
        results[name] = classification_metrics(split.test[TARGET], probability, threshold)
    _write_json(results, artifact / "results" / "shifts.json")
    return results
