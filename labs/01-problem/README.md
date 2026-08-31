# Phase 01: define the decision

~~~text
Start -> [Problem] -> Data -> EDA -> Baseline -> Models -> Other views -> Policy -> Shift
~~~

A machine is getting hotter. Should the operator keep it running, inspect it, stop it, or ask a person to review the case?

That is the decision. "Train a random forest" is not the decision.

Open [PROBLEM.md](../../PROBLEM.md). Find the prediction time, target, prediction horizon, available evidence, forbidden evidence, and four possible actions.

## What you will learn and produce

The coach will explain each part of a prediction contract before asking you to fill it. You will produce the six-line contract in [TASK.md](TASK.md) and two examples of information that would leak the future.

You may answer in conversation. After the meaning is correct, the coach can format and save the Phase 01 entry from your answers.

## Run

~~~bash
uv run pytest tests/test_data.py
~~~

The tests are useful here because one of them proves that future and hidden columns do not become features.

## Ask AI

Run the inspection prompt before the blueprint prompt. Do not permit a code change in the first conversation.

## Think

Suppose a model sees target_failure_now or leak_future_temperature. Its score may look excellent. Could an operator have known either value at prediction time? If not, the experiment is answering a question no production system can answer.

## Check

~~~bash
uv run tinyml-maintenance lab check 01
uv run tinyml-maintenance lab next
~~~
