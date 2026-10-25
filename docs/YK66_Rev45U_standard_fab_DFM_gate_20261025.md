# YK66 Rev.45U — standard fabrication DFM gate (2026-10-25)

**STATUS: RESEARCH / HOLD — not approved for manufacturing or 100VAC energization.**

Retain the existing 50×32mm, two-layer, nominal 1.6mm FR-4 PCB and Phoenix Contact 1711725 2-pole screw terminal J1. No integral plug or plug-blade design.

## Frozen *CAD candidate* values

- J1 pad pitch 5.08mm; J1 position x42.40 y18.60mm.
- J1 plated **finished hole nominal 1.30mm**, manufacturer's recommended PCB hole.
- J1 oval copper pads **2.80×2.04mm**; ordinary plated-through-hole process without enhanced-position/press-fit tolerance surcharge.
- L-N *nominal pad* clearance: **5.08−2.04=3.04mm**. This is **not** a certified IEC/PSE safety clearance.
- Nominal minimum annular ring: **(2.04−1.30)/2=0.370mm**.
- JLCPCB normal process finished hole +0.13/−0.08mm and location ±0.05mm. Simplified worst annular ring **(2.04−1.43)/2−0.05=0.255mm** (excludes copper etch, both-axis position drift, solder).
- Minimum possible finished hole **1.22mm**; 0.9mm square manufacturer's nominal pin diagonal ≈**1.273mm**. Actual fit under all combinations of process and lead tolerances is **NOT GUARANTEED**. Actual manufacturer pin ends may have corner rounding; measure actual parts.

## Worst-case constraint trade-off

Assumptions: pitch 5.08mm, nominal L-N copper gap≥3.00mm, minimum annular ring≥0.25mm even when hole is +0.13mm and location shift is 0.05mm, minimum finished hole ≥nominal 0.9mm square diagonal when hole is −0.08mm.

- Max J1 pad dimension along pitch: **2.08mm**.
- Max nominal hole for ≥0.25mm ring: **2.08−2(0.25+0.05)−0.13=1.350mm**.
- Min nominal hole for merely fitting the nominal square pin theoretical diagonal: **0.9×√2+0.08=1.353mm**.
- Thus no strictly worst-case guaranteed solution even before adding any real insertion allowance, copper etch tolerance, pin tolerance or solder fillet. This is a bound **on the conservative guarantee**, not a claim that normal PCB fabrication fails in practice.

## Standard-order engineering pathway

1. Keep Rev45U Gerber and PCB geometry unchanged as the reviewed candidate; do not silently enlarge holes or shrink copper.
2. Specify ordinary 2-layer 1oz FR-4 1.6mm PTH fabrication. Request the *actual material grade/CTI*, and confirm normal DFM/finished-hole rules. Do not call for premium press-fit holes by default.
3. If a **non-energized** mechanical qualification build is authorized, first inspect Phoenix1711725 pin insertion across small-lot sample PCBs, solder both sides, inspect plated barrels and fillets, check pad lifting/cracking and screw terminal supported torque. No AC100V use.
4. Require enclosure support under 0.5–0.6Nm screw torque; do not load the two solder pins with the entire torque. Confirm connector wire entry and strain relief with case fit.
5. Agree pollution degree, transient overvoltage category, insulation class and FR-4 CTI before treating any 3.0mm copper check as normative. Inspect completed solder surfaces, not mask as sole safety barrier.
6. Prove the physical TCO-on-C1 fixture, insulation, and test report match the released PCB revision. User-reported 98°C C1 skin temperature at TCO opening and insulation/abnormal-test passes are not by themselves transferable to a revised PCB.

## Evidence

- Original Rev45U KiCad 10 gate (ERC 0, DRC 0, unconnected 0, schematic parity 0): https://github.com/eieeeeeee/compact-ac-parallel-filter/actions/runs/40101109168
- Terminal manufacturer: https://www.phoenixcontact.com/ja-jp/products/mkds-3-2-508-1711725
- JLCPCB: https://jlcpcb.com/jp/capabilities/Capabilities

**This gate does not change the PCB and does not release the Gerber files for manufacturing.**
