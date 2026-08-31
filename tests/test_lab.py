import json
from pathlib import Path

import pytest

from tinyml_maintenance.lab import GuidedLab, load_phases


def test_manifest_has_a_complete_ordered_journey():
    phases = load_phases()
    assert [phase["id"] for phase in phases] == [f"{number:02d}" for number in range(9)]
    assert all((Path("labs") / f"{phase['id']}-{phase['slug']}" / "README.md").exists() for phase in phases)


def test_start_creates_private_progress_and_log(tmp_path):
    lab = GuidedLab(state_dir=tmp_path / "state")
    message = lab.start()
    assert "Phase 00" in message
    assert lab.state_path.exists()
    assert lab.log_path.exists()
    assert json.loads(lab.state_path.read_text())["current"] == "00"


def test_split_experiment_requires_prediction(tmp_path):
    lab = GuidedLab(state_dir=tmp_path / "state")
    lab.start()
    with pytest.raises(ValueError, match="prediction first"):
        lab.run_split()
    lab.predict_split("A", "The same machines may appear on both sides.")
    output = lab.run_split()
    assert "Random-row logistic AP" in output
    assert "different deployment questions" in output


def test_phase_check_records_completion(tmp_path):
    lab = GuidedLab(state_dir=tmp_path / "state")
    lab.start()
    passed, output = lab.check("00")
    assert passed
    assert "PASS" in output
    assert "00" in lab.load_state()["completed"]


def test_scripted_learner_can_complete_every_phase(tmp_path):
    lab = GuidedLab(state_dir=tmp_path / "state")
    lab.start()
    for phase in lab.phases:
        if phase["id"] == "05":
            lab.predict_split("A", "Rows from one machine may cross the random boundary.")
        finished, _ = lab.next()
        assert finished
    assert lab.load_state()["completed"] == [f"{number:02d}" for number in range(9)]
