# Agent prompts

## Inspect

~~~text
Read PROBLEM.md, docs/DATA_DICTIONARY.md, src/tinyml_maintenance/data.py, and tests/test_data.py. Do not edit files.

Use this repository's data generator to explain what one row represents, how time moves, when degradation resets, how the 24 hour label is formed, and which columns must never reach a model. Name the exact functions involved.
~~~

## Bounded implementation prompt

~~~text
Assume the data generator needs one additional past-only rolling feature. Propose a patch before writing it.

Constraints:
- preserve time order;
- use only the current and earlier rows from the same machine;
- add no dependency;
- add a test that would fail if a future row leaked in;
- name the files you would change.

Wait for approval before editing.
~~~

## Review

~~~text
Review the proposed rolling feature for time leakage, group leakage, incorrect window units, and behavior at the first row of a machine. Do not review code style until those checks are complete.
~~~
