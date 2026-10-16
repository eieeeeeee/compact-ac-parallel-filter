# YK66 R12 — Vendor-priced PLC magnetic coupling and OFF-fault resonance (2026-10-16)
**RESEARCH / IDEALIZED MODEL ONLY. NO AC100V MAINS, NO PCB FAB, NO VALIDATED HARDWARE.** AC100V 50/60Hz L-N two-terminal parallel active differential suppression, one final PCB, independent failsafe, first-unit all-in ¥3500 ex stencil. Safety then buildability and cost, then dB.

## Crucial real supplier parts/prices; one piece in JPY excluding sales tax
| Component | MPN | Reference cost | Adoption |
|---|---|---:|---|
| 12V 3W isolated AC/DC | MEAN WELL IRM-03-12 | ¥915 | CANDIDATE only |
| 870µH PLC transformer 1.307:1 | Würth 750510476 | ¥872 | CANDIDATE only |
| 1.5A typical PLC line AFE | TI AFE031AIRGZT | ¥1038 | REJECT cost-first main path |
| 10MHz GBW analog compensator | TI OPA197IDBVR | ¥412 | Compensator only; NOT enough drive |

AFE031 full 3-part subtotal ¥2825 before tax, ¥3107.50 with modeled 10% tax, **only ¥392.50 left** for AC line protection, independent disconnect, sensor, high-voltage coupling cap, analog control, assembly, PCB, shipping. **Not a viable cost-proven candidate**. OPA197 3-part cost ¥2199 excl tax / ¥2418.90 incl tax and leaves ¥1081.10, but omits REQUIRED driver plus every protection/PCB/etc. IRM-01-12 1W unit ~¥848 would save ¥67 only and its power capacity is not verified. All quote snapshots may change.

References:
- https://www.digikey.jp/en/products/detail/mean-well-usa-inc/IRM-03-12/7704636
- https://www.digikey.jp/ja/products/detail/w%C3%BCrth-elektronik/750510476/4341882
- https://www.digikey.jp/ja/products/detail/AFE031AIRGZT/296-29692-1-ND/2762559
- https://www.digikey.jp/ja/products/detail/texas-instruments/OPA197IDBVR/5962128
- https://www.digikey.jp/ja/product-highlight/w/wurth-electronics-midcom/mid-plc-power-line-communications-coupling-transformers (MID-PLC family reinforced insulation 4kVAC; complete-device verification remains essential)

## NEW HAZARD: primary driver open-circuit fault leaves transformer magnetization resonance
Model assumes manufacturer-listed primary magnetizing Lm=870µH and primary:secondary turns ratio n=1.307; reflected Lm at secondary is approx **509.2µH**. When the primary driver is HIGH IMPEDANCE after fault, magnetizing inductance may remain connected on the secondary, and an AC-side series coupling capacitor C forms a **passive resonant branch**.
`f_0=1/(2π sqrt((Lm/n²)*C))` gives:
| C | Ideal driver-open fault resonance | Ideal 100Vac/60Hz L-N branch reactive current |
|---|---|---|
| 22nF | 47.55kHz | 0.829mArms |
| 47nF | 32.53kHz | 1.772mArms |
| 100nF | 22.30kHz | 3.770mArms |
| 220nF | 15.04kHz | 8.294mArms |
| 470nF | 10.29kHz | 17.719mArms |
| 1µF | 7.05kHz | 37.702mArms |

100nF to 1µF put this illustrative driver-open resonance inside the desired 5–30kHz band. The resonance is absent/altered with a shorted primary (modeled 2ohm). **Simply switching off a driver IC is not proven sufficient: independent disconnection and both open/short/weld failure modes must be analyzed**. This model omits real magnetic loss/ESR/ESL/core nonlinearities and physical safety; no real resonant frequency is measured.

## Finite-ability coupler estimate at hypothetical 5Vpeak driver
A simple ideal transformer with Lm, 2Ω output resistance and AC-side C was evaluated at 5/10/20/30kHz and 9 resistive Norton source/load combinations. At 10kHz:
- 100nF → ~24mA peak line injection in this model.
- 470nF → ~112mA peak.
- 1µF → ~229–240mA peak AND 37.7mA L-N 60Hz capacitor reactive branch.
Under R11's **fixed 100mVpeak HF noise** worst-port hypothetical requirement of **297.895mApeak for 3dB**, even the listed 1µF / 5V drive model lacks sufficient current in the worst condition. This is NOT proof of a working closed-loop driver: finite current, temperature, waveform compliance, magnetic saturation, leakage inductance, insulation, breakdown, surge, phase and coupling losses are not validated. Do not interpret example currents as real ratings or earth leakage.

The full 972-case OFF fault sweep, 216-case driven upper-bound screen, nine local Python unit checks, cost JSON, documentation, and runnable local source are in separately downloadable R12 ZIP; the GitHub companion script reproduces critical invariant resonance/current/cost checks.

## R12 decisions
1. TI AFE031 from commercial mains PLC is **valuable vendor precedent** for LV capacitor + transformer + appropriately qualified HV capacitor + surge protection, but its specific controller and BOM are unsuitable for a proven ¥3500 first-one quote. https://www.ti.com/jp/lit/pdf/jaju540
2. **Keep Würth PLC transformer as a testable part candidate only** pending datasheet bandwidth 5–30kHz, per-winding/core loss, HV isolation and latest safety compliance, total installed size and cost. 4kVAC family reference is not a product approval.
3. Analog control (OPA197 class) can be cost benchmark for compensation, but NOT substitute for high-current driver.
4. No actual specified high-voltage isolation/sense, line-side independent fail-open, protection, or one-board KiCad drawing is available. Both **MAINS HOLD** and **FAB HOLD** remain.
5. Reuse old RC18 S1 128-corner sweep and E50 manufacturing fault checks as test methodology; never claim RC18's old 47–54dB model equals YK66 measurements.

Previous R11: `docs/YK66_R11_LIMITED_VIRTUAL_RESISTANCE_DESIGN_GATE_20261016.md`. Data supplied in local R12 ZIP; the source files do not themselves constitute a manufacturable circuit.
