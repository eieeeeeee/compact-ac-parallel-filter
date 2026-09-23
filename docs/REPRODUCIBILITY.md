# Reproducibility Policy

The goal is that an independent reader can reproduce a design decision without trusting a screenshot or an undocumented spreadsheet.

## Minimum reproducibility standard

A frozen RC18 electrical result should include:

1. source code for the model;
2. all constants required by the model;
3. exact controller coefficients;
4. frequency grids and source-impedance grids;
5. corner definitions;
6. pass/fail thresholds;
7. machine-generated summary and detail CSVs;
8. software versions used by CI.

## Local reproduction

From the repository root:

```bash
python -m pip install -r simulations/rc18-b2.1/requirements.txt
python simulations/rc18-b2.1/validate_rc18.py
```

The script produces:

```text
validation/rc18-b2.1/generated/summary.csv
validation/rc18-b2.1/generated/detail.csv
```

The generated files should be compared with the frozen reference files when reviewing a change.

## Change discipline

Do not silently change a gate constant to make a design pass. A change to a frozen threshold, RC17 reference, corner definition, latency, jitter envelope, or component value is a model revision and should be called out explicitly in the pull request.

## Measurements

When hardware exists, raw measurements should be stored separately from simulations. Measurement files should record instrument, firmware revision, PCB revision, fixture, wiring, source/load condition, sample rate, bandwidth, and relevant calibration information.

Negative and null results should remain in the project history.
