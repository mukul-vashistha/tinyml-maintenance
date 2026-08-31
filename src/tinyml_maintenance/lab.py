"""State and commands for the guided learning lab."""

import json
import shutil
import sys
import tomllib
from pathlib import Path


def load_phases(root: str | Path = ".") -> list[dict]:
    manifest = tomllib.loads((Path(root) / "labs" / "manifest.toml").read_text())
    return manifest["phases"]


class GuidedLab:
    def __init__(self, root: str | Path = ".", state_dir: str | Path | None = None):
        self.root = Path(root)
        self.state_dir = Path(state_dir) if state_dir else self.root / ".tinyml-lab"
        self.state_path = self.state_dir / "progress.json"
        self.log_path = self.state_dir / "student-log.md"
        self.phases = load_phases(self.root)

    def _new_state(self) -> dict:
        return {"version": 1, "current": "00", "completed": [], "predictions": {}}

    def load_state(self) -> dict:
        return json.loads(self.state_path.read_text()) if self.state_path.exists() else self._new_state()

    def save_state(self, state: dict) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(state, indent=2) + "\n")

    def phase(self, phase_id: str) -> dict:
        try:
            return next(phase for phase in self.phases if phase["id"] == phase_id.zfill(2))
        except StopIteration as error:
            valid = ", ".join(phase["id"] for phase in self.phases)
            raise ValueError(f"unknown phase {phase_id}; choose one of: {valid}") from error

    def start(self) -> str:
        if not self.state_path.exists():
            self.save_state(self._new_state())
        if not self.log_path.exists():
            self.state_dir.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.root / "labs" / "STUDENT_LOG_TEMPLATE.md", self.log_path)
        return self.phase_message(self.phase(self.load_state()["current"]))

    def phase_message(self, phase: dict) -> str:
        directory = f"{phase['id']}-{phase['slug']}"
        return "\n".join(
            [
                "TinyML maintenance guided lab",
                "=" * 34,
                f"Phase {phase['id']} of {self.phases[-1]['id']}: {phase['title']}",
                f"Question: {phase['question']}",
                f"Time: about {phase['minutes']} minutes",
                "",
                f"Read: labs/{directory}/README.md",
                f"Then run: uv run tinyml-maintenance lab check {phase['id']}",
            ]
        )

    def doctor(self) -> tuple[bool, str]:
        checks = {
            "Python 3.11 or newer": sys.version_info >= (3, 11),
            "project configuration": (self.root / "configs" / "default.toml").exists(),
            "lab manifest": (self.root / "labs" / "manifest.toml").exists(),
            "problem contract": (self.root / "PROBLEM.md").exists(),
            "test suite": (self.root / "tests").is_dir(),
        }
        lines = [f"{'PASS' if passed else 'FAIL'}  {name}" for name, passed in checks.items()]
        return all(checks.values()), "\n".join(lines)

    def show(self, phase_id: str) -> str:
        phase = self.phase(phase_id)
        readme = self.root / "labs" / f"{phase['id']}-{phase['slug']}" / "README.md"
        return f"{readme}\n\n{readme.read_text().rstrip()}"

    def check(self, phase_id: str) -> tuple[bool, str]:
        phase = self.phase(phase_id)
        required = [self.root / path for path in phase["required"]]
        missing = [str(path.relative_to(self.root)) for path in required if not path.exists()]
        if phase["id"] == "05" and "split" not in self.load_state()["predictions"]:
            missing.append("a split prediction; run `tinyml-maintenance lab predict split`")
        if missing:
            return False, "Phase check failed:\n" + "\n".join(f"MISS  {item}" for item in missing)
        state = self.load_state()
        if phase["id"] not in state["completed"]:
            state["completed"].append(phase["id"])
            state["completed"].sort()
        self.save_state(state)
        lines = [f"PASS  {path.relative_to(self.root)}" for path in required]
        lines.append("Concept check: answer the questions in CHECKPOINT.md before moving on.")
        return True, "\n".join(lines)

    def status(self) -> str:
        state = self.load_state()
        lines = ["TinyML lab progress", "=" * 19]
        for phase in self.phases:
            mark = "DONE" if phase["id"] in state["completed"] else "NOW " if phase["id"] == state["current"] else "TODO"
            lines.append(f"{mark}  {phase['id']}  {phase['title']}")
        lines.extend(["", f"Student log: {self.log_path}"])
        return "\n".join(lines)

    def next(self) -> tuple[bool, str]:
        state = self.load_state()
        current = self.phase(state["current"])
        passed, message = self.check(current["id"])
        if not passed:
            return False, message
        index = self.phases.index(current)
        if index == len(self.phases) - 1:
            return True, "You completed all guided phases. Open challenge/README.md for the independent extension."
        next_phase = self.phases[index + 1]
        state = self.load_state()
        state["current"] = next_phase["id"]
        self.save_state(state)
        return True, self.phase_message(next_phase)

    def predict_split(self, choice: str, reason: str) -> str:
        normalized = choice.upper()
        if normalized not in {"A", "B", "C", "D"}:
            raise ValueError("choice must be A, B, C, or D")
        if not reason.strip():
            raise ValueError("write a reason before running the experiment")
        state = self.load_state()
        state["predictions"]["split"] = {"choice": normalized, "reason": reason.strip()}
        self.save_state(state)
        return f"Saved prediction {normalized}. Now run `uv run tinyml-maintenance lab run split`."

    def run_split(self) -> str:
        state = self.load_state()
        if "split" not in state["predictions"]:
            raise ValueError("make a prediction first with `tinyml-maintenance lab predict split`")
        result_path = self.root / "artifacts" / "results" / "supervised.json"
        if not result_path.exists():
            raise FileNotFoundError("run `uv run tinyml-maintenance supervised` first")
        result = json.loads(result_path.read_text())
        group_logistic = next(row for row in result["comparison"] if row["model"] == "logistic")
        random_ap = result["naive_random_logistic"]["average_precision"]
        group_ap = group_logistic["average_precision"]
        expected = "A" if random_ap > group_ap else "B" if group_ap > random_ap else "C"
        prediction = state["predictions"]["split"]
        outcome = "matched" if prediction["choice"] == expected else "did not match"
        return "\n".join(
            [
                "Random rows versus held-out machines",
                f"Random-row logistic AP: {random_ap:.3f}",
                f"Machine-group logistic AP: {group_ap:.3f}",
                f"Your prediction: {prediction['choice']} ({outcome} this run)",
                "",
                "A score does not make the random split valid. The two splits answer different deployment questions.",
                "Open labs/05-models-and-splits/CHECKPOINT.md and explain that difference.",
            ]
        )

    def reveal(self, phase_id: str, level: str) -> str:
        phase = self.phase(phase_id)
        directory = self.root / "labs" / f"{phase['id']}-{phase['slug']}"
        files = {
            "hint": directory / "CHECKPOINT.md",
            "prompt": directory / "AGENT_PROMPTS.md",
            "reference": directory / "expected" / "REFERENCE.md",
        }
        if level not in files:
            raise ValueError("level must be hint, prompt, or reference")
        return files[level].read_text().rstrip()
