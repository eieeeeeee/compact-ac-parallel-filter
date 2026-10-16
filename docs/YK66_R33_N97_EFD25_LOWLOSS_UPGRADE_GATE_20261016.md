# YK66 R33: N97 / EFD25 low-loss magnetic upgrade gate
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Executive result
A technically better magnetic material/core candidate exists:
**TDK EFD25/13/9 N97, gapped AL=160 nH, nominal gap 0.50 mm.**

It can reduce the core-loss contribution enough to make MAG50 much more robust.
However current one-off procurement is poor, so it is NOT promoted over the E25/13/7 N87 first-unit candidate yet.

## 1. Why N97 matters
TDK classifies:
- N87 = standard low-loss power ferrite
- N97 = lower-loss / minimum-loss family in the <500-kHz class

Manufacturer typical loss at 100 C:
- N87: 25 kHz / 200 mT ~57 kW/m3
- N97: 25 kHz / 200 mT ~45 kW/m3

N97 also has:
- initial permeability ~2300
- Bs ~510 mT at 25 C
- Bs ~410 mT at 100 C
- optimum 25–500-kHz class

Sources:
https://www.tdk-electronics.tdk.com/download/187242/81166f0de556e5b6a94db7793daed936/pdf-n97.pdf
https://www.tdk-electronics.tdk.com/download/540216/d6940b239127a8bab71b22168746021b/pdf-n87.pdf

## 2. Catalog gapped N97 part found
TDK:
B66421U0160K197
- EFD25/13/9
- N97
- AL = 160 nH ±10%
- nominal gap 0.50 mm
- ue ~125
- le = 57 mm
- Ae = 58 mm2
- Ve = 3310 mm3

Source:
https://product.tdk.com/en/search/ferrite/ferrite/ferrite-core/info?part_no=B66421U0160K197

This is important because unlike E25/13/7, the catalog actually includes a 0.5-mm-class **gapped N97** option.

## 3. Main winding for MAG50
Target Lmax ~380 uH.

N = sqrt(380 uH / 160 nH) ≈ 48.7 turns.

Use ~49 turns as the analytical anchor.

EFD25 bobbin:
- winding area ~40.7 mm2
- mean turn length ~50 mm
- AR ~42.3 uohm

Source:
https://www.tdk-electronics.tdk.com/inf/80/db/fer/efd_25_13_9.pdf

Estimated main-winding Rdc:
~0.10 ohm.

This is worse than E25/13/7 N87 MAG50 (~0.07 ohm) because the EFD bobbin has a higher resistance factor / smaller winding area.

## 4. Core-loss screen
Scale the R32 MAG50 unbiased core-loss screen using:
- N97/N87 25-kHz/200-mT/100-C material-loss ratio ~45/57
- Ae increase 58 / 52.5
- Ve increase 3310 / 3020
- turn count ~49 vs ~50

Order-of-magnitude result:
EFD25 N97 worst screened Rcore ~**0.20 ohm** versus ~0.27 ohm for E25 N87 MAG50.

This is not a manufacturer guaranteed equivalent series resistance; it is a relative screen.

## 5. Total resistance comparison
Use the same branch allowances as R32.

### E25/13/7 N87 MAG50
- Rdc ~0.0705
- Rcore screen ~0.270

### EFD25/13/9 N97 MAG50
- Rdc ~0.1005
- Rcore screen ~0.203

Calculated total screen:

| Candidate | Core x1 | Core x1.4 | Core x2 |
|---|---:|---:|---:|
| E25 N87 | ~0.526Ω | ~0.634Ω | ~0.796Ω |
| EFD25 N97 | ~0.504Ω | ~0.585Ω | ~0.707Ω |

At 100-C copper + core x2:
- E25 N87 ~0.827 ohm
- EFD25 N97 ~0.751 ohm

Thus N97/EFD25 buys about ~0.08-ohm worst-stress margin despite its higher copper resistance.

## 6. Resulting resonance attenuation
For EFD25 N97, 100-C copper + x2 core stress, Rtotal ~0.751 ohm:

- Zs=0.5 ohm: ~4.26 dB
- Zs=1 ohm: ~6.89 dB
- Zs=3 ohm: ~12.20 dB

This is materially safer relative to the original <=0.8-ohm target.

## 7. DC-bias mechanism is also documented for N97
TDK publishes N97 reversible permeability versus DC bias at 25 C and 100 C for multiple effective-permeability core families.
The curves show the same basic mechanism YK66 needs:
incremental/reversible permeability falls as Hdc increases.

Source:
https://www.tdk-electronics.tdk.com/download/528886/d28e0ebe7095bcdafa28C3d7d21aa41/pdf-n97.pdf

Therefore N97 is not merely a lower-loss material; it remains compatible in principle with magnetic-bias tuning.

## 8. Procurement blocks first-unit promotion
Current search:
- part is active / production
- DigiKey lists it as orderable but not stocked for single-piece purchase; large tray/minimum order is shown
- distributor aggregation likewise shows large-MOQ supply
- Japanese search listings show the part, but single-unit purchase at a reliable first-unit price is not confirmed

Sources:
https://www.digikey.com/en/products/detail/tdk/B66421U0160K197/26525269
https://www.marutsu.co.jp/RatedList.jsp?goodsClassCode1=16&goodsClassCode2=0043&goodsClassCode3=0001&maker=TDK

For YK66, “first unit <=JPY3,500” means a part that requires hundreds/thousands of pieces cannot be counted as a viable first-unit component.

## 9. R33 decision
### PERFORMANCE WINNER
EFD25/13/9 N97 0.5-mm / AL160 is the better magnetic-loss architecture on paper.

### FIRST-UNIT WINNER
E25/13/7 N87 remains the practical prototype candidate because single-piece availability is currently much better.

### ACTION
Keep PCB/magnetic footprint strategy flexible enough that an N97 EFD25 production variant can be evaluated later without changing the basic YK66 control architecture.

### IMPORTANT
Do not claim N97 has solved DC-bias core loss.
The x1.4/x2 bias multipliers still require actual characterization.

## R34 gate
Move from magnetic physics back to system economics:
build a complete named-BOM cost envelope for the first-unit N87/MAG50 path and identify exactly which items must fall in price for the <=JPY3,500 all-in requirement to survive.
