# B09 — Temporal feature ablation (delta_6h)

The AI-proposed patch scoped the ablation to a single classifier (logistic
regression) rather than re-running all nine phase-05 classifiers for both
feature sets.

Reviewed and accepted: testing every classifier twice would roughly double
experiment cost for a 90-minute exercise without changing the underlying
question (does delta_6h improve ranking). Logistic regression is one of the
models already reported in supervised.json, so the result stays comparable
to existing validation_average_precision numbers.

No other AI suggestion in this patch was rejected. feature_columns() gained
an additive-only `exclude` parameter (default empty, so behavior is
unchanged when unset), and the comparison uses validation data exclusively,
never the final test set.
