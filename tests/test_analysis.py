from tinyml_maintenance.analysis import eda, unsupervised
from tinyml_maintenance.data import SimulationConfig, generate_dataset


def test_analysis_writes_results_and_figures(tmp_path):
    frame = generate_dataset(SimulationConfig(seed=5, n_machines=24, n_steps=60))
    summary = eda(frame, tmp_path)
    clusters = unsupervised(frame, tmp_path)
    assert summary["rows"] == len(frame)
    assert len(summary["story_machine"]["rows"]) == 7
    assert summary["story_machine"]["rows"][-1]["failure_within_24h"] == 1
    assert "kmeans" in clusters["algorithms"]
    assert (tmp_path / "results" / "eda.json").exists()
    assert (tmp_path / "figures" / "unsupervised-views.png").exists()
