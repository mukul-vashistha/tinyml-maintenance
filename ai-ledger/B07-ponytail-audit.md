# B07 — Ponytail complexity audit

## Request to AI

Audit the finished repository in read-only mode as a lazy senior engineer. Find only code that can be deleted, replaced by the standard library, or inlined without changing behavior. Do not perform the ML-correctness review in this pass.

## AI proposal

Ponytail 4.9.0 reported seven simplifications:

1. delete an unused `Makefile` that only repeated documented `uv` commands;
2. remove eight `from __future__ import annotations` imports because Python 3.11 is the minimum runtime;
3. delete the uncalled `fit_regressor` helper;
4. inline the test-only `predict_probability` wrapper and remove its NumPy import;
5. replace PyYAML and a flat YAML config with TOML and Python's `tomllib`;
6. remove the unused `inspection_cost` setting;
7. remove the unused package `__version__` constant.

## Human review

Accepted all seven. Each finding was confirmed by repository search before editing. Blueprint files remain YAML because they are human-readable task records and are never parsed by the application, so they require no YAML runtime dependency.

The audit was deliberately run after correctness and ML-validity reviews. Ponytail did not decide the target, split, metric, calibration protocol, or operating policy.

## Evidence

After applying the patch:

```bash
uv lock
uv run tinyml-maintenance all
uv run pytest
python -m compileall -q src tests
git diff --check
```

## Decision

Keep the smaller implementation. The application loses one dependency and several unused surfaces while retaining the same command-line behavior and experiment outputs.

## Follow-up cleanup

The beginner-first lab revision received a second repository-wide pass. It:

- deleted `docs/READER_PATH.md`, which duplicated navigation already present in the README, article, and student guide;
- linked the otherwise unreachable model matrix from Phase 05;
- removed the stale Phase 00 requirement for `AI_USE.md`;
- replaced obsolete article and walkthrough instructions with the implemented coach flow;
- reduced internal documentation to the decisions still needed for maintenance;
- sorted imports and removed redundant casts reported by Ruff.

No dependency or new runtime abstraction was added. Ruff, skill validation, compilation, and all tests pass.
