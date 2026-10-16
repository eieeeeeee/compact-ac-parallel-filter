# YK66 R20: Real-switch / real-inductor gate for low-impedance adaptive shunt
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Fixed concept
- Plug-in-only AC100V 50/60Hz.
- Two-terminal L–N parallel device. No series insertion between outlet and load.
- Goal: reduce household conducted power-line noise as much as practical.
- First-unit target <= JPY 3,500 including PCB, components, assembly, tax and shipping; stencil excluded.
- 0.1 ohm remains a hard-source survivability / stress corner, not a universal attenuation acceptance point.

## R20 question
R19 showed that adaptive-Q resonant termination is physically attractive, but the tuning element must be real, low-loss, mains-capable and cheap.
R20 compares the practical tuning mechanisms rather than ideal reactances.

# 1. Concrete low-loss resonator candidate
A useful off-the-shelf inductor was found:
- Bourns 5252-RC
- 125 uH
- 3.5 A
- DCR 80 mOhm max
- SRF 2.25 MHz
- DigiKey Japan one-off price about JPY311 before tax
Source: https://www.digikey.jp/en/products/filter/fixed-inductors/71

At 20 kHz, ideal resonance needs C = 506.6 nF.
A standard 470 nF X2 capacitor shifts ideal resonance only to about 20.764 kHz.
Example X2:
- KEMET R463I347050N0M
- 0.47 uF, 310 VAC, X2
- DigiKey Japan one-off price about JPY164 before tax
Source: https://www.digikey.jp/ja/products/detail/kemet/R463I347050N0M/5731179

Ideal 506.6 nF would draw about 19.1 mA RMS of 60-Hz reactive current at 100 Vrms.
This is not earth leakage and not real-power dissipation, but it is real branch RMS current that all series components must tolerate.

## Resonance leverage with one realistic low-DCR inductor
If a mains relay contributes its documented maximum initial contact resistance of 100 mOhm, the optimistic lower bound before capacitor ESR and AC/core loss is:
Rtotal >= 0.08 + 0.10 = 0.18 ohm.

Simple analytical model:
- resistive source Zs
- 10-ohm load
- tuned branch exactly at resonance
- branch R = 0.18 ohm
- no capacitor ESR, no inductor AC loss, no wiring parasitics

Ideal peak voltage-noise attenuation at resonance:
| Zs | Calculated peak attenuation |
|---:|---:|
| 0.1 ohm | 3.81 dB |
| 0.5 ohm | 11.24 dB |
| 1 ohm | 15.64 dB |
| 3 ohm | 22.81 dB |
| 6 ohm | 26.78 dB |

This is an upper-bound-style result, NOT a product claim.
At 0.1 ohm there is almost no loss margin: real AC winding resistance, capacitor ESR, PCB copper and contact aging can easily push the branch below 3 dB.
At 0.5 ohm and above, resonance gives much more useful margin.

# 2. Solid-state switch comparison: the surprising result

## 2.1 600-V PhotoMOS: reject for the low-Q-loss path
Panasonic examples:
- AQY206GV: 600 V, max Ron 15 ohm, one-off price around JPY2,600 depending variant/stock
  https://www.digikey.jp/ja/products/detail/panasonic-electric-works/AQY206GV1Y/18689845
- AQY216EHA: 600 V, max Ron 120 ohm, around JPY500-700
  https://www.digikey.jp/ja/products/detail/panasonic-industry/AQY216EHAX/18343160
- AQY284SX: 400 V, max Ron 35 ohm, around JPY266
  https://www.digikey.jp/ja/products/detail/panasonic-industry/AQY284SX/8549355

R19 requires branch resistance in roughly the sub-ohm to few-ohm region.
Therefore these PhotoMOS parts destroy the desired Q and are rejected as the resonant-current-path switch.

## 2.2 Triac-type optically isolated SSR: reject as precision low-signal tuning switch
Panasonic AQH3223:
- 600 V repetitive peak off-state
- 1.2 A RMS
- 12 A nonrepetitive surge
- 5 kVrms I/O isolation
- about JPY301 one-off
- peak on-state voltage is around 1 V class in the family data
Sources:
https://industry.panasonic.com/jp/ja/products/control/relay/solid-state/number/aqh3223
https://industry.panasonic.com/ac/cdn/e/control/relay/solid-state/catalog/semi_eng_aqh.pdf
https://www.digikey.jp/en/products/detail/panasonic-industry/AQH3223AZ/4757806

This is excellent for switching ordinary AC loads, but a ~1-V junction drop and thyristor holding/latching behavior are strongly nonlinear relative to millivolt/100-millivolt noise signals.
It is not a clean sub-ohm small-signal element for an adaptive high-Q resonator.
Reject as the primary tuning switch.

## 2.3 Back-to-back 600-V MOSFET pair: hold, not winner
A low-cost 600-V MOSFET example can be only a few hundred yen, but an AC bidirectional switch needs at least a back-to-back pair and a suitable gate-drive arrangement.
Example:
Infineon IPD60R1K4C6, 600 V, one-off around JPY236.
https://www.digikey.jp/ja/products/detail/infineon-technologies/IPD60R1K4C6ATMA1/5332863

Even before the gate-drive / isolation / protection burden, two devices add resistance and cost per tuning bit.
Higher-current lower-Rds parts can reduce loss but increase price and gate capacitance.
For multiple tuning states this rapidly approaches the cost/complexity of a full active filter.
Hold only for a future one-switch helper function, not a large capacitor-bank DAC.

# 3. Mechanical mains relay: technically best switch, but state count kills cost/power
Omron/Aratas G5Q family:
- 277 VAC max switching voltage
- 10 A contact class
- 100 mOhm max initial contact resistance
- 4 kVAC coil-contact dielectric strength
- 8 kV impulse withstand between coil and contacts in the referenced datasheet
- 5-V SPST coil version about JPY290-300 one-off
- SPST coil power about 200 mW
Sources:
https://www.digikey.jp/ja/products/detail/aratas-formerly-omron-components/G5Q-1A4-DC5/1815721
https://components.omron.com/sites/components.omron.com.eu/files/datasheet_pdf/J155-E1.pdf

This is the first investigated mains-capable switch whose contact resistance is low enough to preserve the resonator Q.

But R19 showed approximate 10–80-kHz state counts for one low-loss trap:
- true 0.1-ohm hard source: hundreds of tuning states
- 1 ohm: ~50 states class
- 3 ohm: ~20 states class
- 6 ohm: ~12–16 states class

Therefore a relay-per-capacitor-state architecture is rejected.

A small binary / coarse bank is still plausible for only a few coarse ranges.
However four G5Q-class relays already cost roughly JPY1,160 before tax and can consume up to roughly 0.8 W of coil power if all are energized.
Six relays would be roughly JPY1,740 before tax and around 1.2 W coil power.
That creates another expensive power-supply problem.

Conclusion:
**mechanical relays are acceptable only as 1–2 coarse-range selectors, not as the main high-resolution tuning DAC.**

# 4. Why a cheap 3–6 bit direct capacitor bank is now rejected
A fixed 125-uH inductor requires:
- about 2.03 uF for 10 kHz
- about 506.6 nF for 20 kHz
- about 126.7 nF for 40 kHz
- about 31.7 nF for 80 kHz

That is a ~64:1 capacitance range.

A direct 6-bit mains capacitor bank can in principle span such a range, but:
- six low-loss mains switches are too expensive,
- six relay coils create a power-supply burden,
- PhotoMOS resistance is much too high,
- triac SSRs are nonlinear,
- six back-to-back MOSFET switch cells are no longer a cheap/simple design.

Reject as primary YK66 architecture.

# 5. New preferred tuning mechanism: magnetically variable inductor, but redesigned for YK66
The strongest surviving path is a magnetically controlled resonant inductor.

Relevant published classes:
- 2025 IEEE TEMC tunable EMI notch: core saturation + capacitor bias, continuous tuning, experimentally useful attenuation; authors explicitly discuss applicability beyond its original band.
  DOI: https://doi.org/10.1109/TEMC.2025.3620422
- DC-biased EE-core variable inductors use a main AC winding and opposing control windings on side legs so induced AC voltage can cancel in the control circuit:
  https://doi.org/10.1109/ACCESS.2024.3462849
- Orthogonal-flux variable inductors are a known class where a control field changes effective permeability without placing semiconductor switches in the main current path:
  https://patents.google.com/patent/US6674320B2/en
- A newer 2026 resonant-converter study again uses DC-biased EE-core variable inductance:
  https://www.mdpi.com/2079-9292/15/14/2999

The 2025 EMI prototype used substantial control current and additional bias-isolation magnetics, so it cannot be copied into YK66.
The R21 task is therefore not "copy that inductor", but:
**design a YK66-specific dual/orthogonal control-winding inductor whose control ampere-turns are obtained with many turns and modest current, while keeping the mains/noise winding low resistance.**

If that can be achieved, one variable magnetic element can replace many high-voltage relay/MOSFET tuning switches.

# 6. Secondary passive simplification: multi-tuned / C-type shunt sections
Power-system filter literature confirms:
- double-tuned shunt networks create two low-impedance harmonic points in one combined branch;
- C-type high-pass filters can obtain wide high-frequency shunting while reducing fundamental-frequency resistor loss.

Sources:
https://apseng.co.uk/Technical/passive-ac-harmonic-filters
https://www.mathworks.com/help/simscape-electrical/ref/passiveharmonicfilterthreephase.html
https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/hve2.12291

A coarse analytical sweep of a 4-element C-type topology in the YK66 simplified 1/3/6-ohm source model did NOT produce a broad-band breakthrough over a plain 1-uF shunt / damped RC.
Therefore C-type is not promoted to the main architecture.
Its value is as a possible high-frequency helper or as a way to reduce the tuning span of the main resonator.

# 7. Cost gate with actual one-off component anchors
Current one-off distributor anchors found:
- 125-uH low-DCR inductor: ~JPY311
- 470-nF X2 capacitor: ~JPY164
- ATTiny202-class MCU: ~JPY87
  https://www.digikey.jp/en/products/detail/microchip-technology/ATTINY202-SSFR/9554943
- G5Q mains power relay: ~JPY290
- PhotoMOS 600-V low-R candidate: far too expensive and still too resistive
- Triac SSR: ~JPY301 but unsuitable for low-signal high-Q tuning

Illustrative tuning-core subtotal:
- inductor + one X2 + MCU + one G5Q ~= JPY852 before tax
- add three more G5Q relays + three more 470-nF-class X2 caps -> about JPY2,214 before tax total for those named parts alone

The second case leaves too little of the JPY3,500 first-unit budget for:
- fuse / surge / discharge protection
- sensing
- control supply
- PCB
- assembly
- tax
- shipping

Therefore R20 rejects a 4–6 relay high-resolution bank on economics even before full safety qualification.

# 8. Updated architecture ranking after real-part gating
1. **Magnetically variable low-loss resonant shunt + passive HF branch** — PRIMARY R21 research.
2. **Fixed/dual-tuned passive coarse absorption + one magnetic fine-tune degree** — very promising cost reducer.
3. **One or two mechanical mains relays only for coarse range selection** — acceptable helper.
4. **PZT resonant absorber behind a mains-safe coupling/protection barrier** — wildcard; qualification unresolved.
5. **Back-to-back HV MOSFET one-switch helper** — hold.
6. **Large PhotoMOS/SSR tuning bank** — reject.
7. **Large mechanical relay capacitor DAC** — reject.
8. **Full broadband active cancellation** — RC18 benchmark, not primary YK66 cost path.

# 9. Key engineering interpretation
The low-impedance problem cannot be solved by "more capacitance" or "smarter software" alone.
What matters is creating a sub-ohm-to-few-ohm **effective shunt only at the noise frequency** while keeping the 50/60-Hz burden tolerable.

R20 proves that this can be physically plausible at a selected frequency with commodity low-DCR magnetics.
The remaining difficulty is moving that low-impedance point over the household noise band without paying for dozens of high-voltage switches.

This is why magnetic permeability tuning has moved to first place.

# R21 gate
Design and compare three YK66-specific magnetic structures at the analytical level:
A. DC-biased EE core with opposing control windings
B. orthogonal-flux / transverse-bias structure
C. coarse tapped inductor + only one magnetic fine-tune range

For each:
- required L range for a fixed X2 capacitor
- required permeability ratio
- required ampere-turn control envelope
- main-winding DCR target
- control-winding copper loss target
- expected Q at 10/20/40/80 kHz
- core size / material class
- whether one-off BOM can still plausibly stay <= JPY3,500
- fail-safe behavior with control current lost or saturated

No mains prototype or AC100V energization is authorized by R20.
