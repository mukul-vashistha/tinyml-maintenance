# Checkpoint

Hint: a split is valid because it matches deployment, not because it produces a lower or higher score.

Answer:

1. Why does the primary split hold out complete machines?
   Holding out complete machines simulates the real deployment question: will this model
   work on a machine it has never seen? If rows from the same machine land on both sides
   of the split, that is data leakage; the model effectively gets to peek at that
   machine's pattern during training, so its validation/test score is inflated and no
   longer tells us anything honest about generalizing to a genuinely new machine.

2. Why is the random split still kept in the project?
   It is not deleted because it answers a different, still-useful question: how well can
   the model predict on more data from machines it has already partly seen? That is a
   valid question in its own right, it is just not the deployment question this project
   cares about, so it is kept as a labeled comparison (`naive_random_logistic`) rather than
   used to pick or evaluate the real model.

3. Why did our prediction about score inflation fail in this generated dataset?
   The AI ledger predicted that leakage from the random split would necessarily produce a
   higher score. In this run it produced a lower one (0.320 vs 0.363 for the machine-group
   split). Leakage does not guarantee a direction of score movement; it could inflate the
   score or depress it. What leakage actually breaks is what the number is measuring: once
   rows leak across the split, the score stops measuring "performance on an unseen
   machine," regardless of whether that broken number happens to be higher or lower.

4. Why does that surprise not change the deployment argument?
   Validity comes from whether the split matches the deployment question, not from which
   split produced a higher or lower score. The random split still lets rows from the same
   machine appear on both sides, so it still cannot answer "will this work on a new
   machine," no matter which way its score happened to move this time. A split that wins
   on the scoreboard by accident is still the wrong evidence for the question we are
   asking.

5. Which evidence selected random forest?
   `validation_average_precision`, never the final test scores. Model selection deliberately
   avoids peeking at test data before final evaluation: if the winning model were chosen by
   looking at test scores, the choice would be tuned to that one held-out sample and the
   reported test performance would overstate how good the model really is. Using a separate
   validation slice keeps the test set as an honest, untouched check at the end.

6. What does the model-comparison blueprint record before implementation, and what does its
   AI ledger record afterward?
   The blueprint (`blueprints/B03-model-comparison.yaml`) is a contract of scope and
   constraints agreed before any code was written: the intended outcome, explicit
   non-goals (including "choosing from test performance alone"), and invariants that must
   hold, such as one shared group split and untouched final test probabilities. The AI
   ledger (`ai-ledger/B03-model-comparison.md`) is a record of what actually happened
   during implementation: what the AI proposed and what got rejected, a bug the AI
   introduced that violated one of the blueprint's own non-goals (sorting candidates by
   test average precision) and how review caught it, and a wrong prediction the AI made
   (that leakage would necessarily raise the score) that the experiment disproved. The
   blueprint is the rule agreed to in advance; the ledger is the evidence of whether that
   rule was followed, broken, and caught.
