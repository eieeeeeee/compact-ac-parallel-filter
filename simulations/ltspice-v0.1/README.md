# LTspice simulation v0.1

This folder contains editable LTspice analysis sheets for reproducing two pre-prototype calculations.

## Files

- `shunt_filter_ac_v0_1.asc` — small-signal AC sweep of the 1 µF shunt branch
- `discharge_v0_1.asc` — ideal post-unplug discharge of 1 µF through 440 kΩ

Both files are plain-text LTspice `.asc` sheets. The circuit is defined by visible SPICE directives so that the assumed values can be reviewed and edited directly.

## 1. AC sweep

Open `shunt_filter_ac_v0_1.asc`, click **Run**, and plot:

```text
dB(V(vout)/V(vin))
```

The source resistance is stepped through:

```text
0.1 Ω, 1 Ω, 10 Ω, 50 Ω
```

The capacitor model is:

```text
C = 1 µF
ESR = 0.08 Ω
ESL = 25 nH
```

These ESR and ESL values are illustrative assumptions, not guaranteed KEMET R53 data. Replace them with measured impedance or manufacturer frequency data when available.

The 50 Ω curve is a repeatable test-fixture case. It does not mean that a household outlet has 50 Ω source impedance. Real attenuation depends on the noise source impedance, house wiring, connected equipment, placement and frequency.

The fuse, TMOV and LED branch are omitted from this linear small-signal model. Their primary roles are protection and indication; the MOV is normally non-conductive at the AC test amplitude.

## 2. Discharge

Open `discharge_v0_1.asc`, click **Run**, and plot:

```text
V(cap)
```

Nominal model:

- initial voltage: 141.421 V, equal to the peak of 100 V RMS
- C1: 1 µF
- Rbleed: 440 kΩ
- time constant: 0.44 s
- predicted crossing of 60 V: approximately 0.377 s
- predicted voltage at 1 s: approximately 14.6 V

The model is ideal and does not include component tolerance, resistor voltage coefficient, interruption phase, instrument loading or external coupling.

## Scope and safety

These files are simulations only. They do not demonstrate EMI performance, surge protection, regulatory compliance or safe mains construction. The hardware remains unbuilt and untested on mains.
