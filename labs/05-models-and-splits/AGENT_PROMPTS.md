# Agent prompts

## Inspect

~~~text
Read src/tinyml_maintenance/modeling.py, src/tinyml_maintenance/experiments.py, tests/test_modeling.py, and artifacts/results/supervised.json. Do not edit files.

Explain what each split represents in deployment terms. Then explain what each model family can reveal. Do not choose a model from the test metrics.
~~~

## Bounded implementation prompt

~~~text
Propose one small test that proves no machine appears in more than one group split. Then propose one test that proves model selection depends only on validation_average_precision. Do not change production code unless a test exposes a real defect.
~~~

## Review

~~~text
Review the model selection path. Look for test-set selection, preprocessing fitted outside the pipeline, machine overlap, future columns, and a conclusion that changes after seeing the random split result.
~~~
