# Checkpoint

Hint: sort by machine_id and timestamp, then look at the generator state before and after a failure.

You should be able to answer:

1. Why do we generate histories instead of independent rows?
2. Which columns are legitimate at prediction time?
3. How does the code create the 24 hour target?
4. Why can a rolling mean be valid while future temperature is not?
5. Which tests would fail if time order changed?
