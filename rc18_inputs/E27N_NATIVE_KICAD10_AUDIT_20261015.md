# RC18 E27N — Native KiCad 10.0.6 audit, 2026-10-15 (NONFAB HOLD)

## Provenance
- Branch: `rc18-e27n-native-hold-20261015`
- E27N source ZIP: `RC18_E27N_KICAD17_PIN_TYPE_CANDIDATE_NONFAB_HOLD_20261015.zip`
- Source SHA256: `08f54bf0db5b2b2e6d93e7fb55b135cd289205a46bcc8b98da169ced962b3652`
- Source manifest: **40 / 40 verified**, unchanged before/after; KiCad native command version **10.0.6**.
- Final normalized CI run: https://github.com/eieeeeeee/compact-ac-parallel-filter/actions/runs/38699045972
- Artifact with raw reports and CLI logs: https://github.com/eieeeeeee/compact-ac-parallel-filter/actions/runs/38699045972/artifacts/11955319370

## Native results from final CI run

| Check | Exact result |
|---|---|
| ERC | **2 errors, 3 warnings** |
| Schematic footprint warnings | **U1302, U1005, U1003** have unresolved/empty footprint library IDs |
| ERC unconnected pin errors | **U1005 pin 3 (Q_N)**; **U1006 pin 1 (NC)** |
| PCB geometric/rule violations | **0 reported DRC violations** |
| PCB unconnected pads | **3** |
| PCB schematic-parity issues | **66** |
| PCB missing footprints | **64** |
| Other parity differences | **R304 value mismatch** and **R304 Exclude-from-BOM mismatch** |
| Overall Native verification exit | **FAIL/HOLD**; all ERC and DRC commands return code 5 |

### Unconnected PCB paths
- **SW_SOURCE**: R304 pad 2 to existing F.Cu track end
- **R302_KELVIN_N**: R302 pad 2 to Q301 pad 3
- **TEST_A**: existing B.Cu track end to Q302 pad 3

### Important boundaries
- The earlier 117 DRC warnings and 178+ ERC warnings were largely due to the runner lacking a KiCad global footprint table; correcting the **runner's library setup** removed those environment-related warnings without changing source KiCad files.
- A geometric DRC count of zero **does not imply ERC/parity/footprint/unconnected PASS**.
- This branch uses an **unmodified E27N candidate ZIP**; no source schematic or PCB revisions were made by the CI audit.
- The original 17 release-stop entries remain tracked and **none is formally cleared** by this run. The "native CLI unavailable" technical obstacle is overcome, but native-zero, exact pad/net parity, safety, and manufacturing evidence are not.
- 64 FIT items remain unplaced. Independent PRE_VERIFIED high-source, overcurrent protection, startup faults, fail-off, and 41-requirement performance remain unverified.

**HOLD_NO_POWER / NO_AC / NO_ORDER / NO_FAB.**
