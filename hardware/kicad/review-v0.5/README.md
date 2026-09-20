# KiCad 10 review PCB v0.5

This folder contains a separate **50 × 35 mm** pre-prototype PCB study for electrical-spacing review and later A/B measurements. It does not replace the 32 × 28 mm KiCad 9 Rev.A design.

## Files

- `wall_filter_v0_5.kicad_pcb` — routed KiCad 10 PCB
- `wall_filter_v0_5.kicad_dru` — project design rules
- `fp-lib-table` — project-local footprint mapping
- `WallFilter_Custom.pretty/` — 12 local footprints
- `PCB_NOTES_v0_5.md` — revision notes and DRC summary
- `STATIC_CHECK_v0_5.txt` — independent static geometry/connectivity check

The official KiCad 10 DRC output is archived at [`measurements/drc/DRC_KiCad10_v0_5_20260920.rpt`](../../../measurements/drc/DRC_KiCad10_v0_5_20260920.rpt).

## Verification snapshot

KiCad 10 official DRC, 2026-09-20:

- DRC violations: **0**
- unconnected pads: **0**
- footprint errors: **0**

Static checker:

- pads checked: 26
- routed segments checked: 23
- reported minimum L/L_FUSED-to-N copper spacing: 4.5 mm
- reported minimum copper-to-rectangular-board-boundary distance: 2.0 mm

These checks verify the rules and geometry represented in the files; they do **not** establish regulatory compliance or safety on mains.

## Implemented branches

- fused L input
- C1: 1 µF X2 main shunt capacitor
- R1 + R2: 220 kΩ + 220 kΩ discharge chain
- MOV1: 140 VAC thermally protected MOV candidate
- low-current LED branch and antiparallel protection diode
- C2: optional 0.1 µF X2 footprint, **DNP initially**
- R3/C3: optional series RC damping footprint, **DNP initially**

## Required review before fabrication or energization

- Match every footprint to the exact manufacturer drawing and ordered part.
- Confirm voltage, pulse, power, flammability and safety approvals for each part.
- Review creepage/clearance for the final material, pollution degree, enclosure and applicable standard.
- Finalize plug blades, retention, enclosure, insulation and accessible-part protection as one mechanical system.
- Review fuse clearing and TMOV coordination under credible faults.
- Perform unpowered continuity/insulation checks before any controlled mains test.

**PRE-PROTOTYPE / NOT YET BUILT / NOT YET TESTED ON MAINS.**
