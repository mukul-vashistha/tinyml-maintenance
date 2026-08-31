# Milestones

| Milestone | Outcome | Demo command | Freeze boundary |
|---|---|---|---|
| M1 | Reproducible synthetic fleet and safe baseline | `uv run pytest tests/test_data.py tests/test_modeling.py` | Dataset schema and feature policy |
| M2 | Evidence-led EDA | `uv run tinyml-maintenance eda` | EDA questions and split definitions |
| M3 | Supervised and regression comparison | `uv run tinyml-maintenance supervised` | Model shortlist and metrics |
| M4 | Unsupervised views | `uv run tinyml-maintenance unsupervised` | Feature space and latent validation only |
| M5 | Calibration, cost policy, and shift report | `uv run tinyml-maintenance experiments` | Validation-selected policy |
| M6 | Reproducible blog and challenge | `uv run tinyml-maintenance all` | Claims trace to generated artifacts |
