# YK66 R35: MAG59 one-relay / two-state recovery architecture
Date: 2026-10-17
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Executive result
A simpler architecture was found that preserves the two-terminal plug-in concept while reducing:
- high-voltage relay count from 2 -> 1
- coarse resonant capacitor components from 3 -> 2
- maximum normal resonant capacitance from ~762 nF -> ~490 nF

Research name:
**YK66-MAG59**

The cost saving is real, but it demands a much larger magnetic tuning ratio:
~5.5:1 instead of MAG50's 3.5:1.

## 1. Core magnetic target
Keep the same TDK E25/13/7 N87 / 0.50-mm-gap family.

Set:
- Lmax ~525 uH
- target ratio ~5.5:1
- Lmin ~95.5 uH

Using AL ~151 nH:
Nmain = sqrt(525 uH / 151 nH) ≈ **59 turns**

TDK bobbin resistance-factor screen:
Rdc ≈ 28 uohm * 59^2 ≈ **97 mOhm**

## 2. Only two normal capacitance states
Base X2:
- 100 nF

One relay adds:
- 390 nF

Normal states:
- relay OFF: 100 nF
- relay ON: 490 nF

Ideal resonance spans at L=525 -> 95.5 uH:

| State | C | Relay count | Resonance span |
|---|---:|---:|---:|
| high | 100 nF | 0 | ~21.97–51.51 kHz |
| low | 490 nF | 1 | ~9.92–23.27 kHz |

The ranges overlap around 22–23 kHz.
Therefore 10–50 kHz is covered with **one relay only**.

## 3. 50/60-Hz burden improves
Maximum normal resonant capacitance:
490 nF.

At 100 V / 60 Hz:
I ≈ 18.5 mA RMS.

Compare:
MAG50 max normal 762 nF -> ~28.7 mA.

MAG59 saves about 10 mA of 60-Hz branch current and leaves more current budget for the housekeeping supply / HF absorber.

## 4. Tolerance screen
Post-calibration target screen:

### tighter production-calibrated case
- C effective error ±3%
- Lmax ±3%
- magnetic ratio 5.4–5.6

Result:
- worst center-frequency coverage ~98.9%
- max center-frequency gap ~0.44 kHz

### looser case
- C ±5%
- Lmax ±5%
- ratio 5.3–5.7

Result:
- worst coverage ~95.4–96.5% depending ratio envelope
- max gap roughly 1.4–1.8 kHz

Conclusion:
MAG59 needs stronger end-of-line magnetic/capacitance calibration than MAG50.

## 5. Magnetic MMF penalty
Using the same R26/R32 saturation-knee screen:

| L ratio | MMF screen |
|---:|---:|
| 3.5:1 | ~72 At |
| 4.0:1 | ~79 At |
| 4.5:1 | ~85 At |
| 5.0:1 | ~91 At |
| **5.5:1** | **~96 At** |
| 6.0:1 | ~101 At |

Thus MAG59 is still inside the former 0–120-At serious research envelope.

With the old 60-turn-per-leg control winding screen:
current is roughly 0.8-A class and copper loss roughly 0.29 W at 25 C.

Control power is higher than MAG50 but still not automatically disqualifying.
Increasing control turns may reduce required current but has winding-volume / capacitance / labor consequences.

## 6. Core-loss screen
Using the same conservative N87 screen:
- Nmain ~59 turns
- states 100 / 490 nF
- L ~95.5–525 uH

Worst best-state unbiased equivalent Rcore in sampled 10–50-kHz map:
~0.31 ohm.

Branch resistance screen:
- main copper AC allowance = 1.5 x Rdc
- one relay contact = 0.10 ohm
- C + PCB = 0.05 ohm

Results:
- core x1.0 -> Rtotal ~0.61 ohm
- core x1.4 -> ~0.73 ohm
- core x2.0 -> ~0.92 ohm
- 100 C copper + core x2 -> ~0.96 ohm

Ideal resonance attenuation at the harsh 100-C/x2 screen:
- Zs=0.5 ohm -> ~3.5 dB
- Zs=1 ohm -> ~5.8 dB
- Zs=3 ohm -> ~10.6 dB

Therefore MAG59 gives up thermal/loss margin versus MAG50 but still retains useful attenuation in the realistic >=0.5-ohm source cases.

## 7. Current one-off cost saving
Current representative one-off anchors:

Magnetic:
- same E25 core pair + bobbin ~JPY559

Switching:
- one ALDP112W ~JPY175 instead of two ~JPY350

Tuning X2:
- 100 nF X2 ~JPY70
- 390 nF / 310-VAC X2 ~JPY226–276

Housekeeping:
- 1.8-uF X2 ~JPY368
- MCU ~JPY85
- 500-mA approved fuse ~JPY130

Named subtotal using the lower current 390-nF price:
**~JPY1,613 ex tax**

MAG50 named subtotal was ~JPY1,831.

Direct saving:
~JPY218 before secondary savings in PCB area / assembly / routing.

This is helpful but not enough by itself to guarantee JPY3,500 all-in.

## 8. Important system trade
MAG59 exchanges:
**fewer expensive high-voltage parts**
for
**more magnetic tuning depth and more control MMF**.

This is exactly the type of trade YK66 should make only if the magnetic element can provide the ratio cheaply.

If measured 5.5:1 requires:
- >~1 A continuous control current,
- excessive DC-bias core loss,
- or a more expensive magnetic assembly,
then the saved relay/capacitor cost disappears and MAG50 should remain primary.

## 9. R35 decision
### PROMOTE TO HEAD-TO-HEAD TEST
MAG59 becomes a cost-recovery challenger to MAG50.

### MAG50 remains the performance-risk baseline
- lower tuning ratio
- better thermal/core-loss margin
- higher BOM cost

### MAG59 advantage
- one relay
- two coarse X2 components
- lower normal mains reactive current
- ~JPY200+ direct named-BOM saving

### MAG59 risk
- 5.5:1 magnetic range not experimentally validated on this geometry
- less loss margin
- tighter calibration requirement

## R36 gate
Do not choose MAG59 only because it is cheaper.
R36 must compare MAG50 and MAG59 under exactly the same:
- measured/behavioral L(Idc,T)
- DC-bias core-loss multipliers
- realistic Zgrid envelope
- control supply loss
- first-unit full cost envelope

Additionally investigate whether the housekeeping dropper / HF network can safely share a passive function and remove another dedicated component block.

No AC100V fabrication or energization is authorized by R35.
