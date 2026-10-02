#!/usr/bin/env python3
import sys
from pathlib import Path
import pcbnew

PCB=Path(sys.argv[1]).resolve()
b=pcbnew.LoadBoard(str(PCB))
fps={fp.GetReference():fp for fp in b.GetFootprints()}

REFS=[
 "U2","R201","R202","R203","R204","R205","R206","R210","R211",
 "C201","C203","C204","C210","C211","C220","C221","D201",
 "U3","R313","R314","C313","C314",
 "U1"
]
PREFIXES=("VLINE_","ISENSE_")

def xy(p):
 q=p.GetPosition()
 return pcbnew.ToMM(q.x),pcbnew.ToMM(q.y)

print("=== P2.1 ANALOG PAD AUDIT ===")
for ref in REFS:
 fp=fps.get(ref)
 if not fp:
  print("MISSING",ref); continue
 x,y=pcbnew.ToMM(fp.GetPosition().x),pcbnew.ToMM(fp.GetPosition().y)
 print(f"REF {ref} fp=({x:.4f},{y:.4f}) rot={fp.GetOrientationDegrees():.1f}")
 for p in fp.Pads():
  n=p.GetNetname()
  if n and (n.startswith(PREFIXES) or ref in ("U2","U3","R201","R202","R203","R204","R205","R206","R210","R211","C201","C203","C204","C210","C211","C220","C221","D201","R313","R314","C313","C314")):
   px,py=xy(p)
   print(f" PAD {ref}.{p.GetNumber()} net={n} xy=({px:.4f},{py:.4f})")

print("=== ANALOG NET MEMBERS ===")
nets=sorted({p.GetNetname() for fp in b.GetFootprints() for p in fp.Pads()
             if p.GetNetname().startswith(PREFIXES)})
for name in nets:
 parts=[]
 for fp in b.GetFootprints():
  for p in fp.Pads():
   if p.GetNetname()==name:
    x,y=xy(p); parts.append(f"{fp.GetReference()}.{p.GetNumber()}@({x:.4f},{y:.4f})")
 print(name+": "+" ".join(parts))
