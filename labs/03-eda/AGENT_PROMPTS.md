# Agent prompts

## Inspect

~~~text
Read artifacts/results/eda.json and inspect the two EDA figures. Also read src/tinyml_maintenance/analysis.py. Do not edit files.

Return at most five observations. For each one, state the next modeling or evaluation decision it could change. Do not suggest another plot unless you can name the decision it would inform.
~~~

## Bounded implementation prompt

~~~text
Propose one additional EDA check only if the current artifacts cannot answer an important question from PROBLEM.md. State the question, the smallest code change, the output, and the acceptance check. Wait for approval before editing.
~~~

## Review

~~~text
Review the proposed EDA work. Remove duplicate views, plots with no decision attached, and any comparison that accidentally uses hidden generator state as production evidence.
~~~
