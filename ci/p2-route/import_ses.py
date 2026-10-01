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
pcbnew.SaveBoard(str(out), board)

# Full-route gate: connectivity is now enforced by KiCad.
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
print("unconnected_items=error")
print(f"out={out}")
