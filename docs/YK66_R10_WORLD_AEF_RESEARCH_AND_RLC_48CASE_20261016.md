# YK66 R10: world active-EMI research and quantified selection (2026-10-16)

STATUS: RESEARCH AND ANALYTICAL ONLY. NOT AC100V SAFE. NO NEW YK66 KICAD/PCB, NO FABRICATION PERMISSION. Worldwide literature reviewed selectively, not exhaustively.

## Commitments
One final AC100V/50–60Hz L–N two-terminal parallel differential-mode (DM) board, no separate low-voltage product board; independent physical failsafe, first-unit <=3500JPY PCB+BOM+SMT+tax+shipping excluding stencil, safety and buildability before maximum dB. Existing RC18 47–54dB refers to a different model.

## Worldwide idea review (do not copy a different application outright)
1. **Japan 1999:** Akagi, Fujita and Wada's shunt voltage-detection-based *harmonic termination*: sense noise voltage at installation point, present high impedance at 50/60Hz and emulate low resistance for harmonics. 200V/20kW feeder laboratory demonstration, NOT a 5–30kHz/100Vac/cheap plug-in demonstration. **ADOPT control principle.** https://ousar.lib.okayama-u.ac.jp/34002 ; doi:10.1109/28.767015. Their 2002 whack-a-mole study shows other network nodes can suffer worsening: https://cir.nii.ac.jp/crid/1360855569151012736.
2. **USA 2020:** Narayanasamy et al. IEEE differential-mode active EMI filter with a low-voltage SMD *analog twin* compensation network. **ADOPT compensation design METHOD**, not its unverified mains coupler. https://par.nsf.gov/servlets/purl/10241029 ; doi:10.1109/TEMC.2020.3006427.
3. **France 2025:** Gahfif et al. hybrid voltage/current multiple injection for specific GaN 1kW converter with almost 50dB in selected reported conditions. The circuit needs per-line multiport sensing/injection and power hardware, **not available to our two-terminal plug-in**. **ADOPT impedance black-box identification and parasitic design methods only.** https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/pel2.70090.
4. **Korea 2024:** KR20240156342A patent for compact independent active EMI module, described VSCC and optional transformers, potentially no distinct input/output in some embodiments. Much of context is CM; **research isolation/packaging only, check patents/jurisdictions**. https://patents.google.com/patent/KR20240156342A/en
5. **UK/USA 2023:** Collins/Goodrich US20230421134A1 adjustable shunt with separated op-amp shaping/decoupling stage that avoids the capacitive injection branch disrupting stability. **ADOPT phase/stability separation concept, NOT the ground-referenced patented hardware**. US publication indicated abandoned; not a worldwide freedom-to-operate conclusion. https://patents.google.com/patent/US20230421134A1/en
6. **China 2024:** Cai et al. multi-current injection with combined feedback/feedforward on a DC–AC converter; larger/multiport, not the initial 2-terminal low-cost hardware. https://www.jstage.jst.go.jp/article/elex/21/2/21_20.20230542/_article/-char/en
7. **USA 2025:** APEC synchronized-switching AEF 23dB @150kHz on a 6–12V→24V boost design. Requires a known clock and a different port. Research-only. doi:10.1109/APEC48143.2025.10977158.
8. **REJECT components directly:** TI TPSF12C1 CM AEF (not DM), TI LM5149 DM buck AEF limited to 80V DC, negative-impedance single-point patent technique with significant stability concerns (https://patents.google.com/patent/US11646720B2/en), 2026 self-learning RL/MCU complexity. Publication existence does not establish IP freedom/safety/price.
9. **Standard:** IEC 61000-4-19 addresses 2–150kHz AC port DM **immunity** testing, not a filter's attenuation or AC100V product approval. https://webstore.iec.ch/en/publication/4188.
10. **Impedance measurement:** in-circuit DM impedance extraction study https://arxiv.org/abs/2110.00208 supports future professional measurements without adding an inaccessible third sense point to our final board.

## NEW R10 RLC test: 48 theoretical series-shunt prototypes (local ZIP contains reproducible Python)
Nine Norton resistive ports Rs={0.1,1,5}ohm, Rl={5,10,20}ohm. Y(s) = 1/[R+sL+1/(sC)] at s=jω. Sweep C={10,22,47}nF, R={0.2,1,10,100}ohm, resonance={5,10,20,30}kHz -> 48 cases. 8/8 source sanity tests PASS.
**Illustrative ideal NOT physically validated:** C=22nF, R=0.2ohm, L=11.51377mH resonates at 10kHz and yields theoretical >=3.46487dB for all nine *purely resistive* ports exactly at 10kHz. However across 5–30kHz the worst sampled reduction is almost zero (5.70e-8dB). Half-power approximate bandwidth is only 2.765Hz, Q≈3617. At 100Vrms 60Hz this hypothetical L–N resonant branch draws 0.8294mA RMS fundamental current (not earth leakage). Under 100mV OFF-state noise voltage in each condition, up to **335.53mA peak** flows in the ideal shunt at 10kHz. With artificial ±j2ohm source/load stresses, worst port noise worsened ~+0.04085dB: Re Y positive doesn't guarantee all measured voltages fall at complex loads.
This is a clear REJECTION of claiming a narrow, ideal RLC notch meets the 5–30kHz 3dB requirement. No winding/core/capacitance/parasitics/fault/stress or 100Vac safety model; nothing released for build.

## R10 engineering architecture choice
Select a **research primary**: L–N two-terminal terminal voltage -> isolated high-frequency differential sensing -> low-lag analog frequency-selective *virtual positive conductance* (with a low-voltage analog twin compensation network candidate) -> output-current-limited driver -> rated and independently fail-open isolated mains injection path. Proper fused/surged commercial AC/DC rail and standalone physical overcurrent/thermal and surge protection are mandatory. Real sense, injection coupler, failsafe component MPNs UNSELECTED. Need complex Zsource/Zload/Hinj measurements, 1–5kHz and 30–700kHz guard, current SOA, loop phase, 50/60Hz dissipation, worst fault, BOM assembly quote and expert review before KiCad release.
**This is a research architecture, NOT a proven manufacturable circuit.** Final YK66 hardware is not complete.

## Traceability
R5 historical audit: docs/YK66_R5_HERITAGE_DEEP_AUDIT_20261016.md
R7 analytical model: docs/YK66_R7_SINGLE_BOARD_9CASE_AND_BOM_DECISION_20261016.md
R8 current envelope: docs/YK66_R8_CURRENT_ENVELOPE_AND_NONFAB_GATE_20261016.md
R9 international forum review: docs/YK66_R9_GLOBAL_FORUM_EVIDENCE_AND_SELECTION_20261016.md
A complete Japanese 13-source adoption matrix and 48-case model are supplied as a downloadable R10 ZIP; this GitHub commit records the substantive findings, NOT the ZIP bytes.
