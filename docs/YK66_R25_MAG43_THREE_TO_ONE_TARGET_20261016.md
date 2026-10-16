# YK66 R25: MAG43 / 3.0:1 tuning target and two-switch architecture
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Executive result
R24 found that the real problem is not resonance tracking itself; it is production tolerance creating uncovered intervals.

The cheapest repair is NOT a third high-voltage switch.
The new primary target is:
**43-turn E25/13/7 N87 main winding + 3.0:1 magnetic tuning + two coarse X2 switches + measured/static-trim capacitance calibration.**

Research name:
**YK66-MAG43**

## 1. Why 43 turns
TDK E25/13/7 N87 anchor:
- AL ≈151 nH for the selected 0.50-mm-gap catalog geometry
- bobbin resistance factor AR ≈28 uohm

At 43 turns:
- Lmax = 151 nH * 43^2 ≈ **279.2 uH**
- target Lmin at 3.0:1 = **93.1 uH**
- main-winding DC resistance estimate = 28 uohm * 43^2 ≈ **51.8 mOhm**

This lands almost exactly on the R24 tolerance-optimized Lmax.

TDK core source:
https://www.tdk-electronics.tdk.com/inf/80/db/fer/e_25_13_7.pdf

## 2. Nominal frequency map with standard X2 values
Keep:
- C0 = 100 nF
- CA = 180 nF
- CB = 680 nF

States:
- 100 nF
- 280 nF
- 780 nF
- 960 nF

With L = 279.2 -> 93.1 uH:

| C state | Ideal tunable resonance span |
|---:|---:|
| 960 nF | 9.72–16.84 kHz |
| 780 nF | 10.78–18.68 kHz |
| 280 nF | 18.00–31.18 kHz |
| 100 nF | 30.12–52.17 kHz |

All internal handoffs overlap nominally.
The architecture therefore has margin at both ~18 kHz and ~30 kHz.

## 3. 3.0:1 is only a modest extension beyond published hardware
The 2026 EE25/20/6 variable-resonant-inductor experiment uses:
- 48-turn AC winding
- 30-turn x2 DC control windings
- 0–1 A bias
- experimental design range 40–110 uH = **2.75:1**

Source:
https://doi.org/10.3390/electronics15142999

The same paper's earlier system simulation uses a much wider abstract variable range of 20–129 uH, but the built magnetic design is 40–110 uH.
Therefore the >6:1 simulation range must NOT be treated as experimentally proven hardware capability.

YK66 needs 3.0:1:
3.0 / 2.75 = 1.091
or only about **9.1% more ratio** than the experimental hardware class.

That is credible enough for modeling, but not yet proven on the selected N87 E25/13/7 geometry.

## 4. N87 manufacturer bias curves support the physical mechanism
TDK explicitly publishes reversible permeability versus DC magnetic field for E/P/RM/PM cores and effective-permeability families including 50 / 100 / 200 / 500 / 1000.
The curves show large reductions in reversible permeability as HDC enters the saturation knee.

Source:
https://www.tdk-electronics.tdk.com/download/187238/990c299b916e9f3eb7e44ad563b7f0b9/pdf-n87.pdf

TDK also specifies N87:
- initial permeability ~2200 ±25%
- Bs ~490 mT at 25 C and ~390 mT at 100 C at H=1200 A/m / 10 kHz
- 25–500-kHz preferred range
- typical 25-kHz/200-mT/100-C core loss 57 kW/m3

The selected gapped core has effective permeability around the low-hundreds class.
Moving L by 3:1 requires the incremental effective permeability to fall by approximately the same 3:1 factor.
The TDK bias curves show that this type of permeability reduction is physically available under DC bias.

However the exact HDC required for the YK66 side-winding flux path cannot be read directly from the generic P/RM/PM/E curves.
A reluctance-network or finite-element magnetic model is still required.

## 5. Control-MMF envelope raised
R23 treated about 30–60 A-turns as preferred and 120 At as a research ceiling.

R25 widens the serious simulation envelope to:
- 0–120 At normal study range
- 150–180 At stress/model range

Reason:
3.0:1 may require operation farther into the incremental-permeability knee than the published 2.75:1 example.

With 60 turns per control leg:
- 0.5 A = 30 At/leg
- 1.0 A = 60 At/leg

For two symmetric control windings the magnetic-circuit interpretation depends on flux path and winding polarity; simple multiplication by path length is not a validated field calculation.

Using the R23 copper screen (~0.45 ohm total for two 60-turn control windings with ~0.129-mm2 copper):
- 0.5 A -> ~0.11 W copper loss
- 1.0 A -> ~0.45 W copper loss

Thus even the higher-current end can remain inside the previous ~0.5-W winding-loss target, before driver loss.

## 6. Low-voltage driver remains cheap enough
A compact H-bridge can provide bidirectional bias adjustment if required.
Current one-off examples are around JPY130–140 class:
- TI DRV8220
- TI DRV8837C
- Toshiba TB67H450AFNG

The driver cost is not the decisive problem.
The isolated AC/DC supply remains the costly line item.

## 7. Why static capacitance trimming is preferable to another relay
Suppose the raw X2 parts are ±20%.
The controller can always find the actual resonance if it physically exists, but it cannot create an overlap between two states that are too far apart.

A production/test procedure can therefore:
- measure actual capacitor values,
- add small permanently connected X2 trim capacitance to a branch if required,
- record actual state endpoints,
- calibrate magnetic-bias setpoints.

This shifts tolerance management from expensive high-voltage switching hardware into:
- a few inexpensive fixed capacitors,
- measurement,
- firmware calibration.

For the first prototype this is especially attractive.

The eventual production economics of end-of-line trimming still need comparison against tighter-tolerance capacitor procurement.

## 8. Cost architecture after R25
Primary architecture keeps only two power-relay functions.
Do not add a third relay unless MAG43 cannot reach the required tuning range.

Current cost blockers in order:
1. isolated low-voltage power supply
2. custom magnetic winding / assembly
3. independent surge/fault protection
4. PCB + assembly + shipping
5. coarse relay contacts

The H-bridge and MCU are comparatively minor.

## 9. New acceptance criteria
### Magnetic range
- desired: Lmax/Lmin >= 3.0 at room temperature
- minimum investigate threshold: >=2.9
- characterize at temperature extremes

### Resonator loss
- Rtotal target <=0.8 ohm across the useful 10–50-kHz map
- use actual core loss under simultaneous DC bias, not unbiased catalog-only estimates

### Production coverage
After measured C calibration:
- target effective capacitance error <=±5%
- Lmax calibration error <=±5%
- 10–50-kHz center-frequency physical coverage >=99% in the nominal 3.0:1 model
- residual gaps must still provide >=3 dB in the realistic Zgrid envelope via resonator skirts

### Hard-source case
At 0.1-ohm source:
- no oscillation
- no uncontrolled current
- no thermal violation
- attenuation is not required to meet the realistic-grid target

## 10. R25 decision
**MAG43 / 3.0:1 becomes the primary YK66 magnetic architecture.**

R23 MAG42 / 2.75:1 remains the fallback if:
- 3.0:1 requires excessive bias current,
- DC bias raises core loss too much,
- temperature collapses tuning range.

The third-relay / 8-state bank remains a contingency only.

## R26 gate
R26 must focus on the one remaining uncertain physical quantity:
**actual L(IDC) and core loss under DC bias for an E25-class 43-turn resonator.**

Tasks:
1. derive a reluctance-network behavioral model from the TDK N87 reversible-permeability curves,
2. calibrate the model against the published 40–110-uH / 0–1-A EE25 result,
3. predict control current for 279 -> 93 uH,
4. sweep 10–50 kHz and 25/60/100 C,
5. estimate equivalent core-loss resistance under bias,
6. reject MAG43 if 3.0:1 needs >1 A continuous bias or pushes Rtotal above 0.8 ohm for too much of the band,
7. if rejected, compare PM pre-bias and the three-relay bank on cost rather than hiding the failure.

No AC100V fabrication or energization is authorized by R25.
