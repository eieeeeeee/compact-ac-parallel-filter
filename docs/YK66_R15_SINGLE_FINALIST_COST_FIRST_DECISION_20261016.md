# YK66 R15 — ONE finalist, cost/assembly first (2026-10-16)

**DECISION: PRIMARY RESEARCH CANDIDATE = passive L–N SERIES (C_X2 1µF + R_DAMP 5Ω) SHUNT, retaining coordinated AC protection.** Back-up **ONLY IF MEASURED IMPEDANCE JUSTIFIES** = 1µF + series [1mH (internal model DCR 2.5Ω) || 20Ω]. The original bare 1µF X2 shunt remains a no-additional-circuit *benchmark*, not a third prototype. One intended AC100V PCB, not separate LV study. **NONFAB / MAINS HOLD: no approved physical circuit, no manufacturer-qualified 5Ω part, no independent fault containment, no physical reduction proof, no first-one ¥3500 quote.**

## Why this is the most rational "narrow" decision
R14's 32 variants, 9 resistive source/load cases and 27 fictional reactive cases were compared under precisely the same small-signal model; they are NOT real home-grid measurements.
| Candidate | MAIN shunt parts | 5–30kHz minimum dB 9 resistive cases | 5–30kHz minimum dB 27 reactive cases | guard-band maximum worsening in reactive cases |
|---|---:|---:|---:|---:|
| A original 1µF X2 | 1 | 0.0001084 | -1.3836156 | +2.02407 |
| **B series 1µF X2 + 5Ω R** | **2** | **0.0042018** | **-0.4520613** | **+0.43004** |
| D series 1µF + [1mH L || 20Ω R], hypothetical winding DCR2.5Ω | 3 | 0.0160734 | -0.0708741 | +0.28704 |

In the tested models B meets the *guard band worsening* criterion of <=0.5dB, with no coil, less cost, fewer failure modes than D. D's improvement in guaranteed 9-case target attenuation is only 0.0118716dB compared with B; without measured source impedances, a coil costing roughly ¥297 excl tax and further qualification cannot be justified. **Both B and D FAIL 5–30kHz >=3dB requirement; none of the 32 screened alternatives pass.** The B candidate remains a *low-cost filtering research baseline*, NOT the previously sought active cancellation product. It does not provide controlled high-attenuation synthetic admittance.

## Fundamental physics limit (high confidence, ideal only)
Worst resistive case Rs=0.1Ω and Rload=5Ω gives Zparallel≈0.0980392Ω. For a single *ideal* capacitive shunt at 5kHz, achieving 3.000dB by voltage division requires
`C=sqrt(10^(3/10)-1)/(2π f Zparallel) = 323.906 µF`.
If placed across 100Vrms 60Hz, ideal current would be `100*2π*60*C = 12.211 A rms`. This is **not** an acceptable direct-line capacitor suggestion: it is an explanatory lower-barrier showing why an inexpensive tiny universal 5–30kHz shunt cannot guarantee the full nine-case performance. RLC can target frequencies but cannot trivially resolve bandwidth, parasitic, fault or cost constraints.

## Preliminary *functional* BOM (not qualified for fabrication)
- F1, commercial line fuse/fuse coordination, previous Littelfuse 37402500000 **candidate** 1;
- MOV1, thermal MOV, previous TMOV14RP140E **candidate** 1;
- C1, 1µF **across-the-line X2** previous KEMET R533N410050P0K **candidate** 1;
- R_DAMP, **5Ω flame-resistant, surge/pulse, short-fault and fuse I²t coordinated** **UNSELECTED** 1; **never** substitute an arbitrary 0603 or general-purpose low-watt resistor;
- R1/R2, 220kΩ per manufacturer voltage/pulse/flame requirements **UNSELECTED final series** 2;
- J1, plug and enclosed electrical interface with mechanically retained parts **UNSELECTED** 1.
- LED1, D1, R4, R5 eliminated in the minimum-build study (four parts), contingent on function/label review. **LED dark ≠ absence of mains**. This changes original 9 electronic components to six *candidate* electrical components plus one interface; **not a verified safe product**.
- No separate control IC, PSU, PLC transformer, low-voltage injector, GaN, or STM32. Those are **not silently described as installed**.
- Only once a real 1-pc quote for each part/PCB/assembly/packaging/shipping/tax passes 3500 JPY can "cost PASS" be claimed.

## Serious short-fault blockers
In the proposed *series* RC shunt, if X2 C1 fails short, the 5Ω resistor may momentarily be exposed to 100Vrms: **nominal 20A and 2000W** until another element opens. This arithmetic is NOT a predicted real continuous event; it is an **unacceptable unqualified fault mode** without coordinated fuse, certified resistor failure mode, thermals and isolation review. The physically reversed two-prong plug may energize either marked conductor; avoid assuming the conductor labeled N is always neutral. Fusing and disconnection protection must be qualified across both polarities. Thermally protected MOV failure, hot components, enclosure, creepage/clearance, discharge after unplug, and surge leakage MUST be reviewed.

## Stop/go and scope
- **GO ONLY** to component safety sourcing, independent fuse/I²t and thermal fault review, full cost quote, KiCad of **the final AC100V design** (not a separate test PCB), and professionally controlled isolated measurement planning. Merely passing KiCad ERC/DRC does not pass mains safety.
- **NO-GO** for PCB fab, mains plug-in, or marketing as high-performance 5–30kHz active filter now.
- If 5–30kHz 3dB minimum across nine assumptions remains *non-negotiable*, R15 selected candidate **does not meet the target**. Do not fabricate it under that pretense; re-open a properly current-rated AC DM active/different-port topology, with higher likely cost. **User priority currently is safety, cost, manufacturability over dB**, so a narrow passive research finalist is fair without claiming the original active target fulfilled.
- Requirement of first-piece <=¥3500 **not yet verified**.

## Traceability
- Original `main/simulations/ltspice-v0.1`, `main/bom/BOM.md`.
- `docs/YK66_R13_ORIGINAL_10_PART_PASSIVE_VS_ACTIVE_COST_TRADE_20261016.md`.
- `docs/YK66_R14_GLOBAL_SEVEN_TOPOLOGIES_32CASE_MINPART_COMPARISON_20261016.md`.
- Model values at R14 CSV in user-generated R14 ZIP. Vendor datasheet and third-party product safety review required for all mains-path parts.
