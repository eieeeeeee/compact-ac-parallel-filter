# YK66 R26: Gap / bias / core-loss trade and MAG43 physical screen
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Fixed product concept
- Plug-in-only AC100V 50/60 Hz.
- Two-terminal L-N parallel device; no series insertion into the protected load.
- Goal: reduce household conducted power-line noise as much as practical.
- First-unit target <= JPY 3,500 including PCB, components, assembly, tax and shipping; stencil excluded.
- 0.1-ohm source remains a hard-source survival/stability corner, not the main attenuation acceptance point.

## R26 question
R25 promoted MAG43:
- E25/13/7 N87 class core
- ~43-turn main winding
- Lmax ~279 uH
- target Lmin ~93 uH
- 3.0:1 tuning
- 100/180/680-nF X2 coarse bank
- two high-voltage relay functions

The unresolved question is whether 3.0:1 can be reached without:
1. excessive DC control MMF,
2. excessive core-loss equivalent series resistance,
3. excessive winding copper loss.

## 1. TDK E25/13/7 gapped-core options
TDK lists, for E25/13/7 N87/N27 core sets consisting of one ungapped + one gapped half:

| Physical gap | AL | effective permeability ue |
|---:|---:|---:|
| 0.10 mm | 489 nH | 425 |
| 0.16 mm | 347 nH | 302 |
| 0.25 mm | 250 nH | 218 |
| 0.50 mm | 151 nH | 131 |
| 1.00 mm | 91 nH | 79 |

Source:
https://www.tdk-electronics.tdk.com/inf/80/db/fer/e_25_13_7.pdf

The 0.50-mm core is NOT automatically the best magnetic-control core.
A smaller gap gives more sensitivity to permeability change, but forces fewer main turns for the same 279-uH Lmax, raising AC flux per ampere and therefore core loss.

## 2. Reluctance-based requirement for a 3:1 inductance drop
Use only as a first analytical screen:
1/ue ≈ 1/ur + Rgap_normalized

Take N87 initial relative permeability ~2200 and the catalog ue above.
To reduce L by exactly 3:1 while holding geometry fixed, ue must also drop 3:1.

The corresponding material incremental/reversible permeability target is approximately:

| Gap | ue0 | material ur required for 3:1 |
|---:|---:|---:|
| 0.50 mm | 131 | ~64 |
| 0.25 mm | 218 | ~104 |
| 0.16 mm | 302 | ~141 |
| 0.10 mm | 425 | ~194 |

Interpretation:
- 0.50 mm needs deeper material saturation/permeability collapse.
- 0.25 mm needs materially less permeability collapse.
- 0.10–0.16 mm are easier to tune magnetically, but their lower required main-turn count raises AC core flux and loss.

This approximation ignores fringing and the exact three-leg side-bias flux path; it is not a finished magnetic model.

## 3. Behavioral MMF calibration
Published EE25-class variable-resonant-inductor experiment:
- 48-turn main AC winding
- 30-turn control coil on each outer leg
- 0–1 A DC control
- 40–110 uH experimental variable range = 2.75:1
Source:
https://doi.org/10.3390/electronics15142999

A normalized behavioral model was calibrated so that:
- 2.75:1 on the 0.50-mm-like screen corresponds to roughly 60 total-loop A-turns,
- permeability-vs-field curvature is represented by a simple square-law saturation screen.

THIS IS NOT A DIRECT TRANSFER OF PC40 DATA TO N87.
It is only a relative gap trade model.

Predicted order-of-magnitude MMF for 3.0:1:

| Gap | Behavioral MMF for 3:1 |
|---:|---:|
| 0.50 mm | ~64 At |
| 0.25 mm | ~50 At |
| 0.16 mm | ~42 At |
| 0.10 mm | ~36 At |

Therefore the extra step from published 2.75:1 to YK66 3.0:1 does not look like a huge control-current jump in the model.

## 4. Control-winding power screen
Provisional control winding:
- 60 turns on each side leg
- two coils series-opposed for HF cancellation in the control loop
- approximate total copper resistance ~0.45 ohm using the R23 geometry/wire screen

Effective total-loop turns = about 120 turns.

Examples:
- 64 At -> ~0.53 A -> copper loss ~0.13 W
- 80 At -> ~0.67 A -> copper loss ~0.20 W
- 120 At -> 1.00 A -> copper loss ~0.45 W

Conclusion:
**control-copper dissipation is no longer the primary blocker.**

The exact magnetic-circuit MMF interpretation still needs FEM or prototype calibration.

## 5. Main turns required at each gap for the same ~279-uH Lmax
Using the TDK AL values:

| Gap | AL | Turns for ~279 uH | TDK bobbin DC-resistance-factor estimate |
|---:|---:|---:|---:|
| 0.50 mm | 151 nH | ~43 T | ~52 mOhm |
| 0.25 mm | 250 nH | ~33–34 T | ~31 mOhm |
| 0.16 mm | 347 nH | ~28 T | ~23 mOhm |
| 0.10 mm | 489 nH | ~24 T | ~16 mOhm |

The copper DCR improves as the gap gets smaller.
But the lower turn count increases B for the same L and branch current:
B ∝ L*I / (N*Ae)

Core loss therefore moves in the opposite direction.

## 6. Core-loss equivalent resistance screening
R23 used a deliberately conservative Steinmetz-like screen anchored to the N87 manufacturer curves.
This remains only an order-of-magnitude tool; it is not a TDK guaranteed equation and does not include DC-bias loss change.

For each gap, the main turns were chosen to keep the same ~279-uH Lmax and the same 100/280/780/960-nF frequency map.

Worst "best available C state" unbiased-core equivalent loss screen over 10–50 kHz:

| Gap | Main turns | Worst screened Rcore |
|---:|---:|---:|
| 0.50 mm | 43 | ~0.24 ohm |
| 0.25 mm | ~33–34 | ~0.40 ohm |
| 0.16 mm | ~28 | ~0.55 ohm |
| 0.10 mm | ~24 | ~0.78 ohm |

This is the key trade.

## 7. Total resonant resistance stress screen
Use a deliberately simple budget:
- main-copper AC resistance ≈ 1.5 x estimated DC winding resistance
- one relay contact = 0.10 ohm max initial class
- capacitor ESR + PCB/interconnect allowance = 0.05 ohm
- core-loss multiplier under DC bias tested at 1.0 / 1.5 / 2.0 x unbiased screen

Result:

| Gap | Rtotal at core x1.0 | core x1.5 | core x2.0 |
|---:|---:|---:|---:|
| 0.50 mm | ~0.47 ohm | ~0.59 ohm | ~0.71 ohm |
| 0.25 mm | ~0.60 ohm | ~0.80 ohm | ~1.00 ohm |
| 0.16 mm | ~0.74 ohm | ~1.01 ohm | ~1.29 ohm |
| 0.10 mm | ~0.95 ohm | ~1.34 ohm | ~1.73 ohm |

R25 target:
Rtotal <= 0.8 ohm over as much of the useful 10–50-kHz map as practical.

## 8. Gap decision
### PRIMARY: 0.50-mm gap / ~43 turns
Reasons:
- best resistance margin,
- most tolerant of DC-bias-related core-loss increase,
- already aligned with the MAG43 frequency map,
- control-copper power remains modest even if MMF rises into the 60–80-At class.

### SECONDARY FALLBACK: 0.25-mm gap / ~34 turns
Use only if the 0.50-mm geometry cannot achieve 3.0:1 with acceptable MMF.
Advantages:
- roughly 20–25% less behavioral control MMF,
- lower copper DCR.

Disadvantage:
- higher AC core-loss equivalent resistance,
- exceeds the 0.8-ohm target if DC bias roughly doubles the unbiased core-loss screen.

### REJECT AS PRIMARY: 0.16 / 0.10 mm
Their core-loss margin becomes too small for the low-impedance YK66 objective.

## 9. Main-winding copper implementation screen
For 43 turns and a ~50-mm mean turn length:
total copper length is about 2.15 m.

To obtain ~50 mOhm DC winding resistance needs roughly 0.7–0.8 mm2 total copper cross section.

Practical screening examples:
- ~4 parallel AWG24-class strands
- ~6 parallel AWG26-class strands

At 50 kHz copper skin depth is about 0.30 mm.
The strand radii of those examples are below or near that value, so pure skin effect is manageable.
Proximity effect remains important and requires winding-layout measurement/modeling.

This is not a released winding specification.

## 10. Temperature screen
TDK N87 gives approximately:
- Bs ~490 mT at 25 C
- Bs ~390 mT at 100 C
Source:
https://www.tdk-electronics.tdk.com/download/540216/d6940b239127a8bab71b22168746021b/pdf-n87.pdf

Lower Bs at high temperature generally means the core enters the bias knee at lower applied field, so the 25-C MMF estimate should not simply be multiplied upward for 100 C.
However:
- reversible permeability changes with temperature,
- core loss changes with temperature,
- gap and winding resistance change,
- the side-bias geometry is not a uniform-H field.

Therefore R26 does NOT issue a numeric L(IDC,T) sign-off.
Temperature must be measured/calibrated in R28/prototype magnetic characterization.

## 11. R26 decision
### PASS
MAG43 with a 0.50-mm-gap E25/13/7 N87-class core remains the primary magnetic architecture.

### PASS AS FALLBACK
0.25-mm gap / ~34-turn main winding if 3.0:1 tuning current is too high.

### REJECT
0.10–0.16-mm gaps as the primary low-loss resonator.

### Still unresolved
- actual N87 core loss under simultaneous DC bias + 10–50-kHz AC excitation
- exact 3-leg reluctance network and L(IDC)
- side-winding physical construction and insulation
- custom winding first-unit assembly cost

## R27 gate
The magnetic physics no longer appears to be the largest BOM blocker.
R27 must attack the low-voltage supply and relay power:
- isolated module vs non-isolated appliance-style buck,
- relay substitution,
- self-generated switching noise,
- resulting total first-unit cost.

No AC100V fabrication or energization is authorized by R26.
