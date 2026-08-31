# Agent prompts

## Inspect

~~~text
Read src/tinyml_maintenance/experiments.py, evaluation.py, policy.py, and their tests. Use artifacts/results/supervised.json and thresholds.csv. Do not edit files.

Trace how the selected model's raw score becomes a calibrated probability, a cost-selected threshold, and one of four actions. Identify which rows fit each step and where the test set first appears.
~~~

## Bounded implementation prompt

~~~text
Propose one test that fails if calibration and policy selection reuse the same validation machines. Propose another test for the boundary between schedule_inspection and stop_now. Wait for approval before editing.
~~~

## Review

~~~text
Review the policy for a hard-coded 0.5 threshold, calibration on test data, threshold selection on test data, shared calibration and policy rows, and missing human-review behavior.
~~~
