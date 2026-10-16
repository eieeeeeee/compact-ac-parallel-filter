# YK66 R21: Three-band coarse-C + 3:1 magnetic fine-tune architecture
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Objective
Reduce the main adaptive-resonator tuning burden enough that YK66 can plausibly remain:
- plug-in-only,
- two-terminal L–N parallel,
- low part count,
- first-unit target <= JPY 3,500.

R20 rejected large high-voltage capacitor-switch banks. R21 therefore asks:
**How little magnetic tuning range is actually required if higher frequencies are handed to the passive HF branch and only coarse capacitor states are switched?**

# 1. Breakthrough: do NOT magnetically tune 10–80 kHz continuously
A single fixed capacitor would require a 64:1 inductance range to move resonance from 10 to 80 kHz:
L proportional to 1/f^2.

That is too large.

However the passive HF shunt becomes increasingly useful above roughly 50 kHz.
Therefore the magnetic resonator only needs to cover approximately 10–50 kHz.

If two cheap coarse capacitor switches are added, four capacitance states are available.
A 3:1 continuously variable inductance can then cover the entire 10–50 kHz region with overlap.

## Candidate coarse capacitor set
Base capacitor: 68 nF
Switchable addition A: 120 nF
Switchable addition B: 470 nF

Four states:
- 68 nF
- 188 nF
- 538 nF
- 658 nF

Variable inductance target:
- Lmin = 135 uH
- Lmax = 405 uH
- tuning ratio = 3.0:1

Ideal resonance coverage:

| Capacitance state | Resonance span with L=405→135 uH |
|---:|---:|
| 658 nF | 9.75–16.89 kHz |
| 538 nF | 10.78–18.68 kHz |
| 188 nF | 18.24–31.59 kHz |
| 68 nF | 30.33–52.53 kHz |

There are overlaps at each handoff.
Therefore **two coarse capacitor switches + one 3:1 variable inductor are mathematically enough to cover about 9.75–52.5 kHz continuously in ideal resonance placement.**

Above ~50 kHz, the separate passive HF shunt takes over progressively.

This is dramatically simpler than the 6-bit / dozens-of-state tuning approach.

# 2. Fundamental-current burden remains moderate
Maximum coarse state = 658 nF.

At 100 Vrms / 60 Hz, ideal capacitive branch current is:
I = 2*pi*60*658 nF*100 V ≈ 24.8 mA RMS.

At 50 Hz it is about 20.7 mA RMS.

This is not earth leakage; the branch is L–N.
It is nevertheless real RMS current that the capacitor, relay contacts and inductor winding must continuously carry.

The high-frequency passive helper adds its own reactive current, so final total branch current still needs a product-level budget.

# 3. Required resonator resistance is much less extreme once 0.1 ohm is treated correctly
At exact resonance, for a resistive Thevenin source and branch resistance R:
A_dB = 20 log10(1 + Zth/R)

With 10-ohm illustrative load:

| Total resonant branch R | Zs=0.1Ω | Zs=0.5Ω | Zs=1Ω | Zs=3Ω | Zs=6Ω |
|---:|---:|---:|---:|---:|---:|
| 0.3Ω | 2.48 dB | 8.26 dB | 12.11 dB | 18.78 dB | 22.61 dB |
| 0.5Ω | 1.57 dB | 5.81 dB | 9.00 dB | 14.99 dB | 18.59 dB |
| 0.8Ω | 1.01 dB | 4.06 dB | 6.59 dB | 11.79 dB | 15.10 dB |
| 1.0Ω | 0.82 dB | 3.38 dB | 5.62 dB | 10.39 dB | 13.53 dB |

Interpretation:
- 0.1-ohm hard source still demands extremely low loss and remains a stress case.
- For 0.5–1 ohm and above, a total branch resistance around 0.5–1 ohm can still produce useful resonance attenuation.
- This makes a custom variable inductor physically much more realistic than R19's sub-0.2-ohm universal target.

R21 provisional target:
**Rtotal <= 0.8 ohm over the active resonant band**, with lower preferred.
This is an engineering target, not yet proven.

# 4. 3:1 magnetic tuning is now close to published experimental capability
A 2026 EE-core variable resonant inductor experiment reports:
- EE25/20/6 PC40 ferrite core
- center-leg air gap 1.04 mm
- main AC winding 48 turns
- two DC control windings, 30 turns each, series-opposed
- DC bias current 0–1.0 A
- inductance tuning 40–110 uH

Tuning ratio:
110 / 40 = 2.75:1

Source:
https://www.mdpi.com/2079-9292/15/14/2999
DOI: https://doi.org/10.3390/electronics15142999

YK66 now asks for 3.0:1, not 64:1.
That is only about 9% more tuning ratio than the published 2.75:1 example.

The absolute inductance is higher (135–405 uH), and our operating band is lower, so the magnetic design is NOT transferable directly.
But the required tuning ratio is now experimentally credible as a technology class.

# 5. New low-control-power direction: permanent-magnet-biased orthogonal core
A particularly relevant Japanese research path was found.

Aizu, Nakamura, Ohinata and Arimatsu (Tohoku University / Tohoku Electric Power) reported an:
**Orthogonal-Core-Type Variable Inductor with Permanent Magnets**

The permanent magnet is inserted in the DC-control magnetic path.
Reported concept:
- a finite magnetic bias exists even at zero control current,
- positive/negative control current then varies the operating point,
- reactive-power control becomes continuous around the permanent-magnet bias.

2023 paper:
https://www.jstage.jst.go.jp/browse/msjtmsj/7/1/_contents/-char/en
DOI: https://doi.org/10.20819/msjtmsj.23TR508

Earlier 2022 conference summary:
https://www.magnetics.jp/kouenkai/2022/doc/program/29ALL.pdf

This does NOT prove a small YK66 inductor or low-cost 10–50-kHz operation.
The published hardware is much larger and aimed at power-system reactive-power control.

But the concept is strategically important:
**a permanent magnet can supply part of the control flux for free, reducing the amount of continuous electrical bias required.**

R21 therefore promotes a new candidate:
### PM-biased orthogonal variable resonator
- mains/noise winding: low-resistance AC winding
- orthogonal DC control path: electrically separate
- permanent magnet supplies baseline bias
- small bidirectional control current trims inductance around that bias

Potential advantage:
continuous tuning without many high-voltage switches and with lower steady control power.

Commercialization would require an IP/FTO review; literature availability is not a patent clearance.

# 6. Two-switch coarse capacitor bank is now the preferred switching architecture
Instead of six high-voltage tuning switches:
- one X2 68-nF base capacitor remains connected in the resonant branch,
- one mains-rated switch adds ~120 nF,
- one mains-rated switch adds ~470 nF.

This yields four useful states.

The exact implementation and switching sequence are NOT released for mains construction yet.
The important architectural result is simply:
**2 high-voltage switching functions are enough instead of 6+ if the magnetic element provides ~3:1 fine tuning.**

Candidate relay class from R20:
- Omron/Aratas G5Q
- 277 VAC max switching voltage
- 100 mOhm max initial contact resistance
- 4 kVAC coil-contact dielectric strength
- around JPY290 one-off for a 5-V SPST version
https://www.digikey.jp/ja/products/detail/aratas-formerly-omron-components/G5Q-1A4-DC5/1815721
https://components.omron.com/sites/components.omron.com.eu/files/datasheet_pdf/J155-E1.pdf

Two such relays cost about JPY580 before tax instead of roughly JPY1,740 for six.

The remaining weakness is continuous coil power.
A latching/contact-selection mechanism or a lower-power switching method remains desirable, but the state count is now small enough that this is no longer the dominant architecture blocker.

# 7. Cost envelope improves materially
Named one-off anchors:
- ATTiny202-class MCU: ~JPY87 before tax
- two G5Q relays: ~JPY580
- 470-nF X2 example: ~JPY164
- smaller X2 values are expected to be same-order or lower, but exact MPNs are not frozen
- custom variable magnetic component: NOT costed yet
- passive HF branch: NOT frozen
- safety/protection/PCB/assembly/shipping: still required

R21 no longer spends JPY1,500–2,000 just on a high-resolution relay bank.

The variable inductor becomes the single main cost/risk item.

# 8. Proposed final functional split
## 9.8–52.5 kHz
Adaptive resonant termination:
- 4 coarse C states from 2 switches
- 3:1 continuously variable magnetic inductance
- target Rtotal <= 0.8 ohm where practical
- dominant-noise-frequency tracking

## ~50 kHz upward
Passive HF shunt:
- ordinary safety-rated passive network
- no active driver
- overlap with the magnetic branch around the transition region

## Below ~10 kHz
Do not force YK66 to act as a power-harmonic conditioner.
Measure first.
If a strong household noise population exists below 10 kHz, it becomes a separate gate because the required L/C and grid-current burden rise sharply.

# 9. New primary architecture
**YK66-PM3R (research name):**
Permanent-magnet-assisted / DC-biased variable resonant shunt
+ 2-bit coarse X2 capacitor selection
+ passive HF absorber.

This is now preferred over:
- full active current cancellation,
- 6-bit high-voltage capacitor banks,
- large PhotoMOS arrays,
- many fixed RLC traps.

# 10. R22 gate
The next work must determine whether the magnetic component is actually manufacturable.

R22 tasks:
1. Select a core family suitable for 10–50 kHz and 135–405 uH.
2. Estimate main-winding turns, gap, flux density and copper DCR.
3. Estimate control ampere-turns required for 3:1 tuning.
4. Compare:
   A. ordinary DC-biased EE core,
   B. PM-biased orthogonal core,
   C. conventional saturable reactor.
5. Put a hard power ceiling on the control winding.
6. Verify that control loss does not erase the JPY3,500 advantage.
7. Build a nonlinear magnetic SPICE/behavioral model before any mains prototype.

No AC100V fabrication or energization is authorized from R21.
