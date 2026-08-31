# Decision phases: 07 and 08

## Phase 07: turn a score into an action

Use one case to separate:

```text
raw score -> calibrated probability -> selected threshold -> action
```

Explain the difference before testing it. Ask the learner why ranking quality does not make a score a trustworthy probability and why 0.5 is not a universal threshold.

Require separate evidence roles:

- training rows fit the model;
- calibration rows fit the probability mapping;
- different validation rows select the policy threshold;
- held-out test rows evaluate the completed policy once.

Reject calibration or threshold selection on final test rows. Human review is an action for unsupported or uncertain evidence, not another model class.

## Phase 08: decide what to do under shift

Ask the learner to review this claim:

```text
ROC-AUC remains high on machine type D, so the model is robust.
```

Require ranking metrics, confusion matrix, recall at the transferred threshold, and action behavior. The current result retains ranking information on type D while catching no failures at the transferred threshold.

The learner must decide whether to automate, abstain, or request human review. A new threshold needs separate validation evidence; selecting it on the unseen-type test rows would contaminate evaluation.

Finish with a handoff that states evidence, decision, remaining risk, and one next experiment. The coach may edit and save it, but the learner supplies the operating judgment.
