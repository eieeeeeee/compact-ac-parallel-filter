# RC18 E27P — Native ERC 2-pin + PV microamp R304 DNP parity ECO (NONFAB HOLD)

Date 2026-10-15. Source E27N ZIP SHA256 `08f54bf0db5b2b2e6d93e7fb55b135cd289205a46bcc8b98da169ced962b3652`.

Exact design mutations relative to frozen E27N candidate:
1. Sheet 11: add NC at U1005 pin 3 (unused Q_N output), coordinate (172.72, 106.68) mm.
2. Sheet 11: add NC at U1006 pin 1 (component NC), coordinate (172.72, 149.86) mm.
3. PCB R304 footprint value: `100k FIT` → `DNP_PV_MICROAMP`, matching schematic.
4. PCB R304 footprint attr: `smd` → `smd exclude_from_bom`, matching schematic and explicit E25B safety note. Do not physically populate R304.

No other schematic or PCB source fields altered. Manifest recomputed, 40 original listed design artifacts retained. Mutation reversibility checked against E27N exact SHA; these edits do NOT prove electrical safety.

Open work after this ECO: 3 PCB unconnected nets (`SW_SOURCE`, `R302_KELVIN_N`, `TEST_A`), 64 unplaced FIT components, three unresolved package footprint IDs (U1003/U1005/U1302), missing PRE_VERIFIED producer and independent OCP/fail-off behavior. 17 release-stop categories remain OPEN pending independent formal evidence, even if native ERC 0 / DRC geometric 0 / one parity delta reduced.

All E27N and E27P candidates are 12V isolated LOW VOLTAGE FIRST PROTOTYPE ONLY; never test on AC mains, never energize or fabricate from this revision.
