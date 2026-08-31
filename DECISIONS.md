# Engineering decisions

## D01 — Use libraries, not ceremonial reimplementation

Use sklearn for algorithms, preprocessing, metrics, and model composition. A from-scratch algorithm is an optional exercise, not part of the shipped system.

Rejected: a miniature sklearn clone. It adds code without improving the decision system.

## D02 — Generate a time-ordered synthetic fleet

The generator exposes its assumptions and hidden state, making leakage, shift, and clustering validation testable.

Rejected: presenting a downloaded dataset as unexplained ground truth.

## D03 — Define generalization before splitting

The primary question is performance on machines not used for training, so the primary split groups by machine. Temporal and unseen-type splits answer different questions.

Rejected: one convenient random split for every claim.

## D04 — Compare models as views

The model shortlist contains distinct assumptions: linear odds, question-based trees, ensembles, margins, and neighbourhoods. It is not an exhaustive estimator tournament.

Rejected: automated hyperparameter search before understanding baselines.

## D05 — Separate ranking, calibration, and policy

Average precision compares rare-event ranking. Calibration checks probability meaning. A separate validation subset selects a cost-sensitive action threshold.

Rejected: choosing a model and threshold from final test F1.

## D06 — Abstention is a valid output

Unsupported machine types and low-confidence cases may require human review. Returning a number does not create evidence.

Rejected: forced automation of every observation.

## D07 — Keep the architecture vertical and small

Use a handful of direct modules and sklearn's estimator protocol. Add a layer only when two real callers require it.

Rejected: base estimator classes, plugin interfaces, feature-store abstractions, model-serving scaffolds, and an experiment-tracker service.

## D08: guide learners through the completed repository

The guided lab uses the working implementation as evidence. Learners inspect it, predict experiment outcomes, review AI proposals, run tests, and propose bounded changes. The independent challenge is where they modify production code without step-by-step instructions.

This avoids maintaining a second incomplete ML implementation that could drift away from the reference.

## D09: the CLI checks evidence, not understanding

Phase checks confirm that required files, tests, predictions, and artifacts exist. CHECKPOINT.md contains the questions a learner must answer. The command line does not pretend that file presence proves comprehension.

## D10: natural writing is an acceptance check

Learner-facing prose follows the supplied humanizer rules. Claims must come from project evidence or the teaching material. The automated check rejects high-signal chatbot phrases, decorative punctuation, and several stock AI words. A human review still checks rhythm, clarity, and whether the writing sounds like the instructor.
