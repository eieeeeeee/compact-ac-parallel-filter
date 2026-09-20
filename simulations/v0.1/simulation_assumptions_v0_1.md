# Simulation v0.1 — assumptions and interpretation

## Status

These figures are pre-prototype calculations, not measured performance. They are intended to expose the model and invite review before parts are ordered. The final repository will retain these predictions alongside measured results.

## Capacitor impedance model

Each capacitor is represented by an ideal capacitance in series with illustrative ESR and ESL:

| Nominal capacitance | ESR | ESL |
|---:|---:|---:|
| 0.10 µF | 0.15 Ω | 15 nH |
| 0.47 µF | 0.10 Ω | 20 nH |
| 1.00 µF | 0.08 Ω | 25 nH |
| 4.00 µF | 0.06 Ω | 40 nH |

These are transparent engineering assumptions, not guaranteed values for the selected KEMET R53 part. They must be replaced or bounded using measured impedance or manufacturer frequency data.

## Attenuation model

The filter is modeled as a shunt impedance across L-N, driven through a purely resistive Thevenin source impedance of 0.1, 1, 10, or 50 Ω. The predicted voltage ratio is:

`H(f) = Zfilter(f) / (Zsource + Zfilter(f))`

The 50 Ω curve represents a convenient test-fixture condition; it is not a claim that a household outlet has 50 Ω source impedance. Real attenuation depends on wiring, connected equipment, noise-source impedance, placement, and frequency.

## Discharge model

- Supply: 100 V RMS
- Initial capacitor voltage: 141.4 V peak
- C1: 1.0 µF
- Bleeder: 220 kΩ × 2 series = 440 kΩ
- Time constant: 0.44 s
- Ideal exponential discharge: `V(t) = 141.4 exp(-t/0.44)`

Component tolerance, resistor voltage coefficient, interruption timing, and residual source coupling are not included.

## 60 Hz current

The plot uses ideal capacitive current `I = 2πfCV` at 100 V RMS and 60 Hz. It is reactive current, not equivalent to real power consumption.

## Safety scope

Simulation does not establish regulatory compliance or safe construction. Before energized use, the assembled prototype requires enclosure, insulation, strain relief, temperature, abnormal-condition, fuse-clearing, dielectric-strength, and controlled mains-measurement review.
