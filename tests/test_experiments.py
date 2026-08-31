from tinyml_maintenance.experiments import select_model


def test_model_selection_uses_validation_not_test_score():
    rows = [
        {"model": "valid_choice", "validation_average_precision": 0.7, "average_precision": 0.4},
        {"model": "test_leak", "validation_average_precision": 0.5, "average_precision": 0.9},
    ]
    assert select_model(rows) == "valid_choice"
