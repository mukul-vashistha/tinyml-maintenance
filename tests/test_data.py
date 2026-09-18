import pandas as pd

from tinyml_maintenance.data import SimulationConfig, _rolling_features, feature_columns, generate_dataset


def small_config(seed: int = 7) -> SimulationConfig:
    return SimulationConfig(seed=seed, n_machines=24, n_steps=60)


def test_generation_is_deterministic_and_time_ordered():
    first = generate_dataset(small_config())
    second = generate_dataset(small_config())
    pd.testing.assert_frame_equal(first, second)
    assert first.groupby("machine_id")["timestamp"].apply(lambda values: values.is_monotonic_increasing).all()


def test_different_seeds_produce_different_data():
    first = generate_dataset(small_config(seed=1))
    second = generate_dataset(small_config(seed=2))
    assert not first.equals(second)


def test_rolling_features_ignore_future_rows():
    frame = generate_dataset(small_config())
    rolling_columns = [
        column
        for column in frame.columns
        if column.endswith(("_mean_24h", "_std_24h", "_delta_6h")) or column == "warning_count_24h"
    ]
    raw = frame.drop(columns=rolling_columns)
    before = _rolling_features(raw.copy())

    machine_rows = raw.index[raw["machine_id"] == raw["machine_id"].iloc[0]]
    earliest_index, latest_index = machine_rows[0], machine_rows[-1]

    mutated = raw.copy()
    mutated.loc[latest_index, "temperature"] += 100
    after = _rolling_features(mutated)

    assert before.loc[earliest_index, "temperature_mean_24h"] == after.loc[earliest_index, "temperature_mean_24h"]


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


def test_feature_columns_can_exclude_a_temporal_group():
    frame = generate_dataset(small_config())
    delta_columns = [column for column in frame.columns if column.endswith("_delta_6h")]
    assert delta_columns

    reduced = feature_columns(frame, exclude=delta_columns)
    assert set(delta_columns).isdisjoint(reduced)

    # excluding one group must not weaken the existing leakage/identifier filtering
    assert not any(name.startswith(("target_", "latent_", "leak_")) for name in reduced)
    assert {"machine_id", "timestamp", "step"}.isdisjoint(reduced)

    # an empty exclusion must reproduce the original, unmodified feature list
    assert feature_columns(frame, exclude=[]) == feature_columns(frame)


def test_invalid_horizon_is_rejected():
    config = SimulationConfig(n_machines=24, n_steps=60, step_hours=6, horizon_hours=25)
    try:
        generate_dataset(config)
    except ValueError as error:
        assert "divisible" in str(error)
    else:
        raise AssertionError("invalid horizon should fail")
