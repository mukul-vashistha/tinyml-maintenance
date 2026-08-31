# Experiment contracts

## E01 — Data validity

Hypothesis: the synthetic fleet is deterministic, time ordered, rare-event, and non-trivial.

Controls: fixed seed and configuration. Checks: schema, ordering, class rate, hidden-feature exclusion, and repeated generation equality.

## E02 — Primary supervised comparison

Hypothesis: nonlinear sensor interactions improve ranking over a linear baseline.

Control: one group-by-machine split, shared features, and validation-selected threshold for every model. Model selection: validation average precision. Final comparison: untouched held-out-machine evidence.

## E03 — Split sensitivity

Hypothesis: changing the split changes the question and the measured result.

Comparison: random rows, held-out machines, future time, and unseen machine type. The experiment does not assume which score must be largest.

## E04 — Calibration and cost policy

Hypothesis: a separately calibrated score and validation-selected threshold support lower scenario cost than a default threshold.

Controls: disjoint calibration, policy, and test machines. Outputs: Brier score, reliability bins, threshold table, and risk-coverage curve.

## E05 — Remaining useful life

Hypothesis: nonlinear regressors reduce absolute error relative to linear models on held-out machines.

Limitation: the synthetic target is censored at the generated history boundary and should not be interpreted as a real industrial RUL benchmark.

## E06 — Operating-regime discovery

Hypothesis: unsupervised methods recover at least part of the generator's hidden regimes.

Evaluation: silhouette, noise rate, and adjusted Rand agreement with the hidden regime. The hidden regime is used only for experiment validation, never as a model input.
