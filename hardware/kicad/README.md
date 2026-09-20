# KiCad hardware

This directory contains two editable PCB studies. They are kept as separate revisions because their board size and implementation choices differ.

## Revision index

| Revision | KiCad | Board | Purpose | Status |
|---|---:|---:|---|---|
| Rev.A | 9 | 32 × 28 mm | compact mechanical study | pre-prototype |
| [review-v0.5](review-v0.5/README.md) | 10 | 50 × 35 mm | spacing and optional DNP branch study | official DRC: 0 violations |

Neither revision has been manufactured or tested on mains.

## Rev.A files in this directory

- `compact-ac-parallel-filter.kicad_pro` — project
- `compact-ac-parallel-filter.kicad_sch` — schematic
- `compact-ac-parallel-filter.kicad_pcb` — exact 32 × 28 mm PCB outline
- `ACP.kicad_sym` — local symbols
- `ACP.pretty/` — project-local footprints
- `PLACEMENT.csv` — placement coordinates

## Status

**PRE-PROTOTYPE / NOT YET TESTED ON MAINS.**

These files are for design review before fabrication. No physical-fit, mains, thermal, surge, EMC, PSE, or third-party safety validation has been completed.

## Rev.A mechanical basis

- PCB: **32.0 × 28.0 mm**
- nominal PCB thickness: **1.6 mm**
- C1: 22.5 mm lead pitch, 26.5 × 10 mm top-view body envelope
- MOV1: 7.5 mm nominal lead spacing; the footprint reserves a **17 mm maximum body envelope**
- F1: 5.08 mm pitch, 8.5 mm diameter envelope
- large THT parts are on the front; low-power resistor/LED/diode parts are on the back

At 32 × 28 mm the large-part courtyards are deliberately packed to the mechanical limit. If final creepage, clearance, enclosure or tolerance review fails, increase the PCB size rather than reducing safety margin.

## J1 limitation

`J1` is **not a Japanese/Type-A plug-blade footprint**. It is a provisional electrical interface to a separately mechanically retained plug assembly. Plug insertion/removal force must not be carried only by the PCB pads.

## Before ordering

1. Choose one reviewed hardware revision; do not mix files from different revisions.
2. Apply the final mains creepage/clearance rules for the actual regulatory environment.
3. Verify enclosure and component maximum dimensions against manufacturer drawings.
4. Verify every resistor's working/pulse voltage, power and flame behavior.
5. Verify the final LED and diode part numbers.
6. Replace J1 with the final plug/enclosure mechanical interface.
7. Review fuse/MOV coordination and abnormal-condition behavior.
8. Run ERC/DRC again with the exact ordered components and manufacturing rules.

## Rev.A topology

```text
AC L -- F1 --+-- C1 1uF X2 --+-- N
             |                |
             +-- MOV1 --------+
             |                |
             +-- R1 -- R2 ----+
             |                |
             +-- R4 -- R5 -- LED1 --+
                              |      |
                              +--D1--+  reverse clamp
                                     |
                                     N
```

C2 and optional RC damping are intentionally not implemented on the 32 × 28 mm Rev.A PCB. The 50 × 35 mm review-v0.5 board provides DNP footprints for measurement-driven comparison.
