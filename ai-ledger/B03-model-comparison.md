# B03 — Model comparison

AI proposed logistic regression, decision tree, random forest, gradient boosting, SVM, KNN, tuning, feature selection, and an experiment tracker.

The engineer retained the model families because each supplies a distinct view. Tuning, tracking infrastructure, custom wrappers, and a model-registry class were rejected. A plain dictionary and sklearn pipelines are sufficient.

All models receive the same group split. Validation average precision selects the candidate; thresholds are also selected on validation evidence. Final test average precision is reported only after selection.

The first patch violated this contract by sorting candidates on test average precision. Tests covered data boundaries and probability shape but did not cover selection provenance. ML review caught the error, and the saved comparison now carries `validation_average_precision` explicitly.

AI also predicted that the naive random-row split would necessarily produce a higher score. The experiment did not support that claim: logistic average precision was lower under the random split in this seeded dataset. The split is still invalid for the stated unseen-machine question. Leakage changes what is being measured; it does not promise a particular direction of score movement.
