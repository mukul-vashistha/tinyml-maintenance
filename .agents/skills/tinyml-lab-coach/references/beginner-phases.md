# Beginner phases: 00 to 02

## Phase 00: understand the project story

Start with this meaning, using natural language rather than reading it as a script:

```text
Machines report sensor readings every six hours. This project estimates whether
a machine may fail within the next 24 operating hours. The estimate can support
continue, schedule inspection, stop now, or human review. We will slowly follow
that path through the repository. You are not expected to understand the files yet.
```

Tell the learner that the phase will produce a short explanation of the problem, why it is useful, and one path to evidence. The coach can write that explanation into the log after the learner answers.

Ask first:

```text
Why might a warning before a failure be more useful than detecting the failure
only when it happens?
```

Then introduce `PROBLEM.md` as the file where the operating question is written. Explain the distinction between:

- prediction: what may happen;
- horizon: how far ahead;
- action: what someone may do;
- cost: how harmful a wrong decision is.

Do not ask about blueprints or AI ledgers in this phase. After the learner understands the story, introduce one small connection:

```text
PROBLEM.md -> src/tinyml_maintenance/data.py -> artifacts/results/eda.json
```

Explain that the problem defines the 24-hour target, `_future_labels` creates it, and the EDA result reports the resulting positive rate. Tests may be mentioned as protection against broken behavior, but designing an off-by-one test is optional enrichment.

If the learner answers with a cost or an action when asked for the prediction, acknowledge that the detail belongs to the project, then teach the distinction. State the actual prediction, whether the machine may fail within the next 24 operating hours, and ask the learner to restate it. Do not use a generic horizon such as "the next N days."

Accept when the learner can explain the project in their own words and identify one piece of evidence.

## Phase 01: define one prediction

Begin with the machine story from Phase 00. Explain that a model cannot be evaluated until one prediction has an exact meaning.

Build the contract one field at a time:

```text
Decision:
Prediction time:
Target:
Horizon:
Available evidence:
Possible actions:
```

Explain a field before asking the learner to fill it. Use `leak_future_temperature` and `latent_degradation` to introduce future and hidden information. Ask whether an operator could know the value at the prediction timestamp.

The learner should explain two leakage risks. The coach may format and save the completed contract after verifying it against `PROBLEM.md`, `data.py`, and `tests/test_data.py`.

## Phase 02: follow one machine through time

Explain what one row means before opening the generator: one machine at one six-hour timestamp.

Guide the learner through five consecutive rows. Ask what stays fixed, what changes, and what may reset after a failure. Then explain:

- four six-hour observations make the 24-hour horizon;
- a rolling feature uses current and earlier observations from the same machine;
- a future label looks ahead and cannot be a feature;
- the final four rows are removed because their full future window is unavailable.

Only after this explanation ask the learner to propose one determinism check and one leakage check. The coach may explain existing tests before asking how a missing boundary test could work.
