# Reference explanation

One row is one machine at one six-hour timestamp. Machines keep their type and site while load, sensor readings, age, maintenance time, and hidden degradation change.

The generator labels a row positive when a failure occurs within the next four observations. It removes the last four rows for each machine because their complete future window is unavailable.

Rolling features use the current and previous observations from the same machine. The target and leak_future_temperature look forward, so they are forbidden features. feature_columns enforces that boundary and the tests check it.
