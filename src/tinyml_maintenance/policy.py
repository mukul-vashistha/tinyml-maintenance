"""Translate calibrated risk into a small, explicit operating policy."""

import numpy as np


def assign_actions(
    probability: np.ndarray,
    inspection_threshold: float,
    stop_threshold: float = 0.50,
    abstain_margin: float = 0.01,
    supported: np.ndarray | None = None,
) -> np.ndarray:
    if not 0 < inspection_threshold < stop_threshold < 1:
        raise ValueError("thresholds must satisfy 0 < inspection < stop < 1")
    p = np.asarray(probability, dtype=float)
    if not np.isfinite(p).all() or ((p < 0) | (p > 1)).any():
        raise ValueError("probabilities must be finite and between zero and one")
    support = np.ones(len(p), dtype=bool) if supported is None else np.asarray(supported, dtype=bool)
    if len(support) != len(p):
        raise ValueError("supported mask must match probabilities")
    action = np.full(len(p), "continue", dtype=object)
    action[p >= inspection_threshold] = "schedule_inspection"
    action[p >= stop_threshold] = "stop_now"
    near_boundary = (np.abs(p - inspection_threshold) <= abstain_margin) | (
        np.abs(p - stop_threshold) <= abstain_margin
    )
    action[near_boundary | ~support] = "human_review"
    return action.astype(str)
