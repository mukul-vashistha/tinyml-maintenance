"""Render the technical blog from verified experiment artifacts."""

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def render_blog(project_root: str | Path = ".") -> Path:
    root = Path(project_root)
    results = root / "artifacts" / "results"
    required = ["eda.json", "supervised.json", "regression.json", "unsupervised.json", "shifts.json"]
    missing = [name for name in required if not (results / name).exists()]
    if missing:
        raise FileNotFoundError(f"run experiments before rendering the blog; missing: {', '.join(missing)}")
    context = {Path(name).stem: _read_json(results / name) for name in required}
    environment = Environment(
        loader=FileSystemLoader(root / "blog"),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    output = root / "blog" / "index.md"
    output.write_text(environment.get_template("index.md.j2").render(**context).rstrip() + "\n")
    return output
