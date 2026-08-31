# Instructions for AI coding agents

Read `PROBLEM.md`, the relevant file under `blueprints/`, and the existing code path before editing.

- Prefer sklearn, the Python standard library, or an existing repository function over new infrastructure.
- Never use `target_*`, `latent_*`, `leak_*`, identifiers, or future readings as model features.
- Match the split to the deployment question. The primary evaluation must hold out machines; model choice uses validation data; the test set remains untouched until final evaluation.
- Propose a blueprint before a non-trivial patch. Keep each patch bounded and review the diff.
- Test software behavior and ML invariants. A plausible metric is not evidence that the evaluation is valid.
- Record accepted, corrected, and rejected AI suggestions under `ai-ledger/`; record surprising experiments in `FAILURES.md`.
- Review correctness before using Ponytail to remove unnecessary complexity.
- Finish by running `uv run pytest` and the relevant CLI stage. Run `uv run tinyml-maintenance all` when results or the blog may change.
