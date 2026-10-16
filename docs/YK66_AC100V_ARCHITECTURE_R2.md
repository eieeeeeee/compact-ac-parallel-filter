# YK66 AC100V R2 — isolated DM injection concept and go/no-go gates

Date: 2026-10-16 JST
Status: **B CONCEPT SELECTED FOR ANALYSIS; NONFAB_HOLD / MAINS_HOLD**
Parent: [R1 engineering screen](YK66_AC100V_ENGINEERING_SCREEN_R1.md)

## Decision: select architecture B as the single analysis candidate
End product remains **AC100 Vrms, 50/60 Hz, L–N PARALLEL ACTIVE differential-mode (DM)** noise reduction, not a passive-only filter and not a low-voltage product. To avoid a line-referenced low-voltage user interface, the leading candidate is a **fully isolated control domain plus separately qualified wideband isolated sensing and isolated injection barrier**. This selection is an architecture decision, **not proof that a manufacturable safe circuit exists**. Alternative A (live/hot control) is not being advanced for first prototype. Architecture B likely worsens the ¥3,500 first-unit cost.

Functional concept only (not an electrical wiring diagram):

```text
      L / N mains input [HAZARDOUS VOLTAGE DOMAIN]
                 |
      input/fuse/surge protection  <--- independent safety design TBD
                 |
        +--------+-------------------------------> to line/load environment
        |        |
        |    qualified DM sense barrier --> isolated analog sense/ADC
        |
        +-- independently disconnectable, rated L-N injection path
             [qualified series coupling, fault limit, transformer secondary]
                                   || reinforced/appropriate isolation barrier
                       isolated HF injection transformer primary <-- current
                       driver <-- independent HW shutdown <-- 3.3V controller
                                                             ^
                                 certified AC/DC 12V and 3.3V regulator
                   [LOW-VOLTAGE CONTROL DOMAIN, no intentional mains return]
```

**This schematic is a study topology only. No component values, winding construction, wiring, fuse or relay ratings are approved.** The injection secondary/coupling and line-side sense parts must survive continuous line voltage, surges and fault energy; the transformer's specified insulation and 50/60Hz volt-second behavior remain unresolved. An X-class safety capacitor's recognition does not independently approve the entire coupling path. A fuse alone does not guarantee all electronic faults disconnect safely.

## Non-negotiable single-fault review
| Case | Hazard to eliminate | Gate-evidence needed |
|---|---|---|
| Injection coupling capacitor short/open | L–N fault current, hot transformer, lingering energized nodes | Fault-rated series path / interruption coordination, discharge proof, independent test |
| Isolation barrier failure | AC mains reaching isolated control, test connectors or accessible enclosure | Manufacturer isolation/surge/creepage data plus applied insulation/fault test |
| Disconnect welds closed | Fault continues despite software stop | Independent hardware interruption and fault-energy analysis; welded-contact analysis |
| Current-sense open/saturated/aliased | Injection runaway or out-of-phase reinforcement | Bounded analog driver, independent HW fault latch, degraded-to-off behavior |
| MCU stalled / firmware fault / startup | Unlimited PWM or sporadic injection | Default-disabled hardware and power-on-reset interlock verified |
| Supply failure / brownout | Uncontrolled switching, relay chatter | Undervoltage lockout and de-energize-to-open proof |
| Surge and 50/60Hz fundamental pickup | Isolation stress, transformer core saturation/thermal fault | Mains rated barrier and line-frequency injection-path analysis |
| Inadvertent ground connection | Mains injected into scope/PC/programmer ground | Safe test setup and no directly exposed programming/debug connectors |

**Do not energize using AC100V from this document.** Independent qualified electrical safety engineering review, enclosure and protective insulation definition, actual applicable Japanese regulatory/PSE classification, and relevant product/EMC standard determination remain F0/F7 gates.

## Quantitative R2: cancellation timing, NOT a device performance claim
In an ideal one-tone current feedforward model, with noise current `I_n`, actual opposing injection is `I_inj = alpha * I_n * exp(-j*2*pi*f*tau)`. The residual fraction is

`r = |1 - alpha * exp(-j*2*pi*f*tau)|`, and reduction is `-20log10(r)` dB.

This omits unknown line impedance, amplifier saturation, transformer transfer function, closed-loop instability, delayed sensing, sample/hold and conducted noise measurement arrangements. A 1% gain error alone caps perfect-phase cancellation at **40dB**. If gain is ideal, a pure uncompensated delay of **0.5 microseconds** gives approximately **20.5dB** reduction at 30kHz; **1 microsecond** gives about **14.5dB**. For 50dB at 30kHz the pure-delay tolerance is only about **0.0168 microseconds (16.8ns)**. Real phase compensation may alter per-tone figures, but cannot be assumed across the band and changing load.

A 10mA noise peak requires 10mA ideal cancellation-current peak in this simple equal-and-opposite model; a 30mA peak requires 30mA, and 80mA requires 80mA. **No actual noise-current spectrum has been measured**. A provisional 50mA *analysis-only* current budget flags the 80mA case; it is not a validated continuous current rating. Previous 178mA is a **historical protection trip threshold**, not an authorized operating point. The earlier 1uF, 4.7ohm and 0.33ohm low-voltage component values are **not** accepted as mains components.

Run (Python standard library, no extra dependencies):
```bash
python3 tools/yk66_cancel_screen_r2.py --json /tmp/yk66_r2.json --csv /tmp/yk66_r2.csv
python3 -m unittest discover -s tests -p 'test_yk66_cancel_screen_r2.py' -v
```

## Single-target early bench demonstration (not final product)
- Build **only an isolated extra-low-voltage dummy-source test fixture first**, with known source/load impedance and injected disturbance current. This bench article is not the AC100V end product.
- First gate at **10kHz**: record baseline and controlled-injection noise current/voltage, phase, clipping, supply power and hardware-trip response. Acceptance is **repeatable measured reduction at the chosen point without signal reinforcement outside it**, not a nominal 45–50dB marketing claim.
- Validate across 5/10/20/30kHz, perturb impedance, test loss of sensing/firmware drive and brownout. Separately verify 30–700kHz watchdog band. No passage to mains without F0–F7 safety signoff.
- Carry forward only after confirmed injection/sensor transformer models, isolation ratings, fault interrupt mechanism, current-loop stability margin, thermal analysis, wiring/clearance, enclosure and price quotations.
- KiCad mains schematic/PCB and order-ready Gerbers are **held**. RC18's previous ERC/DRC result does not carry over to YK66.

## Cost position (ex-tax planning, not a fresh purchase quote)
IRM-03-12 12V/3W **¥915 reference**, STM32G474 historical **¥1,300 estimate**, subtotal **¥2,215**, headroom **¥1,285** against PCB + components + assembly target **¥3,500** (stencil excluded). Safety-qualified sense/injection barriers, shutdown/disconnection, surge protection, regulators, PCB and assembly still unpriced. **¥3,500 feasibility remains unproven and high risk.** No safety item may be omitted to force the cost target.

## Manufacturer references / relevance limits
- TI active EMI filter [VSCC principles](https://www.ti.com/document-viewer/lit/html/SSZT179/GUID-5C0D06C5-28CC-49A6-A027-B85B887C8230): illustrative *automotive converter* example, not a validated AC100V DM implementation.
- TI [TPSF12C1EVM-FILTER](https://www.ti.com/tool/TPSF12C1EVM-FILTER): **common-mode** single-phase AEF; not a substitute for YK66's **differential-mode** design.
- KEMET [IEC 60384-14 X/Y capacitor applications](https://www.kemet.com/en/us/capacitors/ceramic/ceramic-disc-safety-capacitors.html): X class for L–N, Y for line–ground, subject to chosen component's approvals.
- MEAN WELL [IRM-03 series specification](https://www.meanwell.com/Upload/PDF/IRM-03/IRM-03-SPEC.PDF): 12V/250mA (3W) output for IRM-03-12; module qualification does not certify finished appliance.

## R2 design gate
**F0: BLOCKED** (actual rated isolation/sense/injection part selections pending)
**F1: BLOCKED** (no validated differential-mode 100Vac physics model)
**F2: BLOCKED** (fault hardware and limits pending)
**F3: BLOCKED** (measured power budget absent)
**F4: BLOCKED** (full dynamic closed-loop stability absent)
**F5: BLOCKED** (priced one-off BOM absent)
**F6: BLOCKED** (YK66 native KiCad checks absent)
**F7: BLOCKED** (regulatory/product safety review absent)
**F8: BLOCKED** (no prototype / no 100Vac measured test)

This R2 is concrete progress on architecture and reproducible phase/current screening. It is **NOT FAB RELEASE**.
