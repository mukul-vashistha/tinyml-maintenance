# Agent prompts

## Inspect

~~~text
Read PROBLEM.md, src/tinyml_maintenance/data.py, and tests/test_data.py. Do not edit files.

Explain what one prediction means. State the prediction time, target, horizon, available features, forbidden columns, and operating actions. Point out any mismatch between the written contract, code, and tests.
~~~

## Propose a blueprint

~~~text
Propose the smallest blueprint that would prove the problem contract is enforced. List assumptions, files that may change, tests, and one command that supplies evidence. Do not implement it yet. Do not add infrastructure or dependencies.
~~~

## Review

~~~text
Challenge your blueprint. Which check proves software behavior, and which check proves that the ML question is valid? Remove any task that does not help answer the current decision.
~~~
