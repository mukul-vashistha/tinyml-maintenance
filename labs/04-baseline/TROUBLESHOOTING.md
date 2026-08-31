# Troubleshooting

Do not compare model rows using test average precision to choose a winner. The comparison stores validation average precision separately for selection.

The threshold shown for each model was selected on validation data using operating costs. It is not the default 0.5 threshold.

Accuracy is not always useless. It is misleading here because one class dominates and the minority class carries the operational risk.
