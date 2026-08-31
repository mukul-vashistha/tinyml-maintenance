# AI use policy and disclosure

AI is the implementation environment for this repository. It is used to inspect files, propose blueprints, generate bounded patches, suggest tests, diagnose failures, and draft explanations.

AI output is not accepted because it compiles or sounds confident. Each non-trivial change passes four distinct reviews:

1. repository fit;
2. software correctness;
3. ML and evaluation validity;
4. unnecessary-complexity review using Ponytail principles.

Learner-facing prose also passes the supplied humanizer review. That check looks for unsupported claims, inflated language, chatbot filler, repetitive structure, decorative formatting, and punctuation habits that do not match the teaching voice. It does not replace a factual review.

The task records under `ai-ledger/` distinguish the proposal from the accepted decision. They summarize relevant interactions rather than pretending to be verbatim hidden reasoning.

## Reproducible interaction pattern

```text
inspect without editing
→ propose blueprint
→ challenge assumptions
→ freeze scope and checks
→ generate one patch
→ inspect diff
→ run evidence
→ shrink or correct
→ record decision
```

## Ponytail

Ponytail 4.9.0 is used as a complexity lens. Its source was reviewed at commit `2ed6c52c9d7e5e56942508591085fd45dea277d3`. It asks whether code needs to exist, whether the repository, standard library, platform, or installed dependency already provides it, and only then permits the minimum new code.

Ponytail does not assess ML leakage, correctness, security, or performance. Those reviews remain separate.
