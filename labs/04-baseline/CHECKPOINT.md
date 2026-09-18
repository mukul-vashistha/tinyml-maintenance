# Checkpoint

Hint: ask what the dummy model predicts for every row.

Answer:

1. How can 96 percent accuracy coexist with zero recall?
   The dummy model calls every row healthy. Failures are only about 4% of the data, so
   getting the other 96% ("healthy") right for free still looks like a high accuracy score,
   even though it misses the entire failure set it was built to catch.

2. What question does average precision answer?
   Across every possible threshold, do the true failures rank near the top of the model's
   risk scores?

3. Why do we still need threshold metrics after selecting by average precision?
   Average precision is threshold-independent and good for comparing models, but once you
   commit to a real decision you need to know what happens operationally at the score you
   actually act on, how many alerts fire, how many failures get missed.

4. What does logistic regression reveal that the dummy cannot?
   That a less "accurate" model can be far more valuable, because it actually catches
   failures (high recall) instead of trading all of its accuracy for predicting the
   majority class.

5. Which dataset may select the model, and which dataset must remain untouched?
   The validation set may select the model; `choose_best` in experiments.py picks the
   winner using `validation_average_precision` only. The test set (the plain
   `average_precision`, `accuracy`, `recall`, etc. columns) must remain untouched until
   final evaluation; using it to pick a model would let the project cheat by fitting to
   the test set, and the final numbers would no longer reflect real-world performance.
