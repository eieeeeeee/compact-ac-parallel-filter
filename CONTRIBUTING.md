# Contributing

This project welcomes technically falsifiable contributions: circuit corrections, model improvements, measurements, component substitutions, firmware changes, test fixtures, and failed reproductions.

## Pull-request standard

A change that affects an RC18 frozen parameter should state what changed, why it changed, which gate is expected to move, and whether the electrical-validation workflow passes.

Do not weaken a threshold or remove a difficult corner merely to recover a green CI result. If the model or acceptance rule itself is wrong, change it explicitly and document the reason.

## Evidence

Prefer raw data and executable analysis over screenshots. A graph is useful; the CSV and the script that generated it are more important.

## Safety

Do not submit instructions that imply the pre-prototype RC18 low-voltage simulation has already established a safe mains interface. Any mains-connected hardware contribution must clearly identify the safety assumptions and unverified elements.
