#!/usr/bin/env python3
import sys, pcbnew

def snap(path):
    b=pcbnew.LoadBoard(path)
    out={}
    for fp in b.GetFootprints():
        ref=fp.GetReference()
        if ref.startswith("H"): continue
        pos=fp.GetPosition()
        pads=[]
        for p in fp.Pads():
            pads.append((p.GetNumber(),p.GetNetname(),p.GetPosition().x,p.GetPosition().y,p.GetSize().x,p.GetSize().y,p.GetDrillSize().x,p.GetDrillSize().y))
        out[ref]=(pos.x,pos.y,round(fp.GetOrientationDegrees(),6),tuple(sorted(pads)))
    return out

if len(sys.argv)!=3:
    raise SystemExit("usage: verify_rc18_stage1_equivalence.py rc17.kicad_pcb rc18.kicad_pcb")
a=snap(sys.argv[1]); b=snap(sys.argv[2])
if a.keys()!=b.keys():
    print("REFERENCE SET DIFF", sorted(set(a)^set(b))); raise SystemExit(2)
bad=[]
for ref in sorted(a):
    if a[ref]!=b[ref]: bad.append(ref)
if bad:
    print("NON-EQUIVALENT FOOTPRINT/PAD TOPOLOGY",bad); raise SystemExit(3)
print("STAGE1_EQUIVALENCE PASS",len(a),"functional footprints; pad nets/positions/orientations identical")
