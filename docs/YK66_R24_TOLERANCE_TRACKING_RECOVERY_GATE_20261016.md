# YK66 R24: Tolerance / tracking recovery gate
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Purpose
Test whether the R23 MAG42 architecture remains useful when real X2 capacitor tolerance, magnetic range tolerance, and coarse-state boundaries are included.

Fixed product constraints:
- AC100V 50/60Hz plug-in-only
- two-terminal L-N parallel device
- first-unit target <= JPY 3,500 all-in except stencil
- no series insertion into the protected load

## 1. Real X2 tolerance is not a small detail
A current KEMET R46 100-nF / 310-VAC X2 part is specified at **±20% capacitance tolerance**.
Source:
https://search.kemet.com/component-documentation/download/specsheet/R463I3100DQM1M

Würth WCAP-FTXX confirms the required 310-VAC X2 class and provides standard 100 / 120 / 150 / 180 / 220 / 680-nF values for across-the-mains filtering.
Source:
https://www.we-online.com/en/components/products/WCAP-FTXX

Therefore the ideal R23 state map cannot be accepted using nominal values only.

## 2. Hard corner test of the R23 2-switch bank
R23 nominal:
- C0 = 100 nF
- switch A = 180 nF
- switch B = 680 nF
- four states = 100 / 280 / 780 / 960 nF
- nominal Lmax ≈ 266.4 uH
- nominal magnetic ratio = 2.75:1

A deterministic corner sweep was run with:
- each of the three capacitors independently ±20%
- Lmax scale ±10%
- usable magnetic ratio 2.6–2.9
- target frequency span 10–50 kHz
- controller assumed able to choose any available L continuously inside the actual range

Result:
- worst continuous-frequency coverage only about **76.7%**
- worst uncovered interval about **6.7 kHz**

Conclusion:
**automatic frequency tracking cannot recover a physical hole if none of the four C states can resonate there.**
The R23 nominal 2-switch / 2.75:1 architecture is therefore NOT tolerance-robust with unselected ±20% X2 parts.

This is a major correction to R23.

## 3. Monte-Carlo confirmation
A 100,000-case Monte-Carlo screen with a wider stress envelope:
- C0 / CA / CB each independently uniform ±20%
- Lmax uniform ±15%
- tuning ratio uniform 2.5–3.0

showed:
- only ~1.3% of random units had mathematically complete 10–50-kHz center-frequency coverage
- median maximum uncovered interval ~1.8 kHz
- 95th percentile maximum gap ~4.9 kHz
- 99th percentile maximum gap ~6.3 kHz

This does NOT include attenuation skirts, so some center-frequency gaps can still have useful attenuation.
But it proves the nominal state map cannot be treated as production-robust.

## 4. Three-switch / eight-state repair works technically but hurts the cost target
An 8-state bank using three switched capacitor additions was exhaustively searched with standard-value candidate capacitors.

Example strong candidate under:
- each capacitor ±20%
- Lmax ±10%
- magnetic ratio fixed at 2.75
- 10–50-kHz target

was approximately:
- base 68 nF
- additions 82 / 220 / 680 nF
- max total C about 1.05 uF

Worst corner screen:
- ~98% frequency-center coverage in the best optimized cases
- maximum residual center gap roughly 0.6–0.8 kHz for optimized combinations

Thus a third coarse state bit is an effective tolerance cure.

However a third mains relay adds roughly:
- another ~JPY290 one-off device cost in the G5Q class
- another ~0.2 W coil power
- more PCB area and assembly

This is unattractive because the control power supply is already a cost bottleneck.

## 5. Power-supply cost is now a first-class blocker
Current Japan one-off reference:
MEAN WELL IRM-01-5:
- 5 V / 1 W
- 85–305 VAC input
- CB / CE / cURus / TUV approvals
- about JPY 835–848 before tax
Source:
https://www.digikey.jp/en/products/detail/mean-well-usa-inc/IRM-01-5/7704616

IRM-02-class 2-W modules are about JPY882 class.
A 1-W supply is already marginal if:
- two relays can consume ~0.4 W,
- magnetic bias copper can approach 0.1–0.45 W,
- MCU / sensing / driver losses are added.

Therefore adding a third continuously energized relay is economically and thermally expensive even though the relay itself is cheap.

## 6. Bias driver itself can be cheap
The low-voltage bidirectional magnetic-control driver is not the major BOM blocker.

Examples at current DigiKey Japan one-off pricing:
- TI DRV8220: 1.76-A H-bridge, about JPY131
- TI DRV8837C: 1-A H-bridge, about JPY140
- Toshiba TB67H450AFNG: 3-A class, about JPY140

Sources:
https://www.digikey.jp/en/products/filter/power-management-pmic/motor-drivers-controllers/744
https://www.digikey.jp/en/products/detail/toshiba-semiconductor-and-storage/TB67H450AFNG-EL/16573092

The expensive item is safely obtaining isolated low-voltage power from AC100V, not generating bidirectional coil current once that rail exists.

## 7. Better repair: slightly increase magnetic tuning ratio and trim actual capacitance
Instead of adding a third mains relay, R24 tested how much guaranteed magnetic ratio is needed with the existing 2-switch 100/180/680-nF bank.

With independent ±20% capacitor tolerance and ±10% Lmax variation, after optimizing nominal Lmax:
- ratio 2.75 -> worst coverage ~83%
- ratio 3.0 -> ~88%
- ratio 3.25 -> ~92%
- ratio 3.5 -> ~95.5%
- ratio 4.0 -> ~98%
- ratio 4.5 -> ~99%
- ratio 5.0 -> ~100%

This shows that brute-force production tolerance would require too much magnetic range.

But YK66 does not need to accept raw ±20% state ratios:
the actual three X2 capacitances can be measured during assembly and statically trimmed / binned.
The controller already searches for the resonance, so absolute component value need not be accurate; only physical coverage and overlap matter.

## 8. Manufacturing-calibrated two-switch path
The most promising low-cost approach is now:
1. measure actual C0, CA, CB,
2. use small safety-rated parallel trim values or part selection to bring the effective state ratios near target,
3. calibrate actual Lmax/Lmin during end-of-line test,
4. store state boundaries / bias setpoints in MCU nonvolatile memory,
5. perform frequency tracking in operation.

No additional high-voltage tuning switch is needed.

A ±3–5% *post-trim effective capacitance* target is realistic enough to study, even if the raw X2 parts are ±20%.

## 9. Critical numerical result: 3.0:1 magnetic range is the new sweet spot
For the present 100/180/680-nF bank:
- nominal magnetic ratio 3.0
- post-trim C error ±5%
- Lmax spread ±5%

an optimized Lmax around 278–279 uH gives:
- worst center-frequency coverage about **99.2–99.4%**
- worst uncovered center interval only about **0.25–0.31 kHz**

With tuning-ratio variation:
- 2.95–3.05 -> ~98% worst center coverage
- 2.90–3.10 -> ~96.6%
- 2.85–3.15 -> ~95.2%

Because the resonant branch has finite attenuation bandwidth, a few hundred hertz center gap does not automatically mean a noise-amplification hole.
It still needs the full Rtotal / source-impedance model, but the geometry is now practical.

## 10. R24 decision
### REJECT
- raw ±20% capacitors with 2.75:1 tuning and no calibration
- adding many relay states as the primary production strategy

### HOLD
- third relay / 8-state bank as fallback
- tighter-tolerance X2 procurement if it proves cost-effective

### PROMOTE
**2-switch bank + measured/static-trim C + self-calibrated magnetic tracking + guaranteed ~3.0:1 inductance ratio**

This has a much better cost/performance balance than simply adding switching hardware.

## R25 gate
1. move the main winding from 42 to ~43 turns so Lmax lands near the tolerance-optimized ~279 uH point,
2. target Lmin ~93 uH, i.e. 3.0:1,
3. check whether N87 DC-bias data and the published 2.75:1 EE25 experiment support that extra ~9% tuning ratio,
4. estimate the MMF and control power needed to reach 3.0:1,
5. keep the 2-switch 100/180/680-nF X2 bank,
6. quantify how small the static trim capacitors must be.

No AC100V prototype is authorized by R24.
