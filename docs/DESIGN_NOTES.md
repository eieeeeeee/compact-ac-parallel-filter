# Design Notes

## Project architecture

The initial version is a **direct plug-in parallel network** connected across 100 V AC mains.

It is not a pass-through power filter and has no downstream outlet or load path.

## Preliminary topology

After the input fuse, the following branches are intended to be connected across line and neutral:

- 1 µF X2 capacitor
- 220 kΩ + 220 kΩ discharge resistor chain
- thermally protected MOV
- low-current indicator LED branch
- optional DNP X2 capacitor footprint
- optional DNP RC damping footprint

## Why no CMC in v0.1

A conventional common-mode choke is normally placed in series with line and neutral feeding a load. In the present one-port parallel-only architecture there is no downstream current path through such a choke.

Therefore a CMC is intentionally omitted from the first design.

## Mechanical target

### PCB

Target: **approximately 32 × 28 mm**

This is a size goal, not a mandatory limit.

The PCB must be enlarged if necessary to satisfy:

- creepage/clearance requirements
- component body spacing
- fuse/MOV placement
- thermal behavior
- routing
- manufacturing tolerances
- plug mechanics

### Enclosure

Target: **approximately 38 × 34 × 27 mm**

The enclosure is expected to use vertical component volume efficiently because the X2 capacitor and 14 mm MOV are physically larger than most remaining parts.

## Component placement priorities

1. Fuse near the mains input.
2. MOV electrically after the fuse.
3. Keep high-current surge paths short.
4. Place C1 and its discharge resistors close together.
5. Keep mains-connected copper away from enclosure openings and accessible surfaces.
6. Do not use dense copper pours merely to reduce routing length.
7. Reserve sufficient edge spacing around the PCB perimeter.

## Electrical observations

A 1 µF capacitor across 100 V AC carries a nominal reactive current of approximately:

- 31 mA at 50 Hz
- 38 mA at 60 Hz

This is reactive current, not equivalent real power dissipation, but it is relevant to component stress and circuit behavior.

## Version policy

The project remains **pre-prototype** until a physical unit is assembled.

No efficiency, EMI-reduction, surge-protection, thermal, or safety-performance claim should be made before measurement.
