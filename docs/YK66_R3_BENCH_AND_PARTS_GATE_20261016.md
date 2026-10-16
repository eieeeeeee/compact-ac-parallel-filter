# YK66 R3: measured-proof preparation and parts safety screen (2026-10-16)

**Status: analytical-model PASS, bench NOT MEASURED, FAB HOLD, AC100V MAINS HOLD.** End product remains a safely engineered AC100V/50–60Hz, L–N parallel **active** noise-reduction device. R3 is a *temporary isolated <=12V DC test fixture* only.

## Reproducible theoretical output

For a hypothetical 10-ohm resistive Norton port and 10mA peak disturbance, baseline Vpk = 100mV. A **hypothetical** current injector at 50% cancellation with a second-order bandpass centered at 10kHz, Q=8, and 0.5us delay predicts 50.049320mV and **6.012036dB** reduction at 10kHz. Full point-wise 30–700kHz, 1kHz resolution (671 points), worst *predicted* increase is **+0.016431dB at 105kHz**. There is no hardware timing/saturation/impedance/fault model and no evidence of real performance.

**Old 50dB question:** For *ideal* shunt C across a resistive Norton source, attenuation is `10 log10(1+(2*pi*f*R*C)^2)` dB. This ignores ESR/ESL and self resonance. Numbers under entirely different termination and frequency:
| Capacitance | Frequency | Assumed impedance | Ideal only |
|---|---:|---:|---:|
| 0.1uF | 10kHz | 10ohm | 0.0171dB |
| 1uF | 10kHz | 10ohm | 1.4451dB |
| 0.1uF | 1MHz | 50ohm | 29.9474dB |
| 1uF | 1MHz | 50ohm | 49.9430dB |

**1MHz / 50ohm / ideal 1uF ≈50dB is NOT actual 5–30kHz YK66 performance, nor AC100V measurement.** Real 1MHz capacitors can depart drastically from the ideal due to inductance. Passive and active figures must not be simply added.

## Bench validation gates (not authorization for mains)

1. Use *only* a verified isolated and current-limited DC fixture at or below 12V, a documented signal generator and return, and a calibrated 10-ohm test impedance. No L/N plug, mains hookup, AC100V injection secondary, live scope probing or earth-ground connection to live mains.
2. Obtain 3 baseline readings at 10kHz, preserve raw traces and FFT settings, noise floor, peak/RMS definition, generator/source impedance, scope probe and instrument bandwidth.
3. Apply *bounded, independently disableable* opposing injection, repeat 3 OFF-ON-OFF comparisons without moving wires or changing termination. At each trial record Voff, Von, physical injection current, phase, power and clipping. Compute measured reduction `20log10(Voff/Von)`.
4. First physical pass threshold is >=3dB measured reduction across all three trials at 10kHz with raw evidence; this is not the original 45–50dB product target.
5. Evaluate at 5/10/20/30kHz and the 30–700kHz watchdog band with real measurement floor and coverage recorded. Any unmeasured points are UNKNOWN. At measured points increase must be <=+0.5dB. Sweep source/load impedance for unexpected amplification.
6. Demonstrate physically independent hardware fail-OFF on sense loss, controller halt, brownout, driver fault, overcurrent and manual emergency stop at **extra-low voltage**. Historical 178mA is an old fault-trip threshold, *not* a continuous operating allowance.
7. Before any AC100V board release: complete a professionally reviewed insulated L/N line-sense, isolated current injector, coupling stress at 50/60Hz and surge, single-fault disconnection (including welded contact and capacitor short), rated protection components, thermal/fire and discharge, enclosure, creepage/clearance, leakage, EMC and applicable Japanese regulatory classification. Qualified lab tests only.

## Candidate components; none authorizes construction

- **MEAN WELL IRM-03-12:** 85–305Vac input, 12V at 250mA (3W), *reference only*, not a substitute for complete electrical safety review. https://www.meanwell.com/Upload/PDF/IRM-03/IRM-03-SPEC.PDF
- **STM32G474:** RC18 reuse proposal, old approximate ¥1300 single-MCU estimate not a verified new price; not required to run the initial bench model.
- **KEMET R46 X2:** manufacturer states AC310V across-the-line X2 use, and explicitly **not for use in “series with mains” applications**; cannot treat X2 rating as proof of a safe series injection coupler. https://content.kemet.com/datasheets/KEM_F3095_R46_X2_310_110C.pdf
- **Mains sensing isolation, injected-current transformer, independent cut-off, surge protection, fusing, thermal enclosure:** specific qualified part models **TBD / BLOCKED**.

Legacy *planning* subtotal is ¥915 + ¥1300 = ¥2215, leaving ¥1285 versus ¥3500 (1 unit PCB+components+assembly, stencil excluded). All isolation, injection, protection and manufacturing prices are still unknown; therefore **cost goal NOT PROVEN**.

## Gate status
R3 formula + unit model: PASS (model only). Actual low-voltage A/B experiment: NOT DONE. Safety hardware and line injection: BLOCKED. Native YK66 KiCad ERC/DRC: NOT DONE. Commercial mains and fabrication release: **PROHIBITED**.

Companion runnable source: `tools/yk66_bench_r3.py`, `tests/test_yk66_bench_r3.py` (run Python 3 standard-library tests locally). The numerical model cannot certify safety or attenuation of an AC100V device.