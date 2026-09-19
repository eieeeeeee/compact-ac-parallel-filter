# Preliminary BOM — v0.1.0-preprototype / KiCad Rev.A

**Status:** design-stage BOM only.  
**Prototype manufactured:** no.  
**Mains tested:** no.

| Ref | Part / target specification | Qty | PCB implementation | Status |
|---|---|---:|---|---|
| F1 | Littelfuse **37402500000** | 1 | THT, 5.08 mm pitch | Selected candidate |
| C1 | KEMET **R533N410050P0K** / R53 | 1 | THT, 22.5 mm pitch | Selected |
| R1, R2 | **220 kΩ each** | 2 | **1206 SMD on B.Cu** | Exact mains-qualified part TBD |
| MOV1 | Littelfuse **TMOV14RP140E** | 1 | THT, 7.5 mm nominal pitch | Selected candidate |
| R4, R5 | **47 kΩ each** | 2 | **1206 SMD on B.Cu** | Exact mains-qualified part TBD |
| LED1 | blue LED | 1 | 1206 SMD on B.Cu | Exact part TBD |
| D1 | **1N4148W-class** reverse clamp | 1 | SOD-123 on B.Cu | Exact part TBD |
| J1 | plug-assembly electrical interface | 1 | two THT pads, 10 mm pitch | **Provisional; not plug blades** |
| C2 | 0.1 µF X2 | 0 | no footprint on Rev.A | Future measurement variant |
| R3/C3 | RC damping network | 0 | no footprint on Rev.A | Future measurement variant |
| PCB | FR-4, **32 × 28 mm** | 1 | KiCad Rev.A | Pre-prototype |

## Important BOM limitations

The 1206 resistor footprint is fixed for the current compact layout, but the **actual resistor manufacturer/series is not yet fixed**. The selected components must be checked for working voltage, overload/pulse voltage, power dissipation, flame behavior and applicable approvals before fabrication.

The same applies to LED1 and D1: the footprint and function are defined, but the exact orderable part numbers remain to be selected.

## Discharge network

R1 + R2 = 440 kΩ nominal across C1.

With C1 = 1 µF, the nominal RC time constant is approximately **0.44 s**. Actual post-unplug voltage decay must be measured on the physical prototype.

## Compact Rev.A exclusions

C2 and the optional RC damping branch are intentionally omitted from the 32 × 28 mm PCB. Adding them is deferred until measurements show a reason to do so.

A common-mode choke is not included because this is a one-port parallel architecture rather than a pass-through filter.
