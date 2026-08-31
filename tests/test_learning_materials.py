import re
import xml.etree.ElementTree as ET
from pathlib import Path

LEARNER_FILES = [
    Path("README.md"),
    Path("AI_USE.md"),
    Path("blog/index.md"),
    Path("docs/STUDENT_LAB_GUIDE.md"),
    Path("ai-ledger/B08-guided-lab.md"),
    *Path("labs").glob("**/*.md"),
]


def test_learner_materials_have_resolvable_local_links():
    missing = []
    pattern = re.compile(r"!?(?:\[[^]]*\])\(([^)]+)\)")
    for source in LEARNER_FILES:
        for target in pattern.findall(source.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (source.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                missing.append(f"{source}: {target}")
    assert not missing


def test_each_phase_has_the_full_learning_contract():
    required = {"README.md", "TASK.md", "AGENT_PROMPTS.md", "CHECKPOINT.md", "TROUBLESHOOTING.md"}
    phase_directories = sorted(path for path in Path("labs").iterdir() if path.is_dir())
    assert len(phase_directories) == 9
    for phase in phase_directories:
        assert required <= {path.name for path in phase.iterdir()}
        assert (phase / "expected" / "REFERENCE.md").exists()


def test_student_guide_and_coach_are_part_of_the_repository():
    guide = Path("docs/STUDENT_LAB_GUIDE.md")
    skill = Path(".agents/skills/tinyml-lab-coach/SKILL.md")
    claude_skill = Path(".claude/skills/tinyml-lab-coach/SKILL.md")
    references = [
        Path(".agents/skills/tinyml-lab-coach/references/teaching-method.md"),
        Path(".agents/skills/tinyml-lab-coach/references/rubric-ladder.md"),
        Path(".agents/skills/tinyml-lab-coach/references/beginner-phases.md"),
        Path(".agents/skills/tinyml-lab-coach/references/experiment-phases.md"),
        Path(".agents/skills/tinyml-lab-coach/references/decision-phases.md"),
    ]

    assert skill.exists()
    assert claude_skill.exists()
    assert all(path.exists() for path in references)
    guide_text = guide.read_text()
    assert all(
        f"## Phase {phase_id}:" in guide_text
        for phase_id in ("00", "01", "02", "03", "04", "05", "06", "07", "08")
    )
    assert ".tinyml-lab/student-log.md" in guide_text
    skill_text = skill.read_text()
    assert "explain the machine problem before mentioning repository structure" in skill_text
    assert "You may draft and update `.tinyml-lab/student-log.md`" in skill_text
    assert "Never invent an answer" in skill_text


def test_phase_zero_explains_the_problem_before_repository_structure():
    readme = Path("labs/00-start-here/README.md").read_text()
    checkpoint = Path("labs/00-start-here/CHECKPOINT.md").read_text()

    assert readme.index("sensor readings every six hours") < readme.index("PROBLEM.md")
    assert "You are not expected to understand the repository yet." in readme
    assert "blueprints/" not in checkpoint
    assert "ai-ledger/" not in checkpoint


def test_coach_support_fades_and_ai_drafting_is_disclosed():
    rubric = Path(".agents/skills/tinyml-lab-coach/references/rubric-ladder.md").read_text()
    log_template = Path("labs/STUDENT_LOG_TEMPLATE.md").read_text()

    for level in range(1, 7):
        assert f"## Level {level}:" in rubric
    assert "Drafted by AI from my answers and reviewed by me" in log_template
    assert "Remove anything you did not say, inspect, run, or understand." in log_template


def test_learner_prose_avoids_high_signal_ai_writing_patterns():
    text = "\n".join(path.read_text() for path in LEARNER_FILES)
    assert not re.search(r"[—–“”]", text)
    assert not re.search(
        r"(?i)\b(delv(?:e|ing)|tapestry|testament|pivotal|seamless|vibrant|"
        r"underscores?|showcases?|fostering)\b|"
        r"I hope this helps|let me know|without further ado|let's dive|"
        r"here's what you need to know|at its core|the real question is",
        text,
    )


def test_readme_diagrams_are_valid_svg():
    for path in Path("docs/images").glob("*.svg"):
        root = ET.parse(path).getroot()
        assert root.tag.endswith("svg")
