"""Synthetic, time-ordered predictive-maintenance data."""

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SimulationConfig:
    seed: int = 42
    n_machines: int = 120
    n_steps: int = 120
    step_hours: int = 6
    horizon_hours: int = 24

    @property
    def horizon_steps(self) -> int:
        if self.horizon_hours % self.step_hours:
            raise ValueError("horizon_hours must be divisible by step_hours")
        return self.horizon_hours // self.step_hours


TYPE_PARAMS = {
    "A": {"temp": 58, "vibration": 1.0, "pressure": 102, "rpm": 1450, "wear": 0.0100},
    "B": {"temp": 64, "vibration": 1.3, "pressure": 96, "rpm": 1320, "wear": 0.0115},
    "C": {"temp": 53, "vibration": 0.8, "pressure": 108, "rpm": 1580, "wear": 0.0090},
    "D": {"temp": 69, "vibration": 1.6, "pressure": 92, "rpm": 1240, "wear": 0.0130},
}

SITES = ("north", "inland", "coastal")
FORBIDDEN_FEATURE_PREFIXES = ("target_", "latent_", "leak_")
IDENTIFIER_COLUMNS = {"machine_id", "timestamp", "step"}


def _future_labels(failures: np.ndarray, horizon: int, step_hours: int) -> tuple[np.ndarray, np.ndarray]:
    n = len(failures)
    near = np.zeros(n, dtype=np.int8)
    rul = np.full(n, n * step_hours, dtype=float)
    future_failures = np.flatnonzero(failures)
    for i in range(n):
        future = future_failures[future_failures > i]
        if future.size:
            distance = int(future[0] - i)
            rul[i] = distance * step_hours
            near[i] = int(distance <= horizon)
    return near, rul


def _rolling_features(frame: pd.DataFrame) -> pd.DataFrame:
    sensors = ["temperature", "vibration", "pressure", "rpm", "power"]
    grouped = frame.groupby("machine_id", sort=False)
    for sensor in sensors:
        rolling = grouped[sensor].rolling(4, min_periods=1)
        frame[f"{sensor}_mean_24h"] = rolling.mean().reset_index(level=0, drop=True)
        frame[f"{sensor}_std_24h"] = rolling.std().fillna(0).reset_index(level=0, drop=True)
        frame[f"{sensor}_delta_6h"] = grouped[sensor].diff().fillna(0)
    frame["warning_count_24h"] = (
        grouped["warning_event"].rolling(4, min_periods=1).sum().reset_index(level=0, drop=True)
    )
    return frame


def generate_dataset(config: SimulationConfig | None = None) -> pd.DataFrame:
    """Generate telemetry from hidden degradation and fault mechanisms."""

    config = config or SimulationConfig()

    if config.n_machines < 12 or config.n_steps <= config.horizon_steps + 8:
        raise ValueError("simulation is too small for meaningful splits and labels")

    rng = np.random.default_rng(config.seed)
    rows: list[dict[str, object]] = []
    type_choices = np.array(["A", "B", "C", "D"])
    type_probs = np.array([0.34, 0.30, 0.26, 0.10])
    start = pd.Timestamp("2026-01-01", tz="UTC")

    for machine_number in range(config.n_machines):
        machine_id = f"M{machine_number:04d}"
        machine_type = str(rng.choice(type_choices, p=type_probs))
        site = str(rng.choice(SITES))
        params = TYPE_PARAMS[machine_type]
        threshold = float(rng.normal(1.0, 0.055))
        degradation = float(rng.uniform(0.04, 0.22))
        load = float(rng.uniform(0.25, 0.75))
        age_hours = int(rng.integers(500, 8000))
        hours_since_maintenance = int(rng.integers(0, 500))
        failures = np.zeros(config.n_steps, dtype=np.int8)
        machine_rows: list[dict[str, object]] = []

        for step in range(config.n_steps):
            ambient = 24 + 7 * np.sin(2 * np.pi * step / 80) + (4 if site == "coastal" else 0)
            load = float(np.clip(0.78 * load + 0.22 * rng.beta(2.5, 2.0), 0.05, 1.0))
            degradation += params["wear"] * (0.55 + 0.85 * load) * rng.uniform(0.85, 1.18)
            sudden_fault = rng.random() < 0.0008 + 0.0025 * load
            failed = bool(degradation >= threshold or sudden_fault)
            failures[step] = int(failed)

            temperature = params["temp"] + 12 * degradation + 5 * load + 0.15 * ambient + rng.normal(0, 1.4)
            vibration = params["vibration"] + 2.4 * degradation**2 + 0.8 * load + rng.normal(0, 0.12)
            pressure = params["pressure"] - 10 * degradation + 2.5 * load + rng.normal(0, 1.8)
            rpm = params["rpm"] + 230 * load - 90 * degradation + rng.normal(0, 24)
            power = 18 + 13 * load + 5 * degradation + (2 if machine_type == "D" else 0) + rng.normal(0, 0.9)
            sensor_dropout = rng.random() < 0.012 + (0.012 if site == "coastal" else 0)
            warning = int(temperature > params["temp"] + 16 or vibration > params["vibration"] + 2.0)
            regime = "high_load" if load > 0.72 else "idle" if load < 0.28 else "normal"

            machine_rows.append(
                {
                    "machine_id": machine_id,
                    "machine_type": machine_type,
                    "site": site,
                    "timestamp": start + pd.Timedelta(hours=step * config.step_hours),
                    "step": step,
                    "age_hours": age_hours,
                    "hours_since_maintenance": hours_since_maintenance,
                    "load": load,
                    "ambient_temperature": ambient,
                    "temperature": np.nan if sensor_dropout else temperature,
                    "vibration": vibration,
                    "pressure": pressure,
                    "rpm": rpm,
                    "power": power,
                    "sensor_missing": int(sensor_dropout),
                    "warning_event": warning,
                    "latent_degradation": degradation,
                    "latent_regime": regime,
                    "target_failure_now": int(failed),
                }
            )

            age_hours += config.step_hours
            hours_since_maintenance += config.step_hours
            if failed:
                degradation = float(rng.uniform(0.05, 0.16))
                hours_since_maintenance = 0

        near, rul = _future_labels(failures, config.horizon_steps, config.step_hours)
        future_temperature = np.array([r["temperature"] for r in machine_rows], dtype=float)
        future_temperature = np.roll(future_temperature, -config.horizon_steps)
        future_temperature[-config.horizon_steps :] = np.nan
        for i, row in enumerate(machine_rows):
            row["target_failure_within_24h"] = int(near[i])
            row["target_remaining_useful_life"] = float(rul[i])
            row["leak_future_temperature"] = future_temperature[i]
        rows.extend(machine_rows[:-config.horizon_steps])

    frame = pd.DataFrame(rows).sort_values(["machine_id", "timestamp"]).reset_index(drop=True)
    return _rolling_features(frame)


def feature_columns(frame: pd.DataFrame, exclude: Iterable[str] = ()) -> list[str]:
    """Return prediction-time columns and reject hidden/future values by construction.

    ``exclude`` names additional columns to drop (for example, one temporal
    feature group under ablation). It never overrides the identifier and
    leakage filtering above.
    """

    excluded = set(exclude)
    return [
        column
        for column in frame.columns
        if column not in IDENTIFIER_COLUMNS
        and not column.startswith(FORBIDDEN_FEATURE_PREFIXES)
        and column not in excluded
    ]


def save_dataset(frame: pd.DataFrame, path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    return output


def load_dataset(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["timestamp"])
