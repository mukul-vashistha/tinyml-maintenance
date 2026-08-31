# Evaluation rubric

Score each dimension from 0 to 4. A score of 2 means functional but incomplete judgment; 4 means strong evidence and a clear trade-off.

| Dimension | What strong work demonstrates |
|---|---|
| Repository comprehension | Correct extension point and preserved conventions |
| Problem decomposition | Small blueprint with explicit non-goals |
| AI usage | Useful context and bounded prompts, not repeated vague repair requests |
| AI application | Library and AI used where appropriate; unnecessary generation avoided |
| Understanding limits | Plausible AI mistake identified and corrected |
| ML judgment | Split, metric, threshold, and interpretation match the question |
| Testing | A check fails for the meaningful broken behaviour |
| Experimentation | Hypothesis, control, result, and limitation are explicit |
| Simplicity | Small coherent diff; existing capabilities reused |
| Handoff | Another engineer can reproduce and continue the work |

Automatic rejection conditions: target leakage, tuning on the final test set, unexplained deletion of safety checks, fabricated experiment results, or an un-runnable submission.
