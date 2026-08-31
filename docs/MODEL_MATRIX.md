# Reviewed model matrix

This matrix is a reviewed decision artifact, not an automatic model menu.

| Candidate | View | Necessary preparation | Main risk | Rejection experiment |
|---|---|---|---|---|
| Dummy prior | Operational floor | None | High accuracy with zero failure recall | Inspect confusion counts |
| Logistic regression | Linear odds and coefficient direction | Imputation, scaling, one-hot encoding | Nonlinearity and unstable correlated coefficients | Compare validation AP with nonlinear models |
| L1/L2/ElasticNet | Shrinkage and stability | Same as linear model | Sparse-looking output may be overinterpreted as causality | Repeat across seeds and correlated features |
| Decision tree | Readable chain of questions | Imputation and encoding | Unstable, overfit leaves | Group-held-out comparison and depth restriction |
| Random forest | Averaged nonlinear tree patterns | Imputation and encoding | Probability may be poorly calibrated | Reliability curve and Brier score |
| Gradient boosting | Sequential residual correction | Imputation and encoding | Validation overfitting through tuning | Untuned baseline first; final test only after selection |
| SVM | Margin separation | Scaling and encoding | Decision score mistaken for probability | Explicit calibration check |
| KNN | Similar historical states | Scaling and encoding | Distance collapse in many dimensions | PCA/feature ablation and held-out-machine AP |
| Linear/Ridge/ElasticNet regression | Simple useful-life relation | Same preprocessing | Censoring and nonlinear degradation | Compare MAE/RMSE with nonlinear regressors |
| K-means | Spherical operating groups | Numeric imputation and scaling | Forced clusters | Compare ARI and silhouette |
| DBSCAN | Density groups and outliers | Scaled lower-dimensional view | One cluster or parameter instability | Report noise and cluster count across settings |
| Gaussian mixture | Overlapping soft groups | Numeric imputation and scaling | Distribution assumptions | Compare against hidden simulated regime |

The current shortlist is intentionally small. XGBoost is discussed as an alternative but not added because sklearn boosting already answers the first nonlinear comparison without another dependency.
