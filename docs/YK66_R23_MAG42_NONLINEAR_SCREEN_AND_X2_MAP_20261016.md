# YK66 R23: Magnetic nonlinear screening, turns optimization, and standard-X2 retune map
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Executive result
R22 used a 50-turn E25/13/7 N87 main winding because the catalog AL=151 nH gives 377.5 uH directly.

R23 finds a better system-level point:
**42 main turns is superior to 50 turns for YK66.**

Why:
- lower copper DCR,
- lower AC flux density and core-loss equivalent resistance,
- still keeps maximum X2 capacitance near 1 uF,
- keeps 60-Hz L-N reactive current close to the original 1-uF YK66 baseline,
- enables a very convenient three-capacitor coarse bank using standard values near 100 nF / 180 nF / 680 nF.

The magnetic concept remains alive, but core-loss and exact DC-bias tuning remain HOLD items until an actual nonlinear measurement/model is available.

# 1. Source data used

## TDK E25/13/7 N87
TDK B66317:
- le = 57.5 mm
- Ae = 52.5 mm2
- Amin = 51.5 mm2
- Ve = 3020 mm3
- N87 initial permeability ~2200
- one ungapped + one 0.50-mm-gapped half: AL ~151 nH, effective permeability ~131
- standard bobbin B66208: winding area AN=61 mm2, mean turn length lN=50 mm, AR=28 uohm

Sources:
https://www.tdk-electronics.tdk.com/inf/80/db/fer/e_25_13_7.pdf
https://product.tdk.com/en/search/ferrite/ferrite/ferrite-core/info?part_no=B66317G0500X187

N87 material:
- Bs = 490 mT at 25 C and 390 mT at 100 C, specified at H=1200 A/m, 10 kHz
- optimum listed frequency range 25–500 kHz
- typical Pv = 57 kW/m3 at 25 kHz, 200 mT, 100 C
- material curves include DC magnetic bias and core-loss-vs-frequency/flux plots

Source:
https://www.tdk-electronics.tdk.com/download/540216/d6940b239127a8bab71b22168746021b/pdf-n87.pdf

## Experimental variable-inductor anchor
He et al., Electronics 2026:
- EE25/20/6 PC40
- center gap 1.04 mm
- main winding 48 turns
- control windings 30 turns x 2 on outer legs
- series opposition for AC decoupling
- IDC = 0–1.0 A
- measured/used variable inductance 40–110 uH = 2.75:1

DOI:
https://doi.org/10.3390/electronics15142999

# 2. DC-bias MMF sanity check: 30x2 turns is physically credible
The published 30-turn x2 / 1-A control arrangement corresponds to roughly 60 total control ampere-turns around the symmetric control-flux loop.

Using the E25/13/7 effective magnetic path length only as a first geometric scale:
H_equiv ~ 60 At / 57.5 mm = ~1040 A/m.

TDK specifies N87 saturation flux density at H=1200 A/m.
This does NOT prove the E25/13/7 side-leg control structure will give exactly 2.75:1, because:
- DC control flux geometry differs from le,
- outer-leg cross section differs from center-leg Ae,
- center gap is not necessarily in the DC control loop,
- bias changes incremental/reversible permeability rather than simply using a static Bs point.

But it explains why the published 30-turn x2 / 1-A structure is in the correct order of magnitude:
**the control MMF reaches the permeability-knee/saturation-field scale of N87.**

R23 initial nonlinear-control sweep remains:
- total control-loop MMF: 0–120 At
- preferred useful range: about 30–60 At if 2.75:1 can be achieved there.

# 3. Control-winding copper power is no longer the main blocker
Approximate side-leg control winding screening model:
- two equal control coils
- mean turn length estimated ~28 mm/turn including insulation/clearance
- copper resistivity 0.01724 ohm*mm2/m

Example: 60 turns per outer leg using ~0.129 mm2 copper (roughly AWG26 copper area class):
- total copper length both coils ~3.36 m
- estimated total Rdc ~0.45 ohm
- 0.5 A gives 30 At per leg / ~60 At around the symmetric control loop
- copper loss ~0.11 W
- 1.0 A gives ~120 At total-loop MMF
- copper loss ~0.45 W

This is a geometry screening estimate, NOT a finished winding design.

Important new conclusion:
**If side-leg space and insulation permit ~60 turns/leg, the previous <=0.5-W control-copper target is plausible.**

The harder issues become:
- physical side-coil manufacturability,
- insulation strategy,
- bias-driver loss,
- actual MMF-to-L curve.

# 4. Main-winding turn-count optimization
For the TDK 0.50-mm-gapped E25/13/7:
Lmax = AL*N^2
Rdc estimate = AR*N^2

To preserve the same resonance coverage, capacitances scale approximately as (50/N)^2.

Screening table:

| Main turns | L range at 2.75:1 | Max coarse C | 100V/60Hz current at max C | TDK-bobbin Rdc estimate | Relative core-loss screen at worst high-band low edge |
|---:|---:|---:|---:|---:|---:|
| 50 | 137–378 uH | 0.685 uF | 25.8 mA | 70 mOhm | ~0.475 ohm |
| 46 | 116–320 uH | 0.809 uF | 30.5 mA | 59 mOhm | ~0.402 ohm |
| 44 | 106–292 uH | 0.885 uF | 33.3 mA | 54 mOhm | ~0.368 ohm |
| **42** | **96.9–266 uH** | **0.971 uF** | **36.6 mA** | **49 mOhm** | **~0.335 ohm** |
| 40 | 87.9–242 uH | 1.070 uF | 40.3 mA | 44.8 mOhm | ~0.304 ohm |
| 38 | 79.3–218 uH | 1.186 uF | 44.7 mA | 40.4 mOhm | ~0.274 ohm |

The last column is only a screening estimate described in Section 6.

**42 turns is selected for R24**, because it keeps the largest coarse capacitance approximately at the familiar 1-uF class while cutting main-winding DCR and magnetic flux versus 50 turns.

# 5. Standard X2 values now almost perfectly cover 10–50 kHz
With:
- Nmain = 42
- Lmax = 266.4 uH
- Lmin = 96.9 uH
- tuning ratio = 2.75:1

Use:
- base C0 = 100 nF
- switched addition C1 = 180 nF
- switched addition C2 = 680 nF

Four capacitance states:
- 100 nF
- 280 nF
- 780 nF
- 960 nF

Ideal resonance ranges:

| C state | Resonance span |
|---:|---:|
| 960 nF | 9.95–16.50 kHz |
| 780 nF | 11.04–18.31 kHz |
| 280 nF | 18.43–30.56 kHz |
| 100 nF | 30.84–51.14 kHz |

There are two tiny center-frequency gaps:
- about 120 Hz around 18.37 kHz
- about 280 Hz around 30.70 kHz

Those are much smaller than the useful attenuation width once source impedance is in the >=0.5-ohm class.

Example using Rtotal=0.8 ohm and a 10-ohm illustrative load:
- at the 18.37-kHz gap midpoint: ~4.0 dB at Zs=0.5 ohm, ~6.6 dB at Zs=1 ohm, ~11.8 dB at Zs=3 ohm
- at the 30.70-kHz gap midpoint: ~3.9 dB at Zs=0.5 ohm, ~6.5 dB at Zs=1 ohm, ~11.6 dB at Zs=3 ohm

Thus **standard-value X2 parts are sufficient; custom 75/130/480-nF values are not needed.**

At Zs=0.1 ohm, 3-dB universal coverage is not an acceptance requirement; it remains the hard-source stability/current/survival case.

# 6. Core-loss equivalent resistance: first screening, not yet a sign-off
Core loss is critical because the resonant branch needs low effective series resistance.

A screening Steinmetz-like fit was used only to estimate order of magnitude:
- conservative room-temperature reference ~120 kW/m3 at 25 kHz / 200 mT, read from the TDK N87 loss curves
- frequency exponent ~1.36, consistent with 25-to-100-kHz published loss scaling
- flux exponent ~2.0, consistent with the rough spacing of TDK's 25/50/100/200-mT curves

This is NOT a manufacturer equation and must not replace measurement.

For the 50-turn case it produced approximately 0.03–0.48 ohm equivalent core-loss resistance across candidate resonance states.
Moving to 42 turns scales B roughly with N and reduces this screening loss by about (42/50)^2 ~= 0.71.

Result:
- worst screened core-loss contribution falls to about **0.34 ohm** near the low end of the 100-nF high-frequency state
- much of the remaining map is lower

This is encouraging but not decisive.

Potential Rtotal budget for the 42-turn branch:
- main copper DC: ~0.05 ohm
- AC/proximity uplift: unresolved, target <0.10–0.15 ohm total main copper
- one relay contact: up to ~0.10 ohm initial-spec class from R20
- X2 ESR: unresolved, expected to be materially below ohms but must be measured at 10–50 kHz
- core-loss equivalent: screening ~0.05–0.34 ohm
- PCB/interconnect: tens of milliohms target

Therefore **Rtotal <=0.8 ohm remains plausible**, but is not yet proven.

# 7. Actual resonance current and flux under the existing 100-mV noise model
Use:
- baseline open-circuit HF noise = 100 mV RMS
- Rtotal = 0.5 ohm
- 10-ohm load
- Nmain = 50 shown first as the conservative older magnetic-flux anchor

Calculated branch current / Bpk for Lmax:
- Zs=0.1 ohm: ~167 mA RMS, ~34 mT
- Zs=0.5 ohm: ~102 mA RMS, ~21 mT
- Zs=1 ohm: ~71 mA RMS, ~14 mT
- Zs=3 ohm: ~36 mA RMS, ~7 mT
- Zs=6 ohm: ~24 mA RMS, ~5 mT

At 42 turns and the correspondingly lower L range, B falls roughly another 16%.

So under a 100-mV household-noise model, normal resonant AC flux is far below N87's 390–490-mT saturation values.

But a 1-V HF disturbance would increase those flux swings by roughly 10x before nonlinearity/current limiting, so abnormal-noise and surge protection remain mandatory.

# 8. Real X2 price anchors improve the BOM outlook
Current DigiKey Japan one-off examples:
- 100 nF / 310 VAC X2, KEMET R46 family: roughly JPY95–130 class
  https://www.digikey.jp/ja/products/detail/kemet/R463I3100DQM1M/9685188
- 180 nF / 310 VAC X2, Würth 890334025025CS: about JPY80 before tax
  https://www.digikey.jp/en/products/detail/w%C3%BCrth-elektronik/890334025025CS/5038876
- 680 nF / 310 VAC X2, KEMET R463I368050H7M: about JPY188 before tax
  https://www.digikey.jp/ja/products/detail/kemet/R463I368050H7M/15822599

Coarse-C subtotal is therefore only about **JPY360–400 before tax** at one-off distributor pricing.

TDK core half price currently varies by listing/update:
- gapped N87 B66317G0500X187: roughly JPY170–210 before tax
- ungapped mate is lower-cost order-of-magnitude

Sources:
https://www.digikey.jp/ja/products/detail/tdk/B66317G0500X187/3914718
https://www.digikey.jp/en/products/filter/ferrite-cores/936

This materially strengthens the <=JPY3500 plausibility versus the former relay-DAC architecture.

# 9. Relay standby-power check
A latching power relay would eliminate coil standby power, but currently found 250-V latching power-relay examples are too expensive for YK66 (roughly JPY1700+ each in one-off distributor pricing).

The low-cost path therefore still favors two ordinary small mains-rated relays for coarse C selection.
The previous G5Q-class estimate is about 200 mW coil power each, so two relays can cost roughly 0.4 W when both energized.

This means control-power optimization must consider:
- relay state coding so the common operating state minimizes energized coils,
- whether a normally-closed/contact-form alternative can reduce average coil use,
- whether a single multifunction relay topology can replace two coils without raising cost/contact resistance.

Do NOT replace the low-loss relay contacts with high-Ron PhotoMOS solely to save coil power; R20 showed that would destroy resonator Q.

# 10. R23 architecture freeze for next modeling gate
Research candidate becomes:

**YK66-MAG42**
- TDK-class E25/13/7 N87
- one ungapped + one ~0.50-mm-gapped half as geometry anchor
- 42-turn low-loss main winding
- target variable L ~97–266 uH (2.75:1)
- two symmetric side control windings, provisional 60 turns/leg
- target control-loop MMF ~0–60 At normal, up to 120 At research sweep
- standard X2 coarse bank: 100 nF + switched 180 nF + switched 680 nF
- four states: 100 / 280 / 780 / 960 nF
- adaptive resonance about 10–51 kHz
- passive HF shunt above that
- no broadband cancellation amplifier

# 11. R23 decision
## PASS
- Main-turn reduction 50 -> 42 is beneficial.
- Standard safety-capacitor values can replace custom values.
- Control-winding copper-power target <=0.5 W is analytically plausible.
- Coarse capacitors remain inexpensive enough for the JPY3500 target.
- Rtotal <=0.8 ohm is still physically plausible in screening.

## HOLD
- Exact L(IDC) curve for this E25/13/7 side-bias geometry.
- AC resistance / proximity-effect measurement.
- Core-loss equivalent resistance under simultaneous DC bias and 10–50-kHz AC.
- Side-winding insulation/manufacturing method.
- bias driver + control supply cost and loss.
- full safety/fault behavior.

## New key risk
**Core loss is now a first-class design variable.**
At high Q it can behave exactly like unwanted series resistance.
The next optimization must minimize not only copper DCR but also Bpk and core-loss resistance.

# R24 gate
1. Create a behavioral L(IDC,T) curve using TDK N87 DC-bias data plus the published 2.75:1 variable-inductor result as calibration bounds.
2. Sweep Nmain=38–46 and automatically optimize C states under:
   - max 60-Hz branch current,
   - max Rcore equivalent,
   - <=2 coarse switches,
   - 10–50-kHz coverage.
3. Add capacitor tolerance +/-10/20%, AL/gap tolerance and relay/contact resistance tolerance.
4. Determine whether automatic frequency tracking can recover all tolerance-induced resonance error.
5. Cost the bias driver + low-voltage supply.
6. Reject the magnetic approach if worst-case Rtotal exceeds 0.8 ohm over too much of the 10–50-kHz range.

No AC100V fabrication or energization is authorized by R23.
