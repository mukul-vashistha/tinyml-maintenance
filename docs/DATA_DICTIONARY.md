# Data dictionary

## Identity and time

| Column | Availability | Meaning |
|---|---|---|
| `machine_id` | Available, excluded from model | Machine identity used for group splitting |
| `machine_type` | Available | Synthetic machine family A–D |
| `site` | Available | Synthetic operating site |
| `timestamp` | Available, excluded from model | Observation time |
| `step` | Available, excluded from model | Six-hour simulation index |

## Current and historical evidence

`age_hours`, `hours_since_maintenance`, `load`, ambient conditions, five current sensors, sensor-missing and warning indicators, and 24-hour rolling mean/variation/delta features are available at prediction time.

Rolling features include the current observation and prior observations from the same machine. They never include a future row.

## Targets

| Column | Use |
|---|---|
| `target_failure_within_24h` | Primary classification target |
| `target_remaining_useful_life` | Regression target |
| `target_failure_now` | Generator audit only; forbidden input |

## Hidden and deliberately leaked fields

| Column | Reason retained | Model status |
|---|---|---|
| `latent_degradation` | Verify generator behaviour | Forbidden |
| `latent_regime` | Compare clustering to known simulation state | Forbidden |
| `leak_future_temperature` | Demonstrate prediction-time leakage | Forbidden |

`feature_columns()` rejects identifiers and every column beginning with `target_`, `latent_`, or `leak_`.
