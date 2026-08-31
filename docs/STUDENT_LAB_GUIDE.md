# How to use the TinyML student lab

## What are we trying to build?

A group of machines reports temperature, vibration, pressure, load, and other readings every six hours.

At each reading, we want to estimate whether a machine may fail within the next 24 operating hours. The estimate can support four actions:

- continue running;
- schedule an inspection;
- stop the machine;
- ask a person to review an uncertain or unsupported case.

The lab follows that path from beginning to end. You will define the prediction, understand the data, inspect exploratory analysis, compare models, choose evaluation evidence, turn a score into an action, and test what happens when the operating world changes.

You are not expected to understand the repository when you begin. Each phase explains one new part and connects it to what you already learned. The assistance also changes over time. At first, the AI coach explains concepts and helps write your notes. Later, it challenges your model choices and evidence. In the final challenge, you make the engineering decisions yourself.

## A self-guided, hands-on environment

You do not need a live instructor, a study partner, or the technical article. You need:

- the repository;
- Python 3.11 or newer;
- [uv](https://docs.astral.sh/uv/);
- an AI coding environment that can read local files and use a terminal.

Codex, Claude Code, Cursor, and similar coding agents can all be used. Keep the conversation, files, experiments, and tests in the same coding environment. This is easier than copying terminal output into a separate browser chatbot.

The technical article remains available when you want a complete narrative, but the coach must teach the lab without assuming that you read it.

## Start the project

Open the repository in your coding agent or start the agent from the repository root. Then run:

```bash
uv sync --extra dev
uv run tinyml-maintenance lab start
uv run tinyml-maintenance lab doctor
```

If the lab opens a later phase, it found an earlier session. Preserve that record and begin again:

```bash
mv .tinyml-lab .tinyml-lab-previous
uv run tinyml-maintenance lab start
```

Each student should use a separate clone. Local progress lives in `.tinyml-lab/` and is ignored by Git.

## Start the AI coach

The canonical skill is:

```text
.agents/skills/tinyml-lab-coach/SKILL.md
```

### Codex or an agent that discovers repository skills

```text
Use $tinyml-lab-coach in beginner mode and start Phase 00.
```

### Claude Code

The repository also has a Claude entry point under `.claude/skills/`. Use:

```text
Use the tinyml-lab-coach skill in beginner mode and start Phase 00.
```

### Manual fallback

If the agent reports an unknown skill:

```text
Read .agents/skills/tinyml-lab-coach/SKILL.md and follow it.
Start Phase 00 in beginner mode.
```

To resume later:

```text
Use the TinyML lab coach. Check my current phase and continue from my saved log.
```

Working professionals may say:

```text
Use accelerated mode. I understand basic supervised learning and want to focus
on engineering judgment.
```

## What the terminal and coach do

The terminal creates reproducible evidence. It generates data, runs experiments, executes tests, and checks that expected outputs exist.

The coach explains the problem, asks questions, inspects evidence with you, and challenges unsupported conclusions. It can also draft and write your learning record.

Neither part replaces the other. A command can pass while the explanation is wrong. A fluent explanation can sound correct while the code is broken.

## What gets written

The learning record is:

```text
.tinyml-lab/student-log.md
```

You may write it yourself, or the coach may write it from your conversation. When the coach writes, it must:

- use answers you actually gave;
- verify factual claims against repository evidence;
- separate your explanation from the AI explanation;
- record only commands and files that were actually inspected;
- show what remains uncertain;
- let you review and correct the saved entry.

The coach cannot copy a reference answer and pretend that you understood it. Early phases may contain more AI drafting. By the later phases, you should supply most of the engineering reasoning.

Do not edit `.tinyml-lab/progress.json` or generated results by hand.

## How a phase works

The exact balance changes as you progress, but the learning loop is:

```text
Understand the question
-> see one example
-> inspect a small part of the repository
-> run or read evidence
-> explain what it means
-> review the explanation
-> save the learning record
```

At the end of a phase:

```bash
uv run tinyml-maintenance lab check PHASE
uv run tinyml-maintenance lab next
```

Replace `PHASE` with `00`, `01`, and so on. The check proves that required files exist. The conversation and saved evidence show what you understand.

## How the difficulty grows

| Phases | What changes |
|---|---|
| 00 | The coach explains the story and helps you enter the repository |
| 01 to 02 | You define the prediction and learn how time and labels work |
| 03 to 04 | You interpret figures and model metrics |
| 05 to 06 | You make predictions, revise hypotheses, and review AI claims |
| 07 to 08 | You make operating decisions from calibration, policy, and shift evidence |
| Challenge | You inspect, plan, change, test, and hand off an extension independently |

## Phase 00: understand the project story

You begin with the machine, not the directory tree.

The coach explains that readings arrive every six hours and the project predicts possible failure within 24 operating hours. Your first question may be:

```text
Why is a warning before failure more useful than detecting failure only when it happens?
```

After you answer, the coach introduces `PROBLEM.md` and explains the difference between a prediction, horizon, action, and cost. Then you follow one small path:

```text
PROBLEM.md
-> src/tinyml_maintenance/data.py
-> artifacts/results/eda.json
```

A suitable final explanation is short:

```text
The system estimates whether a machine may fail within the next 24 hours.
Advance warning gives an operator time to inspect or stop it. PROBLEM.md states
the question, data.py creates the future-failure label, and eda.json shows that
the generated data contains positive examples.
```

This is an example of the expected depth, not text that must be copied.

## Phase 01: define one prediction

Now turn the story into a precise contract:

```text
Decision:
Prediction time:
Target:
Horizon:
Available evidence:
Possible actions:
```

The coach explains each field before asking you to fill it. It also shows two leakage examples:

- `leak_future_temperature` comes from the future;
- `latent_degradation` exists inside the simulator but is not observed by an operator.

The useful review question is:

```text
Could the operator know this value at the prediction timestamp?
```

The coach may format and save the completed contract after you answer.

## Phase 02: follow one machine through time

Run:

```bash
uv run tinyml-maintenance generate
uv run tinyml-maintenance eda
uv run pytest tests/test_data.py
```

Inspect five consecutive rows for one machine. Learn what stays fixed, what changes, and what resets after failure.

The main distinction is:

```text
A rolling feature uses the current and earlier readings from the same machine.
A future label looks ahead to determine what happens after the current row.
```

Four six-hour observations form the 24-hour horizon. The final four rows for each machine are removed because their complete future window is unavailable.

At this stage, the coach can explain existing tests before asking you to propose one determinism check and one leakage check.

## Phase 03: make EDA change the next experiment

Run:

```bash
uv run tinyml-maintenance eda
```

Inspect the failure distribution and sensor overlap figures. Connect each observation to a decision:

```text
Because I observed ______, the next experiment should ______.
```

Example:

```text
Because failures are rare, the next experiment should not use accuracy alone.
Because sensor values overlap, the next experiment should use a multivariable
baseline rather than one hard temperature rule.
```

A description of a color or shape is not enough unless it changes what you test next.

## Phase 04: understand the baseline

Run:

```bash
uv run tinyml-maintenance supervised
uv run pytest tests/test_evaluation.py tests/test_experiments.py
```

The coach explains accuracy, recall, precision, and average precision before asking for an interpretation.

The dummy model reaches roughly 96 percent accuracy while catching no failures. Your task is to explain how both statements can be true and why the operating problem needs more than accuracy.

Do not conclude that accuracy is always useless. Explain why it is misleading for this class balance and decision.

## Phase 05: compare models and splits

Make a prediction before seeing the experiment:

```bash
uv run tinyml-maintenance lab predict split
uv run tinyml-maintenance lab run split
```

The saved run reports approximately:

```text
Random-row logistic AP: 0.320
Machine-group logistic AP: 0.363
```

Many learners expect the random split to score higher. It does not in this run. Keep the original prediction and explain why the outcome does not make random rows a valid test for unseen machines.

This phase introduces required AI review. You should identify one material claim that needs verification, correction, or qualification.

## Phase 06: compare different ML questions

Run:

```bash
uv run tinyml-maintenance regression
uv run tinyml-maintenance unsupervised
uv run pytest tests/test_analysis.py
```

Compare:

| View | Question | Output | Common mistake |
|---|---|---|---|
| Classification | Is failure near? | Risk score or class | Treating ranking as an action |
| Regression | How much useful life remains? | Estimated hours | Hiding a large absolute error |
| Clustering | Which observations group together? | Cluster assignment | Inventing business labels from a plot |

The first two PCA components preserve about 51.2 percent of transformed variance. They are a partial view. A clean-looking cluster does not prove that it represents "degrading machines."

## Phase 07: turn a score into an action

Run:

```bash
uv run tinyml-maintenance supervised
uv run pytest tests/test_evaluation.py tests/test_policy.py
```

Follow:

```text
raw score -> calibrated probability -> selected threshold -> action
```

Training, calibration, policy selection, and final testing have different jobs. The selected threshold is about 0.04 in the saved run, but it is not a universal maintenance threshold. It follows from the calibrated scale and the scenario costs.

Your record should explain why 0.5 is not automatic, where the threshold comes from, and when the policy asks for human review.

## Phase 08: decide what happens under shift

Run:

```bash
uv run tinyml-maintenance shifts
uv run pytest
```

Review this AI claim:

```text
ROC-AUC remains high on machine type D, so the model is robust.
```

On unseen type D, ranking still contains information, but recall at the transferred threshold is zero. The existing action rule catches no failures in that group.

Decide whether the system should automate, abstain, or request human review. State what new validation evidence would be needed before changing the threshold. The coach may edit your final handoff, but the operating judgment must come from you.

## When you are stuck

Ask the coach to explain the concept with the running machine example. You can also reveal help in stages:

```bash
uv run tinyml-maintenance lab reveal 04 --level hint
uv run tinyml-maintenance lab reveal 04 --level prompt
uv run tinyml-maintenance lab reveal 04 --level reference
```

Replace `04` with your phase. Use the reference after making an attempt. A reference is material for checking your explanation, not a substitute for it.

## The independent challenge

The guided phases slowly remove support. The [90-minute challenge](../challenge/README.md) asks you to add one capability to an unfamiliar codebase.

You will inspect the repository, write a blueprint, use AI for a bounded patch, review the diff, add a meaningful test, run one controlled experiment, record one AI suggestion you corrected or rejected, and leave a reproducible handoff.

At that point, the coach reviews your engineering process. It does not create the initial judgment for you.
