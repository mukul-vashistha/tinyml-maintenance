# Phase 05: compare models and test the split

~~~text
Start -> Problem -> Data -> EDA -> Baseline -> [Models and split] -> Other views -> Policy -> Shift
~~~

We are not trying seven algorithms because interviews expect seven names. Each model gives us a different view of the same evidence.

| Model | A useful way to think about it |
|---|---|
| Logistic regression | One weighted boundary |
| Decision tree | A short sequence of questions |
| Random forest | Many trees voting on different samples |
| Gradient boosting | Trees correcting earlier mistakes |
| KNN | Similar historical observations |
| SVM | A separating boundary built around difficult cases |

The split matters as much as the estimator. If the deployment goal is a new machine, rows from one machine cannot appear on both sides.

## What you will learn and produce

You will make a split prediction before seeing the result, preserve it when the result disagrees, and defend the evaluation from the deployment question. You will also explain why model selection uses validation evidence rather than the most attractive final test score.

AI review becomes a required part of the work here. Read `blueprints/B03-model-comparison.yaml` to see what was agreed before implementation and `ai-ledger/B03-model-comparison.md` to see what AI proposed and what the experiment corrected. Record one material AI claim you verified or qualified.

Use the [reviewed model matrix](../../docs/MODEL_MATRIX.md) when you need the preparation, main risk, and rejection experiment for each candidate.

## Predict before running

~~~bash
uv run tinyml-maintenance lab predict split
~~~

Choose:

~~~text
A. Random-row split will have higher AP
B. Machine-group split will have higher AP
C. They will be about the same
D. I do not know yet
~~~

Then run:

~~~bash
uv run tinyml-maintenance lab run split
uv run pytest tests/test_modeling.py tests/test_experiments.py
~~~

## Think

The result may disagree with your prediction. Keep the prediction. A wrong hypothesis is useful when the experiment makes you revise the explanation.

## Check

~~~bash
uv run tinyml-maintenance lab check 05
uv run tinyml-maintenance lab next
~~~
