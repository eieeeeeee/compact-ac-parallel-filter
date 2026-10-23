# RC18-Lite Rev.27 — Official KiCad DRC 0 / Unconnected 0

- Validated: 2026-10-22 14:14:57 UTC
- Official KiCad CLI: 10.0.7
- GitHub Actions run: https://github.com/eieeeeeee/compact-ac-parallel-filter/actions/runs/39791403418
- DRC violations: **0**
- Unconnected: **0**
- Exit code: **0**
- Validated corrected board SHA256: `710af374fd54fdae40df21c435d10b9e4e489b096224a8441e405cb257613bda`
- Official artifact: https://github.com/eieeeeeee/compact-ac-parallel-filter/actions/runs/39791403418/artifacts/12432287024

## Rules not checked
The official JSON includes these ignored checks:
`missing_courtyard`, `track_not_centered_on_via`, `tuning_profile_track_geometries`, `footprint_filters_mismatch`, `footprint_type_mismatch`.

## Remaining safety and manufacturing gates
- Actual TMOV14RP175E lead tolerance versus plated-hole pattern.
- J1 AC-input connector and mains plug strain relief / mechanical retention.
- Fuse total-clearing I²t versus 4.7 ohm fusible resistor and MOV fault energy; available short-circuit current.
- Applicable insulation creepage/clearance and enclosure fire/heat requirements.
- Qualified mains safety testing and PSE applicability.
- Schematic/ERC is not provided, so schematic-to-PCB parity is not established.

**PCB DRC PASS. MAINS ENERGIZATION AND FABRICATION RELEASE NOT APPROVED.**
