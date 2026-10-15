# YK66 / Engineering Screen R1 — AC100 V Active Parallel Injection (NONFAB)

Date: 2026-10-16 JST
Status: **ANALYTICAL_SCREEN_PASS / ARCHITECTURE_HOLD / FAB_HOLD / MAINS_HOLD**
Baseline: `rc18-r2-3-1c-native-gate`; immutable earlier candidate. Mathematical test workflow checks **this model only**.

## 1. Mission and architecture decisions
- Japanese 100 Vrms, 50/60 Hz **line-to-neutral (L-N) parallel ACTIVE differential-mode** conducted-noise cancellation, not a series filter and not a passive X-capacitor-only substitution.
- First article (Macnica) is Fly-Buck, useful only **after an appropriate DC front end**; LM5161 max input **100 VDC**, whereas nominal rectified 100 Vrms sinusoid reaches ~141.42 Vpeak; at 107 Vrms ~151.32 Vpeak, excluding surges.
- Baseline for power budgeting is **IRM-03-12, 12 V 250mA / 3 W / 85–305 Vac / 37×24×15 mm**, reference one-unit listing **¥915 ex tax** (stock/quote must be rechecked). This is *only* a module candidate, **not approval of the finished apparatus**.
- Add a 3.3V conversion stage and determine 12V-driver, MCU, analog, gate-drive, latch and measurement actual power from datasheets/bench. Existing 178mA is a **hardware fault trip**, NOT continuous allowable current.
- RC18 native ERC/DRC 0 on 2026-10-10 belongs solely to **that historical design variant**; it does not validate YK66 AC100V.

### Physical isolation architecture choices — NOT yet selected

**A: All active injection circuitry referenced to mains (HOT) and completely enclosed**
- A power module that began isolated cannot be described as safe SELV after intentional mains referencing. No user-exposed ports, external programming, scope ground, touch buttons, cable shields or accessible test points without an appropriate independent safety barrier.
- Safe firmware debugging must be via qualified isolation and documented measurement arrangement. Requires full mains product insulation/fault review. Cheap relative to multiple power domains perhaps, but not assumed safe.

**B: Isolated safe-side MCU; signal and power cross via rated isolation into mains HOT driver, or certified line-injection isolation transformer**
- Galvanic barriers must be fully specified including functional/common-mode bandwidth and insulation ratings, not inferred from X2 components or a generic power transformer.
- Adds isolation devices/transformer, protection, loss and size; 3,500 yen target seriously constrained.

**C: Passive X2 shunt benchmark**
- Can be a separate, mains-rated comparison apparatus if properly engineered. **Does NOT fulfill the YK66 active-noise-cancellation requirement** and may create a different response.

The required fault response is to return to a benign electrically disconnected injection state with **independent hardware cutoff**, not only a software shutdown. Whether the proposed contactor/semiconductor arrangement is actually fail-open remains unverified.

## 2. First-principles checks of legacy RC18 values
Legacy low-voltage evaluation values: **C=1µF**, **R301=4.7Ω**, current shunt=**0.33Ω**, hardware nominal trip=**178mA peak**, ideal tone excitation=**12V peak**. This is a *linear series R-C thought experiment*. It does **not** model the transformer, actual mains bridging, firmware, voltage rating, nonlinear GaN/MOS switching, transients or safe operating area.

### Hypothetical passive L-N R-C current at the fundamental
| Voltage | Frequency | Current RMS | 4.7Ω damping loss | Apparent power |
|---|---|---:|---:|---:|
| 100Vrms | 50Hz | 31.416mA | 4.639mW | 3.142VA |
| 100Vrms | 60Hz | 37.699mA | 6.680mW | 3.770VA |
| 107Vrms | 50Hz | 33.615mA | 5.311mW | 3.597VA |
| 107Vrms | 60Hz | 40.338mA | 7.648mW | 4.316VA |

The 107V used here is an illustrative upper sustained grid-voltage value from Japan's voltage-quality rule, **not a design maximum for surges/overvoltage category**. The X2-specific capacitance/rating, bleed circuit and enclosure have **not** been selected; these numbers cannot be used for component derating or mains energization.

### Ideal sinusoidal injection tone into that series R-C
| Frequency | Calculated tone current at 12Vpk | Peak voltage at 178mA trip |
|---|---:|---:|
| 5kHz | 372mA | 5.736Vpk |
| 10kHz | 719mA | 2.971Vpk |
| 20kHz | 1,275mA | 1.676Vpk |
| 30kHz | 1,641mA | 1.301Vpk |

**Critical finding:** A full 12Vpk tone, if the simple R-C impedance is presented to it, exceeds the nominal 178mA trip threshold over the studied band. Actual driver dynamics and 100V injection topology may make it **worse or different**. Simply reusing the 12V PWM driver and C=1µF across the line is not a valid design. The injection impedance/current operating envelope and independent trip threshold must be re-engineered together.

At 12V ×178mA = **2.136W instantaneous arithmetic reference**, the 3W module has only **0.864W arithmetic headroom** before control and losses. This product is **not** a valid estimate of average input power because a trip threshold is not a steady load and injected current may be reactive.

### Is 45–50dB broad-band cancellation a reasonable first prototype gate?
- For ideal equal-amplitude two-tone cancellation, **50dB** requires normalized residual **≤0.3162%**; a pure phase mismatch must be about **≤0.181°**. At 30kHz the equivalent timing error is only **16.8ns**.
- **45dB:** ≤0.5623% residual; phase ~0.322°; equivalent 29.8ns at 30kHz.
- Those are *ideal mathematical sensitivity examples*, **not** an actual RC18 prediction. Source/load impedance changes, ADC/DAC delay, current-sense phase, actuation clipping, EMI feedback and tolerance compound the challenge.
- Initial hardware goal should be **showing a repeatable, measured noise reduction without degrading another band**, then expanding coverage. Old 45/50dB targets may remain stretch goals, but are not evidence of operation.

## 3. Cost gate — numbers must remain explicit
| Cost item | 1-unit assumption (JPY ex tax) | Evidence |
|---|---:|---|
| IRM-03-12 3W module | 915 | DigiKey reference listing 2026-10 |
| STM32G474CBT6 | 1,300 | Historical RC18 estimate **not verified as current one-off price** |
| Partial subtotal | 2,215 | Arithmetic |
| Residual under 3,500 | **1,285** | To cover *all* remaining parts, PCB and assembly |
| HV-rated coupling, independent cutoff, thermal/surge protection, isolation, detection, other ICs, passives, PCB, assembly | **UNKNOWN** | No complete quotes |

**Status: COST_UNPROVEN / HIGH RISK.** Do not substitute a bulk 1,500-piece MCU unit price for a one-off purchase. A distributor listing can show a part currently out of stock; availability and lead time must be verified at purchase. Stencil excluded by initial user rule. Plug/enclosure/shipping, legal compliance, EMC and safety qualification must be separately budgeted even if not part of the 3,500-yen accounting.

## 4. Named engineering release gates and decisions

| Gate | Condition | Current |
|---|---|---|
| F0 | Isolation architecture and mains-potential zones documented and independently reviewed | BLOCK |
| F1 | Active injection connection functionally proven with complete mains-rated device model | BLOCK |
| F2 | No-fault and single-fault surge/thermal/OCP/current operating envelope assessed | BLOCK |
| F3 | Complete 12V, 3.3V and injector power budget incl. transients | BLOCK |
| F4 | GPIO pinout, analog ranges, firmware load, phase margins & stable control validated | BLOCK |
| F5 | Real purchasable single-unit safety-qualified BOM + PCB + assembly ≤¥3,500 | BLOCK |
| F6 | Full KiCad native ERC/DRC/Unconnected/Parity for the **same** YK66 candidate | BLOCK |
| F7 | Product/regulatory/thermal/insulation/enclosure/qualified laboratory plan completed | BLOCK |
| F8 | Prototype built; safe specialist AC100V testing and measured ON/OFF conducted-noise results | BLOCK |

**Do not create or release fab/order files from this screen.** Gate F0–F8 are not waived by code coverage, success in GitHub Actions, generic insulation claims or math.

## 5. Concrete next design change order (avoid branch churn)
1. **Freeze a complete L-N injection mechanism** as one of A/B above and draw zones, fault loops, normal current and transient energy paths, barrier crossings, and disconnection element. No optimization before proof.
2. **Decide whether isolation transformer/isolator protection makes 3,500 yen unattainable** using actual one-unit prices; maintain safety, if needed amend architecture or openly amend price target.
3. **Select one scalar current-loop controller plus hard-independent trip**, not multiple firmware optimization modes or competitor ranking; validate DC-loop, analog gain/phase, and single-frequency tone first.
4. Build KiCad candidate with manufacturer libraries and fully specified footprints; check native geometry, pin parity, installation/electrical rules.
5. Under qualified lab conditions only, compare filtered/unfiltered **differential L-N** conducted-noise with identical source, artificial mains network, load and measurement bandwidth. No claims of common-mode efficacy without separate test arrangements.

## Sources
- Macnica Fly-Buck article: https://emb.macnica.co.jp/articles/5793/
- TI LM5161: https://www.ti.com/product/LM5161
- MEAN WELL IRM-03-12: https://www.meanwell.com/Upload/PDF/IRM-03/IRM-03-SPEC.PDF
- DigiKey 1 unit PSU price: https://www.digikey.jp/en/products/detail/mean-well-usa-inc/IRM-03-12/7704636
- Previous RC18 gate successful geometry: https://github.com/eieeeeeee/compact-ac-parallel-filter/actions/runs/38014998876
- KEMET X/Y capacitor intended use: https://www.kemet.com/en/us/capacitors/ceramic/ceramic-disc-safety-capacitors.html
- Japan voltage regulation: https://laws.e-gov.go.jp/law/407M50000400077/
- Metering of low-frequency conducted disturbances needs appropriate custom validated measurement conditions; regulatory conducted EMC bands should be addressed separately.
