# B01 — Data and baseline

## Context given to AI

Build the smallest vertical slice for a predictive-maintenance learning system. Use established libraries, preserve time order, make near-term failure rare, and create deliberate leakage traps that tests exclude.

## AI proposal

Generate machine histories from latent degradation, derive observable sensors, label future failures, use a group split, and train a sklearn pipeline.

## Engineer review

Accepted the single generator and sklearn pipeline. Rejected a generic model registry, streaming layer, feature store, custom base estimator, and random row split. Required hidden columns to remain in the dataset only for generator and clustering validation and to be forbidden by feature selection.

## Verification

The blueprint acceptance command must prove deterministic generation, time ordering, rare-event presence, forbidden-feature exclusion, disjoint machines, and finite probabilities.

## Remaining risk

Synthetic mechanisms are illustrative. Passing on this dataset is not evidence of factory readiness.
