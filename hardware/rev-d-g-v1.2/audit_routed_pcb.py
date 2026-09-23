#!/usr/bin/env python3
import sys, csv, math, json
import pcbnew
from collections import defaultdict

board=pcbnew.LoadBoard(sys.argv[1])
targets=[
 "GAN_SW","GAN_HB","GAN_F1","GAN_F2","ACTIVE_OUT",
 "INJ_C_NODE","INJ_R_NODE","INJ_LINE",
 "HRTIM_HI_RAW","HRTIM_LI_RAW","GAN_HI","GAN_LI",
 "ISENSE_RAW","ISENSE_ADC","FORCE_SAFE","+12V","+5V","BUCK_SW"
]
stats={n:dict(length_mm=0.0,segments=0,vias=0,widths=[],layers=set(),locked_segments=0) for n in targets}

for item in board.Tracks():
    name=item.GetNetname()
    if name not in stats: continue
    s=stats[name]
    if isinstance(item, pcbnew.PCB_VIA):
        s["vias"]+=1
        continue
    try:
        s["length_mm"]+=pcbnew.ToMM(item.GetLength())
    except Exception:
        a=item.GetStart(); b=item.GetEnd()
        s["length_mm"]+=math.hypot(pcbnew.ToMM(b.x-a.x),pcbnew.ToMM(b.y-a.y))
    s["segments"]+=1
    s["widths"].append(pcbnew.ToMM(item.GetWidth()))
    try: s["layers"].add(board.GetLayerName(item.GetLayer()))
    except Exception: pass
    try:
        if item.IsLocked(): s["locked_segments"]+=1
    except Exception: pass

rows=[]
for n in targets:
    s=stats[n]
    rows.append({
      "net":n,
      "length_mm":round(s["length_mm"],3),
      "segments":s["segments"],
      "vias":s["vias"],
      "min_width_mm":round(min(s["widths"]),3) if s["widths"] else "",
      "max_width_mm":round(max(s["widths"]),3) if s["widths"] else "",
      "layers":";".join(sorted(s["layers"])),
      "locked_segments":s["locked_segments"],
    })

out=sys.argv[2] if len(sys.argv)>2 else "route_audit.csv"
with open(out,"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

print("===== ROUTE QUALITY AUDIT =====")
for r in rows:
    print(r)
print("OUTPUT",out)
