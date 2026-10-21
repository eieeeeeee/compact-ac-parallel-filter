# YK66 Rev.AT — Official KiCad 10.0.6 native audit, 2026-10-21

**Result: FAIL — NOT FOR FAB / NOT FOR MAINS.**

Workflow: https://github.com/eieeeeeee/compact-ac-parallel-filter/actions/runs/39546177790

## Verified native results

- KiCad 10.0.6 official Docker runtime: **PASS**
- Source payload integrity check / reconstruction: **PASS**
- ERC: **0** sheet-level violations (native JSON `sheets[].violations`)
- DRC: **199** total items
- Unconnected: **26**
- Schematic parity: **32**

DRC breakdown: **87 shorts between different nets**, **87 solder-mask bridges**, **16 library footprint mismatches**, **6 copper clearances**, **2 silkscreen-on-copper**, **1 silkscreen-edge**.

The first gate's summary mistakenly reported ERC as `null` because its parser looked for a nonexistent top-level `violations` field; the official `ERC_NATIVE.json` contains `sheets:[{violations:[]}]`, i.e. 0 ERC violations. Validator v2 fixes this.

Sample issues:
- `shorting_items`: AC_B trace contacts C_TOP pad of C1 around (150.5, 141.0) mm.
- `clearance`: AC_A trace vs FUSED pad of F1, measured 0.195 mm against the research rule 0.200 mm.
- `unconnected`: J1 pad 1 AC_A disconnected from an AC_A track endpoint.
- `net_conflict`: PCB net `C_TOP` vs schematic `/C_TOP` (net naming / parity).

These are real native KiCad warnings/errors; previously reported independent 11/11 connectivity and 1.55mm clearance are not sufficient.

## Next engineering work

1. Reconcile schematic identifiers and PCB nets by KiCad's native **Update PCB from Schematic** workflow (do not merely suppress parity warnings).
2. Remove all shorts, then unconnected items; rerun native KiCad.
3. Correct pad, silk and footprint library mismatches.
4. Apply product-specific AC100V insulation and safety clearance standards; zero DRC under a placeholder 0.2mm rule is **not** product safety compliance.
5. Verify thermal cutoff response, fuse/MOV coordination, and physical certified plug insert before fabrication.

Research work is independent of prior RC18 workflows. **No 100V energization or Gerber manufacturing authorized.**
