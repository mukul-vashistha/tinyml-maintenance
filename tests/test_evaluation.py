import numpy as np

from tinyml_maintenance.evaluation import (
    calibrate_probabilities,
    classification_metrics,
    risk_coverage,
    select_threshold,
)


def test_metrics_match_manual_confusion_counts():
    metrics = classification_metrics(np.array([0, 0, 1, 1]), np.array([0.1, 0.8, 0.7, 0.2]), 0.5)
    assert (metrics["tn"], metrics["fp"], metrics["fn"], metrics["tp"]) == (1, 1, 1, 1)
    assert metrics["precision"] == 0.5
    assert metrics["recall"] == 0.5


def test_cost_sensitive_threshold_is_selected_on_supplied_data():
    y = np.array([0, 0, 0, 1])
    probability = np.array([0.1, 0.2, 0.4, 0.45])
    threshold, report = select_threshold(y, probability, false_alarm_cost=1, missed_failure_cost=50)
    assert threshold <= 0.45
    assert report.loc[report["threshold"] == threshold, "fn"].iloc[0] == 0


def test_risk_coverage_ends_at_full_empirical_error():
    y = np.array([0, 1, 1, 0, 1])
    probability = np.array([0.1, 0.9, 0.3, 0.6, 0.8])
    report = risk_coverage(y, probability)
    assert report.iloc[-1]["coverage"] == 1.0
    assert np.isclose(report.iloc[-1]["risk"], 2 / 5)


def test_calibration_returns_bounded_probabilities():
    y = np.array([0, 0, 0, 1, 1, 1])
    raw = np.array([0.1, 0.2, 0.4, 0.55, 0.7, 0.9])
    calibrated = calibrate_probabilities(y, raw, np.array([0.05, 0.5, 0.95]))
    assert ((0 <= calibrated) & (calibrated <= 1)).all()


def test_unknown_calibration_method_fails():
    try:
        calibrate_probabilities(np.array([0, 1]), np.array([0.1, 0.9]), np.array([0.5]), "magic")
    except ValueError as error:
        assert "unknown" in str(error)
    else:
        raise AssertionError("unknown calibration method should fail")
