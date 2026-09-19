# Safety

## Hazardous mains voltage

This project is intended to connect directly to **100 V AC mains**. Mains voltage can cause electric shock, burns, fire, equipment damage, or death.

This repository is currently **pre-prototype**. No physical unit has yet been built or validated.

## Current project status

- Physical prototype: **not built**
- Mains powered test: **not performed**
- Thermal test: **not performed**
- Surge/fault test: **not performed**
- Insulation verification: **not completed on hardware**
- Regulatory compliance: **not established**
- Safety certification: **none**

Do not treat any schematic, PCB, BOM, enclosure dimension, or layout in this repository as inherently safe merely because it is published here.

## Design rules for the project

The following are project requirements, not a certification statement:

1. Do not reduce creepage or clearance merely to meet the nominal 32 × 28 mm PCB target.
2. If adequate spacing cannot be maintained, increase the PCB or enclosure size.
3. Keep exposed mains-connected copper inaccessible in the completed enclosure.
4. The plug structure must carry insertion/removal forces mechanically; the PCB should not be used as the sole structural support for plug blades.
5. Use only appropriately rated components for mains-connected positions.
6. Do not substitute ordinary capacitors for X-class safety capacitors.
7. Review fuse and MOV coordination before prototype power-up.
8. Verify discharge voltage after unplugging.
9. Perform first energization using appropriate current limiting, protection, isolation strategy, and test equipment suitable for mains work.
10. Treat oscilloscope grounding and other earth-referenced instruments as potential short-circuit hazards when measuring non-isolated mains circuitry.

## Enclosure

The target enclosure size is approximately **38 × 34 × 27 mm**, but size is secondary to:

- creepage and clearance
- insulation
- flame resistance
- mechanical plug retention
- component temperature
- user inaccessibility to live parts

## Regulatory note

This repository does not claim conformity with PSE, IEC, JIS, UL, CE, or other standards. If the design is ever manufactured, distributed, or sold, the applicable legal and technical requirements must be determined separately.

## Responsibility

Anyone building or modifying this design is responsible for performing their own engineering, safety, and regulatory review.
