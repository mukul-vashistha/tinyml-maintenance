# Experiment phases: 03 to 06

## Phase 03: let EDA change the next experiment

Explain class balance and sensor overlap before asking for an interpretation. Require each observation to complete:

```text
Because I observed ______, the next experiment should ______.
```

Reject visual descriptions with no decision attached. The rare positive class makes accuracy suspicious. Sensor overlap supports a multivariable baseline and gives a reason to compare linear and nonlinear models.

## Phase 04: understand the baseline

Explain dummy prediction, accuracy, recall, precision, and average precision using the failure-warning story. Then let the learner inspect `supervised.json`.

Ask how roughly 96 percent accuracy can coexist with zero recall. Require the learner to separate model ranking from behavior at a selected threshold and to keep final test evidence out of model selection.

## Phase 05: compare models and splits

Require a saved prediction before showing the split result. Preserve the prediction even when it fails.

Ask which deployment question each split answers. Reject the claim that a split is valid because its score is higher or lower. The primary group split is valid because the stated deployment question concerns machines excluded from training.

Require the learner to explain why random forest remains selected by validation average precision even when a different model has attractive final test evidence.

This phase requires one material review of an AI claim.

## Phase 06: compare different ML questions

Have the learner compare classification, remaining useful life regression, PCA, and clustering by question, output, and failure mode.

Explain that two PCA dimensions preserve only part of the transformed variance. Challenge any business label assigned to a cluster from its plot alone. Ask what external or operational evidence would justify the label.

The learner should supply most of the interpretation. The coach may organize and write the final table and reflection.
