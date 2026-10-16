# YK66 R11A — Manufacturer-backed AC power-line high-frequency coupling research
2026-10-16 / Research-only. **No line-coupling BOM approved, no live mains, no Gerber**.

## Breakthrough in sourcing a physical architectural precedent
TI **AFE031/AFE032 narrowband power-line communications** analog front ends have integrated line transmit power drivers and dedicated application notes that discuss **commercial AC mains** voltage/high-frequency coupling. This is a closer physical architecture than a generic OPA197 opamp-only hypothetical active shunt:
- TI AFE031 (https://www.ti.com/product/AFE031): 7–24V power amp with 1.5A quoted output-capability at defined conditions, adjustable current limit, fault interrupt and shutdown, receiver path, SPI to controller, analog/digital rails. NOT a guaranteed 1.5A current capability throughout our 5–30kHz installation or direct 100V connection.
- TI AFE032 (https://www.ti.com/product/AFE032): up to **1.9A typical**, 3.8MHz GBW typical, Iq 78mA typical, adjustable limit/thermal protection; **programmable internal HPF has 35kHz minimum** (datasheet table 19). Therefore its **built-in Tx/Rx filter settings cannot directly cover YK66 5–30kHz**, so do not install the IC as-is.
- TI application note (https://www.ti.com/jp/lit/ds/symlink/afe031.pdf) Section 10.2.1: low-voltage capacitor, mains-rated high-voltage capacitor, transformer and line inductance are a *line coupling design*, preventing 50/60Hz HV from reaching the low-voltage line amplifier while coupling its signal onto AC conductors.
- TI published AC mains line-coupling reference (https://www.ti.com/jp/lit/pdf/jaju540), Section 3.1.1.2: describes a separate **LV capacitor + transformer + HV capacitor + inductor** and separately the **protection network**. Use as electrical analysis / failure-mode / vendor grounding, not as automatic safety approval for a new product.
- TI application note SBOA130: https://www.ti.com/lit/an/sboa130a/sboa130a.pdf (source location should be checked if page unavailable).

**Current status:** physical transformer, capacitor voltage/class, 5kHz insertion loss/transformer magnetic properties, insulation rating and failure modes are NOT selected or qualified. High-current PLC AFE ICs may also cost more, use difficult QFN-48 assembly, consume substantial idle power and require a microcontroller; **not proven to fit first-piece ¥3500**. Their internal modulation path is NOT the same as stable DM negative-feedback synthetic conductance.

## Fundamental coupling-capacitor tradeoff (purely illustrative model)
For **a hypothetical simple capacitive-only 12Vpeak source**, Ipk=2*pi*f*C*12. For C=22nF:
- 5kHz: **8.294mA peak** maximum capacitive magnitude.
- 10kHz: **16.588mA peak** maximum.
- 30kHz: **49.763mA peak** maximum.
- If same C were put **across 100Vrms 60Hz**, ideal fundamental branch current is **0.8294mA RMS**.
To inject R11 worst-case **297.895mA peak at 10kHz** with only 12Vpeak and a capacitive reactance, the model requires **C >= 395.07nF**. If this C also directly spans 100Vrms 60Hz, the theoretical 60Hz current is **14.90mA RMS**. 1mA is a previous **project screening criterion**, not a universal legal limit. This is **not** an actual transformer-coupled driver transfer calculation.

**Implication:** A 22nF/12V simple capacitor cannot solve full 100mV / Rs=0.1Ohm worst case. A transformer may transform voltage and current, but cannot create power; its primary/secondary turns ratio, winding/current rating, parasitics, 50/60Hz blocking and surge must be modeled from a specific part. Nor does merely selecting any X2 cap safely cross an insulation boundary.

## R11A decision
1. Elevate vendor-documented **transformer + LV/HV coupling + line inductance + surge protection** as first *physical injection-branch research candidate* for the one final YK66 PCB. Not cleared for installation.
2. Treat AFE031/AFE032 as **reference driver and protection parts**, but defer adoption until actual 5–30kHz transfer, physical current and thermal SOA, total BOM/SMT (QFN), and external device control are verified. AFE032 internal 35kHz highpass makes default use unsuitable.
3. Prefer a **simple costed current-driver IC + rated coupling network** if it meets phase/current/safety, rather than carrying a complete PLC modem DSP/SPI stack.
4. Require real isolation manufacturer evidence, 50/60Hz stress, transient and IEC/PSE review, harmonic guard 1–5 and 30–700kHz, and worst 9 source/load networks before KiCad release.
5. Do not describe this method as proven 50dB, 3dB, AC100V-safe or <=¥3500; no physical device has been built.

R11 model: `docs/YK66_R11_LIMITED_VIRTUAL_RESISTANCE_DESIGN_GATE_20261016.md`.
