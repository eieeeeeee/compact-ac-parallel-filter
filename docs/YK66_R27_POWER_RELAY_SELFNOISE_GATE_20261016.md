# YK66 R27: Low-voltage power architecture, relay substitution, and self-noise gate
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## Executive result
R26 indicates the MAG43 magnetic physics is still plausible.
R27 finds that the **isolated low-voltage power module is now a larger cost penalty than the control electronics themselves.**

A new low-cost research path is therefore promoted:
**sealed, non-isolated appliance-style offline buck + 12-V relay/control rail**, provided the entire control domain is treated as hazardous-live and no user-accessible interface exists.

This is NOT a product-safety approval. It is a cost/architecture research path that requires independent mains-safety review.

## 1. Why the isolated module is expensive
Previous anchor:
MEAN WELL IRM-01-class encapsulated AC/DC module:
- around 1 W output class
- one-off cost around JPY 800+ before tax

This consumes a large fraction of the complete JPY3,500 first-unit target before PCB, protection, magnetic winding, assembly and shipping.

The magnetic bias driver itself is much cheaper.

## 2. Low-cost non-isolated offline-switcher class exists
Power Integrations LinkSwitch-TN2 family:
- designed specifically for low-component-count non-isolated offline buck / buck-boost / flyback supplies
- integrated 725-V or 900-V MOSFET depending device
- current limiting, thermal shutdown, overvoltage and short-circuit protection
- 85–265-V input class
- appliance / metering / home-building automation use cases

Current one-off DigiKey Japan examples:
- LNK3204D ~JPY113
- LNK3205D ~JPY133
- LNK3206D ~JPY151

LNK3206D family capability listed by the manufacturer:
- up to ~360 mA CCM universal-input class
- ~225 mA MDCM universal-input class

Sources:
https://www.power.com/products/linkswitch/linkswitch-tn2
https://www.digikey.jp/en/products/filter/power-management-pmic/ac-dc-converters-offline-switchers/748

This is enough current capability for the YK66 control domain by a wide margin.

The final supply still needs rectification / energy-storage / inductor / diode / feedback parts; the IC price is NOT the whole power-supply BOM.

## 3. Why non-isolated control is specifically relevant to YK66
YK66 has:
- no exposed USB,
- no external sensor cable,
- no user-accessible low-voltage connector,
- no required earth/PE connection,
- sealed plug-in usage.

Therefore a research architecture where the MCU, H-bridge, relay coils and magnetic control winding all live in one mains-referenced hazardous-live domain may remove the need for a reinforced-isolation AC/DC module.

Potential advantages:
- much lower BOM cost,
- no custom isolated transformer,
- lower PCB area,
- simpler power path.

But the cost saving is valid only if the final enclosure / PCB / programming / test / fault strategy satisfies the applicable product-safety requirements.
No exposed low-voltage node may be assumed safe merely because it is 5 or 12 V.

## 4. Relay substitution improves cost
Panasonic ALQ312:
- 12-V coil
- 16.7 mA
- 200 mW coil power
- 100 mOhm max initial contact resistance
- 5 A at 250 VAC resistive rating
- 4 kVAC contact-to-coil dielectric strength
- 8 kV contact-to-coil surge withstand
- IEC/EN60335-1-related family compliance
- current one-off DigiKey Japan price about JPY203 before tax

Sources:
https://industry.panasonic.com/jp/ja/products/control/relay/power/number/alq312
https://www.digikey.jp/ja/products/detail/panasonic-electric-works/ALQ312/3511298

Two ALQ312 relays:
- ~JPY406 before tax
- worst simultaneous coil power ~0.4 W
- contact resistance remains in the same 100-mOhm class used by the R20–R26 resonator calculations

This is cheaper than the earlier G5Q price anchor.

## 5. 12-V rail is preferable to a 5-V rail
Relay coil power is the same independent of rail choice, but 12 V reduces relay current:
- two ALQ312 coils together: ~33.4 mA at 12 V

The magnetic control winding is a low-resistance inductive load.
An H-bridge can PWM/current-regulate it from the same 12-V rail.

MCU / sensing can be derived locally from the 12-V live rail with a small regulator.

This avoids designing the whole supply around 5-V / high-current delivery.

## 6. Control-domain power budget
R26 0.50-mm-gap primary case:
- target MMF ~64 At behavioral estimate
- provisional 60 turns per side leg / two side coils
- approximately 0.53 A magnetic-control current
- copper loss about 0.13 W

Conservative operating budget:
- two relays ON: ~0.40 W
- magnetic control copper: ~0.13–0.20 W
- H-bridge loss: ~0.03–0.07 W screening allowance
- MCU + detector / analog front-end: ~0.03–0.08 W
- low-voltage regulation overhead: ~0.02–0.05 W

Total active control load:
roughly **0.61–0.80 W** in a high-consumption state.

This makes a 1-W-class output rail plausible but leaves little thermal margin.
A 1.5–2-W-capable offline buck is a more comfortable design target even if typical consumption is lower.

## 7. Critical discovery: the power supply can pollute the exact line YK66 is trying to clean
LinkSwitch-TN2 switches around the ~66-kHz class and intentionally uses frequency jittering for EMI reduction.

That is just above the MAG43 adaptive-resonator handoff (~50 kHz).

This creates a new mandatory requirement:
**YK66 must reduce its own control-supply conducted emission before claiming household-line noise reduction.**

A device that removes external noise but injects a new 66-kHz signature is a failure.

Therefore:
- the passive HF branch must explicitly include the control-supply switching band,
- 66-kHz fundamental and harmonics must be part of the system simulation,
- input-current spectrum of the offline buck must be included in the same 2-kHz–30-MHz measurement,
- the supply cannot be evaluated as an unrelated housekeeping circuit.

This is a first-class R28 metric.

## 8. Why the 66-kHz class is still preferable to a 30-kHz offline buck
ST also has non-isolated 5-V offline-buck reference designs around 30-kHz switching.

But 30 kHz sits directly inside the MAG43 10–50-kHz adaptive-resonator range.
It would force the tracking system to fight a strong internally generated deterministic tone.

A ~66-kHz supply places its main switching signature into the passive-HF section instead.

Therefore, for YK66:
**a >50-kHz housekeeping switcher is preferable to a ~30-kHz one**, provided the HF passive branch can absorb its conducted signature.

This is not a universal statement for other products.

## 9. Why an off-the-shelf fixed inductor does not replace the variable magnetic part
A search of current fixed-inductor offerings found typical 100-uH parts with:
- ~255 mOhm DCR at ~1.35 A for relatively large shielded drum parts,
- 0.4–1.6 ohm for smaller 100-uH parts.

Examples:
- Bourns SRR1050HA-101Y: 100 uH, 1.35 A, max 255 mOhm
- Bourns SRR1005-101K: 100 uH, 680 mA, max 420 mOhm

Sources:
https://www.digikey.jp/ja/products/detail/bourns-inc/SRR1050HA-101Y/16883864
https://www.digikey.jp/ja/products/detail/bourns-inc/SRR1005-101K/419252

They are useful fixed inductors but do not provide the independent orthogonal DC-control winding needed for MAG43.
No catalog variable-inductor part was found that directly replaces the custom magnetic element.

Therefore custom magnetics remains the largest manufacturability risk.

## 10. First-unit cost screen after R27
Known / semi-known one-off cost anchors before tax:

- E25/13/7 core set + bobbin: roughly several hundred JPY
- 100 / 180 / 680-nF X2 bank: ~JPY360–400
- two ALQ312 relays: ~JPY406
- small MCU: ~JPY80–100
- H-bridge: ~JPY130–150
- LinkSwitch-TN2 IC: ~JPY130–150

Named functional subtotal is roughly **JPY1,500–1,800 class** before:
- offline-buck support components,
- copper wire / winding labor,
- fuse / surge / discharge protection,
- sensing front end,
- passive HF absorber,
- PCB,
- assembly,
- tax,
- shipping.

Conclusion:
**JPY3,500 is still possible only if the custom winding and PCB/assembly/shipping are unusually inexpensive.**
The architecture is no longer obviously impossible on raw component cost, but first-unit all-in cost remains tight.

## 11. Architecture decision after R27
### PRIMARY LOW-COST POWER PATH
Non-isolated appliance-style offline buck, entire control domain treated as hazardous-live.

### PRIMARY RELAY
Panasonic ALQ312-class 12-V 200-mW relay instead of the more expensive previous G5Q anchor.

### HOLD
Encapsulated isolated AC/DC module:
- technically simpler,
- safety partition clearer,
- but likely too expensive for the YK66 first-unit target.

### HARD REQUIREMENT
Housekeeping-supply self-noise must be included in the YK66 noise-reduction metric.

## R28 gate
R28 must stop treating YK66 subcircuits separately and create a system-level conducted-noise model containing:
1. household Thevenin source / frequency-dependent grid impedance,
2. MAG43 resonant shunt,
3. two-relay X2 coarse bank,
4. passive >50-kHz HF absorber,
5. 66-kHz-class offline supply current injection and harmonics,
6. MCU / H-bridge magnetic-bias state,
7. component tolerances and Rtotal,
8. 0.1 / 0.5 / 1 / 3 / 6-ohm source cases.

Pass criteria:
- net line noise decreases, not merely the external-noise component,
- no large new 66-kHz / harmonic peaks,
- realistic-grid dominant noise gets useful attenuation,
- hard-source case remains stable and current-limited,
- total component architecture still has a credible <=JPY3,500 path.

No AC100V fabrication or energization is authorized by R27.
