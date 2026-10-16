# YK66 R8 — cost-first single-board current envelope (2026-10-16)

**Status: ANALYTICAL MODEL PASS (8 unit tests locally); MAINS HOLD; FAB HOLD; NO KICAD PCB RELEASE.**

## Inherited design commitments
AC100V 50/60Hz, L-N two-terminal parallel differential active noise reduction, exactly one final-design PCB with independent hardware safety; no separate low-voltage product PCB. Target first-piece PCB + all parts + assembly + tax + shipping <= JPY 3,500 excluding stencil only. Safety, then cost/ease of manufacture, then attenuation. MCU and GaN not mandatory.

## R8 engineering finding: specify disturbance excitation before promising current
Nine cases: Rs={0.1, 1, 5}ohm x Rl={5, 10, 20}ohm. Purely resistive, ideal Norton small-signal equivalent.

- Zp=Rs||Rl; ideal positive shunt for 3dB Y=(10^(3/20)-1)/Zp = 0.103134 to 4.207883 siemens. No physical Y(s) driver has been proven.
- Perfect antiphase current needed for 3dB = (1 - 10^(-3/20))*Ioff = 0.292054216*Ioff.
- If the injected Norton disturbance source is **10mA peak fixed**, ideal 3dB needs 2.920542mA peak in every case; Voff depends on Zp (0.9804 to 40mV peak).
- If **OFF-state terminal noise voltage is 100mV peak fixed**, implied Ioff=0.1/Zp; ideal current required is **7.301355 to 297.895300mA peak**. Worst is Rs=0.1ohm/Rl=5ohm. This is not 100Vrms mains voltage.
- Hypothetical **20mA peak** current limit, no real driver selected, mathematically suffices for 3dB in 9/9 of fixed-Norton cases but only 3/9 of fixed-voltage cases. For the worst fixed-voltage case the **ideal** attenuation at 20mA is 0.172dB, not 3dB. The 20mA is NOT an OPA197 rating and is NOT a safe or verified injection level.

All figures assume zero phase error, perfectly controlled antiphase injection, no complex impedance, parasitics, delay, current-source compliance, clipping, 50/60Hz injection or thermal/surge stresses. They are a specification **sensitivity test**, not simulated or measured YK66 attenuation. Old RC18 47–54dB figures cannot be claimed for YK66.

## Single-board architecture and parts gate
1. L-N only mains input: coordinated overcurrent, surge, fire and fail-open protections (part numbers unselected).
2. Preliminary auxiliary isolated AC/DC MEAN WELL IRM-03-12 (12V/250mA/3W, 37x24x15mm): JPY 915 excluding tax at one-piece reference price; tax-included JPY 1006.50, shipping separate.
3. Isolated sensing from the **same two L-N terminals**; a third upstream sensor is disallowed (isolation and phase part unselected).
4. Analog compensation candidate TI OPA197, 10MHz GBW and **65mA typical Iout**, NOT a guaranteed driver current; actual protected driver unselected.
5. Qualified AC-side HF injection coupling and an independent fail-open hardware trip: both **unselected**, thus no mains-side pin or connection may be assumed.

After JPY 1006.50 reference power supply alone, theoretical remaining all-in budget is **JPY 2493.50** for protections, detection, driver, coupler, PCB, assembly and shipping. The available component/budget evidence cannot prove all-in <=3500 JPY.

KEMET R46 X2 capacitors are described as across-the-line EMI capacitors and are explicitly **not suitable for series-with-mains** use; X2 does not authorize a high-frequency active-injection isolation network.

## Nonfabrication engineering gates (ALL HOLD)
- H0: Prove suitable safety-rated mains sensing and high-frequency injection coupler, physical MPN, phase response, 50/60Hz blocking, surge and single faults.
- H1: Prove controller-independent hardware fail-open on shorts, opens, brownout, overheat, MOV failure and stuck contacts.
- H2: Measure actual disturbance magnitude and complex source/load impedances; verify driver SOA, current, loop phase margin, out-of-band amplification and 50/60Hz current under parasitics.
- H3: Once H0/H1/H2 resolved, place all blocks into **one** native KiCad project with ERC, DRC, unconnected, net parity, pad copper-island and BOM/FIT/DNP checks.
- H4: Obtain actual 1-unit component / assembly / fab / tax / shipping quote with all protection included.
- H5: Professional Japanese AC100V regulatory and electric safety review before mains power or PCB fabrication.

## Companion local R8 deliverables
Single ZIP prepared during this session containing a 9-case CSV for both excitation regimes, standalone Python calculations, 8 passing unit tests, candidate-only functional BOM, annotated NONFAB SVG partition diagram and a more detailed design decision memorandum. This GitHub report preserves the conclusions; **the local ZIP is not represented as committed to GitHub**.

## Sources
- Prior repo: docs/YK66_R7_SINGLE_BOARD_9CASE_AND_BOM_DECISION_20261016.md
- IRM-03-12 datasheet: https://www.meanwell.com/Upload/PDF/IRM-03/IRM-03-SPEC.PDF
- IRM-03-12 listing: https://www.digikey.jp/ja/products/detail/mean-well-usa-inc/IRM-03-12/7704636
- OPA197: https://www.ti.com/product/OPA197
- KEMET R46 X2: https://content.kemet.com/datasheets/KEM_F3095_R46_X2_310_110C.pdf

**Not an electrical wiring plan. Do not connect it to AC100V or send it to fabrication.**
