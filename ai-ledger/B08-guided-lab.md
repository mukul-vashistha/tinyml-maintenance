# B08: guided learning lab

## Request to AI

Turn the completed repository into a guided experience for beginners and working professionals. Keep the technical depth, but make every phase show where AI helps, where the engineer decides, what command to run, and what the result means.

The supplied writing rules required natural technical English. They rejected sales language, inflated claims, stock AI phrases, decorative emoji headings, forced rhythm, unsupported facts, and em or en dashes.

## AI proposal

AI proposed a manifest with nine phases, one lab command group, local learner progress, separate inspection and implementation prompts, concept checkpoints, reference explanations, a rewritten article, and technical diagrams for the README.

## Engineering review

The completed implementation remains the reference repository. The guided phases focus on inspection, prediction, review, experiments, and small proposed changes. The final 90-minute challenge is where the learner changes production code independently.

The command line checks repository evidence but does not pretend to grade understanding. The beginner-first coach explains concepts before questioning, reviews the learner's evidence, and may draft the private student log from agreed answers. Later phases reduce that support until the learner owns the engineering judgment.

The article uses real rows from the generated dataset for its running machine example. Numeric claims are rendered from saved artifacts.

## Walkthrough

The full learner path was run from phase 00 through phase 08. It included all experiment commands, focused test files, the split prediction, reference reveal, final shift review, and the full test suite. The final status showed every phase complete.

The completed implementation was checked through both beginner and accelerated coaching paths.

## Complexity review

Ponytail found four ways to shrink the new runtime code. All were accepted:

1. use manifest dictionaries directly instead of a one-use Phase dataclass;
2. remove an unused check option;
3. let argparse validate the top-level command;
4. remove a duplicate check from the scripted learner test.

No dependency was added.

## Evidence

~~~bash
uv run tinyml-maintenance all
uv run pytest
uv run python -m compileall -q src tests
git diff --check
~~~
