# Problem contract

## Decision

At each six-hour observation, estimate whether a machine will fail within the next 24 operating hours.

The estimate supports four actions:

| Action | Intended use |
|---|---|
| Continue | Low calibrated risk |
| Schedule inspection | Moderate risk |
| Stop now | High risk where a missed failure is expensive |
| Human review | Unsupported machine type, shift, or low-confidence evidence |

## Prediction-time evidence

Current and historical telemetry, machine metadata, load, environment, and maintenance history are available. Future telemetry, future maintenance, remaining useful life, latent degradation, and future failure state are forbidden inputs.

## Costs

The default demonstration assigns cost 5 to a false alarm and cost 50 to a missed failure. These are scenario values, not claims about a real factory.

## Primary evaluation

- average precision for rare-event ranking;
- recall and precision at a validation-selected operating threshold;
- Brier score and reliability evidence for probability quality;
- expected operational cost;
- per-machine-type slices;
- risk versus coverage when the system may abstain;
- future-time and unseen-machine-type performance.

## Non-goals

- real factory deployment;
- streaming infrastructure;
- algorithm implementations from scratch;
- a universal predictive-maintenance benchmark;
- causal claims from model feature importance.
