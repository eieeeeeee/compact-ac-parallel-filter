# YK66 R34: Procurement and budget reset
Date: 2026-10-17
Status: PROJECT CONSTRAINT UPDATE / ANALYTICAL ONLY

## User-updated constraints
- Procurement source: DigiKey Japan as primary supplier.
- DigiKey shipping cost: excluded from YK66 cost accounting.
- Component budget ceiling: **JPY 6,500**.
- Previous JPY 3,500 all-in target is superseded for the present YK66 development phase.
- Performance, electrical safety margin, reliability and self-noise now take priority over extreme component minimization within the new JPY 6,500 parts budget.

## Construction-platform decision
Do NOT move the AC100V mains section to generic perfboard/universal board solely to save cost.
Reasons:
- uncontrolled creepage/clearance and conductor spacing,
- higher risk of accidental solder bridges / exposed copper,
- poor repeatability of the low-loss resonant path,
- difficult surge/fault-current containment,
- difficult thermal layout and inspection.

A universal board may be used only for isolated/low-voltage magnetic-control experiments.
The final AC100V L-N shunt section should remain on a purpose-designed PCB or equivalent engineered mains-rated construction.

## Safety architecture correction
A fuse alone is NOT considered sufficient protection.

Minimum safety functions remain:
1. overcurrent interruption (fuse or equivalent),
2. surge-energy control,
3. protection against MOV thermal runaway or use of a thermally protected MOV,
4. X2-rated capacitors for across-line use,
5. controlled discharge path where stored charge remains,
6. fail-open behavior / flame and thermal containment,
7. verified creepage/clearance and enclosure.

Current DigiKey anchor:
Littelfuse TMOV14RP140E:
- 140 VAC max continuous
- 6 kA surge
- thermally protected MOV
- ~JPY300 one-off before tax.

This is retained as a strong candidate rather than reducing protection to only a fuse.

## Power-supply re-ranking under JPY 6,500
The higher budget removes the need to accept a noisy or non-isolated housekeeping supply merely to save a few hundred yen.

Three candidates:
### A. 50/60-Hz isolated transformer supply — newly promoted
Example:
Zettler BV301S15015
- 115-V primary
- 15-V secondary / 100 mA
- 1.5 VA
- 4.2-kVrms isolation
- ~JPY577 one-off before tax.
At Japanese 100-V mains the secondary will be proportionally lower than its 115-V rating, so the downstream relay/regulator voltage must be designed around the actual loaded output.

Key advantage:
- no tens-of-kHz switching oscillator,
- therefore much lower risk of the control supply creating a deterministic noise line inside/near the YK66 cleaning band.

### B. Encapsulated isolated AC/DC module — easy/safe reference
MEAN WELL IRM-02-12:
- 85–305 VAC input
- 12 V / 167 mA / 2 W
- approvals CB/CE/cURus/TUV
- ~JPY882 before tax.
Use as a development/reference option if its conducted self-noise passes the system test.

### C. Non-isolated capacitive dropper/offline buck
No longer primary. The JPY 6,500 budget makes the safety/self-noise compromises unnecessary unless later measurements show a clear performance advantage.

## Revised architecture preference
Primary direction:
- purpose-designed mains PCB,
- MAG50 resonant section retained as research primary,
- robust mains-rated relay(s),
- X2 coarse capacitors,
- thermally protected MOV + fuse,
- quiet isolated low-frequency control supply as first choice,
- separate passive HF branch,
- MCU/control section isolated from mains by the power transformer where practical.

## Cost consequence
The new JPY 6,500 component ceiling is large enough that:
- ~JPY600 isolated 50/60-Hz transformer,
- ~JPY300 thermal MOV,
- ~JPY350–700 relay pair,
- ~JPY400 X2 bank,
- ferrite core/bobbin/wire,
- MCU/sensing/driver,
- fuse/bleeder/HF parts
can coexist without forcing the design onto generic perfboard or deleting independent protection functions.

## Next gate
R35 should build the first complete DigiKey-only named BOM under JPY 6,500, excluding shipping, and compare:
1. 50/60-Hz transformer housekeeping supply
2. IRM-02-12 isolated module
for self-noise, power margin and total BOM cost.

No AC100V fabrication or energization is authorized by R34.
