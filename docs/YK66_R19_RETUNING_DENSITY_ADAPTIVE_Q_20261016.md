# YK66 R19: Retuning-density limit, adaptive-Q concept, and continuous-tuning literature
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Purpose
Deepen R18 specifically on the user's hardest requirement:
**plug-in-only, two-terminal parallel operation, <=JPY3500 target, while retaining useful attenuation when the local mains impedance is low.**

## 1. Retuning-density calculation: a hard limit appears
R18 showed that a low-loss series-resonant shunt branch can create a very low impedance at one supraharmonic without a huge 50/60-Hz capacitive current.

For a concrete analytical branch:
- resonance reference: 20 kHz
- L = 134.7356 uH fixed
- C = 470 nF at 20 kHz
- total branch series loss R = 0.2 ohm
- load = 10 ohm resistive for this comparison
- source Zs swept 0.1 / 0.5 / 1 / 3 / 6 ohm
- target: >=3 dB voltage-noise attenuation
- C is assumed tunable so the same L can resonate anywhere from 10 to 80 kHz
- required C range: ~1.88 uF at 10 kHz down to ~29.4 nF at 80 kHz

For this fixed-L series resonance, the >=3 dB useful width is nearly independent of center frequency. Exact small-signal calculations give:

| Zs | Peak attenuation at resonance | >=3 dB width | Approx. number of resonance states to tile 10–80 kHz |
|---:|---:|---:|---:|
| 0.1 ohm | 3.49 dB | 116 Hz | ~604 |
| 0.5 ohm | 10.58 dB | 727 Hz | ~97 |
| 1 ohm | 14.88 dB | 1.270 kHz | ~56 |
| 3 ohm | 21.96 dB | 2.950 kHz | ~24 |
| 6 ohm | 25.91 dB | 4.665 kHz | ~16 |

This is a decisive result:
**Trying to guarantee >=3 dB continuously over 10–80 kHz against a true 0.1-ohm source with one cheap retunable passive trap would require hundreds of accurately placed tuning states.**
That is not a credible <=JPY3500 product path.

Therefore 0.1 ohm should remain a hard-source stress/no-instability/no-overstress corner, NOT a universal minimum-attenuation acceptance condition.

## 2. Adaptive Q / adaptive damping is mathematically preferable
For a real Thevenin impedance Zth and a target of >=3 dB, the usable detuning bandwidth of a series-resonant shunt is not maximized by making R as small as possible.

The bandwidth-optimum series resistance is approximately:
R_opt = Zth / (K^2 - 1), K = 10^(3/20)
Since K^2-1 is ~0.995, R_opt is approximately Zth.

That choice gives about 6 dB peak attenuation at exact resonance and maximizes the frequency interval that still stays above 3 dB.

With the same fixed L = 134.7356 uH and 10-ohm load:
| Zs | Zth=Zs||10ohm | approximate Ropt | max >=3dB width | states for 10–80 kHz |
|---:|---:|---:|---:|---:|
| 0.1 | 0.099 | 0.099 ohm | 166 Hz | ~422 |
| 0.5 | 0.476 | 0.478 ohm | 798 Hz | ~88 |
| 1 | 0.909 | 0.913 ohm | 1.524 kHz | ~46 |
| 3 | 2.308 | 2.319 ohm | 3.869 kHz | ~19 |
| 6 | 3.750 | 3.768 ohm | 6.287 kHz | ~12 |

Implication:
**The best resonant shunt should ideally adapt two parameters, not one:**
1. center frequency (L/C product),
2. effective damping / Q (R).

When the grid is hard, use a low-loss/high-Q state.
When the grid is softer, increase damping so one tuning state covers a wider band and branch current is reduced.

This is the new "adaptive-Q passive terminator" concept.

## 3. A very relevant 2025 experimental result was found
Struzhko, Nemashkalo, Hartman and Leferink, IEEE Transactions on EMC 2025:
"A Tunable EMI Notch Filter for AM Radio in Electrical Vehicles"
DOI: https://doi.org/10.1109/TEMC.2025.3620422

Important observations:
- continuous electrical tuning using **core saturation for an inductor** and **dielectric biasing for a capacitor**
- 540–750 kHz prototype
- up to 60 dB in 50/50-ohm insertion-loss conditions
- real converter experiment reported up to ~30 dB DM-current suppression
- inductance reduction by a factor of 33 versus their compared LPF
- the paper explicitly states that the concept can also be applied to other bands, particularly 2–150 kHz
- it cites earlier work by the same group in the 80–130 kHz range

But this is NOT a direct YK66 solution:
- their complete notch filter is a multi-stage input/output filter, not our two-terminal plug-in shunt
- their tunable inductor uses a DC saturation winding and was tested with bias current up to 1.2 A (the text notes the concept can use up to 2 A at very low bias voltage)
- an additional high-inductance blocking element is used to keep the bias supply impedance from corrupting the tunable inductor
- laboratory supplies and control were used
- 50/50-ohm data cannot be translated to a 0.1-ohm household source

Therefore YK66 may reuse **only the tunable-reactance principle**, not the topology or claimed dB.

## 4. R19 architecture update
Primary research architecture becomes:

### A. High-frequency broadband passive branch
Use cheap passive shunting where capacitance already has useful impedance.
Goal: take the "easy" higher-frequency energy without active power electronics.

### B. One dominant-frequency resonant shunt branch
A low-loss series-resonant branch is connected only as a two-terminal shunt function.
Its resonance is moved toward the strongest detected supraharmonic.

### C. Coarse + fine tuning
Full 10–80 kHz continuous tuning by hundreds of switched states is rejected.
Instead investigate:
- coarse range selection (small number of ranges),
- fine continuous tuning inside one range,
- or a small switched capacitor bank plus a magnetically tunable inductor.

### D. Adaptive damping / Q
A small number of damping states is worth more than blindly maximizing Q:
- low source impedance -> low R, narrow/deep
- higher source impedance -> higher R, wider/less current

### E. No broadband high-current cancellation amplifier unless needed
The resonant branch should carry the majority of the noise absorption current.
Any active circuitry should primarily sense, tune, and protect rather than synthesize all cancellation current.

## 5. What the low-impedance requirement now means
For YK66, "works in low impedance" should be split into two gates:

### Performance gate
Use measured-envelope-informed Japanese / residential impedances and realistic complex loads.
Require useful attenuation on dominant household noise bands.

### Hard-source survivability gate
At 0.1 ohm:
- no oscillation
- no noise amplification beyond the selected guard limit
- no uncontrolled branch current
- no thermal/surge/fault violation
- attenuation may fall below 3 dB

This is much more physically honest than requiring 3 dB over the entire 10–80 kHz range against 0.1 ohm, which the R19 state-density calculation shows is economically unrealistic.

## 6. Japan-specific evidence added
Nakayama & Okada, IEEE ISGT Europe 2025:
"Field Study of Network Impedance in the Range from 2 kHz to 9 kHz in Japan"
DOI: https://doi.org/10.1109/ISGTEurope64741.2025.11305250

The study measured network impedance from **100 V sockets at 58 sites across seven Japanese DSO service areas**.
The public summary says the cumulative 95% impedance values from 2–9 kHz were below the single-phase 230-V AMN impedance being discussed in IEC work.

This is directly relevant: YK66 must not substitute a European 95th-percentile curve for Japanese 100-V data.
The full numeric Japanese distribution is now a priority input for R20 if obtainable.

## 7. R19 decision
1. Fixed RC/X2-only is no longer the main low-frequency route.
2. Full broadband active cancellation remains too expensive/complex for the <=JPY3500 primary route.
3. **Adaptive-Q resonant shunt + passive HF absorption is now the primary YK66 research architecture.**
4. Continuous magnetic tuning is experimentally credible as a technology class, but the published implementation's bias-current/blocking-inductor overhead may be too expensive for YK66.
5. Switched-capacitor/coarse-range tuning may be cheaper, but mains-safe switching parasitics and cost are not yet qualified.
6. PZT remains the wildcard for eliminating the tuning power stage, but mains qualification is still unresolved.

## R20 gate
Directly compare the three practical tuning mechanisms under the same YK66 constraints:
- switched capacitor bank
- magnetically saturated variable inductor
- small active virtual-conductance helper

For each: count real components, estimate parasitic resistance needed to hit the R19 Q targets, estimate control-power burden, identify likely cost blockers, and reject anything that cannot plausibly stay under the first-unit JPY3500 target.

No AC100V fabrication or energization is authorized from R19.
