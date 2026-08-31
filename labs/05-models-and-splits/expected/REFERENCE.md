# Reference explanation

In this run, random-row logistic average precision is about 0.320 and machine-group logistic average precision is about 0.363. The original hypothesis expected the random split to score higher. It did not.

The result does not validate random rows. Random rows ask about more readings from machines already represented during training. The group split asks about machines excluded from training. The second question matches the primary deployment contract.

Random forest had the highest validation average precision, about 0.374, so the project selected it. Its final test average precision is about 0.471.
