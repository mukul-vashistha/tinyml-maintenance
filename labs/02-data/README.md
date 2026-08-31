# Phase 02: build and inspect the data

~~~text
Start -> Problem -> [Data] -> EDA -> Baseline -> Models -> Other views -> Policy -> Shift
~~~

We do not have a real fleet dataset, so we create one. The generator is not trying to copy every factory. It gives us a controlled place where machines age over time, sensors become noisy, failures remain uncommon, and leakage traps are visible.

## What you will learn and produce

The coach will first explain what one row means. You will then follow five consecutive readings from one machine and explain time, maintenance resets, rolling features, future labels, and the missing final window. Finish by proposing one determinism check and one leakage check.

This is your first focused code-reading phase. Ask the coach to explain a function before it asks you to reason about its boundary behavior.

## Run

~~~bash
uv run tinyml-maintenance generate
uv run tinyml-maintenance eda
uv run pytest tests/test_data.py
~~~

Open [the data dictionary](../../docs/DATA_DICTIONARY.md) after the commands finish.

## Ask AI

Ask the agent what one row means and which columns exist only because this is a simulation. Do not ask for a generic EDA plan.

## Think

Independent rows would be easier to generate. They would also erase the machine history we need for rolling features, future labels, maintenance resets, and honest splits.

## Check

~~~bash
uv run tinyml-maintenance lab check 02
uv run tinyml-maintenance lab next
~~~
