# B04 — Calibration and action policy

The initial AI-shaped implementation used the same validation rows to fit calibration and select a threshold. Review found that this made the policy too dependent on one sample.

The correction divides validation machines into calibration and policy-selection groups. Neither group includes final test machines. The scenario costs remain explicit configuration rather than being presented as real factory economics.

Ponytail review retained direct sklearn calibration primitives and rejected a policy class hierarchy.
