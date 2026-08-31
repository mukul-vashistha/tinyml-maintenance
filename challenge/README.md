# 90-minute extension challenge

You are joining a team that already has a working predictive-maintenance system. The code runs, tests pass, and experiment results are saved. Your job is to extend it safely within 90 minutes.

This is not a speed-coding exercise and you are not expected to understand every file. It tests whether you can enter an unfamiliar ML codebase, use an AI coding agent without blindly trusting it, and leave behind a small change that another engineer can reproduce.

## What you receive

You begin with:

- the complete repository and its existing tests;
- generated experiment results in `artifacts/`;
- earlier engineering decisions in `DECISIONS.md` and `FAILURES.md`;
- examples of scoped work in `blueprints/` and `ai-ledger/`;
- any libraries already declared by the project;
- access to a terminal-based AI coding agent.

You do not need to retrain every model or rewrite the project. Reuse what already works.

## Your task

Add one capability from this backlog, or propose an equivalent capability with a similar scope:

| Capability | Question your work should answer |
|---|---|
| Calibration-drift monitoring | How will we notice when predicted probabilities stop matching observed failure rates? |
| Thresholds per machine family | Should machines with different costs or failure patterns use different action thresholds? |
| Uncertainty-aware abstention | Which cases should the system send to a person instead of making an automatic recommendation? |
| Temporal feature ablation | Which time-based features provide real value, and which merely add complexity? |
| New machine type | Does the existing data and evaluation path support a machine family not seen in the original design? |
| New clustering view | Does the cluster expose a useful operating segment, or is it only a visually interesting grouping? |
| Model serialization | Can a saved model be loaded safely with its features and library compatibility checked? |

Choose only one. A narrow capability with strong evidence is better than several unfinished changes.

## Before the timer starts

Set up the repository and confirm that the existing state is healthy:

~~~bash
uv sync --extra dev
uv run tinyml-maintenance lab doctor
uv run pytest
~~~

Read the [problem contract](../PROBLEM.md), [AI use policy](../AI_USE.md), and [evaluation rubric](RUBRIC.md). Skim one existing blueprint and its matching AI ledger entry. This gives you the repository's working pattern without requiring you to read everything.

## Copy-paste starting prompt

Paste this into your coding agent after choosing a capability:

~~~text
I am completing the 90-minute extension challenge in this repository.
My chosen capability is: <write one capability here>.

Do not edit files yet. Inspect PROBLEM.md, AI_USE.md, the relevant source and
test files, and one similar blueprint and AI ledger entry. Explain the smallest
useful extension point using actual file paths.

Then propose a blueprint containing: outcome, non-goals, files likely to change,
ML or software invariants, one meaningful failure test, one controlled
experiment, and a reproducible demo command. Identify any decision that needs
human judgment instead of guessing it. Keep the proposal small enough to finish
and verify within 90 minutes. Wait for my review before writing code.
~~~

Replace the placeholder with your chosen capability. The agent proposes the path; you decide whether the problem, evidence, metric, and scope make sense.

## Suggested 90-minute schedule

| Time | What you do | Evidence you should leave |
|---:|---|---|
| 0 to 10 min | Inspect the problem, repository map, and relevant implementation | Notes with actual file paths |
| 10 to 20 min | State a hypothesis and write the blueprint | One new file in `blueprints/` |
| 20 to 45 min | Request and review one bounded patch | Small implementation diff |
| 45 to 60 min | Write or strengthen the meaningful test | Test that fails for the broken behavior |
| 60 to 75 min | Run one controlled experiment | Command, result, and interpretation |
| 75 to 85 min | Review correctness, ML validity, and unnecessary complexity | One correction or rejected suggestion in `ai-ledger/` |
| 85 to 90 min | Write the decision and handoff | Reproduction steps and remaining risk |

The schedule is guidance, not a scoring rule. If the existing implementation disproves your first idea, record that and reduce the scope instead of hiding the failure.

## Required process

1. Inspect before editing. Locate the requirement, implementation, existing test, experiment path, and decision record related to your capability.
2. Write the blueprint. Define the outcome and explicit non-goals before asking for code.
3. Make a falsifiable prediction. State what result would support the change and what result would make you reject or revise it.
4. Ask for one bounded patch. Give the agent the blueprint, relevant files, invariants, and command it must pass.
5. Review the patch in separate passes. Check repository fit, software correctness, ML validity, and unnecessary complexity.
6. Test behavior, not merely execution. Include at least one test that catches a realistic broken implementation.
7. Run one controlled experiment. Record the exact command, comparison, result, and limitation.
8. Keep an AI ledger. Record at least one suggestion you corrected, rejected, or narrowed and explain why.
9. Write the decision and handoff. Make it possible for another engineer to reproduce the evidence and continue the work.

## What AI may do

AI may help you:

- map an unfamiliar repository using real file paths;
- propose likely extension points and test cases;
- draft a small patch after the blueprint is approved;
- explain a test failure or compare implementation options;
- look for leakage, brittle assumptions, and unnecessary code;
- draft documentation from results you actually produced.

You remain responsible for:

- deciding what operating problem the capability solves;
- deciding which data is available at prediction time;
- choosing the split, metric, control, and acceptance criteria;
- checking that the code matches the repository and the ML claim;
- deciding whether the result is useful enough to keep;
- disclosing uncertainty and remaining risk.

## Worked example: calibration drift

Suppose you choose calibration-drift monitoring. A weak submission adds a generic drift function and asserts that it returns a number. A stronger submission follows this chain:

1. Hypothesis: a shifted machine population will create a measurable gap between predicted risk and observed failure rate.
2. Existing path: inspect how calibration is computed and where shift results are written.
3. Blueprint: add one drift summary, avoid a new monitoring framework, and preserve existing evaluation behavior.
4. Failure test: construct probabilities and outcomes with a known mismatch, then prove the check detects it.
5. Controlled experiment: compare the original evaluation slice with one shifted slice while keeping the model fixed.
6. Decision: explain whether the signal is actionable, which threshold is provisional, and what production data would still be required.
7. AI ledger: record an agent suggestion you rejected, such as silently retraining the model when the task was only to detect drift.

The important part is the traceability from question to code, test, result, and decision. The exact capability can be different.

## Submission

Submit:

- a working, focused implementation;
- tests, including the meaningful broken case;
- the exact experiment and test commands you ran;
- a result artifact or a concise recorded result;
- one blueprint in `blueprints/`;
- one review record in `ai-ledger/`;
- an engineering decision added to `DECISIONS.md` or an equivalent note;
- a concise handoff covering how to reproduce the work and what remains uncertain.

## Definition of done

You are done when another engineer can answer all of these questions from your submission:

- What operating problem does the extension solve?
- Where does it fit into the existing code?
- Which invariant or failure case does the test protect?
- What did the controlled experiment compare?
- What result did you observe, and what does it not prove?
- What did AI suggest, and what did you correct or reject?
- Which command reproduces the result?
- What is the next risk or unanswered question?

You do not receive credit for code you cannot explain or evidence you cannot reproduce.

Read [the full rubric](RUBRIC.md) before submitting. Target leakage, tuning on the final test set, fabricated results, or an un-runnable submission are automatic rejection conditions.
