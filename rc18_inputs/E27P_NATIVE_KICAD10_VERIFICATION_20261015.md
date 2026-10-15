# RC18 E27P — 修正した実設計・Native 10.0.6検証レポート（製造停止）

2026-10-15 / NONFAB HOLD

## 目的
E27N元ファイルを保全し、Native KiCadで検出したERCエラー2件とR304製造属性2件だけを個別候補へ直接修正した。実際の配線は今回変更しない。

## データと検証証拠
- 原本 E27N: SHA256 `08f54bf0db5b2b2e6d93e7fb55b135cd289205a46bcc8b98da169ced962b3652`
- 修正候補 E27P: SHA256 `f83469afb17b854eaa9bebff13a463b0bdfc192fbf4137fe56f7e347301a707a`
- GitHub 新専用ブランチ：`rc18-e27p-erc-r304-dnp-hold-20261015`（元の `main` 不変）
- GitHub Actions 実行：https://github.com/eieeeeeee/compact-ac-parallel-filter/actions/runs/38700687713
- 実行器: KiCad **10.0.6** Docker 公式タグ、40ファイル原本マニフェスト照合、原本は読み取り専用。

## 今回のECO（回路変更箇所2ファイルだけ）
1. `11_INDEPENDENT_FAULT_LATCH_E25C.kicad_sch` に **U1005 Q_N ピン3 NC**、**U1006 pin1 NC** の２マーカーを追加。
2. `RC18_RevB_SI.kicad_pcb` で **R304** フットプリントの表示値を `100k FIT` → `DNP_PV_MICROAMP`、BOM属性を `smd exclude_from_bom` に変更。`08_INJECTION_DISCONNECT.kicad_sch` の既存DNP指定を一致させた。メーカー公表の光起電電流を上回る100k抵抗負荷問題に関するE25B設計注意文を尊重。
3. これ以外の全電気接続、部品座標、銅パターン、既存MOSと保護機能は変更せず。
4. 元の2設計ファイルへ逆変換する検証でバイト同一（SHA256一致）を確認。

## Native結果：E27NからE27Pへの比較

| 指標 | E27N前 | E27P後 |
|---|---:|---:|
| ERC errors | 2 | **0** |
| ERC warnings | 3 | **3** （U1003/U1005/U1302の未検証フットプリント） |
| DRC geometry violations | 0 | **0** |
| PCB unconnected | 3 | **3** |
| PCB schematic-parity errors | 66 | **64** （未配置64 FIT） |
| R304 value/BOM parity | 2 | **0** |

**E27P runner status=FAIL**：ERC警告3、PCBの未接続3、未配置64が残るのでNative完全PASSではない。

## ブロッカー管理の更新
元の管理17項目のうち、**E25R-NATIVE（Web/Native kicad-cli検証不能）だけは技術的に解消**した。したがってE27Pの新しい管理表では「技術障害の解消1件、未解消16項目」とする。ただし**製造リリース許可0件**、独立保護未検証。元のE25R台帳は変更しない。

## 次工程優先順
A. 残るPCB未接続3ネットを**安全な電気ネット対応＋配線形状／クリアランス／Kelvin経路確認**して独立候補にECO。SW_SOURCE R304はDNPのため安易に電流枝へ接続しない。R302_KELVIN_N・TEST_Aは実スイッチング配線なので短絡・SOA・基板層間の分離確認が必須。
B. U1003/U1005/U1302の注文型番とメーカー外形・pad mapを確定し、ERC 0 errors /0 warningsへ。
C. 64 FIT部品の実PCB配置、全net parity、DRC・zone refill、独立PRE_VERIFIED/OCP/失電OFFなど16工程の解消。

**NO POWER / NO AC / NO ORDER / NO FAB**。現行設計は試験用の12V絶縁回路のみ、交流100V接続厳禁。