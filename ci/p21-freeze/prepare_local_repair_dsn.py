#!/usr/bin/env python3
import sys
from pathlib import Path
import pcbnew

pcb=Path(sys.argv[1]).resolve()
dsn=Path(sys.argv[2]).resolve()
b=pcbnew.LoadBoard(str(pcb))

# Only these three congested repair windows may move.
BOXES=[
    (9.5,18.5,19.0,25.5),   # Q101 / BRANCH / ISENSE / 12V input
    (29.5,38.5,26.0,34.0),  # D201 / VLINE / analog
    (3.5,9.5,28.0,36.0),    # X1 / HSE DNP option
]

def inside(x,y):
    x/=1e6; y/=1e6
    return any(x0<=x<=x1 and y0<=y<=y1 for x0,x1,y0,y1 in BOXES)

locked=unlocked=0
for item in b.GetTracks():
    allow=False
    if isinstance(item, pcbnew.PCB_VIA):
        p=item.GetPosition()
        allow=inside(p.x,p.y)
    else:
        a=item.GetStart(); c=item.GetEnd()
        allow=inside(a.x,a.y) or inside(c.x,c.y)
    item.SetLocked(not allow)
    if allow: unlocked+=1
    else: locked+=1

pcbnew.SaveBoard(str(pcb),b)
if not pcbnew.ExportSpecctraDSN(b,str(dsn)):
    raise SystemExit("ExportSpecctraDSN failed")
print(f"LOCAL_REPAIR_DSN locked={locked} unlocked={unlocked}")
print(dsn)
