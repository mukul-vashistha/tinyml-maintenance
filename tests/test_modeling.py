import numpy as np

from tinyml_maintenance.data import SimulationConfig, feature_columns, generate_dataset
from tinyml_maintenance.modeling import fit_classifier, group_split


def dataset():
    return generate_dataset(SimulationConfig(seed=11, n_machines=36, n_steps=72))


def test_group_split_keeps_machines_disjoint():
    split = group_split(dataset())
    train = set(split.train["machine_id"])
    validation = set(split.validation["machine_id"])
    test = set(split.test["machine_id"])
    assert train.isdisjoint(validation)
    assert train.isdisjoint(test)
    assert validation.isdisjoint(test)


def test_logistic_baseline_returns_finite_probabilities():
    frame = dataset()
    model, split = fit_classifier(frame)
    probabilities = model.predict_proba(split.test[feature_columns(frame)])[:, 1]
    assert len(probabilities) == len(split.test)
    assert np.isfinite(probabilities).all()
    assert ((0 <= probabilities) & (probabilities <= 1)).all()


def test_pipeline_never_receives_forbidden_columns():
    frame = dataset()
    model, _ = fit_classifier(frame)
    expected = set(feature_columns(frame))
    observed = set(model.named_steps["preprocess"].feature_names_in_)
    assert observed == expected
