# Agent prompts

## Inspect

~~~text
Read src/tinyml_maintenance/analysis.py, the regression and unsupervised result files, and FAILURES.md. Do not edit files.

Explain the separate questions answered by classification, remaining useful life regression, PCA, k-means, DBSCAN, and Gaussian mixtures. Use the saved numbers. Do not assign business names to clusters without external evidence.
~~~

## Bounded implementation prompt

~~~text
Propose one diagnostic that checks whether cluster assignments correspond to an observed variable. Keep it separate from supervised model features and do not claim causal meaning. State the smallest patch and acceptance check, then wait.
~~~

## Review

~~~text
Review the interpretation for cluster storytelling, target leakage, choosing a method because its plot looks clean, and treating two PCA dimensions as the full dataset.
~~~
