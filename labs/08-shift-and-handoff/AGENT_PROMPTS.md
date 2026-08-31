# Agent prompts

## Inspect

~~~text
Read artifacts/results/shifts.json, FAILURES.md, src/tinyml_maintenance/modeling.py, and challenge/README.md. Do not edit files.

Evaluate future-time and unseen-machine-type behavior. Separate ranking quality from threshold behavior. Use the confusion matrix. State whether the current policy can automate actions on type D.
~~~

## Bounded extension prompt

~~~text
Propose one 90-minute extension that reduces the unseen-type risk. Choose one capability only. Name the files, tests, experiment, acceptance criteria, and a result that would make you reject the change. Do not implement until I approve the blueprint.
~~~

## Review and handoff

~~~text
Review the completed extension for leakage, test-set tuning, unsupported robustness claims, unnecessary code, and missing documentation. Produce a handoff with commands, evidence, remaining risk, and one next experiment.
~~~
