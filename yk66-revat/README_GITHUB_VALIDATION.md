# YK66 Rev.AT — KiCad 10.0.6 native ERC/DRC validation

**Research candidate only — NOT FOR FAB / NOT FOR MAINS / NOT PSE APPROVED.**

- Original scope: flat two-layer 60 × 50 mm PCB candidate, 15 electronic parts plus a **provisional** plug terminal.
- Rev.AT source is stored in 8 integrity-checked compressed text payload parts under `yk66-revat/payload/`, to accommodate repository connector text-size limits.
- Restore with `python3 yk66-revat/reconstruct.py` (Python 3.10+). This recreates `.kicad_sch`, `.kicad_pcb`, footprints and library tables.
- KiCad UUID values are deterministically remapped while preserving shared identifiers between files; geometry, nets and other serialized text are preserved.
- CI workflow: `.github/workflows/yk66-revat-native.yml` on branch `yk66-revat-native-gate` only. No cron.
- Native reports: ERC, DRC, Unconnected, Schematic parity, with raw JSON stored as GitHub Actions artifacts.
- **A successful native ERC/DRC check cannot demonstrate insulation safety, thermal-fuse response, fuse/MOV protective coordination, valid OEM plug attachment, or PSE compliance.**
- `J1` is a provisional test connector; the physical plug insert and safety dimensions are unresolved.

Original RC18 branches and workflows are intentionally not modified.
