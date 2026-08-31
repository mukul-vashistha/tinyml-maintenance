"""Leakage-safe splits and sklearn model pipelines."""

from dataclasses import dataclass

import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import (
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import ElasticNet, LinearRegression, LogisticRegression, Ridge
from sklearn.model_selection import GroupShuffleSplit
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from .data import feature_columns

TARGET = "target_failure_within_24h"
REGRESSION_TARGET = "target_remaining_useful_life"


@dataclass(frozen=True)
class DataSplit:
    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame


def group_split(frame: pd.DataFrame, seed: int = 42) -> DataSplit:
    """Split by machine so one asset cannot appear on both sides."""

    outer = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=seed)
    train_val_idx, test_idx = next(outer.split(frame, groups=frame["machine_id"]))
    train_val = frame.iloc[train_val_idx]
    test = frame.iloc[test_idx]
    inner = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=seed + 1)
    train_idx, val_idx = next(inner.split(train_val, groups=train_val["machine_id"]))
    return DataSplit(
        train=train_val.iloc[train_idx].copy(),
        validation=train_val.iloc[val_idx].copy(),
        test=test.copy(),
    )


def temporal_split(frame: pd.DataFrame, train_step: int = 78, validation_step: int = 98) -> DataSplit:
    return DataSplit(
        train=frame[frame["step"] < train_step].copy(),
        validation=frame[(frame["step"] >= train_step) & (frame["step"] < validation_step)].copy(),
        test=frame[frame["step"] >= validation_step].copy(),
    )


def unseen_type_split(frame: pd.DataFrame, machine_type: str = "D") -> DataSplit:
    known = frame[frame["machine_type"] != machine_type]
    validation_machines = sorted(known["machine_id"].unique())[::5]
    return DataSplit(
        train=known[~known["machine_id"].isin(validation_machines)].copy(),
        validation=known[known["machine_id"].isin(validation_machines)].copy(),
        test=frame[frame["machine_type"] == machine_type].copy(),
    )


def naive_random_split(frame: pd.DataFrame, seed: int = 42) -> DataSplit:
    """Deliberately unsafe split retained for the leakage lesson."""

    shuffled = frame.sample(frac=1, random_state=seed)
    n = len(shuffled)
    return DataSplit(
        train=shuffled.iloc[: int(0.6 * n)].copy(),
        validation=shuffled.iloc[int(0.6 * n) : int(0.8 * n)].copy(),
        test=shuffled.iloc[int(0.8 * n) :].copy(),
    )


def _preprocessor(frame: pd.DataFrame) -> ColumnTransformer:
    features = feature_columns(frame)
    categorical = [column for column in features if frame[column].dtype == "object"]
    numeric = [column for column in features if column not in categorical]
    return ColumnTransformer(
        [
            ("numeric", Pipeline([("impute", SimpleImputer()), ("scale", StandardScaler())]), numeric),
            ("categorical", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical),
        ],
        verbose_feature_names_out=False,
    )


def classifier_pipeline(frame: pd.DataFrame, estimator: object) -> Pipeline:
    return Pipeline([("preprocess", _preprocessor(frame)), ("model", estimator)])


def classifiers(seed: int = 42) -> dict[str, object]:
    return {
        "dummy": DummyClassifier(strategy="prior"),
        "logistic": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=seed),
        "logistic_l1": LogisticRegression(
            l1_ratio=1.0, solver="saga", C=0.15, max_iter=2000, class_weight="balanced", random_state=seed
        ),
        "logistic_elasticnet": LogisticRegression(
            solver="saga",
            l1_ratio=0.5,
            C=0.20,
            max_iter=2000,
            class_weight="balanced",
            random_state=seed,
        ),
        "tree": DecisionTreeClassifier(max_depth=5, min_samples_leaf=20, class_weight="balanced", random_state=seed),
        "random_forest": RandomForestClassifier(
            n_estimators=120, max_depth=8, min_samples_leaf=8, class_weight="balanced", n_jobs=-1, random_state=seed
        ),
        "gradient_boosting": GradientBoostingClassifier(n_estimators=100, max_depth=2, random_state=seed),
        "svm": CalibratedClassifierCV(SVC(C=1.0, class_weight="balanced", random_state=seed), method="sigmoid", cv=3),
        "knn": KNeighborsClassifier(n_neighbors=15, weights="distance"),
    }


def regressors(seed: int = 42) -> dict[str, object]:
    return {
        "linear": LinearRegression(),
        "ridge": Ridge(alpha=10.0),
        "elastic_net": ElasticNet(alpha=0.01, l1_ratio=0.4, max_iter=3000, random_state=seed),
        "random_forest": RandomForestRegressor(
            n_estimators=100, max_depth=9, min_samples_leaf=6, n_jobs=-1, random_state=seed
        ),
        "gradient_boosting": GradientBoostingRegressor(n_estimators=100, max_depth=2, random_state=seed),
    }


def fit_classifier(frame: pd.DataFrame, name: str = "logistic", seed: int = 42) -> tuple[Pipeline, DataSplit]:
    split = group_split(frame, seed)
    estimator = classifiers(seed)[name]
    model = classifier_pipeline(split.train, estimator)
    features = feature_columns(frame)
    model.fit(split.train[features], split.train[TARGET])
    return model, split
