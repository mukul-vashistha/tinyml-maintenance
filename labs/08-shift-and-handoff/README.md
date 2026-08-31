# Phase 08: test shift, abstain, and hand off the work

~~~text
Start -> Problem -> Data -> EDA -> Baseline -> Models -> Other views -> Policy -> [Shift]
~~~

The model worked on held-out machines from the generated fleet. Now we change the world.

One test moves forward in time. Another holds out machine type D. On the unseen type, the model still ranks risky rows above safer rows reasonably well, but the transferred threshold catches no failures.

The model knows something. The old action rule does not work.

## What you will learn and produce

You will review a confident AI robustness claim using ranking metrics, the confusion matrix, recall at the transferred threshold, and action behavior. Then you will decide whether to automate, abstain, or request human review.

The coach may edit and save the handoff, but the decision, remaining risk, and next experiment must come from you. This is the final guided step before independent engineering.

## Run

~~~bash
uv run tinyml-maintenance shifts
uv run pytest
~~~

Read [the shift results](../../artifacts/results/shifts.json) and [the recorded failures](../../FAILURES.md).

## Ask AI

Give the agent the unseen-type ROC-AUC, average precision, confusion matrix, and recall. Ask whether the system can act, not whether one ranking number looks good.

## Think

An abstention is useful when the evidence no longer supports an automated action. It gives the operator a route to human review while the team investigates recalibration, thresholds by machine family, or new training data.

## Check

~~~bash
uv run tinyml-maintenance lab check 08
uv run tinyml-maintenance lab next
~~~

Then open [the independent challenge](../../challenge/README.md).
