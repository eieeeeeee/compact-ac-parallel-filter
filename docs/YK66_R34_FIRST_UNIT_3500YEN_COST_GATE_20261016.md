# YK66 R34: First-unit JPY3500 all-in cost gate
Date: 2026-10-16
Status: COST GATE / RESEARCH ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Purpose
Test the current MAG50/N87 architecture against the user's hard commercial constraint:

**First physical unit total <= JPY 3,500 including PCB, parts, assembly, tax and shipping; stencil excluded.**

This gate deliberately uses current one-off pricing rather than future volume pricing.

## 1. Current one-off price anchors

### Magnetic core set
TDK E25/13/7 N87:
- B66317G0500X187, 0.50-mm-class gapped half: JPY210
- B66317G0000X187, ungapped half: about JPY143
- B66208B1110T001 horizontal bobbin: about JPY206
- B66208A2010X000 yoke/clip class: about JPY77

Sources:
https://www.digikey.jp/en/products/detail/tdk/B66317G0500X187/3914718
https://www.digikey.jp/en/products/detail/tdk/B66317G0000X187/3914721
https://www.digikey.jp/en/products/detail/tdk/B66208B1110T001/3914554

Magnetic hardware subtotal before copper/winding labor:
~JPY636.

### Coarse switching
Panasonic ALDP112W:
- 12-V, 200-mW coil
- 5-A / 277-VAC max switching class
- one-off ~JPY175

Two:
~JPY350.

Source:
https://www.digikey.jp/en/products/detail/panasonic-electric-works/ALDP112W/3641420

### Housekeeping dropper capacitor
KEMET R533N418050P1M:
- 1.8 uF
- 310 VAC
- X2
- +/-20%
- one-off ~JPY394

Source:
https://www.digikey.jp/ja/products/detail/kemet/R533N418050P1M/13577886

### MCU
Microchip ATTINY202:
~JPY85–87 one-off.

Source:
https://www.digikey.jp/ja/products/detail/microchip-technology/ATTINY202-SSNR/9554991

### Rectifier
Diodes Incorporated MB10S-13:
- 1-kV bridge
- one-off roughly JPY88–100 depending current listing snapshot.

Source:
https://www.digikey.jp/ja/products/detail/diodes-incorporated/MB10S-13/7241380

### Fuse
Littelfuse 37402500000:
- 250 mA / 250 VAC time-delay board fuse
- one-off Mouser Japan ~JPY259.

Source:
https://www.mouser.jp/ja/ProductDetail/Littelfuse/37402500000

### Thermally protected MOV
Littelfuse TMOV14RP140E:
- 140-VAC max
- 6-kA surge class
- thermally protected
- one-off ~JPY301.

Source:
https://www.digikey.jp/ja/products/detail/littelfuse-inc/TMOV14RP140E/1154438

## 2. Conservative first-unit raw-part envelope
Not all R34 line items are frozen MPNs yet. The following reserves are used rather than hiding the missing cost:

| Cost item | R34 one-off reserve |
|---|---:|
| N87 core pair + bobbin + yoke | JPY636 |
| ALDP112W x2 | JPY350 |
| 1.8-uF X2 dropper | JPY394 |
| 82/180/680-nF X2 bank | JPY400 reserve |
| ATTINY202 | JPY85 |
| 1-kV bridge | JPY100 |
| PCB fuse | JPY259 |
| thermal MOV | JPY301 |
| low-voltage regulator / bias switch / detector / passives | JPY250 reserve |
| winding copper + insulation materials | JPY200 reserve |
| manual custom-magnetic winding / assembly reserve | JPY400 |
| plug/enclosure/mechanical reserve | JPY250 |

Conservative raw subtotal:
**about JPY3,625 before consumption tax, PCB fabrication, PCB assembly, and shipping.**

Therefore MAG50 already fails the <=JPY3,500 first-unit all-in target before the board is ordered.

## 3. Shipping makes ordinary DigiKey one-off procurement especially unfavorable
DigiKey Japan currently states:
- orders >=JPY6,000: free shipping
- orders below JPY6,000: JPY2,000 shipping charge

Source:
https://www.digikey.jp/ja/help-support/delivery-information/delivery-time-and-cost

A YK66-specific one-off DigiKey order that stays below JPY6,000 therefore pays a shipping charge that is itself more than half the complete YK66 target.

This means:
**the JPY3,500 requirement cannot be met by independently buying the one-off BOM from DigiKey and then separately buying PCB/assembly.**

## 4. PCB/assembly fixed costs are also too large for a literal single-unit order
JLCPCB currently advertises:
- 2-layer PCB <=100x100 mm: USD2 for 5 boards
- Japan promotional shipping around USD4.5 on the Japanese landing page
- Economic PCBA setup ~USD8.18
- stencil ~USD1.53 (stencil is excluded from the user's target)
- hand-soldering project fee ~USD3.58 if required

Sources:
https://jlcpcb.com/help/article/how-do-i-place-an-order
https://jlcpcb.com/jp/JPV
https://jlcpcb.com/help/article/pcb-assembly-price

Even before component prices, normal prototype PCB + PCBA fixed fees and shipping consume a material part of a JPY3,500 budget.

Coupons can reduce setup cost, but the engineering cost target must not depend on a temporary promotion.

## 5. R34 verdict
### FAIL — current MAG50 first-unit procurement architecture
This is a cost failure, not a physics failure.

MAG50 cannot honestly be called a <=JPY3,500 first-unit design if:
- premium one-off distributor components are purchased separately,
- custom magnetics are hand-wound as a paid assembly step,
- PCB/PCBA is ordered separately,
- all shipping is charged to the first unit.

## 6. What must change
At least two of the following are required:
1. reduce the number of high-value mains components,
2. eliminate one relay / one large X2 class,
3. eliminate or simplify custom-magnetic assembly labor,
4. source most ordinary electronics through the PCBA assembler instead of DigiKey,
5. use a domestic/combined supply chain that does not add JPY2,000 component shipping,
6. reduce outsourced PCBA fixed fees or move to a simpler assembly flow.

The JPY3,500 target remains fixed.
The architecture, not the target, must move.

## R35
Before changing the magnetic architecture, re-test the obvious cheap fallback:
multi-resonant fixed passive shunts with no MCU, relay or power supply.
If that still cannot retain useful broadband effect at Zs~0.5 ohm, proceed to a one-relay high-range magnetic architecture.
