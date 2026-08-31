"""Command-line entrypoint for every reproducible project stage."""

import argparse
import tomllib
from pathlib import Path

from .analysis import eda, unsupervised
from .data import SimulationConfig, generate_dataset, load_dataset, save_dataset
from .experiments import regression, shifts, supervised
from .lab import GuidedLab
from .reporting import render_blog


def load_config(path: str | Path) -> dict:
    return tomllib.loads(Path(path).read_text())


def simulation_config(config: dict) -> SimulationConfig:
    return SimulationConfig(
        seed=config["seed"],
        n_machines=config["n_machines"],
        n_steps=config["n_steps"],
        step_hours=config["step_hours"],
        horizon_hours=config["horizon_hours"],
    )


def ensure_data(config: dict):
    path = Path(config["data_path"])
    if not path.exists():
        save_dataset(generate_dataset(simulation_config(config)), path)
    return load_dataset(path)


def run(command: str, config: dict) -> None:
    if command in {"generate", "all"}:
        path = save_dataset(generate_dataset(simulation_config(config)), config["data_path"])
        print(f"generated {path}")
    frame = ensure_data(config) if command != "blog" else None
    if command in {"eda", "all"}:
        summary = eda(frame, config["artifact_dir"])
        print(f"EDA: {summary['rows']} rows, failure rate {summary['failure_rate']:.3%}")
    if command in {"supervised", "experiments", "all"}:
        result = supervised(
            frame,
            config["artifact_dir"],
            config["seed"],
            config["false_alarm_cost"],
            config["missed_failure_cost"],
        )
        print(f"best classifier: {result['best_model']}")
    if command in {"regression", "experiments", "all"}:
        result = regression(frame, config["artifact_dir"], config["seed"])
        print(f"best regressor: {result['comparison'][0]['model']}")
    if command in {"unsupervised", "experiments", "all"}:
        result = unsupervised(frame, config["artifact_dir"], config["seed"])
        print(f"PCA variance in two dimensions: {sum(result['pca_explained_variance']):.1%}")
    if command in {"shifts", "experiments", "all"}:
        shifts(
            frame,
            config["artifact_dir"],
            config["seed"],
            config["false_alarm_cost"],
            config["missed_failure_cost"],
        )
        print("shift evaluation complete")
    if command in {"blog", "all"}:
        print(f"rendered {render_blog()}")


def _run_lab(arguments: list[str]) -> None:
    parser = argparse.ArgumentParser(prog="tinyml-maintenance lab")
    commands = parser.add_subparsers(dest="lab_command", required=True)
    for name in ("start", "doctor", "status", "next"):
        commands.add_parser(name)
    show = commands.add_parser("show")
    show.add_argument("phase")
    check = commands.add_parser("check")
    check.add_argument("phase")
    predict = commands.add_parser("predict")
    predict.add_argument("experiment", choices=["split"])
    predict.add_argument("--choice", choices=["A", "B", "C", "D"])
    predict.add_argument("--reason")
    run_experiment = commands.add_parser("run")
    run_experiment.add_argument("experiment", choices=["split"])
    reveal = commands.add_parser("reveal")
    reveal.add_argument("phase")
    reveal.add_argument("--level", choices=["hint", "prompt", "reference"], default="hint")
    parsed = parser.parse_args(arguments)
    lab = GuidedLab()
    if parsed.lab_command == "start":
        print(lab.start())
    elif parsed.lab_command == "doctor":
        passed, message = lab.doctor()
        print(message)
        if not passed:
            raise SystemExit(1)
    elif parsed.lab_command == "status":
        print(lab.status())
    elif parsed.lab_command == "show":
        print(lab.show(parsed.phase))
    elif parsed.lab_command == "check":
        passed, message = lab.check(parsed.phase)
        print(message)
        if not passed:
            raise SystemExit(1)
    elif parsed.lab_command == "next":
        passed, message = lab.next()
        print(message)
        if not passed:
            raise SystemExit(1)
    elif parsed.lab_command == "predict":
        choice = parsed.choice or input("A, B, C, or D: ")
        reason = parsed.reason or input("Why? ")
        print(lab.predict_split(choice, reason))
    elif parsed.lab_command == "run":
        print(lab.run_split())
    elif parsed.lab_command == "reveal":
        print(lab.reveal(parsed.phase, parsed.level))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = ["generate", "eda", "supervised", "regression", "unsupervised", "shifts", "experiments", "blog", "all", "lab"]
    parser.add_argument("command", choices=commands)
    parser.add_argument("--config", default="configs/default.toml")
    arguments, remaining = parser.parse_known_args()
    if arguments.command == "lab":
        _run_lab(remaining)
        return
    if remaining:
        parser.error(f"unrecognized arguments: {' '.join(remaining)}")
    run(arguments.command, load_config(arguments.config))


if __name__ == "__main__":
    main()
