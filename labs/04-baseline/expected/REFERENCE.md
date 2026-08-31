# Reference explanation

The dummy model predicts the majority class. Its accuracy is about 96.3 percent, but its recall and F1 score are zero because it identifies no failures.

The logistic model creates a useful risk ranking, so average precision rises well above the failure rate. Logistic regression also gives us a simple boundary and a baseline for judging whether added nonlinearity earns its complexity.

The project selects a model by validation average precision. Test metrics describe the final selected candidate; they do not choose it.
