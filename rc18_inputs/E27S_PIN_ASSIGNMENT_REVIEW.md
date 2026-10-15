# RC18 E27S — 単一MCU集約に向けた48ピン実配線監査とアナログ電源ピン名称ECO

**2026-10-15 / NONFAB HOLD / 新規設計バリアント・製造不可**

## 進めた作業

- E27Rのチップ統合構想を、実際のE27P KiCad 15シート、STM32G474CBT6 U1/LQFP48へ対応付けた。
- 既存48ピンの名称とグローバルネットラベル、PCB U1の48パッドを対応付け、CSVへ記録。パッケージpin 19はGND、20はVREF_FILT、21は3V3に接続済み。
- メーカーのLQFP48定義（ST DS12288 Figure 6、AN5346）に従い、U1シンボル19番 **VSS→VSSA**、21番 **VDD→VDDA** として、ライブラリ `RC18_Custom.kicad_sym` と階層シートの埋込キャッシュ `03_MCU_DIGITAL.kicad_sch` だけを修正した。
- 修正を逆変換すると原本のSHA256と一致。銅配線、ネットラベル、ピン番号、実装属性、外付け部品は変更なし。原本40ファイルを再SHA検証。
- PA5(13): OPAMP2_VINM / VLINE_FINE_VINM、PA6(14): OPAMP2_VOUT / VLINE_FINE_OUT、PA7(15): OPAMP2_VINP / VLINE_FINE_VINP、PB13(27): ADC3_IN5 / VLINE_WIDE_ADC、PA8(30)・PA9(31): HRTIM1_CHA1/2 / SI_HI/SI_LOという**候補割当**を実ネットと照合。これらはMCUのアナログ/タイマ資源の潜在的用途を示すもので、CubeMX同時動作コンフィグ・実ファームでは未検証。

## 設計上の新しい問題点

1. **名称の修正だけではVDDAアナログ供給を安定化できない。** 21番は3V3、19番はGND。VDDAの適切なバイパス・基準帰路・供給リップル、VREF+ (20番 VREF_FILT) の許容と給電をメーカーの推奨回路へ照合する必要がある。現時点は安全保証なし。
2. **OPAMP2はすでにFine経路に割当ラベルがある。** U2=TLV9062IDGKRはシート04でVLINE_BUFを形成し、VLINE_WIDE_ADCとVLINE_FINE_VINPへ出す前段。OPAMP2使用中だからといってU2を削除できない。入力ノイズ・同相範囲・飽和・位相・等価回路・GPIO多重割当・2.909MS/s ADCサンプル条件を検証する必要。
3. **STM32には12Vの注入電流源がない。** 既存Si出力段・注入コンデンサ・独立178mAハードOCP・失電OFF・E-STOP・PRE_VERIFIEDの現物HIGH元を維持する。

## Native検証の境界

- 旧E27PのKiCad 10.0.6実績：ERC 0 errors /3 warnings、DRC幾何0、PCB未接続3、未配置64、パリティ64。これはE27Sが自動的にPASSするという意味ではない。
- E27SのKiCad ERC/DRCはGitHub Actionsで**このZIPのSHAを指定して再実行**する必要がある。
- 部品削減実績0、実証原価削減0円。159 FIT / 40 DNP / 64未配置 / 17元停止条件（環境問題1件のみ技術的解決）。

## 次工程

1. 新規E27S専用ブランチでNative KiCad10.0.6 ERC/DRC/parityを実行、ログを公開保存。
2. U2 TLV9062の移転可能性を実際の回路トポロジーとADC位相で検証し、削除する場合は具体的な配線変更候補だけを作る。
3. VDDA/VSSA/VREF+回路の低周波〜ADC高周波ノイズ経路、電流、バイパスのメーカー設計条件を確定。
4. 独立物理保護を残し、部品変更前後で整合のあるBOMとKiCadを作る。

メーカー参照：
- ST DS12288 LQFP48 Figure 6: https://www.st.com/resource/en/datasheet/stm32g474qe.pdf
- ST AN5346 ADC reference/analog supply: https://www.st.com.cn/resource/en/application_note/an5346-stm32g4-adc-use-tips-and-recommendations-stmicroelectronics.pdf

**HOLD_NO_POWER_NO_AC_NO_ORDER_NO_FAB**。旧Si／E27P原本とGitHub mainは不変。