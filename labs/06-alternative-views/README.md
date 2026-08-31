# Phase 06: use regression and clustering as other views

~~~text
Start -> Problem -> Data -> EDA -> Baseline -> Models -> [Other views] -> Policy -> Shift
~~~

Classification asks whether a failure is near. Regression asks how much useful life may remain. Clustering asks whether the observed machine states form natural groups.

These are different questions. One result does not replace another.

## What you will learn and produce

You will compare classification, remaining useful life regression, and clustering by question, output, and failure mode. The coach will challenge any business meaning assigned from a plot alone.

At this stage, supply most of the interpretation yourself. The coach may organize the comparison table and saved record after reviewing your evidence.

## Run

~~~bash
uv run tinyml-maintenance regression
uv run tinyml-maintenance unsupervised
uv run pytest tests/test_analysis.py
~~~

Inspect:

- [regression results](../../artifacts/results/regression.json)
- [unsupervised results](../../artifacts/results/unsupervised.json)
- [unsupervised views](../../artifacts/figures/unsupervised-views.png)

## Ask AI

Ask for an interpretation tied to the operating question. Do not permit the agent to name clusters from a plot alone.

## Think

The clusters do not recover the simulator's hidden operating regimes cleanly. That is an answer. K-means, DBSCAN, and a Gaussian mixture describe density in different ways, but none proves that the world contains the business categories we hoped to find.

## Check

~~~bash
uv run tinyml-maintenance lab check 06
uv run tinyml-maintenance lab next
~~~
