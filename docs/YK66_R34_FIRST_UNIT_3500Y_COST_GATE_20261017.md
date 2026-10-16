# YK66 R34: First-unit all-in JPY 3,500 cost gate
Date: 2026-10-17
Status: COST / ARCHITECTURE GATE — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Fixed requirement
The cost requirement is NOT relaxed:
- first unit,
- PCB,
- components,
- assembly,
- tax,
- shipping included,
- stencil excluded,
- target <= JPY 3,500.

## 1. Current MAG50 first-unit named-part floor
Current one-off distributor snapshots (JPY, pre-tax; prices fluctuate):

Magnetic skeleton:
- TDK B66317G0500X187, E25/13/7 N87 gapped half: ~JPY170–210
- TDK B66317G0000X187, E25/13/7 N87 ungapped half: ~JPY133–186
- TDK B66208B1110T001 bobbin: ~JPY206–240

Switching:
- Panasonic ALDP112W 12-V relay x2: JPY175 each = JPY350

MAG50 coarse X2 bank, cost-screened with readily available standard values:
- 100 nF / 310 VAC X2: ~JPY70
- 150 nF / 310 VAC X2: ~JPY76
- 680 nF / 310 VAC X2: ~JPY158

Housekeeping dropper:
- KEMET R533N418050P0K 1.8 uF / 310 VAC X2: ~JPY429

Control:
- ATTINY202 class MCU: ~JPY85

Protection:
- 250 mA / 250 VAC PCB fuse, Littelfuse 374-class: ~JPY259 one-off reference
- thermally protected MOV TMOV14RP140E: ~JPY306
- 200-V / 1-A bridge rectifier reference: ~JPY116

Named-parts subtotal:
- low snapshot: ~JPY2,358 pre-tax
- high snapshot: ~JPY2,485 pre-tax
- with 10% JCT: ~JPY2,594–2,734

This subtotal STILL EXCLUDES:
- magnet wire
- custom winding labor
- unipolar bias transistor / current control
- low-voltage reservoir/regulation
- noise sensing
- discharge/bleeder and minor passives
- passive >50-kHz helper
- PCB fabrication
- PCB assembly
- enclosure / plug hardware
- shipping

Therefore the current MAG50 architecture is already too expensive to satisfy the all-in first-unit target through ordinary one-off distribution.

## 2. Outsourced PCBA floor makes the failure explicit
JLCPCB Economic PCBA pricing, current published schedule:
- setup fee: USD 8.18/order
- stencil: USD 1.53/order
- hand-solder labor: USD 3.58/order
- manual assembly: additional per-joint fee
Source:
https://jlcpcb.com/help/article/pcb-assembly-price

Stencil is excluded from the YK66 target by requirement, so it is not counted here.

Current USD/JPY reference used:
~158.031 JPY/USD.

Converted:
- setup fee alone: ~JPY1,293
- hand-solder labor fee: ~JPY566

Even WITHOUT hand solder, PCB fabrication, shipping, winding, sensing or unresolved parts:
- named parts after JCT + JLC setup = ~JPY3,886–4,026

With JLC hand-solder order fee:
~JPY4,452–4,592

Therefore:
**MAG50 + conventional outsourced prototype assembly FAILS the JPY3,500 first-unit gate before the design is complete.**

## 3. Other assembly channels do not prove a first-unit pass yet
Seeed Fusion currently advertises:
- PCBA order quantity from 1 piece
- free shipping on PCBA orders
- turnkey assembly
Sources:
https://www.seeedstudio.com/pcb-assembly.html
https://support.seeed.cc/portal/en/kb/articles/seeed-fusion-pcb-assembly-service-quick-questions

However exact operation/engineering/components cost requires an uploaded Gerber/BOM/assembly package.
Do NOT count Seeed as a JPY3,500 pass without a real quote.

Elecrow's current web quote interface displays a promotional assembly-cost field, but final PCBA pricing depends on uploaded BOM/design, PCB cost, parts and shipping.
Do NOT base the engineering target on a promotion.

## 4. Important conclusion
The present cost problem is no longer a 50-yen optimization problem.

A few changes such as:
- cheaper relay,
- cheaper MCU,
- one fewer passive,
cannot recover the missing margin.

For a true first-unit all-in <=JPY3,500 target, one of the following must happen:
A. raw electronics BOM falls to roughly JPY1,300–1,700 class, OR
B. assembly/PCB/shipping service has nearly zero NRE/setup, OR
C. the magnetic/control architecture loses several major blocks.

MAG50 as currently composed does not satisfy A.

## 5. Current major one-off cost blocks
Approximate order of magnitude:
1. magnetic core set + bobbin: ~JPY510–640
2. 1.8-uF dropper X2: ~JPY429
3. two relays: JPY350
4. fuse + thermally protected MOV: ~JPY565
5. three coarse X2 capacitors: ~JPY300
6. MCU + rectifier: ~JPY200
7. unresolved control/sense/HF parts/winding: still additional

The first-unit target is therefore constrained by architecture, not PCB trace optimization.

## 6. R34 decision
### FAIL
Current MAG50 physical architecture under ordinary one-off component sourcing + outsourced assembly.

### DO NOT relax
- AC100V plug-in-only concept
- safety protection
- low-impedance performance goal
- JPY3,500 first-unit all-in target

### NEXT
Cost-down must remove blocks, not merely substitute brands.

R35 first action:
replace the awkward 82-nF state and reduce magnetic loss with a cheaper standard-X2 map.
R36 research action:
evaluate transformer-coupled low-voltage tuning, where high-voltage relays and continuous DC magnetic bias may be replaced by a fixed coupling transformer plus low-voltage switched secondary reactance.

No AC100V fabrication or energization is authorized by R34.
