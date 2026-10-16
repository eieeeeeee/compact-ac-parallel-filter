# YK66 R9 overseas forum/vendor design selection (2026-10-16)

**Research and phasor calculation only; no manufacture or AC100V connection authorized.** Requirements: Japan AC100V 50/60Hz, plug L-N TWO TERMINALS parallel (not inline) with differential-mode (DM) active suppression at 5–30 kHz, independent hardware failsafe, single final PCB, prototype first-piece price target ¥3500 all-in except stencil, and easy assembly over headline dB.

## Overseas source findings that materially change the selection

1. Texas Instruments TPSF12C1 and TPSF12C3 are **COMMON-MODE AEF**, not DM cancellation chips. TI E2E contains a case where CM improved but DM emissions deteriorated; TI engineer confirms device is not a good fit to DM applications. TPSF12C1 datasheet explicitly rejects differential signal when extracting common-mode noise. Therefore **reject device for YK66**. Do not misrepresent TI max 25dB CM as YK66 DM.
   - TI forum: https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1557633/tpsf12c1-the-performance-of-cm-has-improved-while-that-of-dm-has-deteriorated
   - Manufacturer: https://www.ti.com/lit/gpn/TPSF12C1

2. **ADOPT THE VALIDATION METHOD, NOT THE IC** from TI's TPSF12CX-MATHCAD common-mode AEF calculator: the concept of voltage sense to current injection, measured complex impedance, gain/phase margin, parasitic L/C/R, compensated/damped response, enabled vs disabled insertion loss. A future YK66 *DM-specific* plant/actuator model must be derived afresh; no CM circuit/netlist directly transposed.
   - https://www.ti.com/tool/TPSF12CX-MATHCAD
   - https://www.ti.com/tool/TPSF12CX-DESIGN-CALC

3. Electronics Stack Exchange experts note a differential LC mains filter needs damping to prevent resonance and source/load interaction. Thus preserve R5 P15 all-15 fail at 1–5kHz, and a guard from 30–700kHz; simulate resistor/capacitor electrical and fault energy. BUT mains inline-L+X2 is TWO-PORT, not a two-terminal parallel plug-in, and must NOT replace the user's requested architecture.
   - https://electronics.stackexchange.com/questions/551005/whats-the-difference-between-these-two-differential-mode-emi-filters

4. EEVblog engineers emphasize that typical LISN/50-ohm fixture attenuation is different from low source-impedance real mains, and real PCB layout/parasitic/capacitor SRF matter. Keep R8 nine resistive impedances AND require physical complex Zsource/Zload at each target frequency.
   - https://www.eevblog.com/forum/projects/how-to-test-a-low-impedance-filter-circuit/
   - https://www.eevblog.com/forum/beginners/how-can-i-design-a-emi-filter-for-smps/
   - https://electronics.stackexchange.com/questions/765072/how-to-calculate-this-ti-emi-filter-design

5. TI LM25149-Q1 includes an **active DIFFERENTIAL-MODE EMI reduction function**, but belongs to a 3.5–42V DC buck controller; it cannot be connected to rectified 100VAC (~141V peak nominal) or used as the two-terminal line shunt. Reject as YK66 AC mains candidate.
   - https://www.ti.com/product/LM25149-Q1

## Ranked YK66 architecture selection
- **PRIMARY ENGINEERING RESEARCH PATH (not build-qualified):** two-terminal L-N voltage sensing + low-delay continuous-time ANALOG DM compensation + bounded current injection + commercially appropriate mains isolated coupling + independent fail-OFF/open and surge/fusing.
- **PASSIVE COMPARISON ONLY:** appropriately qualified X2 line-to-line shunt with fuse/discharge/thermal design. Ideal 10kHz / 10Ω voltage attenuation = 0.00083 dB (22nF) to 1.445dB (1µF); real parasitic values are unmodeled. An X2 capacitor does NOT prove active-driver isolation and is NOT an active alternative.
- **REJECT for goals:** TPSF12C1/TPSF12C3 CM ICs; LM25149-Q1 DC buck AEF; inline mains chokes requiring four connection terminals; old RC18 MCU/GaN power stage transplanted as-is.
- **Unknown:** No vendor/forum evidence establishes an off-the-shelf, validated, safe, affordable mains-rated 2-wire parallel DM cancellation IC for our 5–30kHz application. We cannot promise the topology will satisfy all goals.

## R9 phase-delay calculation = substantive new regression
For normalized measured noise voltage 1 and ideal antiphase injected noise a exp(-j φ), residual = |1 − a exp(−j φ)|; ideal cancellation dB = −20 log10(residual). Phase from effective delay τ is 360 f τ degrees. This is an abstract phasor thought experiment: no finite-current driver, impedance or AC safety claimed.

| a | delay @ 30kHz | phase | theoretical attenuation |
|---|---:|---:|---:|
| 0.5 | 0us | 0deg | +6.021dB |
| 0.5 | 1us | 10.8deg | +5.723dB |
| 0.5 | 5us | 54deg | +1.790dB |
| 1.0 | 1us | 10.8deg | +14.507dB |
| 1.0 | 5us | 54deg | +0.838dB |

For a perfectly matched cancellation amplitude a=1, ideal 50dB at 30kHz requires total phase error <~0.181deg = <~16.78ns equivalent delay. Source/load variation and magnitude error make this much harder, not easier. Do NOT specify a casual low-speed DSP delay for 50dB target. In the low-cost primary option, prioritize continuous-time analog inner control with minimal effective phase lag, subject to **actual stability and safety verification**.

## Permanent R9 design requirements
- R9-DM-01: Verify vendor IC senses DM, not CM; L-N only, not PE/chassis or inaccessible upstream reference.
- R9-LP-02: Require real closed loop and positive/negative loop phase margins for worst source/load plus measured complex impedances and coupling hardware.
- R9-EMI-03: Record suppression and amplification, identical LISN/port conditions OFF/ON/OFF across 1–5, 5–30, 30–700kHz; pay attention to source impedance and parasitics.
- R9-DAMP-04: Damped resonances, short faults, component energy, real temperature, startup and recovery must be included.
- R9-SAFE-05: Independent hardware current limit, thermal/trip, fail-open, commercial surge/creepage/clearance and enclosure; protection qualification and one-piece BOM+fab+SMT+shipping/tax quote required.
- R9-NONFAB-06: H0/H1/H2 in R8 remain BLOCKED. No complete KiCad YK66 schematic/PCB approved; old existing KiCad files are not this new product.

Source: docs/YK66_R8_CURRENT_ENVELOPE_AND_NONFAB_GATE_20261016.md, docs/YK66_R5_HERITAGE_DEEP_AUDIT_20261016.md.
