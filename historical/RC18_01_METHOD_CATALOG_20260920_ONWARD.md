# RC18 操作・解析・検証手法の保存台帳（2026-09-20以降）

**重要：この資料は再利用可能な設計・検証手法の保管庫であり、製造承認ではない。** 最新基準は E24 Source-only ECO 作業ブランチ。製造HOLD、最新Native ERC/DRC/Unconnected/parityは未PASS。旧PASSは旧版にのみ有効。

| 領域 | 再利用する手法 | 主要な元データ／実行物 | 証拠と適用条件 |
|---|---|---|---|
| Native KiCad | Ubuntu 24.04/GitHub Actionsで公式 KiCad 10.0.6、ERC+DRC+parity+ゾーン再充填 | CURRENT_E24_NATIVE_KICAD_HANDOFF_HOLD/NATIVE_KICAD_10_0_6/、RC18_P21_R1_2_ONECLICK_NATIVE_GATE.zip | 旧R1.2とR2.3.1CのPASSログ。E24のPASSを意味しない。KiCadの実バイナリ自体は未同梱 |
| Freerouting | `.dsn`設計入力→Freerouting→`.ses`固定→Native KiCad DRC。Golden SESをSHA256で保存 | `QUICK_REPLAY_SOURCES/FREEROUTING_INPUT_P2.dsn`, `FREEROUTING_GOLDEN_P2.ses`, `OCT01_NATIVE_DRC_FULL.rpt` | 2026-10-01 P2 DRC0/Unconnected0、P2当時の回路専用 |
| 階層回路図/ライブラリ | KiCad10で9シート＋rootの階層回路図、ライブラリの同梱、ネットピン整合 | P2_KiCad10_ERC0、E24の `.kicad_sch`, `.kicad_pro`, `.kicad_pcb`, custom library | 別版の設計結果を混ぜない |
| S1 128-corner | 7因子2水準128コーナー＋5–30kHz＋30kHz超alias＋Si遅延＋CMP/電流監査 | `RC18_RevB_SI_S1_PASS_FINAL_PACKAGE.zip`, `QUICK_REPLAY_SOURCES/S1_128CORNER.py` | 9/30最終HF19系は「モデル内PASS」。実機性能は別途測定 |
| 過去モデルの来歴監査 | 128-cornerの旧条件再生、係数provenanceを必須ゲートにする | `RC18_RevB_SI_S1_FINAL_VERIFY_PACKAGE_v2.zip` | 9/28側はBLOCKED_PROVENANCE。9/30最終HF19との差を保管 |
| HF Guard DSP | 19-tap HF19、FMAC係数の固定データと係数検証 | `RC18_RevB_SI_HF_GUARD19_FROZEN_PACKAGE.zip`, `HF19_COEFF_VERIFY.py` | frozen JSONとSHA256を維持、未確認の係数へ置換しない |
| MCUリアルタイム処理 | STM32G474 FMAC/DMA、DWTサイクル、Scope SAMPLE→COMMIT実測評価 | S4_15 D8-D15、`D15_TIMING_EVALUATOR.py` | 期限967.25ns・guard>=328ticks。合成CSVの自己診断と実機測定を区別 |
| 制御・保護コード | Q2.30固定小数点、fastpath、fault latching、deadline missのHOLD/SAFE FADE | `RC18_S4_1_CODE_PACKAGE.zip`, `RC18_S4_FAILSAFE_PACKAGE.zip`, `RC18_S4_12_FIXEDPOINT.c/.h` | コード/Hostテスト。MCU実機・過電流ハードウェア試験は別ゲート |
| 物理過渡 | SPICE/NGspice/封じ込め境界、突入、PWM高調波、VDSリンギング、熱 | `RC18_R2_3_1C_DEEP_SIM_PACKAGE.zip`, `RC18_R2_4_TRANSIENT_SCREENING.zip` | 保守モデル・仮定を記録、実機波形と混同しない |
| 半導体寄生 | Coss/Qossと寄生容量・SWリンギングの感度解析 | `rc18_si3_coss_qoss_compare.py`, `rc18_carrier_parasitic_sweep.py` | 比較の前提条件と参照部品を固定 |
| ベンダー照合 | pinout / landpattern / 実寸・向き・干渉 / 部品定格の自動監査 | S2_AUDIT_PACKAGE、S2_VENDOR_REFERENCE_PACKAGE、`RC18_R2_3_1_96PART_FULL_AUDIT.xlsx` | 販売店変更・footprint更新ごとに再監査 |
| 製造工程 | Gerber/Drill/BOM/CPLクロス検証、LCSCマッピング、数量別コスト | `RC18_R2_JLCPCB_RELEASE.zip`, R2.1/R2.2パッケージ | 旧製造版のデータ。E24仕様に流用して発注不可 |
| フェイルセーフECO | PRE 220Ω、FAULT強制停止、接点電圧、Source共通化とパッド・ビア・ゾーンを考慮した配線探索 | `RC18_R2_4_1A_ECO_CIRCUIT_PACKAGE.zip`, E23/E24 handoff | Sourceのみ作業ブランチはHOLD。Gate/Drain/旧net回復とparity未完 |
| 早期比較履歴 | 9月21～23日 RevB/RevD の抽象/低電圧モデル、サンプル系/ジッタ・Si/GaN比較 | `07_EARLY_REVISION_REFERENCES/` | 現行仕様より古い比較・検討資料。現行回路として実装しない |

| 9/20の壁コンセント型旧設計 | wall_filter v0.4→v0.5 KiCad DRC修正（28→0）・OpenSCAD/STLケース/部品フィットゲージ | `00_20260920_WALL_FILTER_EMC_REFERENCE/wall_filter_case_v0_1.zip`と両DRCレポート | 現在のRC18とは別設計。AC100V製造・PSE認証合格とみなさない |
**`ORIGINAL_HISTORICAL_ARTIFACTS/` は当時の原本コピー、`QUICK_REPLAY_SOURCES/` は主要パッケージからバイト単位で取り出した実行入口、`CURRENT_E24_NATIVE_KICAD_HANDOFF_HOLD/` はE24の作業環境。**


| 9/20の壁コンセント型旧設計 | wall_filter v0.4→v0.5 KiCad DRC修正（28→0）・OpenSCAD/STLケース/部品フィットゲージ | `00_20260920_WALL_FILTER_EMC_REFERENCE/wall_filter_case_v0_1.zip`と両DRCレポート | 現在のRC18とは別設計。AC100V製造・PSE認証合格とみなさない |