# YK66 R35: MAG46 cost-down retune with 100/150/680-nF X2
Date: 2026-10-17
Status: RESEARCH / COST DOWN — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Purpose
R34 proves that the main architecture must become cheaper.
Before abandoning magnetic tuning, remove the awkward 82-nF coarse state and reduce resonator loss using readily available X2 values.

## 1. New candidate
Research name:
**YK66-MAG46**

TDK E25/13/7 N87 / ~0.50-mm-gap anchor:
- AL ~151 nH
- target Lmax ~320–325 uH
- magnetic tuning ratio target ~3.5:1
- Lmin ~91–93 uH
- main turns ~46
- TDK-bobbin DC resistance estimate ~59–60 mOhm

Coarse X2 bank:
- base C0 = 100 nF
- relay A adds 150 nF
- relay B adds 680 nF

Normal states:
- 100 nF
- 250 nF
- 780 nF

Both-relays 930-nF state is optional fallback/calibration only.

## 2. Nominal resonance coverage
At Lmax = 320 uH, Lmin = 91.4 uH:

- 100 nF: ~28.1–52.6 kHz
- 250 nF: ~17.8–33.3 kHz
- 780 nF: ~10.1–18.9 kHz

The three normal states overlap except for only a tiny endpoint issue near 10 kHz.
At Lmax around 325 uH, the 780-nF branch reaches ~10.0 kHz directly.

The actual optimum depends on post-trim tolerance and measured L range.

## 3. Post-trim tolerance screen
Screen:
- C components post-trim / binned to ±5%
- Lmax ±5%
- magnetic ratio 3.4–3.6
- target 10–50 kHz

Optimizing nominal Lmax around 320 uH:
- worst physical center-frequency coverage ~98.5%
- worst center gap ~0.60 kHz

This is not as strong as the original MAG50 82/180/680 map (~99.7% screen),
but finite resonator bandwidth can bridge this in realistic source-impedance cases.

The cost/supply advantage is that all three values are common active 310-VAC X2 parts.

## 4. Current one-off X2 price anchors
Würth WCAP-FTXX:
- 100 nF / 310 VAC X2: ~JPY70
- 150 nF / 310 VAC X2: ~JPY76
- 680 nF / 310 VAC X2: ~JPY158

Sources:
https://www.digikey.jp/en/products/detail/w%C3%BCrth-elektronik/890334025017CS/5038873
https://www.digikey.jp/en/products/detail/w%C3%BCrth-elektronik/890334023025/5038960
https://www.digikey.jp/en/products/detail/w%C3%BCrth-elektronik/890334025045/5038982

Coarse-bank subtotal:
~JPY304 before tax.

## 5. Magnetic loss improves
R23/R32 conservative core-loss screening was repeated for:
- ~46-turn main winding
- 100 / 250 / 780-nF states
- 10–50 kHz
- N87 E25-class geometry

Worst best-state unbiased equivalent core-loss screen:
~0.21 ohm.

Main winding Rdc:
~0.060 ohm.

Simple total branch screen:
- AC copper = 1.5 x Rdc
- relay contact = 0.10 ohm
- capacitor + PCB = 0.05 ohm

Results:
- core x1.0: Rtotal ~0.45 ohm
- core x1.4: ~0.53 ohm
- core x2.0: ~0.65 ohm

This is materially better than MAG50's prior ~0.80-ohm x2 stress result.

## 6. Why MAG46 is useful even if R34 cost still fails
MAG46 does NOT by itself solve the JPY3,500 first-unit economics.

It does:
- use easier-to-source X2 values,
- reduce main copper,
- lower estimated core-loss contribution,
- improve low-impedance attenuation margin,
- retain max one normally energized relay state.

Therefore MAG46 becomes the **magnetic fallback benchmark** against which radically cheaper architectures must be compared.

## R35 decision
### PROMOTE AS MAGNETIC BENCHMARK
MAG46 replaces MAG50 as the lowest-loss / supply-friendly magnetic reference.

### NOT A COST PASS
The first-unit all-in cost still fails because:
- custom magnetic component,
- relays,
- housekeeping supply,
- protection,
- assembly/NRE
remain.

## R36
Investigate a transformer-coupled tunable shunt:
- X2 line-coupling capacitor on mains side
- fixed high-frequency transformer/coupled inductor
- switched low-voltage reactive network on secondary
- no high-voltage tuning relays if possible
- no continuous DC core-bias power
- exploit impedance reflection and leakage/magnetizing resonance

Published PLC coupling literature already validates:
- series coupling capacitor + transformer as a power-line band-pass interface,
- resonance of leakage inductance with coupling capacitance,
- secondary-side switched impedance/capacitor networks as a way to tune high-voltage input impedance.

Key references:
https://doi.org/10.1109/TPWRD.2004.835260
https://www.mdpi.com/2079-9292/8/9/1022
https://patents.google.com/patent/EP2747282A1/en

No AC100V fabrication or energization is authorized by R35.
