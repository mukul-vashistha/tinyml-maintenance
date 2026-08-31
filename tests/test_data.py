import pandas as pd

from tinyml_maintenance.data import SimulationConfig, feature_columns, generate_dataset


def small_config(seed: int = 7) -> SimulationConfig:
    return SimulationConfig(seed=seed, n_machines=24, n_steps=60)


def test_generation_is_deterministic_and_time_ordered():
    first = generate_dataset(small_config())
    second = generate_dataset(small_config())
    pd.testing.assert_frame_equal(first, second)
    assert first.groupby("machine_id")["timestamp"].apply(lambda values: values.is_monotonic_increasing).all()


def test_dataset_contains_rare_positive_events():
    frame = generate_dataset(SimulationConfig(seed=9, n_machines=48, n_steps=90))
    rate = frame["target_failure_within_24h"].mean()
    assert 0.005 < rate < 0.35


def test_prediction_features_exclude_hidden_future_and_identifiers():
    frame = generate_dataset(small_config())
    features = feature_columns(frame)
    assert features
    assert not any(name.startswith(("target_", "latent_", "leak_")) for name in features)
    assert {"machine_id", "timestamp", "step"}.isdisjoint(features)


def test_invalid_horizon_is_rejected():
    config = SimulationConfig(n_machines=24, n_steps=60, step_hours=6, horizon_hours=25)
    try:
        generate_dataset(config)
    except ValueError as error:
        assert "divisible" in str(error)
    else:
        raise AssertionError("invalid horizon should fail")
