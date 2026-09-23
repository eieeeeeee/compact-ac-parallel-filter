# RC18-COST-MAX Stage 2 — Power-stage qualification

Reference: LMG2100R044.

Primary candidate: **TI CSD87330Q3D + Diodes DGD0507A**.

Why this candidate:
- preserves separate HIN/LIN control, so the existing STM32G474 HRTIM complementary-control architecture is retained;
- 30 V / 20 A power block gives large margin on a 12 V RC18 rail;
- 1.5 MHz rated switching capability;
- DGD0507A has separate HIN/LIN/EN, 3.3 V logic, integrated bootstrap diode and about 20/23 ns typical on/off propagation;
- power silicon is 3.3 x 3.3 mm and driver is 3 x 3 mm;
- current 10-piece reference cost is roughly USD 1.57 for the pair versus roughly USD 7.5-class for LMG2100.

Qualification is system-level, not a claim that silicon switching loss is lower than GaN. The candidate may dissipate more than LMG2100 but must remain below the RC18 thermal/loss budget while preserving PWM bandwidth, current margin and output-voltage accuracy.

The simulation gate covers 0.5–4.5 A and 250 kHz–1.5 MHz. It rejects the candidate if:
- rated current < 10 A;
- switching capability < 1 MHz;
- propagation delay > 35 ns;
- modeled worst-case stage loss > 1 W;
- 4.5 A conduction droop > 0.35% of the 12 V bus.

Only after this gate passes should the RC18 PCB be changed.
