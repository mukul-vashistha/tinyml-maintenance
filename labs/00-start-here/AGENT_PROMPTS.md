# Agent prompts

## Begin as a teacher

~~~text
I have not read the technical article and may be new to predictive maintenance.

Explain what this project is trying to do using one machine that reports readings every six hours. Explain the 24-hour prediction and the four possible actions. Tell me what I will produce in Phase 00, then ask one simple question.

Do not begin with repository structure or a quiz. Do not edit files yet.
~~~

## Explore one path

Use this only after the learner understands the problem:

~~~text
Help me follow the 24-hour prediction from PROBLEM.md into the label code in src/tinyml_maintenance/data.py and then to one saved result. Explain each file before asking me what it means. Use only actual repository evidence.
~~~

## Draft the record

~~~text
Using only what I said and the evidence we inspected, draft my Phase 00 entry. Separate what I explained, what AI explained, and what evidence we checked. Show me a short summary, then write the agreed entry to .tinyml-lab/student-log.md. Do not invent an answer or claim that I ran something I did not run.
~~~
