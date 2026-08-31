# Reference explanation

The selected random forest has a test average precision of about 0.471. After calibration, the Brier score is about 0.0246. A lower Brier score means the probabilities are closer to observed outcomes.

Validation machines are split evenly: 1,392 rows fit calibration and 1,392 different rows select the operating threshold. At the 0.04 calibrated threshold, recall is about 81.7 percent, precision is about 27.7 percent, and expected cost is about 0.740 per row.

The policy assigns continue, schedule inspection, stop now, or human review. The action counts are evidence about the policy's behavior, not proof that the costs are correct for a real factory.
