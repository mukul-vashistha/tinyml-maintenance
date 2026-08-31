from tinyml_maintenance.cli import load_config, simulation_config


def test_default_config_builds_valid_simulation():
    config = load_config("configs/default.toml")
    simulation = simulation_config(config)
    assert simulation.horizon_steps == 4
    assert simulation.n_machines == 120
