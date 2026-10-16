# YK66 R28: System-level self-noise budget and 66-kHz housekeeping trap
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Purpose
R27 identified a system-level contradiction:
a low-cost offline buck can power YK66, but it can also inject conducted switching noise into the exact AC line YK66 is intended to clean.

R28 therefore models the YK66-generated noise as part of the line-noise result instead of treating the housekeeping supply as an unrelated block.

## 1. LinkSwitch-TN2 switching band is not a single 66-kHz line
Power Integrations specifies:
- typical oscillator average about 66 kHz
- 25 C average roughly 62–70 kHz
- full-temperature average roughly 58–74 kHz
- typical frequency jitter about 4 kHz peak-to-peak

Source:
https://www.power.com/sites/default/files/documents/linkswitch-tn2_family_datasheet.pdf

Therefore a narrow 66-kHz high-Q trap is not enough.
A supply-noise absorber must tolerate roughly the 58–74-kHz operating envelope plus modulation sidebands.

## 2. System superposition model
At one frequency:
- Vb = terminal noise that would exist without YK66
- Zth = local household Thevenin impedance seen from the socket
- Zf = total YK66 shunt impedance at that frequency
- Ipsu = YK66 housekeeping-supply Norton current injected into the line

External-noise residual:
Hext = |Zf / (Zf + Zth)|

YK66 self-noise voltage:
Vself = |Ipsu| * |Zf || Zth|

For worst-case coherent phase addition:
Vtotal / Vb <= Hext + |Ipsu|*|Zf||Zth|/Vb

This produces a useful engineering quantity:
the maximum YK66 self-noise current that can be tolerated while the total terminal noise still improves by at least 3 dB.

This model is intentionally simple:
- load is represented as 10 ohm resistive in the numeric screen
- Zs is swept 0.1 / 0.5 / 1 / 3 / 6 ohm
- actual household impedance is complex and frequency-dependent
- actual converter current spectrum is still UNMEASURED

## 3. Plain 1-uF shunt is insufficient around the switching band
A 1-uF capacitor alone was screened from 58 to 74 kHz.

Worst attenuation across that band:
- Zs=0.1 ohm: ~0.01 dB
- Zs=0.5 ohm: ~0.16 dB
- Zs=1 ohm: ~0.50 dB
- Zs=3 ohm: ~2.40 dB
- Zs=6 ohm: ~4.65 dB

Conclusion:
**a plain 1-uF X2 branch cannot be relied on to hide a 66-kHz offline supply in a low-impedance socket.**

## 4. Broad low-Q series-resonant shunt improves the 58–74-kHz band
Illustrative fixed housekeeping-noise absorber:
- target center = 66 kHz
- C = 1.0 uF
- ideal L = ~5.82 uH
- total series R = 0.5 ohm

This is a two-terminal parallel series-RLC branch.
It is not the MAG43 branch and does not require active tuning.

Worst calculated attenuation across 58–74 kHz:
- Zs=0.1 ohm: ~0.68 dB
- Zs=0.5 ohm: ~3.22 dB
- Zs=1 ohm: ~5.69 dB
- Zs=3 ohm: ~11.11 dB
- Zs=6 ohm: ~14.60 dB

This is a large improvement over a plain capacitor in the realistic >=0.5-ohm cases.

But 1 uF adds about:
- 31.4 mA RMS at 100 V / 50 Hz
- 37.7 mA RMS at 100 V / 60 Hz
of L-N reactive current.

## 5. Self-noise current budget
Assume Vb = 100 mV RMS at a frequency inside 58–74 kHz.
For the 1-uF / 5.82-uH / 0.5-ohm fixed trap, the worst current that can be added by the YK66 supply while total line noise still remains at least 3 dB below the 100-mV baseline is approximately:

| Zs | Worst 58–74-kHz self-noise current budget |
|---:|---:|
| 0.1 ohm | no 3-dB margin |
| 0.5 ohm | ~5 mA RMS equivalent |
| 1 ohm | ~40 mA |
| 3 ohm | ~67 mA |
| 6 ohm | ~75 mA |

The budget scales approximately linearly with the pre-existing line-noise voltage.
For example if the real baseline is only 10 mV, the 0.5-ohm budget becomes roughly 0.5 mA.

This is why the actual offline-buck input-current spectrum MUST be measured.
A filter cannot be declared successful from external-noise attenuation alone.

## 6. Broader trap gives much more self-noise margin but spends reactive current
A wider candidate screen:
- C = 1.5 uF
- center 66 kHz
- corresponding ideal L ~3.88 uH
- R around 0.3 ohm

Across 58–74 kHz at Zs=0.5 ohm:
- minimum attenuation ~4.7 dB
- 3-dB total-noise self-injection budget ~45 mA per 100-mV external baseline

But 1.5 uF adds:
- ~47 mA at 100 V / 50 Hz
- ~56.5 mA at 100 V / 60 Hz

Combined with the MAG43 coarse bank at its maximum ~960 nF state, total L-N reactive current becomes roughly 90 mA class at 60 Hz before any further HF branch is added.

R28 therefore sets a NON-STANDARD engineering target:
**keep total YK66 60-Hz L-N reactive current below about 100 mA unless a compelling performance result justifies more.**
This is a design budget, not a regulatory limit.

## 7. Critical system result
The 66-kHz offline-supply architecture is technically possible, but it forces YK66 to spend:
- an additional high-value X2 capacitor,
- an additional low-uH inductor,
- additional 50/60-Hz reactive current,
simply to suppress its own power supply.

That is architecturally wasteful.

## 8. Higher switching frequency is not automatically a complete cure
A higher-frequency supply moves its primary signature into a region where passive shunting is easier, but:
- harmonics remain,
- switching edges extend into MHz,
- the YK66 shunt network can interact with the converter input network,
- a different IC/topology may add cost.

A 132-kHz switcher class exists in other Power Integrations families, but the readily applicable low-component-count non-isolated buck route remains LinkSwitch-TN2-class around 66 kHz.
Do not change IC family solely to chase switching frequency without a complete topology/cost review.

## 9. R28 decision
### HOLD
LinkSwitch-TN2 / 66-kHz non-isolated supply remains technically viable.

### DOWNGRADE
It is no longer the preferred cost architecture because its own EMI requires a dedicated suppression burden.

### NEW QUESTION
Can the control system be made low-power enough to use a non-switching or quasi-non-switching mains-derived supply and eliminate the deterministic 66-kHz source entirely?

That is R29.

No AC100V fabrication or energization is authorized by R28.
