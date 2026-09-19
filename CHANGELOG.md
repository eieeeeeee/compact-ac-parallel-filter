# Changelog

All notable design changes should be documented here.

## [0.1.0-preprototype] — 2026-09-19

### Added

- Initial public repository structure
- Pre-prototype safety notice
- Preliminary BOM
- Design notes
- Prototype test plan
- KiCad workspace placeholder
- Measurement workspace placeholder

### Preliminary design target

- 100 V AC, 50/60 Hz
- PCB target: approximately 32 × 28 mm
- enclosure target: approximately 38 × 34 × 27 mm
- C1: 1 µF X2
- discharge network: 220 kΩ + 220 kΩ
- compact 250 mA time-lag fuse
- thermally protected MOV
- low-current blue status LED
- no CMC in the initial parallel-only topology

### Validation status

No physical prototype has been manufactured or mains-tested.


### KiCad Rev.A 32 × 28 mm hardware added

- Added editable KiCad 9 schematic and PCB
- Fixed PCB outline at 32 × 28 mm for the current mechanical study
- Added project-local symbols and footprints
- Placed C1, MOV1 and F1 on the front
- Moved low-power resistors, LED and clamp diode to B.Cu
- Added placement CSV
- Marked J1 as a provisional plug-assembly interface, not a final blade footprint
- Removed C2/RC footprints from this compact revision pending measurements
