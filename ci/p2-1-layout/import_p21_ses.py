#!/usr/bin/env python3
import sys,json
from pathlib import Path
import pcbnew

pcb=Path(sys.argv[1]).resolve()
ses=Path(sys.argv[2]).resolve()
out=Path(sys.argv[3]).resolve()
pro=Path(sys.argv[4]).resolve()

b=pcbnew.LoadBoard(str(pcb))
before=len(list(b.GetTracks()))
if not pcbnew.ImportSpecctraSES(b,str(ses)):
    raise SystemExit("ImportSpecctraSES failed")
after=len(list(b.GetTracks()))
b.BuildConnectivity()
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(out),b)

p=json.loads(pro.read_text(encoding="utf-8"))
ds=p.setdefault("board",{}).setdefault("design_settings",{})
sev=ds.setdefault("rule_severities",{})
sev["unconnected_items"]="error"
# Existing Q602 gate neck is 0.10 mm; all autorouted tracks use the Default
# 0.20 mm width.  Do not relax default clearance here.
ds.setdefault("rules",{})["min_track_width"]=0.10
p["meta"]["filename"]=pro.name
pro.write_text(json.dumps(p,indent=2)+"\n",encoding="utf-8")
print(f"tracks_before={before} tracks_after={after} delta={after-before}")
print("zones refilled; unconnected_items=error")
