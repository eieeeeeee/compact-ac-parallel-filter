# YK66 R18: Low-impedance plug-in shunt feasibility and adaptive passive termination
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Fixed product concept
- Plug into an ordinary AC100V 50/60 Hz outlet only.
- Two-terminal L–N parallel device; no series insertion between outlet and load.
- Goal: reduce household conducted power-line noise as much as practical.
- First-unit target: <= JPY 3,500 including PCB, components, assembly, tax and shipping; stencil excluded.
- Safety/protection must be independently reviewed before mains energization.

## Why the previous 0.1-ohm model is not a representative-only model
0.1 ohm remains an important hard-source stress corner, but measured LV network impedance is strongly frequency-dependent and affected by local appliances and resonances.
Evidence:
- Erhan et al. (ICHQP 2022) measured 10–150 kHz impedance at residential/office LV installations and found magnitude and resonance frequency strongly affected by locally connected devices:
  https://doi.org/10.1109/ICHQP53011.2022.9808479
- A 2022 review citing a four-country measurement campaign gives a 95th-percentile example of about 3 ohm @2 kHz, 6 ohm @20 kHz, 12 ohm @50 kHz, 18 ohm @100 kHz, 18 ohm @150 kHz:
  https://doi.org/10.3390/smartcities5020027
  This is NOT a Japanese-household guarantee.
- Most relevant to Japan: Nakayama & Okada, ISGT Europe 2025, measured network impedance from 100 V sockets at 58 sites in seven Japanese DSO service areas over 2–9 kHz. Their reported cumulative 95% values were below the currently discussed 230 V AMN impedance. DOI:
  https://doi.org/10.1109/ISGTEurope64741.2025.11305250

Therefore YK66 must be evaluated with a frequency-dependent impedance envelope, not a single 0.1-ohm value.

## Fundamental shunt limit
For a resistive Thevenin port Zth and an ideal positive shunt conductance that targets attenuation A:
K = 10^(A/20)
R_shunt_required = Zth / (K - 1)

For a baseline terminal noise of 100 mV RMS, the ideal compensation current after attenuation is:
I = 0.1 * (1 - 1/K) / Zth

### Required equivalent shunt for 3 dB
| Zth | Rsh max for 3 dB | ideal I for 100 mV baseline |
|---:|---:|---:|
| 0.1 ohm | 0.242 ohm | 292 mA |
| 0.5 ohm | 1.212 ohm | 58.4 mA |
| 1 ohm | 2.424 ohm | 29.2 mA |
| 3 ohm | 7.272 ohm | 9.74 mA |
| 6 ohm | 14.544 ohm | 4.87 mA |
| 12 ohm | 29.088 ohm | 2.43 mA |
| 18 ohm | 43.632 ohm | 1.62 mA |

### Required equivalent shunt for 10 dB
| Zth | Rsh max for 10 dB | ideal I for 100 mV baseline |
|---:|---:|---:|
| 0.1 ohm | 0.0462 ohm | 684 mA |
| 0.5 ohm | 0.231 ohm | 137 mA |
| 1 ohm | 0.462 ohm | 68.4 mA |
| 3 ohm | 1.387 ohm | 22.8 mA |
| 6 ohm | 2.775 ohm | 11.4 mA |
| 12 ohm | 5.550 ohm | 5.70 mA |
| 18 ohm | 8.325 ohm | 3.80 mA |

This is the key physical boundary. Low grid impedance is not solved by a smarter algorithm; it directly raises the required shunt current and lowers the required effective impedance.

## Why a large plain capacitor is not the right low-frequency answer
Approximating a 3 dB target by |Xc| = Rsh_required:
at 20 kHz, Zth=0.1 ohm needs ~32.8 uF, which would draw about 1.24 A reactive RMS at 100 V / 60 Hz in the ideal capacitor model.
At Zth=6 ohm, the same 20-kHz target is only ~0.547 uF and about 20.6 mA reactive RMS at 60 Hz.
Therefore the direct-capacitor answer changes by orders of magnitude with network impedance.

## New candidate: adaptive passive resonant termination
A series-loss RLC branch can cancel its own L and C reactance at the target supraharmonic. At resonance the branch impedance approaches its total series loss Rtotal. This can create a very low noise-frequency impedance without requiring a huge 50/60-Hz capacitance.

Illustrative NON-PRODUCTION example used only to expose the physics:
- target f0 = 20 kHz
- C = 470 nF
- ideal resonance L = 134.736 uH
- total branch R evaluated at 0.2 / 0.5 / 1 / 2 ohm
- simplified source/load model: real Zs plus 10-ohm load

At exactly 20 kHz, calculated ideal attenuation:
| Zs | R=0.2 | R=0.5 | R=1 | R=2 |
|---:|---:|---:|---:|---:|
| 0.1 ohm | 3.49 dB | 1.57 dB | 0.82 dB | 0.42 dB |
| 0.5 ohm | 10.58 dB | 5.81 dB | 3.38 dB | 1.86 dB |
| 1 ohm | 14.88 dB | 9.00 dB | 5.62 dB | 3.25 dB |
| 3 ohm | 21.97 dB | 14.99 dB | 10.39 dB | 6.66 dB |
| 6 ohm | 25.91 dB | 18.59 dB | 13.53 dB | 9.17 dB |

The important result is the bandwidth trade:
- In the hard 0.1-ohm case with R=0.2 ohm, >=3 dB exists only roughly 19.945–20.055 kHz (~110 Hz wide).
- With 1 uF and the corresponding 63.33 uH at the same R=0.2 ohm, the >=3 dB band is still only about 240 Hz wide.
- At Zs=6 ohm, C=470 nF and R=2 ohm, >=3 dB spans about 17.26–23.18 kHz (~5.92 kHz), with ~9.17 dB at resonance.

Interpretation:
**Hard-source + low-cost passive trap can be deep OR broad, but not both at once.**
To retain attenuation against a 0.1-ohm source, total loss has to be very low, which forces high Q and a narrow useful band.
This makes frequency tracking / retuning much more valuable than simply adding more passive damping.

## Why "adaptive passive" is different from a full active EMI filter
The proposed research direction is NOT to synthesize the entire cancellation current with an amplifier.
Instead:
1. detect the dominant supraharmonic frequency,
2. retune/select a low-loss passive resonant shunt near that frequency,
3. let the passive branch carry the absorption current,
4. use ordinary passive HF shunting above the range where capacitance is already effective.

This can potentially avoid an expensive high-current broadband active driver.
The control electronics only has to identify/tune the resonance, although real mains-safe switching, supply, failure containment, parasitics and transients are still unresolved.

## Literature support for frequency adaptation
Wang et al., IEEE JESTPE, 2025/2026:
"A frequency-adaptive differential mode active filter for mitigating supraharmonics in the 10-80-kHz range."
- automatically detects dominant switching-frequency-related SH
- controlled notch about 2.3 kHz wide
- controlled-grid prototype with different loads
- up to 40 dB single-tone suppression to the noise floor
- 36 dB first SPWM sideband
- ~17 dB average for +/-500 Hz around 20 kHz
- 25 dB for +/-100 Hz
DOI: https://doi.org/10.1109/JESTPE.2025.3597833

These dB values MUST NOT be copied as expected YK66 performance: source impedance, noise voltage and hardware are different.

Struzhko et al., EMC Europe 2024:
Electrically switchable notch prototype using discrete C/L adjustment:
- resonances approximately 87 / 93.4 / 100 / 109.2 kHz
- measured stop-stage attenuation about 24–25 dB at resonance
- stop-band about 10.8–17.2 kHz in the reported standard source/load setup
DOI: https://doi.org/10.1109/EMCEurope59828.2024.10722154

This validates retunable passive notch hardware as a real research class, but not as a YK66 mains-qualified two-terminal product.

## Piezoelectric branch remains a parallel research candidate
A 2025 study reports PZT conducted-EMI suppression using the low impedance of a piezoelectric ceramic at mechanical resonance:
- 25.1 dB switching-frequency interference-peak reduction in its reported setup
- 68.18% filter-volume and 70.52% weight reduction versus the compared traditional implementation
- parallel PZTs investigated for multiple frequencies
Source: https://www.sciencedirect.com/science/article/pii/S2090447925001765

PZT is attractive because it is naturally narrowband and potentially low-part-count, but YK66 still lacks:
- suitable AC mains safety classification,
- verified voltage/current/surge endurance,
- controlled impedance over production tolerance/temperature/aging,
- costed qualified part,
so it is NOT yet the primary path.

## Updated YK66 architecture ranking
1. **Adaptive passive resonant termination + passive HF shunt** — new primary research path.
2. **Small-current frequency-selective virtual conductance** — secondary helper only where passive tuning is insufficient.
3. **PZT resonant absorber** — high-upside research branch, qualification unknown.
4. **Fixed multiple RLC traps** — useful if dominant noise frequencies are stable, but vulnerable to frequency drift.
5. **Full broadband active cancellation** — remains RC18-style high-performance benchmark, likely unfavorable to YK66 cost.

## New evaluation matrix
Future simulations must include:
A. 0.1-ohm hard-source stress case
B. 0.5–1-ohm low-impedance cases
C. Japan 2–9 kHz measured-envelope-informed case when full numeric data become available
D. 10–150 kHz residential/office measured-envelope-informed cases
E. complex resonant source/load impedances
F. local appliance connection/disconnection perturbations

Metrics:
- attenuation vs frequency
- worst noise worsening anywhere in the sweep
- required branch/current stress
- 50/60-Hz current/dissipation
- retuning resolution and acquisition time
- component tolerance / ESR / DCR / core loss
- cost and part count
- independent failure containment

## Decision after R18
Do NOT optimize YK66 for a fictitious universal 0.1-ohm grid.
Keep 0.1 ohm as a survival/performance stress corner.
The most promising path for a <=JPY3500 plug-in-only two-terminal device is now:
**frequency-adaptive low-loss passive termination for dominant low/mid supraharmonics, combined with cheap passive shunting at higher frequencies.**

The next gate is R19:
quantize the retuning requirement across 10–80 kHz under 0.1 / 0.5 / 1 / 3 / 6-ohm source cases, then calculate how many switched resonance states (or how much continuous tuning range) are required to maintain >=3 dB without creating out-of-band worsening. No mains prototype is authorized before this gate plus fault/safety review.
