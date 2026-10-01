#!/usr/bin/env python3
import sys, json
from pathlib import Path
import pcbnew

pcb = Path(sys.argv[1]).resolve()
ses = Path(sys.argv[2]).resolve()
out = Path(sys.argv[3]).resolve()
pro = Path(sys.argv[4]).resolve()

board = pcbnew.LoadBoard(str(pcb))
before = len(list(board.GetTracks()))
ok = pcbnew.ImportSpecctraSES(board, str(ses))
if not ok:
    raise SystemExit("ImportSpecctraSES failed")
after_import = len(list(board.GetTracks()))

# Freerouting 2.4.1 can leave a few fanout vias that no longer participate
# in the final routed topology after rip-up/optimization.  KiCad 10 correctly
# reports these as via_dangling.  Remove only the four deterministic extras
# observed on the pinned P2 route, matching both net and coordinate.
targets = {
    ("GND", 4.0500, 22.3876),
    ("SW_COMMON", 28.7337, 30.2516),
    ("FAULT_LED_A", 47.0875, 26.0525),
    ("U901_UVLO", 29.6794, 2.4803),
}
removed = []
for item in list(board.GetTracks()):
    if not isinstance(item, pcbnew.PCB_VIA):
        continue
    pos = item.GetPosition()
    x = pcbnew.ToMM(pos.x)
    y = pcbnew.ToMM(pos.y)
    net = item.GetNetname()
    for target in list(targets):
        tnet, tx, ty = target
        if net == tnet and abs(x-tx) <= 0.02 and abs(y-ty) <= 0.02:
            board.Remove(item)
            removed.append((net, x, y))
            targets.remove(target)
            break

if len(removed) != 4 or targets:
    raise SystemExit(f"dangling-via cleanup mismatch: removed={removed}, remaining_targets={sorted(targets)}")

after_cleanup = len(list(board.GetTracks()))
pcbnew.SaveBoard(str(out), board)

pdata = json.loads(pro.read_text(encoding="utf-8"))
dsj = pdata.setdefault("board", {}).setdefault("design_settings", {})
sev = dsj.setdefault("rule_severities", {})
sev["unconnected_items"] = "error"
dsj.setdefault("rules", {})["min_clearance"] = 0.10
for nc in pdata.setdefault("net_settings", {}).setdefault("classes", []):
    if nc.get("name") == "Default":
        nc["clearance"] = 0.10
        nc["track_width"] = 0.20
pdata["meta"]["filename"] = pro.name
pro.write_text(json.dumps(pdata, indent=2) + "\n", encoding="utf-8")

print(f"tracks_before={before} tracks_after_import={after_import} imported_delta={after_import-before}")
print(f"removed_dangling_vias={removed}")
print(f"tracks_after_cleanup={after_cleanup}")
print("unconnected_items=error")
print(f"out={out}")
