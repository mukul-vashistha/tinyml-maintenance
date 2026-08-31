import numpy as np

from tinyml_maintenance.policy import assign_actions


def test_policy_maps_risk_and_abstains_near_boundaries():
    actions = assign_actions(np.array([0.01, 0.06, 0.20, 0.70]), 0.05, 0.50, 0.01)
    assert actions.tolist() == ["continue", "human_review", "schedule_inspection", "stop_now"]


def test_unsupported_case_is_sent_to_human():
    actions = assign_actions(np.array([0.01, 0.8]), 0.05, supported=np.array([True, False]))
    assert actions.tolist() == ["continue", "human_review"]


def test_invalid_policy_is_rejected():
    try:
        assign_actions(np.array([0.2]), 0.7, 0.5)
    except ValueError as error:
        assert "threshold" in str(error)
    else:
        raise AssertionError("invalid thresholds should fail")
