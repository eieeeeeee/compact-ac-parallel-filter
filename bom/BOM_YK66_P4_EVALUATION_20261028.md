# YK66 Rev45U P4 — 評価試作用部品表
作成日: 2026-10-28
対象: 50×32mm、2層、板厚1.6mm。PCB blob 9545336db3f86ee7a858b75458c8d7f374d018e8。
製造データrun: 40661228439。これは評価試作の組立指定であり、製品安全・量産適合の承認ではない。

旧 bom/BOM.md は32×28mm Rev.A用。今回の基板へ使用しない。
本表は基板から13実装部品を抽出し、LEDとダイオードに評価用の発注型番を指定した。基板ファイルのTBD表記・銅箔・形状は変更していない。

| Ref | 数量/基板 | メーカー | 発注型番 | 値・形状 | 確認状態 |
|---|---:|---|---|---|---|
| C1 | 1 | TDK/EPCOS | B32923M3105M003 | 1µF ±20%、305Vrms、X2、22.5mmピッチ | 既存指定。公式製品情報照合済み |
| F1 | 1 | Littelfuse | 0216002.MXEP | 216シリーズ、アキシャル | 既存指定を維持。保証された時間電流特性・実装後保護協調は別途 |
| MOV1 | 1 | Littelfuse | TMOV14RP175E | 熱保護付きMOV | 既存指定を維持。採用理由・保護協調の最終確認は別途 |
| TCO1 | 1 | Sensience/MICROTEMP | G4A01098C | G4温度ヒューズ | 既存指定を維持。納入品の承認・リード加工・C1への熱結合を確認 |
| J1 | 1 | Phoenix Contact | 1711725 | MKDS 3/2-5,08、2極 | 1.30mm穴への公差込み挿入保証は未確定 |
| RL1、RL2 | 2 | YAGEO | RC2512FK-07150KL | 150kΩ ±1%、2512、1W/70℃ | 公式個別仕様書照合済み。実装温度・過渡耐量は別評価 |
| RB1〜RB4 | 4 | YAGEO | RC2512FK-07220KL | 220kΩ ±1%、2512、1W/70℃ | 公式個別仕様書照合済み。難燃・故障時安全の保証を意味しない |
| D1 | 1 | Vishay | 1N4148W-E3-08 | SOD-123 | 評価試作用のメーカー・発注型番を指定 |
| LED1 | 1 | Kingbright | APT3216QWF/G | 白色、1206、3.2×1.6×0.75mm | 評価試作用に選定。微小電流での明るさは未保証 |
| PCB | 1 | 基板製造業者 | 検証済みrunのGerber/Excellon | 50×32mm、2層、1.6mm | 発注仕様書を参照 |

## 接続・組立上の必須対応
基板は独自パッド番号を使う。部品メーカーの端子番号をそのまま基板番号へ対応させない。

| 部品 | A（アノード） | K（カソード） |
|---|---|---|
| LED1 | 基板pad1、/LED_A、(3.7,20.2)mm | 基板pad2、/N、(7.7,20.2)mm |
| D1 | 基板pad1、/N、(7.0,23.0)mm | 基板pad2、/LED_A、(3.0,23.0)mm |

Kingbright図面では端子1=K、端子2=A。本基板のpad1=A、pad2=Kとは逆なので、極性マークを基板pad2(/N)側へ対応させる。Vishay D1のカソード帯は/LED_Aへ対応させる。
座標は基板ファイルの絶対座標であり、裏面を目視した左右方向の指示ではない。

## LEDの形状と明るさ
- メーカー推奨ランドは各1.75×1.5mm、内側間隔2.0mm。現行LEDランドは各2.0×1.8mm、内側間隔2.0mmで、公称形状は推奨ランドを包含する。メーカー推奨と同一ではなく、はんだ量・位置ずれ・実装結果を現物確認する。
- 光度仕様は20mA時。RL1+RL2=300kΩの現行回路はそれより小さい電流となるため、掲載光度をそのまま適用しない。
- 100Vrms、正弦波、抵抗300kΩ、LED順方向電圧を仮に3.3Vとした理想計算: LED電流ピーク約0.460mA、全周期平均約0.145mA。これはシミュレーション・測定結果ではなく、微小電流での明るさも保証しない。
- まず絶縁された低電圧定電流源で0.1〜0.5mAの範囲を評価し、予定の窓・ライトパイプを介した視認性を確認する。今回、抵抗値や基板配線は変更しない。

## 放電抵抗の構成
(RB1+RB2)と(RB3+RB4)の2枝並列。合成220kΩ、C1=1µFの理想時定数0.22秒。
旧Rev.A部品表の440kΩ・0.44秒は今回の基板に適用しない。抜去後の実電圧は別途測定する。

## 一次資料
- LED: https://www.kingbrightusa.com/images/catalog/spec/APT3216QWF-G.pdf （V.6B）
- D1: https://www.vishay.com/docs/86356/1n4148w.pdf （Rev.1.0）
- RL: https://yageogroup.com/component-documentation/download/specsheet/RC2512FK-07150KL
- RB: https://yageogroup.com/component-documentation/download/specsheet/RC2512FK-07220KL
- C1: https://product.tdk.com/en/search/capacitor/film/emi-suppression/info?part_no=B32923M3105M003
- J1: https://www.phoenixcontact.com/en-in/products/printed-circuit-board-terminal-mkds-3-2-508-1711725
- TCO: https://www.sensience.com/wp-content/uploads/2023/10/G4-MicroTemp-Product-Information.pdf
