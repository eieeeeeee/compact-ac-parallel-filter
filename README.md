# Compact AC Parallel Filter

Open-hardware research platform for compact plug-in AC-noise filtering and adaptive parallel-shunt control.

> [!WARNING]
> **PRE-PROTOTYPE / EXPERIMENTAL / NOT MAINS-VALIDATED**
>
> No RC18 physical prototype has yet been manufactured or validated on hazardous mains power. The RC18 active-control work in this repository is currently a **low-voltage architecture and simulation study**. A safe mains coupling/isolation implementation is **not defined by the RC18 simulation model**. Do not interpret simulation, KiCad DRC/ERC, or CI results as safety approval, PSE compliance, EMC certification, or production readiness.

## What makes this repository different

The project publishes not only schematics and PCB files, but also the assumptions, comparison baseline, dense frequency sweeps, corner cases, controller coefficients, numerical implementation checks, and machine-executable pass/fail gates used to make design decisions.

A design change should be able to answer a simple question automatically:

> Does this change still meet the frozen electrical gates, or not?

## Current research branches

| Track | Purpose | State |
|---|---|---|
| Passive plug-in network | Compact X2/MOV/fuse parallel network | Pre-prototype |
| Rev.D / RC17 | Frozen comparison baseline for adaptive active-shunt studies | Simulation reference |
| **RC18-B2.1** | Lower-cost EPC23104 + 3 MHz + asymmetric 3-stage reconstruction + digital biquad | **Simulation gate PASS candidate** |

## RC18-B2.1 frozen candidate

The active-control candidate currently under validation is intentionally kept separate from the mains-safety question.

### Power/control architecture

- EPC23104 integrated GaN power stage
- 3.0 MHz PWM
- 2.0 MHz digital control update
- 0.82 µH / 150 nF first reconstruction section
- 0.47 µH / 100 nF second section
- 0.68 µH / 82 nF third section
- final float32/Q31 biquad validation at total modeled latency 2.041 µs
- bounded timing jitter: ±25 ns

### Frozen digital biquad

```text
H(z) = (b0 + b1 z^-1 + b2 z^-2) / (1 + a1 z^-1 + a2 z^-2)

b0 =  1.96005549
b1 = -2.81840199
b2 =  0.92560172
a1 = -1.02969083
a2 =  0.09694605
Fs = 2.000 MHz
```

### Electrical simulation gates

The CI gate evaluates:

- 241 logarithmic points from 5–30 kHz
- 241 logarithmic points from 30–100 kHz for watchdog testing
- source |Z| = 0.2 / 0.5 / 1 / 2 / 5 / 10 / 20 Ω
- source phase = −60° to +60° in 15° steps
- B2.1 nominal, low-L/C and high-L/C corners
- float32 sequential arithmetic
- Q31 CMSIS-style DF1 arithmetic model
- ±25 ns bounded timing jitter
- active current ceiling = 120 mArms
- command ceiling = 3.39411255 Vrms
- watchdog worsening ≤ +0.5 dB
- strict same-model RC17 equivalence requirement

The current self-contained validation script passes both float32 and Q31 gates. The exact result is regenerated in CI rather than accepted from a hand-edited table.

## Reproduce the RC18 gate locally

```bash
python -m pip install -r simulations/rc18-b2.1/requirements.txt
python simulations/rc18-b2.1/validate_rc18.py
```

Generated results are written under `validation/rc18-b2.1/generated/` by default.

See:

- [`docs/RC18-B2.1-VALIDATION-SPEC.md`](docs/RC18-B2.1-VALIDATION-SPEC.md)
- [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md)
- [`simulations/rc18-b2.1/README.md`](simulations/rc18-b2.1/README.md)
- [`firmware/rc18-b2.1/biquad_coeffs.h`](firmware/rc18-b2.1/biquad_coeffs.h)
- [`validation/rc18-b2.1/README.md`](validation/rc18-b2.1/README.md)

## Repository structure

```text
.
├─ .github/workflows/          # KiCad and electrical validation CI
├─ hardware/                   # KiCad design work
├─ firmware/                   # Controller implementation material
├─ simulations/                # Reproducible models and gate scripts
├─ validation/                 # Frozen reference and generated results
├─ measurements/               # Physical measurements when prototypes exist
├─ bom/                        # BOM and sourcing work
├─ docs/                       # Design decisions, test plans, validation specs
├─ SAFETY.md
├─ CONTRIBUTING.md
├─ CITATION.cff
└─ LICENSE
```

## Evidence policy

Simulation results are predictions from disclosed models, not measurements. Null results, failed revisions, regressions, and negative measurements are part of the engineering record and should not be hidden.

Claims about real-world noise reduction will require controlled measurements using the same noise source, wiring, instrument settings, and comparison procedure. A future validated release should include raw data sufficient for independent re-analysis.

## Development path

`pre-prototype → low-voltage bench validation → isolated/safe interface design → controlled prototype test → independent reproduction → validated release`

A `v1.0` tag is reserved for a release whose documentation matches physically tested hardware.

## Safety and regulatory note

Open-source publication does not imply Japanese PSE compliance, IEC/UL compliance, EMC certification, safety approval, or fitness for connection to the public mains network. KiCad ERC/DRC only checks defined CAD rules; it cannot prove electrical safety or regulatory conformity.

Read [`SAFETY.md`](SAFETY.md) before working with any mains-related hardware in this repository.

## License

Hardware source material is published under **CERN-OHL-W-2.0** as described in [`LICENSE`](LICENSE).

---

## 日本語概要

このリポジトリは、コンセント直挿し型の並列ノイズ対策回路と、適応型アクティブ・シャント制御を研究するオープンハードウェア・プロジェクトです。

RC18では「回路図を公開する」だけではなく、比較基準、241点の周波数掃引、部品ばらつき、0.2～20 Ωのライン条件、±60°位相、watchdog、float32/Q31量子化、演算誤差、タイミングジッタまで公開し、GitHub Actionsで自動的にPASS/FAILを判定できる形を目指しています。

RC18-B2.1は現時点で**低電圧アーキテクチャのシミュレーション候補**です。商用電源へ安全に接続するための結合・絶縁方式は、このシミュレーションだけでは定義されていません。実機・商用電源試験・安全規格確認が終わるまで、完成品や安全確認済み製品として扱いません。
