# Reference explanation

At each timestamp, the system estimates whether the machine will fail within the next 24 hours. It can use current and historical telemetry available by that timestamp. It cannot use target columns, hidden simulator state, future sensor readings, row identifiers, or machine identity.

A false alarm costs 5 units. A missed failure costs 50. The output must eventually support four actions: continue, schedule an inspection, stop now, or ask for human review.

The engineer owns this contract. AI can compare the prose, code, and tests, but it cannot decide what the operator needs or what evidence will exist in production.
