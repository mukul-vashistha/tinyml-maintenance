# Phase 03: use EDA to choose the next question

~~~text
Start -> Problem -> Data -> [EDA] -> Baseline -> Models -> Other views -> Policy -> Shift
~~~

AI can produce many plots in one pass. That is easy. The useful question is: which plot could change what we build?

This project keeps two views. One shows how rare failure labels are. The other shows how sensor values overlap between healthy and near-failure rows.

## What you will learn and produce

The coach will explain class balance and distribution overlap before reviewing your interpretation. You will write one observation from each figure and state which next experiment or evaluation choice it changes.

From this phase onward, the evidence should do more of the teaching. Try to interpret the figure before asking for the reference explanation.

## Run

~~~bash
uv run tinyml-maintenance eda
~~~

Open:

- [failure distribution](../../artifacts/figures/eda-failure-distribution.png)
- [sensor overlap](../../artifacts/figures/eda-sensor-overlap.png)
- [EDA summary](../../artifacts/results/eda.json)

## Ask AI

Give the agent the actual summary and figures. Ask which observation changes the next modeling decision. Reject plot ideas that have no decision attached.

## Think

Failures are uncommon, so a model can look accurate by predicting "healthy" almost every time. The sensor distributions also overlap. One threshold on one sensor will not solve the problem.

## Check

~~~bash
uv run tinyml-maintenance lab check 03
uv run tinyml-maintenance lab next
~~~
