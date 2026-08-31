import re
from pathlib import Path

from tinyml_maintenance.reporting import render_blog


def test_blog_renders_without_template_markers_and_local_links_resolve():
    output = render_blog()
    text = output.read_text()
    assert "{{" not in text and "{%" not in text
    assert "Recall: 81.7%" in text
    assert "Precision: 27.7%" in text
    targets = re.findall(r"!?(?:\[[^]]*\])\(([^)]+)\)", text)
    missing = []
    for target in targets:
        if "://" in target or target.startswith("#"):
            continue
        path = (output.parent / target.split("#", 1)[0]).resolve()
        if not path.exists():
            missing.append(str(path))
    assert not missing


def test_every_blueprint_has_a_ledger_or_explicit_shared_record():
    blueprints = {path.stem.split("-", 1)[0] for path in Path("blueprints").glob("*.yaml")}
    ledgers = {path.stem.split("-", 1)[0] for path in Path("ai-ledger").glob("*.md")}
    assert blueprints <= ledgers
