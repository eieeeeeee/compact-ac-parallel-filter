# RC18 E27N — Native KiCad verification candidate (NONFAB HOLD)

This public branch contains the **E27N low-voltage 12 V RC18 review candidate**, not a released circuit. Publishing is authorized by the project owner in this chat on 2026-10-15.

- Input source: `RC18_E27N_KICAD17_PIN_TYPE_CANDIDATE_NONFAB_HOLD_20261015.zip`
- Source SHA256: `08f54bf0db5b2b2e6d93e7fb55b135cd289205a46bcc8b98da169ced962b3652`
- E27N change: 17 pin electrical-type fixes in library + 17 corresponding schematic cache records; inherited E26L native design otherwise unchanged.
- Target: KiCad **10.0.6** ERC/DRC, refill, schematic parity, unconnected check using GitHub Actions.
- The script reads the ZIP as a whole and runs KiCad on a temporary working copy, never overwriting the source.
- Artifact: `RC18-E27N-KICAD10-NATIVE-NONFAB-<run_id>`.

**17 release blockers remain open at upload.** 64 PCB FIT items remain unplaced, three package mappings await full verification, and independent hardware safety gates (PRE_VERIFIED, OCP, fail-off) remain unproven. A zero ERC/DRC count cannot authorize ordering, energization or manufacturing.

**HOLD: NO POWER / NO AC / NO ORDER / NO FAB.** Prior 100 V AC wall-filter work in `main` is a separate pre-prototype project and is not validated by this RC18 run.
