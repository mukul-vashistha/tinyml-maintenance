# Agent prompts

## Inspect

~~~text
Read PROBLEM.md, artifacts/results/supervised.json, src/tinyml_maintenance/evaluation.py, and tests/test_evaluation.py. Do not edit files.

Compare the dummy and logistic models using the class balance, confusion matrix, recall, precision, and average precision. Explain why accuracy gives the wrong impression here.
~~~

## Bounded implementation prompt

~~~text
Propose one test that prevents the project from selecting a model by test accuracy. The test must use the current result schema and must fail if model selection reads the test metric. Name the file you would change and wait for approval.
~~~

## Review

~~~text
Review the metric explanation. Check whether it confuses ranking with a threshold decision, uses the held-out test set for selection, or claims that one metric is sufficient for every operating question.
~~~
