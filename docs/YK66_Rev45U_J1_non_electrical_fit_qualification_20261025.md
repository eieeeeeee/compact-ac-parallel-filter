# Rev.45U — isolated J1 mechanical qualification stage (2026-10-25)

**Status: Mechanical sample CAD/plots completed, physical tests NOT performed, AC100V release HOLD.**

Retain the original 50 x 32 mm Rev.45U full PCB unchanged.

## Delivered design
- `validation/Rev45U_J1_MECHANICAL_FIT_COUPON_NO_CIRCUIT.kicad_pcb`: **non-electrical mechanical test only**.
- Exact Rev.45U J1 location x42.40 y18.60 mm; holes 1.30 mm PTH at x42.40, y16.06 and y21.14; pad oval 2.80 x 2.04 mm.
- No other parts and NO traces; must never be connected to mains.
- Dedicated `validation/YK66.pretty` + `validation/fp-lib-table` and .kicad_pro for standalone KiCad editing.
- Official KiCad 10 DRC **0 violations, 0 unconnected**, Gerber/Excellon generated in:
  https://github.com/eieeeeeee/compact-ac-parallel-filter/actions/runs/40195200361

## Next non-energized gate
1. If the owner elects, order only ~10 mechanical coupons in ordinary 2-layer / 1.6 mm FR-4 / 1 oz PTH, not full AC100V assembly.
2. Test the actual Phoenix Contact 1711725 insertion across multiple coupons *without forced insertion*, without hole rework, and inspect plated barrels/annular rings.
3. Hand-solder only fit coupons under component-recommended processes, inspect both sides, damage and bridge.
4. Using a mechanical fixture or final casing interface, **support the terminal body** while tightening screws to 0.5–0.6 Nm. Test strain relief and case/tool/wire-entry clearance.
5. Record board lot, part lot, measured holes, and pass/fail for every sample. Do not claim measured results from a CAD simulation.

## Remaining separate safety gates
- PCB FR-4 lot CTI and normative insulation/clearance/creepage, including finished solder.
- Case wire entry and 1711725 support are **not yet designed or validated**.
- Original user-reported TCO on C1 (surface temperature 98 C at opening), insulation/abnormal test results must be linked to the *actual released* PCB assembly and underlying lab records.
- AC100V safety/PSE, fuse-MOV-TCO fault coordination, EMC, full electrical testing.

Manufacturer source: https://www.phoenixcontact.com/en-de/products/pcb-terminal-block-mkds-3-2-508-1711725
JLC standard fab specs: https://jlcpcb.com/capabilities/Capabilities
