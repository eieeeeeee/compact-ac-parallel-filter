# YK66 R11: current-limited virtual resistance, world-research concept converted into numeric requirements
2026-10-16. **Numerical modeling only / FAB HOLD / AC100V MAINS HOLD / real YK66 KiCad PCB NOT ready**.

## Engineering requirements carried over
Japanese AC100V 50/60Hz, L-N only **two-terminal parallel DM ACTIVE** noise reduction, one eventual production-intent PCB, independent real hardware fail-safe. Prototype PCB + all parts + assembly + shipping + tax <= JPY 3500 excluding stencil is an unproved goal. **Safety first**, then cost/buildability, then dB. No separate extra-low-voltage product PCB. Old RC18 47–54dB simulations cannot be claimed as new YK66 measurements.

## R11 quantitative results (Norton ideal equivalent)
Nine source/load pairs Rs={0.1,1,5} Ohm x Rl={5,10,20} Ohm. Current needed for reduction A dB is
`Ireq = (1-10^(-A/20))*|Voff|*(1/Rs+1/Rl)`.
`Voff` represents the **high-frequency noise-voltage peak**, not the AC100V mains voltage.
- At a **fixed 10mA peak Norton-noise current**, ideal 3dB reduction needs only **2.920542mA peak** in each case; baseline terminal noise voltage differs.
- At **fixed 100mV peak OFF-state noise voltage**, 3dB requires up to **297.895300mA peak**, and 50dB requires **1016.774477mA peak**, worst Rs=.1 Ohm, Rl=5 Ohm.
- With perfect-phase ideal 20mA peak driver, fixed 100mV and 3dB is theoretically attainable in just **3/9** purely resistive cases; the worst case can improve only **0.172003dB**.
- For all nine cases with 20mA theoretical output and 3dB ideal target, the fixed noise-voltage peak must be **<=6.713768mV**; this is a **necessary current-size condition, not a sufficient practical safety/performance gate**.

## Sign of shunt admittance is a new important design condition
- A purely real positive virtual conductance G>0 guarantees `|Yport/(Yport+G)| <= 1` if `Re(Yport)>0` (passive port). Thus a *perfect* real virtual resistor will not increase the terminal noise voltage even with reactive source/load.
- An impossible ideal 4.5S virtual conductance within the target band is a **mathematical goal only**, not a fabricated device: for fixed 10mA peak Norton noise, 20mA ideal current limit, and 9 port pairs x 3 illustrative reactive ratios, minimum **3.174343dB**. At fixed 100mV, the same capped mathematical device has worst **0.172003dB**.
- As soon as realistic high-pass, low-pass, driver-bandwidth and delay phase shifts are introduced, Y(s) develops nonzero reactive and sometimes negative real components. The positive-conductance guarantee no longer automatically applies.
- The R11 analytical screening explored **64** delay/HP/LP/gain variants, **27** imaginary-reactance stress cases each, 5/10/20/30kHz and 1–5kHz/30–700kHz guard samples, an ideal 20mA current limiter and a **hypothetical** <=1mA at 100Vrms/60Hz fundamental criterion. **0/64 passed all mathematical gates**. This rejects only the tested simplistic transfer functions, not all practical topologies.
- Illustrative rejected candidate had **-0.239dB worst 5–30kHz attenuation** (noise amplified) and **+2.388dB guard-band worsening** in this mock reactive stress model. No conclusion on actual oscillation without true physical loop dynamics.
- 50dB is not supported by this YK66 model; any physical 50dB specification demands real phase/gain accuracy, source impedance and injection hardware.

## Next engineering priority, not just another ideal sweeper
**Main one-board architecture research candidate:** two-terminal AC port -> coordinated line/surge protection -> safety-qualified DM sensing isolation -> positive-real frequency-selective analog control / low-voltage analog-twin compensation -> physically current-limited injection driver -> separately safety-qualified AC coupling -> independent hardware disable/fail-open. All on ONE intended PCB. This is an **architecture**, not a real electrical pin/wire circuit.
1. **Safety isolation & injection interface:** select actual 50/60Hz rated and surge-qualified sense and HF-current coupling components with manufacturer MPN, insulation evidence, phase/GBW and cost; no ordinary X2 bridging of isolation boundary.
2. **Independent hardware stop:** design real short-fault/mains-disconnect/overheat/UVLO/sensor-loss protection, analyze relay weld and board faults; do not rely on firmware.
3. **Real measured envelope:** establish nuisance disturbance peak amplitude distribution, complex Zsource(f)/Zload(f), 1–5 / 5–30 / 30–700kHz and the output-current compliance. With no measured amplitude, claims of 20mA being adequate are unsupported.
4. **Qualified parts -> single native KiCad PCB:** only then ERC/DRC/unconnected/net-parity, BOM/FIT/DNP, cost incl first-piece SMT, qualified professional safety review. No mains energization until independent safety review and appropriately equipped tests.

**Critical Japanese plug point:** two-prong AC plugs may be inserted with either orientation; labels L/N are not a safe assumption about which input can be touched as a neutral. No accessible test pad or scope earth on hot line.

## Reproducible deliverables
- `tools/yk66_r11_dm_envelope.py` — source/load nine-case, 64 controller approximations, bounded-current/sensitivity model.
- `tests/test_yk66_r11_dm_envelope.py` — numerical regression tests; no hardware safety test.
- `.github/workflows/yk66-r11-dm-environment.yml` — saves machine-generated JSON/CSV as Actions artifact; must retain MAINS/FAB HOLD.
- Full R11 zipped Japanese decision / functional interface / more detailed local model files are separate downloaded artifacts; GitHub source itself is runnable.

Technical reference: https://webstore.iec.ch/en/publication/4188 (IEC 61000-4-19 is a 2–150kHz differential-mode **immunity** test methodology, not a noise-filter attenuation guarantee). Prior project: `docs/YK66_R10_WORLD_AEF_RESEARCH_AND_RLC_48CASE_20261016.md`, `docs/YK66_R5_HERITAGE_DEEP_AUDIT_20261016.md`.
