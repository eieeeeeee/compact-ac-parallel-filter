# RC18-COST-MAX Stage 2B — low-current power-stage qualification

The first Stage-2 candidate (CSD87330Q3D + DGD0507A) is not adopted. DGD0507A is obsolete and the combination is not the cleanest fit to the existing regulated 5-V gate-drive rail.

## New primary candidate

**LMG1205 + IRLHS6376**

- LMG1205: active device, 4.5–5.5 V supply, independent HI/LI inputs, 35 ns typical propagation, 1.5 ns typical matching, several-MHz operation.
- IRLHS6376: active/preferred dual 30-V N-MOSFET, 2 x 2 mm, 63 mOhm max at 4.5 V, 2.8 nC typical Qg.
- Existing RC17 +5 V rail and bootstrap capacitor can be retained.

## Why the current envelope changed

The RC17 current protection is approximately ±0.18 A:

- VMID = 1.65 V
- VTH_HI = 3.3 * 61.9 / (61.9 + 10) ≈ 2.84 V
- VTH_LO ≈ 0.459 V
- INA240A1 gain = 20 V/V
- Rshunt = 0.330 ohm
- Itrip ≈ (2.84 - 1.65)/(20*0.330) ≈ 0.18 A

Therefore qualifying a 35-A replacement at 4.5 A is not representative of the actual controller protection envelope.

## Gate

The Stage-2B screening model sweeps 0.5–5 MHz and checks the actual 0.18-A trip point, 2x trip, 0.5 A and 1 A transient cases.

Candidate adoption requires no modeled loss penalty at the actual trip current across the whole sweep, no worse typical propagation/matching, at least 2x bus-voltage MOSFET rating, at least 5x current-trip margin, and direct compatibility with the existing +5-V rail.

A full-Qrr bound is also emitted. The low-current Qrr model is only a screening approximation; before fabrication the candidate still needs vendor transient-SPICE and bench ringing/thermal validation.
