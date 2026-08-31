# Phase 07: calibrate risk and choose an action

~~~text
Start -> Problem -> Data -> EDA -> Baseline -> Models -> Other views -> [Policy] -> Shift
~~~

The model returns a score. A higher score can rank one machine above another, but an operator still needs two answers:

1. Does a score such as 0.20 behave like a probability?
2. At what score should the action change?

Calibration handles the first question. Validation costs help with the second.

## What you will learn and produce

You will trace one case through raw score, calibrated probability, selected threshold, and action. You will also explain why calibration rows, policy-selection rows, and held-out test rows have different jobs.

The coach may explain the pipeline and edit your record. You must supply the operating reasoning, including when the system should request human review.

## Run

~~~bash
uv run tinyml-maintenance supervised
uv run pytest tests/test_evaluation.py tests/test_policy.py
~~~

Open [the calibration and policy figure](../../artifacts/figures/calibration-policy.png).

## Ask AI

Ask the agent to trace the validation rows. It should find one subset used for calibration and another used for threshold selection. Sharing the same rows would make the policy estimate too optimistic.

## Think

A missed failure costs ten times a false alarm in this project. That moves the useful threshold away from 0.5. The calibrated threshold is 0.04 because calibrated probabilities and operating costs define the scale together.

## Check

~~~bash
uv run tinyml-maintenance lab check 07
uv run tinyml-maintenance lab next
~~~
