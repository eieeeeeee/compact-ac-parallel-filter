# YK66 R13 — Compare ORIGINAL minimalist v0.1 filter against active one-board YK66 (2026-10-16)

**Decision:** Minimize component count using the original 9-electronic-part architecture as a benchmark, but do not silently reclassify its passive filter as a proven 5–30kHz ACTIVE differential-mode device. NO manufacturing or AC100V safety release.

## Originals actually inspected (GitHub main, NOT the newer YK66 branch)
- `simulations/ltspice-v0.1/README.md`
- `simulations/ltspice-v0.1/shunt_filter_ac_v0_1.asc`
- `simulations/ltspice-v0.1/discharge_v0_1.asc`
- `bom/BOM.md`, `hardware/kicad/README.md`
- `hardware/kicad/review-v0.5/README.md`

## Actual v0.1/Rev.A parts
F1 Littelfuse 37402500000 fuse, C1 KEMET R533N410050P0K **1µF X2**, MOV1 Littelfuse TMOV14RP140E, R1=R2=220kΩ bleeder, R4=R5=47kΩ LED limiter, blue LED1, D1 reverse protection diode, J1 provisional electrical input interface. **Nine discrete electrical components excluding connector J1; ten items with connector J1** (PCB additionally). C2 optional 0.1µF X2 and R3/C3 RC branch are not populated in original Rev.A. **No current-controlled driver, noise sensing, compensator or active noise injection.** Rev.A board 32×28mm PREPROTOTYPE, no full safety review. v0.5 spacing revision is 50×35mm, KiCad 10 DRC 0 / unconnected0 for OLD passive board, not electrical safety certificate or approval for YK66 active board. J1 is *not* a mains plug-blade footprint.

## Check original LTspice v0.1 with exact stated small-signal assumptions
Circuit source Vin=1Vac SMALL-SIGNAL only, Rs to Vout; from Vout to AC return: Rbleed=440kΩ parallel with series ESL=25nH, ESR=0.08Ω, C=1µF. External load not modeled. Assumed ESR/ESL are NOT measured/specified KEMET R53 performance.

Compute H=Zpar/(Rs+Zpar); dB reduction = -20log10|H|. For comparison the 94kΩ indication resistor path is added as a high-impedance parallel ideal resistor (negligible at target frequencies; actual diode nonlinear). Values below reproduced with this optional 94kΩ path.

| Frequency | Rs=0.1Ω | Rs=1Ω | Rs=5Ω | Rs=10Ω | Rs=50Ω |
|---|---:|---:|---:|---:|---:|
| 5kHz | 0.0001dB | 0.0051dB | 0.1098dB | 0.4161dB | 5.4117dB |
| 10kHz | 0.0005dB | 0.0200dB | 0.4218dB | 1.4657dB | 10.3759dB |
| 30kHz | 0.0040dB | 0.1758dB | 2.8290dB | 6.6424dB | 19.5545dB |
| 1MHz | 7.0413dB | 22.6038dB | 36.0526dB | 42.0045dB | 55.9286dB |

**50Ω is a lab-fixture/source assumption, not representative household outlet source impedance**. Also the large 1MHz performance comes near assumed self-resonance f=1/(2π sqrt(25nH*1µF)) ≈1.0066MHz: ANY mismatch in physical ESL, EMI, wiring or parts can change it sharply. There is NO verified real-world AC100V 50dB proof.

At AC100Vrms/50Hz, ideal C1 branch reactive current ≈31.416mArms; at 60Hz ≈37.699mArms (not protective-earth leakage). 440k bleeder 100Vrms continuous dissipation ≈22.7mW; nominal theoretical post-unplug τ=.44s. The indication network dissipates additional power. Safe discharge under failures, resistor ratings, surge/impulse and temperature require practical approval.

## Parts-economy proposals
1. **KEEP** 1µF X2 shunt *as a passive comparison/possible standalone passive product*, independent of any hypothetical active control.
2. **KEEP subject to safety design** current/surge protection (fuse + thermal MOV), bleeder resistors, and rated mains-to-enclosure plug mechanics. No cost-cutting removal of actual safety devices.
3. **OPTIONAL DELETE** status LED, 47kΩ×2 resistors and reverse diode if a safety/operability review confirms indication is not required. This removes four components; dark LED does not demonstrate disconnection.
4. **NEVER OMIT** insulation, physical barriers, credible abnormal-fault response and appropriate line/current/capacitor ratings, even if a passive product is chosen.
5. **DO NOT LABEL ORIGINAL PASSIVE SCHEMATIC ACTIVE**. If target remains genuine active synthetic-impedance cancellation at 5–30kHz, it physically requires noise sensing, a compensator, current actuator and mains-rated isolation/injection + independently disconnectable safety; still not qualified nor proven ≤¥3500.
6. A cost-first product choice is **PASSIVE original** for fewest parts and modest variable suppression, **ACTIVE YK66** for genuinely controllable 5–30kHz effect but more cost/risk/engineering. User should explicitly choose if willing to surrender active requirement; without such authorization preserve the full YK66 specifications and use the old passive as a benchmark.

## Safety and development status
No assembled Rev.A/v0.5 board, no actual outlet/EMI measurement, and no proven PSE/product isolation approvals. Prior v0.5 DRC zero does not prove AC100V-safe installation or final manufacturing release. Keep new YK66 branch mainline **FAB HOLD / MAINS HOLD** pending physical failure-mode and professional safety review.
