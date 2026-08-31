# Reference explanation

The best remaining useful life regressor in this run is random forest, with a mean absolute error of about 98.45 hours. That error is large enough to matter operationally and should not be hidden behind the model name.

The first two PCA dimensions preserve about 51.2 percent of transformed variance. They are a partial view.

K-means, DBSCAN, and Gaussian mixtures produce different groupings because they assume different cluster shapes and densities. Their assignments do not cleanly recover the simulator's hidden regimes, so the project keeps the negative result.
