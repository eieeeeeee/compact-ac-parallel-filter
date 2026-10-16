# YK66 R35: Passive fallback rejection and one-relay MAG6R1 rescue
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## 1. Why revisit passive fixed traps
R34 shows that MAG50 is too expensive as a literal one-off product.
The cheapest possible correction would be to remove:
- MCU,
- control power supply,
- magnetic bias electronics,
- relays,
and replace them with several fixed low-loss RLC shunt branches.

Because the grid model has now changed from a universal 0.1-ohm assumption to realistic frequency-dependent cases, this possibility must be re-tested rather than rejected from old R10 results.

## 2. Three-branch global numerical optimization
Model:
- two-terminal parallel shunt
- three series-RLC branches in parallel
- target band 10–50 kHz
- load = 10 ohm resistive for this screening
- source Zs = 0.5 / 1 / 3 ohm
- total branch capacitance <=2.2 uF
  - equivalent 100-V / 60-Hz ideal reactive current <=~83 mA
- branch center frequencies, capacitances and series resistance numerically optimized

Best continuous optimization found approximately:
- branch centers ~11.7 / 19.2 / 38.6 kHz
- C ~0.78 / 0.86 / 0.56 uF
- total C ~2.19 uF
- deliberately lossy branch R ~2.4–2.5 ohm

Performance:
- Zs=0.5 ohm: worst 10–50-kHz attenuation only ~0.41 dB
- Zs=1 ohm: worst ~0.87 dB
- Zs=3 ohm: worst ~2.1 dB

This is not sufficient for the low-impedance objective.

## 3. Five fixed resonant branches also fail
A five-branch optimization was repeated under the same total-C constraint.

Representative optimized centers:
~10.8 / 15.1 / 22.4 / 35.4 / 43.5 kHz
total C ~2.15 uF.

Performance:
- Zs=0.5 ohm: worst ~0.43 dB
- Zs=1 ohm: worst ~0.83 dB
- Zs=3 ohm: worst ~2.06 dB

Important conclusion:
**adding more fixed traps does not solve the broad low-Z problem when total 50/60-Hz capacitance is constrained.**

The branches have to be damped enough to overlap, and once damped their shunt conductance is not low enough to beat a stiff source across the whole band.

Therefore the cheap fully passive fallback is rejected again, now under the updated realistic-grid model.

## 4. New cost-rescue architecture: MAG6R1
If adaptive resonance is physically necessary, reduce high-voltage switching from two relays to one.

Research candidate:
**YK66-MAG6R1**

Target:
- one variable magnetic element
- only one coarse capacitor relay
- two normal capacitance states
- no second coarse relay
- still cover 10–50 kHz

## 5. Optimized two-state map
Post-trim production screen:
- effective C error ±5%
- Lmax error ±5%
- usable magnetic ratio target 6.0 with 5.8–6.2 corner sweep

A strong standard-value solution:
- Lmax nominal ~450 uH
- Lmin ~75 uH
- magnetic ratio ~6:1
- base C = 120 nF
- relay adds 470 nF
- states = 120 nF and 590 nF

Nominal resonance spans:
- 590 nF: ~9.77–23.93 kHz
- 120 nF: ~21.66–53.05 kHz

The two states overlap.

Corner screen:
- post-trim C ±5%
- Lmax ±5%
- magnetic ratio 5.8–6.2

Worst center-frequency coverage:
~99.2%
Worst center gap:
~0.32 kHz.

This is close to MAG50's coverage while using only ONE high-voltage relay.

## 6. Main magnetic winding
Using the same TDK E25/13/7 N87, 0.50-mm-gap AL~151-nH anchor:

To obtain Lmax~450 uH:
Nmain ~54.6 turns.

TDK bobbin-resistance-factor screen:
Rdc ~83 mOhm.

This is higher than MAG50 but remains in the same useful low-resistance class.

## 7. Core-loss screen
Same conservative N87 model as R32:

Worst best-state unbiased equivalent Rcore across sampled 10–50 kHz:
~0.25 ohm.

Simple branch resistance screen:
- main AC copper ~1.5x DC
- one relay contact 0.10 ohm
- capacitor/PCB reserve 0.05 ohm

Result:
- core x1.0: Rtotal ~0.53 ohm
- core x1.4: ~0.63 ohm
- core x2.0: ~0.78 ohm
- 100-C copper + core x2: ~0.82 ohm

Corresponding ideal resonance attenuation:
at core x1.4:
- Zs=0.5 ohm ~4.9 dB
- Zs=1 ohm ~7.8 dB
- Zs=3 ohm ~13.4 dB

At 100-C copper + core x2:
- Zs=0.5 ohm ~4.0 dB
- Zs=1 ohm ~6.5 dB
- Zs=3 ohm ~11.7 dB

Therefore the larger tuning range does NOT automatically destroy the low-loss objective in the screening model.

## 8. Magnetic control cost of 6:1
Using the same behavioral saturation-knee calibration:

Estimated total-loop MMF:
- 3.5:1 ~72 At
- 6.0:1 ~101 At

With the provisional two x 60-turn control winding:
- current ~0.85 A class
- copper loss ~0.32 W at 25 C
- ~0.42 W at 100 C

This is significantly more control power than MAG50.

Therefore MAG6R1 trades:
**one less relay + one less coarse X2 branch**
for
**more DC magnetic-bias power and a harder unproven tuning ratio.**

## 9. Cost implications
Direct component saving relative to MAG50:
- one ALDP112W removed: ~JPY175
- one coarse X2 capacitor function removed: roughly JPY80–200 class
- PCB area / driver / coil-power state logic simplified

Likely direct one-off saving:
~JPY250–400 class.

This alone does not repair the full R34 shipping/assembly deficit.
But it is directionally correct and can combine with PCBA-integrated sourcing.

## 10. R35 decision
### REJECT
Pure 3-branch and 5-branch fixed passive shunts as the primary 10–50-kHz low-Z solution.

### KEEP
MAG50 as the lower magnetic-risk adaptive benchmark.

### PROMOTE AS COST CHALLENGER
**MAG6R1: 6:1 variable magnetic range + one relay + 120/590-nF two-state map.**

## R36 gate
The next decision is not another ideal circuit sweep.
It must answer which architecture has lower *total delivered first-unit cost*:

A. MAG50:
- easier 3.5:1 magnetics
- 2 relays
- lower control power

B. MAG6R1:
- harder 6:1 magnetics
- 1 relay
- higher control power

and combine this with a realistic procurement plan that avoids a standalone JPY2,000 DigiKey shipping charge.

No AC100V fabrication or energization is authorized by R35.
