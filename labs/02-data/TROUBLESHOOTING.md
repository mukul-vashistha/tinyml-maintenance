# Troubleshooting

If data/maintenance.csv is missing, run the generate command from the repository root.

The CSV is intentionally ignored by Git. Anyone can recreate it from the fixed seed and configuration.

Missing sensor values are expected. They test whether the pipeline handles the kind of incomplete evidence a real system may receive.

The rolling window contains four observations because readings arrive every six hours. Four readings represent 24 hours.
