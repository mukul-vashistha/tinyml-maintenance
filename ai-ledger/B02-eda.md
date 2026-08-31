# B02 — Evidence-led EDA

AI was asked for questions the EDA should answer, not for a generic profiling notebook. It proposed correlations, distributions, missingness, slices, and temporal comparisons.

The review retained class balance, machine-type slices, missingness, sensor overlap, and time range. It rejected a large profiling dependency and dozens of plots without decisions attached. The accepted patch uses pandas and two matplotlib figures.

The next decision is justified only if an observation leads to an experiment.
