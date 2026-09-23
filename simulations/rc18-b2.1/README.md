# RC18-B2.1 electrical validation model

This directory contains the self-contained numerical gate for the frozen RC18-B2.1 simulation candidate.

## Run

```bash
python -m pip install -r requirements.txt
python validate_rc18.py
```

From the repository root, omit path changes and run the commands shown in the root README.

## Model content

`validate_rc18.py` includes the disclosed passive Candidate-A model, B2.1 three-section reconstruction model, nominal/low/high LC corners, source impedance/phase grid, digital biquad coefficients, float32 sequential arithmetic model, Q31 DF1 arithmetic model, bounded ±25 ns jitter, and same-model RC17 comparison references.

The output is deliberately machine-readable. CI uploads the generated CSV files as an artifact for every run.

## Interpretation

A PASS means only that the candidate passed the frozen numerical model and thresholds. It is not a safety certification and it is not a physical EMI measurement.
