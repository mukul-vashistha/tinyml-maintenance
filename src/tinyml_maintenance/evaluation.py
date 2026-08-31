"""Evaluation that connects model outputs to operating questions."""

import numpy as np
import pandas as pd
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    log_loss,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    recall_score,
    roc_auc_score,
)


def classification_metrics(y_true: np.ndarray, probability: np.ndarray, threshold: float = 0.5) -> dict[str, float | int]:
    y = np.asarray(y_true, dtype=int)
    p = np.clip(np.asarray(probability, dtype=float), 1e-9, 1 - 1e-9)
    prediction = (p >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, prediction, labels=[0, 1]).ravel()
    ranking_available = len(np.unique(y)) == 2
    return {
        "accuracy": float(accuracy_score(y, prediction)),
        "balanced_accuracy": float(balanced_accuracy_score(y, prediction)),
        "precision": float(precision_score(y, prediction, zero_division=0)),
        "recall": float(recall_score(y, prediction, zero_division=0)),
        "f1": float(f1_score(y, prediction, zero_division=0)),
        "roc_auc": float(roc_auc_score(y, p)) if ranking_available else float("nan"),
        "average_precision": float(average_precision_score(y, p)) if ranking_available else float("nan"),
        "brier": float(brier_score_loss(y, p)),
        "log_loss": float(log_loss(y, p, labels=[0, 1])),
        "threshold": float(threshold),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def threshold_report(
    y_true: np.ndarray,
    probability: np.ndarray,
    false_alarm_cost: float = 5,
    missed_failure_cost: float = 50,
) -> pd.DataFrame:
    rows = []
    for threshold in np.linspace(0.02, 0.98, 97):
        metrics = classification_metrics(y_true, probability, float(threshold))
        metrics["expected_cost"] = (
            metrics["fp"] * false_alarm_cost + metrics["fn"] * missed_failure_cost
        ) / len(y_true)
        rows.append(metrics)
    return pd.DataFrame(rows)


def select_threshold(
    y_true: np.ndarray,
    probability: np.ndarray,
    false_alarm_cost: float = 5,
    missed_failure_cost: float = 50,
) -> tuple[float, pd.DataFrame]:
    report = threshold_report(y_true, probability, false_alarm_cost, missed_failure_cost)
    best = report.sort_values(["expected_cost", "threshold"]).iloc[0]
    return float(best["threshold"]), report


def slice_metrics(frame: pd.DataFrame, probability: np.ndarray, column: str, threshold: float) -> pd.DataFrame:
    scored = frame[[column, "target_failure_within_24h"]].copy()
    scored["probability"] = probability
    rows = []
    for value, group in scored.groupby(column, observed=True):
        metrics = classification_metrics(group["target_failure_within_24h"], group["probability"], threshold)
        rows.append({column: value, "n": len(group), "positive_rate": group["target_failure_within_24h"].mean(), **metrics})
    return pd.DataFrame(rows)


def calibration_table(y_true: np.ndarray, probability: np.ndarray, bins: int = 10) -> pd.DataFrame:
    data = pd.DataFrame({"actual": y_true, "probability": probability})
    data["bin"] = pd.cut(data["probability"], np.linspace(0, 1, bins + 1), include_lowest=True)
    return (
        data.groupby("bin", observed=False)
        .agg(n=("actual", "size"), predicted=("probability", "mean"), observed=("actual", "mean"))
        .reset_index()
    )


def risk_coverage(y_true: np.ndarray, probability: np.ndarray) -> pd.DataFrame:
    y = np.asarray(y_true, dtype=int)
    p = np.asarray(probability, dtype=float)
    confidence = np.abs(p - 0.5) * 2
    order = np.argsort(-confidence)
    prediction = (p >= 0.5).astype(int)[order]
    errors = (prediction != y[order]).astype(float)
    cumulative_risk = np.cumsum(errors) / np.arange(1, len(errors) + 1)
    coverage = np.arange(1, len(errors) + 1) / len(errors)
    points = np.unique(np.minimum((np.linspace(0.05, 1.0, 20) * len(errors)).astype(int), len(errors)) - 1)
    return pd.DataFrame({"coverage": coverage[points], "risk": cumulative_risk[points], "min_confidence": confidence[order][points]})


def regression_metrics(y_true: np.ndarray, prediction: np.ndarray) -> dict[str, float]:
    return {
        "mae": float(mean_absolute_error(y_true, prediction)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, prediction))),
    }


def calibrate_probabilities(
    validation_y: np.ndarray,
    validation_probability: np.ndarray,
    target_probability: np.ndarray,
    method: str = "sigmoid",
) -> np.ndarray:
    """Fit calibration on validation predictions and apply it to untouched probabilities."""

    val_p = np.clip(np.asarray(validation_probability, dtype=float), 1e-6, 1 - 1e-6)
    target_p = np.clip(np.asarray(target_probability, dtype=float), 1e-6, 1 - 1e-6)
    if method == "sigmoid":
        calibrator = LogisticRegression().fit(np.log(val_p / (1 - val_p)).reshape(-1, 1), validation_y)
        return calibrator.predict_proba(np.log(target_p / (1 - target_p)).reshape(-1, 1))[:, 1]
    if method == "isotonic":
        return IsotonicRegression(out_of_bounds="clip").fit(validation_probability, validation_y).predict(target_probability)
    raise ValueError(f"unknown calibration method: {method}")
