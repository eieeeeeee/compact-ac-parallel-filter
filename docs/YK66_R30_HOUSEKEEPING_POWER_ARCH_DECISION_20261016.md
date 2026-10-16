# YK66 R30: Housekeeping power architecture decision
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Purpose
Directly compare the two housekeeping-power paths left by R29, then include a third architecture discovered during R30:
A. 66-kHz LinkSwitch-TN2 buck + ordinary power relays + dedicated self-noise trap
B. capacitive-dropper supply + latching signal relays
C. capacitive-dropper supply + ordinary power relays, but retune the magnetic/capacitor map so no operating state needs both relay coils energized simultaneously

Fixed product concept remains:
- AC100V 50/60Hz
- plug-in-only
- two-terminal L-N parallel
- target first-unit all-in <= JPY3,500 excluding stencil
- no exposed low-voltage interface
- no mains energization until independent safety/fault review

## 1. Current component anchors

### Ordinary power relay
Panasonic ALDP112W:
- 12 V coil
- 200 mW nominal coil power
- 100 mOhm max initial contact resistance
- 5 A / 277 VAC resistive rating
- contact-to-coil dielectric 4 kVrms
- surge withstand contact-to-coil 10 kV
- current one-off DigiKey Japan price about JPY175

Sources:
https://industry.panasonic.com/ap/en/products/control/relay/power/number/aldp112w
https://www.digikey.jp/en/products/detail/panasonic-electric-works/ALDP112W/3641420

Two relays: about JPY350 before tax.

### Latching signal relay
Panasonic TQ2-L2-12V:
- dual-coil latching
- DPDT
- 1 A contact current class in current DigiKey listing
- 125 VAC max switching voltage
- current one-off price roughly JPY430–490 depending listing/stock
- currently poor stock/lead-time situation in the freshest listing

Source:
https://www.digikey.jp/ja/products/detail/panasonic-industry/TQ2-L2-12V/251780

Two relays: roughly JPY860–980 before tax.

### LinkSwitch-TN2
Power Integrations LNK3204D:
- 725-V internal MOSFET
- non-isolated buck / buck-boost / flyback support
- 66-kHz switching
- current one-off DigiKey Japan price about JPY113

Sources:
https://www.power.com/products/linkswitch/linkswitch-tn2
https://www.digikey.jp/ja/products/detail/power-integrations/LNK3204D-TL/6558501

### Large X2 capacitor for a dropper
Current one-off examples:
- 1.5 uF / 310 VAC X2: about JPY324–415
- 1.8 uF / 310 VAC X2: about JPY394–519

Sources:
https://www.digikey.jp/en/products/detail/cornell-dubilier-knowles/155MKP275K/5411113
https://www.digikey.jp/ja/products/detail/kemet/R533N418050P1M/13577886
https://www.digikey.jp/ja/products/detail/kemet/R533R418050P0K/13577901

## 2. Architecture A: 66-kHz buck + ordinary relays
Advantages:
- robust continuous power availability
- integrated protection features in LinkSwitch-TN2 family
- cheap controller IC
- 12-V rail can comfortably power ordinary 200-mW relays and magnetic bias

Disadvantage:
- the supply itself injects a 66-kHz-class conducted signature with frequency jitter
- R28 showed that a plain 1-uF shunt does not hide this in low-impedance mains
- a dedicated 58–74-kHz low-Q trap is required if system-level noise is to improve

R28 representative self-noise trap:
- ~1 uF X2
- ~5.8 uH
- ~0.5-ohm total loss target
- at Zs=0.5 ohm, worst 58–74-kHz ideal attenuation ~3.2 dB
- adds ~37.7 mA L-N reactive current at 100 V / 60 Hz

Cost burden:
- switcher IC ~JPY113
- support components still needed
- two ordinary relays ~JPY350
- 1-uF X2 trap capacitor ~JPY223 class plus low-uH inductor and damping/parasitic burden

This path remains technically credible, but it spends BOM and reactive-current budget suppressing its own supply.

## 3. Architecture B: capacitive dropper + latching TQ relays
Advantages:
- no fixed tens-of-kHz oscillator
- zero relay holding power
- control load can fall to ~0.2–0.35 W class

Disadvantages:
- TQ is a telecom/signal relay with lower switching-voltage/current class than ALDP
- two TQ relays cost roughly JPY500–600 MORE than two ALDP relays
- current availability is poor
- still requires a large X2 dropper capacitor
- rectifier charging pulses still create harmonics / edge noise
- abnormal-current robustness is weaker

Cost conclusion:
The latching relay saves steady power but is economically unattractive at first-unit pricing and weakens the mains-contact margin.

Architecture B is therefore downgraded from primary.

## 4. New R30 finding: ordinary relay power was overestimated
R29 compared:
- 2 ordinary relays = 0.4 W continuous
versus
- 2 latching relays = 0 W continuous.

That is too pessimistic for YK66 because both coarse-capacitor relays do not need to be energized in every tuning state.

For the R25 100/180/680-nF map, selecting the available state with the fewest energized coils over a uniform 10–50-kHz target gives approximately:
- zero energized coils: ~50% of the band
- one energized coil: ~48% of the band
- two energized coils: only ~2% of the band
- mean: ~0.52 energized coils

So the frequency-weighted relay hold power is only about:
0.52 * 0.2 W ~= **0.10 W**
under this artificial uniform-frequency assumption.

This is not a real household noise-frequency distribution, but it proves the ordinary-relay architecture is not inherently a 0.4-W average load.

The remaining problem is the 2-coil worst state near the low end.

## 5. Therefore the best architecture is to eliminate the 2-coil operating state
Instead of paying for latching relays, modify the magnetic tuning ratio and coarse-C map so the entire 10–50-kHz target is covered by only:
- base state: no relay
- mid state: one relay
- low state: the other relay

The fourth both-relays state becomes a calibration/fallback state and is not required during normal coverage.

This turns:
- ordinary robust 277-VAC-class relays
- zero/one coil continuous power
into a lower-cost solution than latching signal relays.

This concept is quantified in R31.

## 6. Capacitive-dropper sizing consequence
If at most ONE 200-mW relay is ever held:
representative steady worst-case load becomes approximately:
- one relay: 0.20 W
- magnetic bias copper: ~0.16–0.20 W
- controller/sensing/driver: ~0.05–0.10 W

Total:
~0.41–0.50 W class.

Ideal series-capacitor current at AC100V:
- 1.5 uF: 47.1 mA at 50 Hz, 56.5 mA at 60 Hz
- 1.8 uF: 56.5 mA at 50 Hz, 67.9 mA at 60 Hz

A 1.5-uF dropper is marginal at 50 Hz after rectifier/regulator losses.
A 1.8-uF class has better power margin.

These are only current/power envelopes, not a released power-supply circuit.

## 7. Safety and self-noise
The capacitive-dropper control domain remains hazardous-live.
It requires:
- sealed inaccessible enclosure
- no exposed programming/debug interface
- controlled production programming/testing
- independent review of creepage, clearance, flame/fault containment, surge and single-fault behavior

The dropper is also NOT noise-free:
rectifier current pulses and diode commutation must be included in the final conducted-noise model.

## R30 decision
### REJECT AS PRIMARY
B. TQ latching relay + dropper:
too expensive and lower mains-contact margin for the benefit obtained.

### HOLD AS FALLBACK
A. 66-kHz LinkSwitch buck:
technically robust, but self-noise burden is architecturally wasteful.

### PROMOTE
C. ordinary ALDP112W-class relays + non-switching/dropper research supply + a new coarse-C/magnetic map that guarantees at most one relay energized in the operating band.

R31 performs that remap.

No AC100V fabrication or energization is authorized by R30.
