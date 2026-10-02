#!/usr/bin/env python3
import sys
from pathlib import Path
import pcbnew

PCB=Path(sys.argv[1]).resolve()
b=pcbnew.LoadBoard(str(PCB))
fps={fp.GetReference():fp for fp in b.GetFootprints()}

TARGET_REFS=[
 "U1","U6","R601","R602","R605","R606",
 "U3","R313","R314","C313","C314",
 "U2","R201","R202","R203","R204","R205","R206","C201","C203","C204"
]
TARGET_NETS={
 "SI_HI","SI_HI_DRV","SI_LO","SI_LO_DRV","SI_DRIVER_EN","U6_EN",
 "ISENSE_RAW","ISENSE_ADC_COMP1","ISENSE_COMP2",
 "VLINE_AC_IN","VLINE_BIAS","VLINE_BUF","VLINE_FINE_OUT",
 "VLINE_FINE_VINM","VLINE_FINE_VINP","VLINE_WIDE_ADC"
}

def pos(p):
 q=p.GetPosition()
 return pcbnew.ToMM(q.x),pcbnew.ToMM(q.y)

print("=== P2.1 CONTROL PAD AUDIT ===")
for ref in TARGET_REFS:
 fp=fps.get(ref)
 if not fp:
  print("MISSING",ref); continue
 x,y=pcbnew.ToMM(fp.GetPosition().x),pcbnew.ToMM(fp.GetPosition().y)
 print(f"REF {ref} fp=({x:.4f},{y:.4f}) rot={fp.GetOrientationDegrees():.1f}")
 for p in fp.Pads():
  n=p.GetNetname()
  if n in TARGET_NETS:
   px,py=pos(p)
   print(f" PAD {ref}.{p.GetNumber()} net={n} xy=({px:.4f},{py:.4f})")

print("=== TARGET NET MEMBERS ===")
for name in sorted(TARGET_NETS):
 parts=[]
 for fp in b.GetFootprints():
  for p in fp.Pads():
   if p.GetNetname()==name:
    x,y=pos(p)
    parts.append(f"{fp.GetReference()}.{p.GetNumber()}@({x:.4f},{y:.4f})")
 print(name+": "+" ".join(parts))
