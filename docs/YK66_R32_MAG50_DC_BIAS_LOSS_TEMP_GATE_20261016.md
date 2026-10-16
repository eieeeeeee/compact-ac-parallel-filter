# YK66 R32: MAG50 DC-bias loss / temperature qualification gate
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Executive result
MAG50 survives a much harder DC-bias/core-loss screen.

Primary candidate:
- E25/13/7 N87 class
- 0.50-mm gap catalog anchor
- ~50-turn main winding
- Lmax ~380 uH
- Lmin ~109 uH
- 3.5:1 target tuning ratio
- 82 / 262 / 762-nF normal coarse states
- max one relay energized during normal 10–50-kHz operation

The key remaining uncertainty is not ordinary copper loss.
It is **core loss under simultaneous DC premagnetization + 10–50-kHz AC flux**.

## 1. New experimental evidence on N87 under DC bias
Recent work directly characterizes TDK N87 under DC premagnetization:
- Muehlethaler et al., APEC 2025, “Core Material Characterization under DC Bias Conditions”
  DOI: 10.1109/APEC48143.2025.10977147
  Reports that DC premagnetization changes complex permeability and therefore magnetic loss.
- Yang et al., IEEE Access 2025, DOI: 10.1109/ACCESS.2025.3630785
  Experimental N87 dataset, 50–400 kHz, 25–100 C, DC bias up to saturation.
  The paper reports loss variation up to roughly 40% due to premagnetization in its measured conditions.
- Older Baguley et al. measurements also show ferrite core loss can increase significantly with DC bias:
  DOI: 10.1109/TMAG.2007.911594

These conditions are not identical to YK66.
Therefore R32 uses:
- x1.4 core-loss multiplier = evidence-informed central stress case
- x2.0 = hard analytical stress case

Neither is a product guarantee.

## 2. Published variable-inductor anchor remains 2.75:1
He et al., Electronics 2026:
- EE25/20/6 PC40
- 48-turn AC winding
- 30-turn x2 side DC windings
- 0–1 A bias
- 40–110 uH = 2.75:1 experimental tuning range

DOI:
https://doi.org/10.3390/electronics15142999

MAG50 target 3.5:1 is not directly experimentally proven on the selected N87 geometry.

## 3. Behavioral tuning model
For screening only, calibrate a saturation-knee model to the published 2.75:1 / ~60-At reference:

L0/L(MMF) ≈ 1 + 1.75*(MMF/60 At)^2

This gives:
- 2.75:1 -> 60 At
- 3.0:1 -> ~64 At
- 3.25:1 -> ~68 At
- 3.5:1 -> ~72 At
- 4.0:1 -> ~79 At

This agrees with the earlier reluctance/permeability screen in order of magnitude.

It is NOT a replacement for FEM or measurement.

## 4. Control-copper temperature screen
Provisional control winding:
- 60 turns per side
- two symmetric coils
- total DC resistance ~0.45 ohm at 25 C screening value

MAG43 target:
- MMF ~64 At
- equivalent current ~0.53 A
- Pcu ~0.128 W at 25 C
- copper at 100 C (+~29.5% R): ~0.166 W

MAG50 target:
- MMF ~72 At
- equivalent current ~0.60 A
- Pcu ~0.161 W at 25 C
- ~0.208 W at 100 C

Conclusion:
**the 3.5:1 extension does not create a control-copper thermal blocker in the analytical model.**

## 5. Resonant-series-resistance comparison
Simple branch budget:
- main-winding AC resistance = 1.5 x catalog-geometry DC estimate
- relay contact = 0.10 ohm
- capacitor + PCB/interconnect allowance = 0.05 ohm
- core-loss equivalent from prior unbiased screen
- core multiplier = 1.0 / 1.4 / 2.0

### MAG43
Approx:
- main Rdc ~0.0518 ohm
- worst screened unbiased Rcore ~0.24 ohm

| Core multiplier | Rtotal | Atten @Zs=0.5Ω | @1Ω | @3Ω |
|---:|---:|---:|---:|---:|
| 1.0 | 0.468Ω | 6.10 dB | 9.38 dB | 15.47 dB |
| 1.4 | 0.564Ω | 5.32 dB | 8.34 dB | 14.14 dB |
| 2.0 | 0.708Ω | 4.47 dB | 7.18 dB | 12.59 dB |

### MAG50
Approx:
- main Rdc ~0.0705 ohm
- worst screened unbiased Rcore ~0.27 ohm

| Core multiplier | Rtotal | Atten @Zs=0.5Ω | @1Ω | @3Ω |
|---:|---:|---:|---:|---:|
| 1.0 | 0.526Ω | 5.60 dB | 8.72 dB | 14.63 dB |
| 1.4 | 0.634Ω | 4.87 dB | 7.73 dB | 13.33 dB |
| 2.0 | 0.796Ω | 4.07 dB | 6.62 dB | 11.82 dB |

At the 0.1-ohm hard-source corner, neither architecture maintains the realistic-grid attenuation target; that remains the survivability/stability corner.

## 6. 100-C copper + x2 core-loss stress
Copper resistance temperature coefficient ~0.00393/K screening.

MAG50:
- main-copper contribution rises with temperature
- x2 core-loss stress
- total screen ~0.827 ohm

Resulting resonance attenuation:
- Zs=0.5 ohm: ~3.95 dB
- Zs=1 ohm: ~6.44 dB
- Zs=3 ohm: ~11.57 dB

This slightly exceeds the original Rtotal<=0.8-ohm research target by ~0.03 ohm, but still remains above 3 dB for the 0.5-ohm realistic-grid screen.

Interpretation:
**MAG50 is not rejected by the high-temperature / x2-loss stress, but its loss margin is narrow.**

MAG43 has more magnetic-loss margin, but worse system power/state economics.

## 7. DC-bias loss multiplier limit
At ~100 C with the current main-copper/contact allowances, MAG50 keeps Rtotal<=0.8 ohm only if the effective DC-bias core-loss multiplier remains roughly below ~1.9.

The 2025 N87 experimental literature reporting ~40% loss variation suggests this is plausible in at least some tested conditions.
But those data are not 10–50-kHz E25 side-biased MAG50 measurements.

Therefore:
- x1.4 = credible central stress
- x1.9 = Rtotal design boundary
- x2.0 = fail-margin / contingency stress

## 8. Independent evidence that large ferrite tuning ratios are physically possible
An older measured tunable-filter prototype using ferrite magnetic bias reported:
- inductance variation 12.4:1
- filter tuning range 3.5:1
- measured rejection 27–36 dB
- NiZn ferrite / RF topology
- very large DC magnetic control MMF (~1260 At)

Patent record:
US7889026B2 / US20090174501A1

This proves 3.5:1 filter tuning is not fundamentally impossible in ferrite.
It does NOT validate YK66’s low-MMF N87 implementation.

## 9. R32 decision
### CONDITIONAL PASS
MAG50 remains primary.

Reason:
- x1.4 DC-bias-loss stress remains well below 0.8 ohm
- x2 stress is still approximately 0.80 ohm at room-temperature copper
- control winding remains below ~0.2 W class
- realistic Zs>=0.5-ohm resonance attenuation remains useful

### FALLBACK
MAG43 remains ready if measured MAG50:
- cannot reach 3.4–3.6 tuning ratio,
- requires excessive current,
- or shows DC-bias core-loss multiplier >~1.9 over too much of 10–50 kHz.

### HARD STOP
Do not freeze the PCB around MAG50 until the magnetic element has an actual L(Idc) + loss characterization.

## R33
Investigate whether a lower-loss ferrite/material/core shape can buy enough Rtotal margin to make MAG50 robust without raising first-unit cost.
