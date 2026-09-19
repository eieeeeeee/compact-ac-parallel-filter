# Test Plan

## Purpose

This document defines the minimum evidence required before the project can move from **pre-prototype** to a tested hardware revision.

## Stage 0 — Before mains connection

- Visual PCB inspection
- Confirm component values and part numbers
- Verify fuse continuity
- Verify no line-to-neutral hard short
- Verify no accidental copper bridges
- Verify polarity/orientation-sensitive parts
- Verify MOV footprint and pin assignment
- Verify LED protection diode orientation
- Measure resistance across input
- Inspect creepage and clearance against the design review
- Inspect enclosure and plug retention
- Confirm no live conductor can be touched from outside

## Stage 1 — Controlled first energization

Perform only with suitable mains safety equipment and engineering controls.

Record:

- input RMS voltage
- input RMS current
- immediate abnormal heating
- audible noise
- odor/smoke
- LED behavior
- fuse behavior
- voltage across C1

If any abnormal condition occurs, disconnect and document it before revising the design.

## Stage 2 — Discharge test

After disconnecting mains:

- measure voltage versus time
- compare measured decay against the nominal RC model
- repeat over multiple cycles
- document instrument impedance because it can alter the measured discharge

## Stage 3 — Thermal test

Measure temperature of:

- C1
- F1
- MOV1
- R1/R2
- LED resistors
- enclosure internal air
- enclosure external surface

Suggested checkpoints:

- 5 min
- 30 min
- 1 h
- extended run if initial temperatures are stable

Record ambient temperature.

## Stage 4 — Electrical measurements

Measure:

- RMS mains current
- real power if suitable equipment is available
- power factor if suitable equipment is available
- waveform with circuit absent/present
- repeatability over multiple plug-in cycles

## Stage 5 — Noise comparison

The central comparison must use identical measurement settings.

Minimum data sets:

1. baseline — device absent
2. device connected
3. optional C2 fitted, if tested
4. optional RC damping fitted, if tested

Use representative loads, for example:

- no local load / ambient line condition
- switching power supply
- LED lamp
- other repeatable electronic load

For each measurement, record:

- instrument
- probe/coupling method
- bandwidth
- sampling settings
- load
- mains frequency
- time/date
- raw files where possible

## Stage 6 — Mechanical review

Check:

- plug insertion/removal force
- enclosure deformation
- PCB movement
- strain on solder joints
- clearances after assembly
- part movement after repeated plugging cycles

## Stage 7 — Revision decision

A new hardware revision should be created whenever a component value, footprint, routing, spacing, enclosure, or protection strategy changes.

Do not silently modify a tested revision.

## Publication policy

Publish null, negative, and unexpected results as well as favorable results.
