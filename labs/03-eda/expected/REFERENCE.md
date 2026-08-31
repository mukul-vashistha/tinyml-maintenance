# Reference explanation

The generated dataset has 13,920 rows and a near-term failure rate of about 3.97 percent. This makes accuracy a poor primary metric because predicting the majority class can exceed 96 percent accuracy.

Near-failure rows tend to show different sensor behavior, but the distributions overlap. That supports a multivariable baseline rather than one hard sensor threshold. It also gives us a reason to compare linear and nonlinear models after the baseline.
