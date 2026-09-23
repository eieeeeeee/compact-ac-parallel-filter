# RC18-COST-MAX

Goal: reduce assembled cost as far as practical without accepting a measurable loss in the electrical performance targets of RC17.

## Rules

1. RC17 stays frozen as the reference.
2. Every electrical change must pass a before/after simulation or an explicit topology-equivalence check.
3. Every PCB revision must pass official KiCad 9 DRC with 0 violations and 0 unconnected pads.
4. Four copper layers remain the default unless measurements show a two-layer board is electrically equivalent.
5. Current-sense and protection parts are not replaced by cheaper parts only on headline specifications; PWM common-mode behavior and protection latency must be checked.
6. LOW VOLTAGE ONLY remains in force.

## Stage 1 — zero-topology-change sourcing reduction

- U1 STM32G474RCT6 -> STM32G474RCT3.
- Same STM32G474RC device class, LQFP64 pinout, 256 KiB Flash, 170 MHz CPU and HRTIM/analog resources.
- RCT3 is rated to +125 C rather than +85 C.
- No power-stage, sensing, protection, filter or injection-path values change.
- CI runs numerical reconstruction/injection plant equivalence and generated-PCB topology equivalence before autorouting/DRC.

## Later stages

- S2: JLC/LCSC Basic/Promotional passive consolidation with equal-or-better voltage rating, tolerance, dielectric and pulse/current rating.
- S3: evaluate internal STM32G474 COMP -> HRTIM fault path versus U4/U5. Remove external parts only if latency/noise-immunity criteria are met.
- S4: power-stage cost challenge. LMG2100 remains reference; lower-cost integrated/Si alternatives must pass switching-loss, ringing, thermal and EMI simulation/bench criteria before adoption.
- S5: shrink board only after S2/S3 placement reduction; keep four layers and controlled return paths.
- S6: final JLC BOM/CPL cost optimization and fabrication package.

The 2,000-yen-class target is a cost objective, not a license to relax performance or protection criteria.
