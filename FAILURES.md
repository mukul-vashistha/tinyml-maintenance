# Failures and corrections

## F01 — The neat random-split story did not appear

AI predicted that random-row leakage would necessarily raise logistic average precision. The experiment produced a lower value than the group split for this seed.

Correction: state the defensible conclusion. Random splitting answers a different question because machines overlap. Invalid evidence can be optimistic or pessimistic; direction is not guaranteed.

## F02 — Calibration and policy initially shared validation rows

The first implementation fitted a sigmoid calibrator and selected the action threshold on the same validation observations.

Correction: divide validation machines into a calibration group and a policy-selection group. Keep the final test untouched.

## F03 — Accuracy made the dummy model look best

The dummy classifier achieved high accuracy by predicting no near-term failures. Its recall and F1 were zero.

Correction: use average precision for rare-event ranking, inspect recall and precision at an operating point, and calculate expected cost.

## F04 — New machine type produced good ranking but no alarms

On the unseen-type split, logistic ranking remained informative while the validation-selected threshold produced zero recall.

Correction: separate ranking from policy transfer. An operating threshold learned on known types is not automatically valid for an unseen type. Abstain or collect adaptation data.

## F05 — Clusters did not recover the generator's regimes

K-means and Gaussian mixtures returned three clusters, but adjusted Rand agreement with the hidden operating regime was close to zero. DBSCAN found one group under the documented setting.

Correction: a colourful projection is a view, not proof that useful natural categories were discovered.

## F06 — The first model comparison selected on test performance

The initial experiment ranked models by average precision on the held-out test machines and used that ranking to choose the model for calibration. The code ran and all existing tests passed, but the final test had silently become a model-selection set.

Correction: rank candidates by validation average precision. Use the selected model's test result only for final reporting. Add the validation selection metric to the saved comparison artifact.
