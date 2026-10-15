# RC18 E27S — STM32G474CBT6 48-pin feasibility and analog supply names (NONFAB HOLD)

2026-10-15. Based on **E27P** original ZIP (SHA256 `f83469afb17b854eaa9bebff13a463b0bdfc192fbf4137fe56f7e347301a707a`).
Candidate ZIP SHA256: `ab240ce51e5d56b19caab85618319387f2a1d75d81dc31418c5fc1573ac367f3`.

This independent candidate corrects **U1 LQFP48 pin 19 VSS→VSSA** and **pin 21 VDD→VDDA** in both the schematic's cached symbol and the local KiCad symbol library. These are **pin name changes only**: power nets remain GND and 3V3, while PCB copper, footprint, component count and project physical connectivity remain unchanged.

48-pin actual-net/alternate-function register and the provisional firmware pin contract are bundled. Manufacturer basis: ST STM32G474CB datasheet DS12288 rev6. **PA8/PA9 HRTIM1_CHA1/2, PB13 ADC3_IN5, PA5/6/7 OPAMP2, PA1/PA3 COMP inputs** are identified; simultaneous pinmux timing and peripheral behavior remain unverified.

This branch includes KiCad **10.0.6** native ERC/DRC checks but does **not** assert noise attenuation, part count reduction or fabrication readiness. Independent OCP, physical PRE_VERIFIED, E-STOP, fail-off and arm interlock remain mandatory. Baseline: 159 FIT / 40 DNP / 64 unplaced FIT / 3 unrouted pads. **No power, AC, ordering or fabrication**. E27P and main unchanged.
