# RC18-B2.1 validation records

`reference-summary.csv` and `reference-detail.csv` are frozen outputs from the self-contained validation model at the time this package was created.

GitHub Actions regenerates the model output into a temporary `generated/` directory and uploads it as a workflow artifact. Reviewers should inspect the numerical diff if a controller, component, model, threshold, or software dependency changes.

Current reference conditions include float32 and Q31 runtime arithmetic models and ±25 ns bounded timing jitter.
