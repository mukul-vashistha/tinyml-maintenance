# Phase 00: understand the project story

~~~text
YOU ARE HERE
Start -> Problem -> Data -> EDA -> Baseline -> Models -> Other views -> Policy -> Shift
~~~

A set of machines reports sensor readings every six hours. We want to estimate whether a machine may fail within the next 24 operating hours.

That warning can support four actions:

- continue running;
- schedule an inspection;
- stop the machine;
- ask a person to review an uncertain or unsupported case.

You are not expected to understand the repository yet. This phase gives you the story first. You will then open one problem file, follow one small path to code and evidence, and explain what you found.

## What you will produce

By the end, you should be able to answer:

~~~text
What is the system predicting?
Why is advance warning useful?
What actions can the estimate support?
Where is the problem written?
Which code or result shows that the 24-hour label exists?
~~~

The AI coach can draft and save your Phase 00 entry in `.tinyml-lab/student-log.md` after you answer. Review the saved entry and correct anything that does not sound like what you meant.

## Run

~~~bash
uv sync --extra dev
uv run tinyml-maintenance lab doctor
uv run tinyml-maintenance lab status
~~~

These commands check the environment. They do not test whether you understand the project.

## Work with the AI coach

Ask the coach to begin in beginner mode. It should explain the machine problem before asking about files.

If your coding agent discovers repository skills:

~~~text
Use $tinyml-lab-coach in beginner mode and start Phase 00.
~~~

If it does not discover the skill:

~~~text
Read .agents/skills/tinyml-lab-coach/SKILL.md and follow it.
Start Phase 00 in beginner mode.
~~~

The first useful question is simple: why is a warning before failure more useful than detecting the failure only when it happens?

After that discussion, open `PROBLEM.md`. The coach will help you separate the prediction, 24-hour horizon, actions, and costs.

## Explore one small path

Once the story is clear, follow:

~~~text
PROBLEM.md
-> src/tinyml_maintenance/data.py
-> artifacts/results/eda.json
~~~

`PROBLEM.md` states the 24-hour prediction. `_future_labels` in `data.py` creates the label. The EDA result reports how many positive labels the generated data contains.

You may also inspect `tests/test_data.py` to see how tests protect the dataset. Designing a new boundary test is optional in this introductory phase.

## Check

Answer the questions in [CHECKPOINT.md](CHECKPOINT.md). Ask the coach to draft the log entry from your answers, then review the file it writes.

~~~bash
uv run tinyml-maintenance lab check 00
uv run tinyml-maintenance lab next
~~~
