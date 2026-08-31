# Reference explanation

At each six-hour observation, the system estimates whether a machine may fail within the next 24 operating hours. Advance warning gives an operator time to continue, inspect, stop, or request human review before a possible failure.

`PROBLEM.md` states this operating question. `_future_labels` in `src/tinyml_maintenance/data.py` creates the 24-hour label from future failure events in the simulator. `artifacts/results/eda.json` reports the resulting class balance, including a near-term positive rate of about 3.97 percent in the saved run.

The prediction describes what may happen. An action describes what someone may do with that estimate. Costs describe how the project values different mistakes. These ideas are related but are not interchangeable.
