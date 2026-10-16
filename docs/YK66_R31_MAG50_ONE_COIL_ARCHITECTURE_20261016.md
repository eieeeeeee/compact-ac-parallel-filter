# YK66 R31: MAG50 three-state / one-coil architecture
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Executive result
A new tuning point is better than MAG43 for the complete low-cost system.

Research candidate:
**YK66-MAG50**

Key idea:
increase magnetic tuning range moderately, then cover 10–50 kHz with only THREE normal operating capacitor states.
The fourth state from two relays is never required in normal operation.

Result:
**at most one relay coil is continuously energized.**

This removes the economic reason to use expensive latching signal relays.

## 1. MAG50 target
TDK E25/13/7 N87, 0.50-mm-gap catalog geometry anchor:
- AL about 151 nH
- choose Lmax target about 380 uH
- required main turns sqrt(380uH/151nH) ≈ 50.2 turns
- Rdc from TDK bobbin factor 28 uohm*N^2 ≈ 70 mOhm

Magnetic ratio target:
**3.5:1**

Lmin:
~108.6 uH

Compared with published 2.75:1 EE25 variable-inductor hardware, 3.5:1 is a larger extrapolation than MAG43 3.0:1.
It therefore needs a harder magnetic proof gate.

## 2. Coarse capacitor map
Use standard X2 values:
- base = 82 nF
- relay A adds 180 nF
- relay B adds 680 nF

Four electrical states exist:
- 82 nF: no relay ON
- 262 nF: relay A ON
- 762 nF: relay B ON
- 942 nF: both ON

But only the first three are needed for normal 10–50-kHz coverage.

With L = 380 -> 108.6 uH:

| Normal state | Relay count | Ideal resonance span |
|---|---:|---:|
| 82 nF | 0 | 28.5–53.3 kHz |
| 262 nF | 1 | 16.0–29.8 kHz |
| 762 nF | 1 | 9.35–17.5 kHz |

The handoffs overlap.

The 942-nF both-relays state spans lower still, but is not required for normal 10–50-kHz operation.
It can remain as a calibration / tolerance / below-10-kHz contingency state.

## 3. Relay power falls sharply
Using minimum-coil state selection across a uniform 10–50-kHz frequency axis:
- no coil: ~53.7% of the band
- one coil: ~46.3%
- two coils: 0%

Mean energized relays:
~0.463

Mean relay power with 200-mW ALDP coils:
~93 mW under this artificial uniform-frequency weighting.

More important:
**worst steady normal-operation relay power = 0.20 W, not 0.40 W.**

## 4. 50/60-Hz branch current improves
Maximum NORMAL coarse capacitance is now 762 nF, not the both-relays 942-nF fallback state.

Ideal L-N reactive current for 762 nF at AC100V:
- 50 Hz: ~23.9 mA
- 60 Hz: ~28.7 mA

This creates more current budget for the housekeeping dropper or HF helper.

## 5. Tolerance robustness
A deterministic screen was run with:
- each of the three capacitor components post-trim to ±5%
- Lmax ±5%
- magnetic ratio 3.4–3.6
- target 10–50 kHz

Optimized around Lmax ~370–380 uH with the 82/180/680-nF bank:
- worst center-frequency coverage ≈99.7%
- worst residual center gap ≈0.1–0.12 kHz

The finite resonator skirts should bridge a gap this small in realistic >=0.5-ohm source cases, subject to the real Rtotal model.

This is materially more robust than the earlier 3.0:1 / four-state map while using LESS relay holding power.

## 6. Magnetic-control penalty of 3.5:1
R26's calibrated reluctance/saturation screening model gives for the 0.50-mm-gap N87 anchor:

| Target ratio | Behavioral total-loop MMF |
|---:|---:|
| 2.75:1 | ~60 At |
| 3.0:1 | ~64 At |
| 3.25:1 | ~68 At |
| **3.5:1** | **~72 At** |
| 3.75:1 | ~75 At |
| 4.0:1 | ~79 At |

This is the surprising result:
in the simple saturation-knee model, extending 3.0 -> 3.5 does not require a proportional increase in MMF.

With two 60-turn control windings, ~72 At total-loop class corresponds to roughly 0.6-A-class control current depending on the exact magnetic path/polarity interpretation.
Using the previous ~0.45-ohm total control-copper estimate gives order-of-magnitude copper loss ~0.16 W.

This is NOT experimentally validated for the selected N87 geometry.

## 7. Core-loss screen
Using the same conservative R23/R26 N87 screening model:
- Nmain ≈50 turns
- 82 / 262 / 762-nF normal states
- L range ~109–380 uH

Worst "best normal state" equivalent core-loss resistance over sampled 10–50-kHz points:
~0.27 ohm.

A simple total branch screen:
- AC main copper allowance ~0.10 ohm
- relay contact ~0.10 ohm
- capacitor/PCB allowance ~0.05 ohm
- core-loss equivalent at 1.5x screen ~0.41 ohm

Total:
~0.66 ohm class worst screening point.

This remains below the R25/R26 0.8-ohm research target.

Again, DC-bias core loss is unmeasured and can invalidate this result.

## 8. 1.5 vs 1.8-uF dropper implication
With MAG50, worst NORMAL relay hold is only one 200-mW coil.

Representative high-load control budget:
- relay 0.20 W
- magnetic-control copper ~0.16–0.20 W
- MCU/detector/driver/regulation ~0.05–0.10 W
Total ~0.41–0.50 W.

At 12 V:
- 1.5-uF dropper gives only ~0.565 VA ideal at 100V/50Hz; margin may be insufficient after conversion losses.
- 1.8-uF gives ~0.678 VA ideal at 100V/50Hz and is more plausible.

Reactive-current budget using the largest normal 762-nF MAG state + 1.8-uF dropper:
- 50 Hz: about 80 mA total ideal L-N capacitive current
- 60 Hz: about 97 mA

Thus even the 1.8-uF dropper can remain near the provisional 100-mA overall design budget, before additional HF-helper capacitance.

Current one-off 1.8-uF / 310-VAC X2 examples are roughly JPY394–519.
Sources:
https://www.digikey.jp/ja/products/detail/kemet/R533N418050P1M/13577886
https://www.digikey.jp/ja/products/detail/kemet/R533R418050P0K/13577901

## 9. Relay choice improves
Panasonic ALDP112W is now preferred to the previous ALQ anchor:
- ~JPY175 one-off vs ~JPY200 class
- 5 A / 277 VAC
- 100-mOhm max initial contact resistance
- 4-kVrms contact-coil dielectric
- 10-kV contact-coil surge
- 200-mW coil
- IEC/EN60335-1-related family compliance

Source:
https://industry.panasonic.com/ap/en/products/control/relay/power/number/aldp112w

Two relays cost only ~JPY350 before tax.

## 10. Comparison with latching relay path
Two TQ2-L2-12V latching relays cost roughly JPY860–980 at current one-off pricing, have lower mains switching-voltage/contact-margin class, and add procurement risk.

MAG50 obtains the main latching-relay benefit—low steady relay power—through **state-map engineering instead of expensive hardware**.

This is a central YK66 design principle:
**spend magnetic tuning range to save high-voltage component cost and power.**

## 11. MAG50 trade
Advantages over MAG43:
- no two-coil normal state
- lower maximum normal X2 capacitance
- lower relay average and worst hold power
- makes a low-power non-switching supply more credible
- better post-trim frequency coverage

Disadvantages:
- 3.5:1 magnetic tuning is farther beyond the published 2.75:1 hardware
- requires larger Lmax / ~50-turn main winding
- needs actual N87 DC-bias/core-loss proof

## R31 decision
**MAG50 becomes the new system-cost primary research candidate.**

MAG43 remains the lower-magnetic-risk fallback.

R32 gate:
1. prove or reject 3.5:1 on the selected E25-class magnetic structure,
2. model 72–100-At side-bias range,
3. include DC-bias core loss,
4. compare 50-turn MAG50 against 43-turn MAG43 at equal measured attenuation,
5. choose one architecture before further PCB/BOM refinement.

No AC100V fabrication or energization is authorized by R31.
