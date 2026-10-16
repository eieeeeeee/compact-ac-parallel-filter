# YK66 R29: Latching-relay + low-power non-switching supply branch
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Executive result
R28 shows that a 66-kHz housekeeping switcher can be made compatible with YK66, but only by adding a significant self-noise trap.

R29 attacks the problem at its source:
**remove continuous relay-coil power, reduce steady control power, then investigate a low-power non-isolated non-switching mains supply.**

The key enabling component class is a latching signal relay.
This is a research direction only; the final mains-safety architecture is not approved.

## 1. Latching relay candidate
Panasonic TQ2-L2-12V:
- 2-coil latching
- DPDT
- official family rating 0.5 A at 125 VAC resistive
- max switching voltage 125 VAC
- initial contact resistance max 75 mOhm
- open-contact dielectric 1000 Vrms / 1 min
- contact-to-coil dielectric 1500 Vrms / 1 min
- latching action means zero steady coil power after the switching pulse
- current one-off DigiKey Japan price around JPY433–491 depending listing/stock

Sources:
https://industry.panasonic.com/ac/cdn/e/control/relay/signal/catalog/mech_eng_tq.pdf
https://www.digikey.jp/ja/products/detail/panasonic-electric-works/TQ2-L2-12V/251780

This relay is much less robust than the ALQ power relay and is NOT accepted yet for abnormal-current operation.
But the MAG43 normal 100-mV-noise model has branch currents roughly below ~0.2 A even in the 0.1-ohm hard-source analytical case.
Therefore the 0.5-A AC contact rating is credible enough for research screening if independent overcurrent/fault containment prevents abnormal branch current.

## 2. Cost/power trade vs ALQ312
Two ALQ312-class ordinary relays:
- roughly JPY406 total before tax
- ~0.4 W continuous coil power when both energized

Two TQ2-L2 latching relays:
- roughly JPY866–982 one-off total depending listing
- zero steady relay-coil power
- only short set/reset energy during state changes

The latching option costs roughly JPY460–580 more in the current one-off market, but it removes the largest continuous load in the R27 control budget.

## 3. Revised steady control-power budget
With latching relays:
- relay hold power: ~0 W
- magnetic control copper: ~0.13–0.20 W target
- controller / detector: ~0.03–0.08 W
- driver / regulation overhead: ~0.03–0.08 W

Steady target:
roughly **0.2–0.35 W** instead of the R27 ~0.6–0.8 W range.

Relay pulse energy is very small compared with continuous operation and can be supplied from a local reservoir capacitor.

## 4. Capacitive-dropper supply becomes physically plausible
A sealed non-isolated capacitive-dropper supply has no fixed tens-of-kHz oscillator.
It therefore avoids the deterministic 66-kHz source that motivated the R28 trap.

Ideal series-capacitor RMS current:
I = 2*pi*f*C*Vac

At 100 Vac:
| Dropper C | 50 Hz current | 60 Hz current |
|---:|---:|---:|
| 0.47 uF | 14.8 mA | 17.7 mA |
| 0.68 uF | 21.4 mA | 25.6 mA |
| 1.0 uF | 31.4 mA | 37.7 mA |
| 1.5 uF | 47.1 mA | 56.5 mA |

For a 12-V live control rail, a 1-uF class dropper has enough ideal current/power order of magnitude to investigate a ~0.2–0.35-W control domain.
Real usable DC current is lower because of rectifier conduction, ripple, regulation and losses.

This is not a released circuit or safe construction instruction.

## 5. Why this is attractive for YK66
Compared with the 66-kHz offline buck:
- no dedicated 66-kHz switching tone,
- fewer high-frequency power-switching edges,
- no 725-V switching MOSFET,
- potentially lower BOM cost,
- control power requirement is now small enough to make the method plausible.

## 6. It does NOT mean "no self-noise"
A capacitive-dropper rectifier can still inject:
- 100/120-Hz charging current,
- low-order line-current harmonics,
- diode commutation edges,
- reservoir-capacitor current pulses.

Therefore the self-noise problem moves; it does not disappear.

R29's hypothesis is only:
**low-frequency rectifier harmonics and controlled diode edges may be easier to keep out of the 10–50-kHz cleaning band than a permanent 66-kHz switching converter.**

This must be proven by a time-domain current model / measurement.

## 7. Total 50/60-Hz reactive-current impact
MAG43 maximum coarse capacitance is ~960 nF.

If a 1-uF dropper is added, total ideal capacitive current order of magnitude at 100 V / 60 Hz is:
- MAG43 max: ~36 mA
- dropper: ~38 mA
- total: ~74 mA

This remains below the R28 provisional 100-mA engineering budget before any additional HF shunt.

A 1.5-uF dropper would move the total to roughly 93 mA before HF helper capacitance and therefore leaves little margin.

R29 therefore prefers investigating the **~0.68–1.0-uF dropper class**, not 1.5 uF.

## 8. New opportunity: eliminate the bidirectional H-bridge
The ordinary side-biased EE-core architecture only needs to move:
- Lmax at approximately zero DC bias
to
- lower L at positive DC bias.

It does NOT inherently need negative control current.

Therefore the R27 H-bridge assumption was unnecessarily complex for the primary EE-core path.

A unipolar current regulator / PWM switch can control the two series-opposed side windings.
This can reduce:
- component count,
- driver loss,
- firmware complexity.

A bidirectional driver is only required again if the permanent-magnet pre-biased architecture is promoted later.

## 9. Bias-winding turn count becomes a system optimization variable
R26 used ~60 turns per control leg because it kept copper power low enough.

If the control winding uses more turns:
- required current falls in inverse proportion to turns,
- winding resistance rises,
- copper loss can remain similar if copper fill is held roughly constant,
- required driver voltage rises.

This can trade high-current PWM for lower-current control and potentially make a simpler low-power supply possible.

However hundreds of fine-wire turns per side leg can create:
- winding-labor cost,
- parasitic capacitance,
- physical fit problems,
- fragile insulation / manufacturability.

R30 must optimize this explicitly rather than fixing 60 turns.

## 10. Safety consequence is severe
A capacitive-dropper control rail is **not isolated from mains**.

Therefore:
- every MCU, relay-drive and bias-control node is hazardous-live,
- no USB/UART/debug connector may be user-accessible,
- programming/test requires a properly isolated production fixture or pre-programmed controller,
- enclosure, creepage/clearance, fire containment and single-fault behavior become primary safety requirements.

The absence of an exposed user connector makes this architecture possible to study, but does not make it automatically safe.

## 11. R29 decision
### PROMOTE FOR DIRECT COMPARISON
Latching-relay + low-power non-switching supply path.

### KEEP AS FALLBACK
LinkSwitch-TN2 + dedicated 58–74-kHz self-noise trap.

### REVISE
Primary EE magnetic control should be unipolar; remove the H-bridge unless later magnetic topology requires bipolar bias.

## R30 gate
Directly compare two complete housekeeping architectures:

A. 66-kHz offline buck + ALQ312 ordinary relays + dedicated self-noise trap
B. low-power capacitive dropper + TQ latching relays + unipolar magnetic current control

For each calculate:
- named one-off BOM,
- 50/60-Hz reactive current,
- steady real power,
- internally generated noise spectrum model,
- resulting terminal-noise penalty,
- PCB area / heat,
- failure modes,
- all-in JPY3,500 plausibility.

No AC100V fabrication or energization is authorized by R29.
