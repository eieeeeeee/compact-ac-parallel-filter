# Simulations

Pre-prototype calculations and transparent model inputs are stored here.

## v0.1

The first dataset compares:

- impedance of 0.1 µF, 0.47 µF, 1 µF and 4 µF capacitor models
- predicted shunt attenuation for several assumed source impedances
- ideal discharge of 1 µF through 440 kΩ
- 60 Hz capacitive current at 100 V RMS

Start with [`v0.1/simulation_assumptions_v0_1.md`](v0.1/simulation_assumptions_v0_1.md) and the [overview image](../images/shunt_filter_simulation_overview_v0_1.png).

These are calculations, not measured product-performance claims. Raw CSV data, the generation script and LTspice-compatible example netlists are included for review and reproduction.

## LTspice v0.1

Editable LTspice analysis files are available in [`ltspice-v0.1/`](ltspice-v0.1/README.md):

- small-signal AC sweep with stepped source impedance
- ideal post-unplug discharge of 1 µF through 440 kΩ

The `.asc` files expose every model assumption as a SPICE directive and can be changed before rerunning the analysis.
