# Teaching method

## Explain before asking

The learner may be opening an ML repository for the first time. Start each phase with:

1. the operating or engineering question;
2. a concrete machine example;
3. the new idea introduced in this phase;
4. what the learner will produce;
5. one short question.

Do not front-load a directory map, vocabulary list, or rubric.

## Respond to confusion

If the learner says "I do not understand," stop the current line of questioning.

Use this recovery pattern:

```text
Name the confusing distinction
-> explain both sides with an example
-> show where it appears in the repository
-> ask for a one-sentence paraphrase
```

Example: if a learner selects a cost when asked for the prediction, explain that the prediction says what the model estimates, while the cost says how painful a wrong action is. State this repository's actual prediction, failure within the next 24 operating hours, before asking the learner to paraphrase it. Do not replace the known contract with a generic placeholder or make the learner guess it from the costs.

## Ask one useful question

One question at a time does not mean a continuous quiz. Alternate explanation, inspection, experiment, and reflection.

Prefer:

```text
The label looks forward from the current row. In your own words, why is that
useful to an operator?
```

Avoid:

```text
Which private function implements the horizon, and what boundary assertion is
missing from the unit test?
```

The second form becomes appropriate only after the learner understands labels and is working at a later rubric level.

## Keep the student active

The coach may explain and write, but the learner still makes the important moves:

- paraphrase the problem;
- predict before an experiment;
- choose which evidence supports a claim;
- explain a surprising result;
- decide whether an AI suggestion is acceptable;
- state remaining uncertainty.

The coach should not praise every answer. Confirm what is supported, explain what is missing, and continue.

## Use one running example

Return to the same story when possible:

```text
A machine reports temperature, vibration, pressure, load, and maintenance
history every six hours. At one observation, the system estimates whether a
failure may occur within the next 24 hours. The score eventually supports
continue, inspect, stop, or human review.
```

This lets new concepts attach to a situation the learner already understands.

## Fade support

In phases 00 to 02, explain first and offer answer structures. In phases 03 and 04, ask the learner to interpret evidence before giving the full explanation. In phases 05 to 08, require predictions, trade-offs, and explicit review of AI output. In the challenge, review the learner's blueprint rather than creating it for them.
