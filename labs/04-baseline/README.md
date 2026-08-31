# Phase 04: build a baseline and choose metrics

~~~text
Start -> Problem -> Data -> EDA -> [Baseline] -> Models -> Other views -> Policy -> Shift
~~~

The dummy model reports about 96 percent accuracy. It finds no failures.

So what happened? Failures make up only a small part of the data. A model can say "healthy" for every row and be right most of the time. That makes accuracy look good while the system does nothing useful.

## What you will learn and produce

The coach will explain the metrics with the failure-warning example. You will compare dummy and logistic results, explain what each number reveals, and choose a model-selection metric without using final test evidence.

The coach can organize the saved entry, but the explanation of why 96 percent accuracy can coexist with zero recall must come from you.

## Run

~~~bash
uv run tinyml-maintenance supervised
uv run pytest tests/test_evaluation.py tests/test_experiments.py
~~~

Read the dummy and logistic rows in [supervised.json](../../artifacts/results/supervised.json).

## Ask AI

Ask the agent to explain the confusion matrix before it recommends a metric. Then ask what logistic regression teaches us even if a nonlinear model later scores higher.

## Think

Average precision tests whether positive cases rise toward the top of the ranking. Recall asks how many failures we catch at a chosen threshold. Precision asks how many alerts are correct. We need all three for different parts of the decision.

## Check

~~~bash
uv run tinyml-maintenance lab check 04
uv run tinyml-maintenance lab next
~~~
