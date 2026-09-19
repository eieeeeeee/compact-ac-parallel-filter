# Preliminary BOM — v0.1.0-preprototype

**Status:** design-stage BOM only.  
**Prototype manufactured:** no.  
**Mains tested:** no.

| Ref | Part / target specification | Qty | Status | Notes |
|---|---|---:|---|---|
| F1 | Littelfuse **37402500000** | 1 | Selected candidate | 250 mA, time-lag, compact radial fuse |
| C1 | KEMET **R533N410050P0K** / R53 series | 1 | Selected | 1 µF, X2, 310 VAC |
| R1 | 220 kΩ flame-retardant resistor | 1 | Value fixed, exact part TBD | Discharge network |
| R2 | 220 kΩ flame-retardant resistor | 1 | Value fixed, exact part TBD | Discharge network; R1+R2 = 440 kΩ |
| MOV1 | Littelfuse **TMOV14RP140E** | 1 | Selected candidate | Thermally protected MOV |
| LED1 | Small blue LED | 1 | TBD | 3 mm THT or compact SMD under evaluation |
| RLED1 | 47 kΩ mains-rated/flame-retardant resistor | 1 | Preliminary | LED current limiting |
| RLED2 | 47 kΩ mains-rated/flame-retardant resistor | 1 | Preliminary | Splits voltage stress |
| D1 | Reverse protection diode for LED | 1 | TBD | Candidate: 1N4007-class device |
| C2 | 0.1 µF X2 | 0/1 | DNP | Optional measurement comparison only |
| R3/C3 | RC damping network | 0/1 each | DNP | Values to be chosen only if measurements justify it |
| PCB | FR-4 PCB, target ~32 × 28 mm | 1 | Target | Final dimensions depend on layout/safety review |
| Enclosure | Plug-in insulated enclosure, target ~38 × 34 × 27 mm | 1 | TBD | Mechanical and material selection not finalized |

## Notes

### C1

The 1 µF X2 capacitor is the main parallel element. It is expected to dominate PCB volume.

### Discharge network

R1 + R2 are placed in series across C1.

Nominal values:

- C = 1 µF
- Rtotal = 440 kΩ
- RC time constant ≈ 0.44 s

The actual unplugged-voltage decay must be measured on the finished prototype.

### Optional parts

C2 and the RC damping network are intentionally **DNP in the first build** unless a pre-build review identifies a clear reason to fit them.

### CMC

No common-mode choke is planned in the initial direct parallel architecture. A CMC would be reconsidered only if the architecture changes to a pass-through filter with a downstream load path.
