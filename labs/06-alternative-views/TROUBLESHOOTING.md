# Troubleshooting

PCA is fitted after preprocessing the legitimate features. Hidden simulator columns are not used.

DBSCAN may label many observations as noise. That behavior comes from its density assumptions and parameter values; it is not a software failure by itself.

The hidden regime is available only because we generated the data. Use it to evaluate an interpretation, not as evidence that a production system would know the regime.
