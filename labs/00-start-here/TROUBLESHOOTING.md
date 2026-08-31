# Troubleshooting

## The coach starts by asking about files

Ask it to restart Phase 00 in beginner mode and explain the machine problem before repository structure.

## The skill is not discovered

Some coding agents do not discover `.agents/skills/`. Ask the agent to read `.agents/skills/tinyml-lab-coach/SKILL.md` directly. Claude users can use the matching entry under `.claude/skills/`.

## The lab opens a later phase

The lab resumes saved progress. To preserve the old record and begin again:

~~~bash
mv .tinyml-lab .tinyml-lab-previous
uv run tinyml-maintenance lab start
~~~

## A question is unclear

Say what is confusing. The coach should explain the distinction with the running machine example, show one relevant file, and then ask for a short paraphrase. It should not repeat the same question.

## The coach writes an answer you did not give

Ask it to remove that claim. The saved record may be drafted by AI, but it must describe the conversation and evidence honestly.
