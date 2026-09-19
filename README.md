# Compact AC Parallel Filter

Compact plug-in experimental AC mains parallel network for **100 V AC, 50/60 Hz** environments.

> [!WARNING]
> ## PRE-PROTOTYPE / EXPERIMENTAL / NOT YET TESTED ON MAINS
>
> This project is currently at the **design stage only**.
>
> **No physical prototype has yet been manufactured or tested.**
>
> The schematic, PCB layout, component selection, insulation distances, enclosure, thermal behavior, surge behavior, failure modes, and noise-reduction performance have **not yet been validated on actual mains power**.
>
> This repository must **not** be interpreted as a finished, certified, production-ready, or safety-approved design.
>
> The design connects directly to hazardous mains voltage. Construction, testing, modification, or use should only be undertaken by persons with appropriate electrical-safety knowledge, equipment, and applicable regulatory review.

## Status

| Item | Current state |
|---|---|
| Version | `v0.1.0-preprototype` |
| Development stage | Design / pre-prototype |
| Target mains | 100 V AC, 50/60 Hz |
| Physical prototype | **NOT BUILT** |
| Mains test | **NOT PERFORMED** |
| EMI/noise performance | **NOT VERIFIED** |
| Thermal test | **NOT PERFORMED** |
| Surge/fault test | **NOT PERFORMED** |
| Safety certification | **NONE** |

## Design target

The initial concept is a compact direct plug-in parallel network using:

- **C1:** 1 µF X2 safety capacitor — KEMET R53 series
- **R1/R2:** 220 kΩ + 220 kΩ discharge network
- **F1:** Littelfuse 37402500000, 250 mA time-lag fuse
- **MOV1:** Littelfuse TMOV14RP140E thermally protected MOV
- **LED:** low-current status indicator with reverse-voltage protection
- **CMC:** not included in the initial parallel-only architecture
- **Optional C2 / RC damping:** reserved for later measurement-based evaluation

### Preliminary mechanical target

- PCB: **approximately 32 × 28 mm**
- Enclosure: **approximately 38 × 34 × 27 mm**

These dimensions are **targets only** and may increase if required to maintain suitable creepage, clearance, thermal spacing, mechanical strength, plug retention, or manufacturability.

## Project goals

1. Design the smallest practical direct plug-in PCB without sacrificing electrical-safety margins.
2. Publish the complete design process, not only favorable results.
3. Measure the effect of the network under controlled conditions.
4. Record temperature, discharge behavior, mains current, noise spectra, and failure-related observations.
5. Revise the PCB based on measured data before calling the design validated.

## Repository structure

```text
.
├─ README.md
├─ SAFETY.md
├─ CHANGELOG.md
├─ LICENSE
├─ bom/
│  └─ BOM.md
├─ docs/
│  ├─ DESIGN_NOTES.md
│  └─ TEST_PLAN.md
├─ hardware/
│  └─ kicad/
│     └─ README.md
├─ measurements/
│  └─ README.md
└─ images/
   └─ README.md
```

## Development stages

### v0.1 — Pre-prototype

- schematic development
- BOM definition
- PCB layout
- enclosure study
- creepage/clearance review
- design review before manufacturing

### v0.2 — Prototype

- first PCB manufactured
- visual inspection
- continuity/isolation checks
- controlled first power-up
- mechanical fit evaluation

### v0.3 — Measurement

- mains current
- discharge time
- thermal measurements
- oscilloscope measurements
- conducted-noise comparison
- before/after data under repeatable loads

### v0.4 — Revised prototype

PCB and BOM revised from measured results.

### v1.0 — Validated open-hardware release

Only after the defined validation work has been completed and the published documentation reflects the tested hardware revision.

## Measurement policy

Negative or null results are still results.

The project intends to publish comparable measurements for:

- baseline without the network
- 1 µF network enabled
- representative resistive/electronic loads
- 50 Hz and 60 Hz where practical
- temperature and long-duration behavior
- noise spectra using identical measurement settings

No performance claim should be made from the circuit diagram alone.

## Regulatory note

Open-source publication does **not** imply compliance with Japanese PSE requirements, IEC standards, or any other product-safety or EMC requirement. Regulatory compliance, certification, and marketability are separate questions from publication of design files.

See [SAFETY.md](SAFETY.md) before working with this design.

---

## 日本語概要

このリポジトリは、AC100 Vコンセントに直接挿す小型並列回路の**設計・測定過程を公開する実験的オープンハードウェアプロジェクト**です。

**現時点では実機未製作・商用電源未試験です。完成品、安全確認済み製品、認証済み製品ではありません。**

初号機を製作・測定するまでは `v0.1.0-preprototype` として扱い、実測結果は成功・不成功を問わず公開する方針です。


## KiCad Rev.A hardware

An editable **KiCad 9 Rev.A pre-prototype** has now been added under [hardware/kicad](hardware/kicad/README.md).

Current layout study:

- exact PCB outline: **32 × 28 mm**
- C1 / MOV1 / F1: front-side THT
- R1 / R2 / R4 / R5 / LED1 / D1: back-side SMD for compactness
- J1: **provisional electrical interface only — not the final plug-blade footprint**
- C2 and optional RC damping: not implemented on this compact Rev.A PCB

The files are still **NOT YET TESTED ON MAINS** and are not a fabrication-approved or certified design.
