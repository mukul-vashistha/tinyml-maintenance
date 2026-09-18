# Checkpoint

Hint: start each answer with the question the method receives.

Answer:

1. How does remaining useful life differ from near-term failure?
   Remaining useful life (RUL) is a regression question: roughly how many more hours can
   this machine run before it fails? Near-term failure is a classification question: will
   it cross into failure within a fixed horizon, yes or no? RUL gives a continuous
   estimate without committing to any horizon; the classification question only makes
   sense once you pick a specific window to ask about.

2. What does mean absolute error tell an operator?
   MAE (about 98 hours for the best regressor, random forest) is the average absolute gap
   between predicted and actual remaining life, in the same units as the target. Lower is
   better. What it hides: it treats every error the same regardless of when in the
   machine's life it happens. Being off by 98 hours when the true RUL is 100 hours is
   operationally serious (the model could say "plenty of time" when failure is imminent),
   while the same 98-hour error when true RUL is 2000 hours barely matters. An average
   error masks this difference between the safety-critical low-RUL range and the
   comfortable high-RUL range.

3. What information do two PCA components retain?
   Only 51.2% of total variance. Compressing the full feature set down to 2 dimensions for
   the plot throws away 48.8% of the differences between machines. That means a visual gap
   or overlap in the 2D plot is not trustworthy on its own: real separation that exists in
   the discarded dimensions can be hidden, and apparent separation shown in 2D can be an
   artifact of the projection rather than real structure in the full feature space.

4. Why do the clustering methods disagree?
   All three post near-zero adjusted rand index against the simulator's true hidden
   regime (kmeans -0.0006, dbscan 0.0, gmm 0.0031) -- essentially no better than random
   agreement with ground truth. Given that the data has no strong natural separation, what
   differs between the methods is their own built-in assumption about what a cluster looks
   like: k-means forces exactly k round, similarly-sized groups regardless of the data;
   DBSCAN looks for a density gap and, finding none, refuses to split the data at all (1
   cluster); GMM allows soft, overlapping ellipses. Each algorithm's partition reflects its
   own structural assumption, not real structure in the machines.

5. What evidence would you need before naming a cluster?
   Evidence external to the clustering output itself: check whether the cluster
   assignment correlates with something the clustering never saw, such as actual failure
   rates, machine type, or maintenance history. If failure rates (or another independent,
   real-world outcome) genuinely differ across clusters, that supports giving the cluster
   a business name like "high-wear machines." A cluster with no visible difference in
   failure rate or any other real outcome is just a shape produced by the algorithm's
   assumptions, not a group with real-world meaning.
