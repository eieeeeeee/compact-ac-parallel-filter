#!/usr/bin/env python3
import sys
from pathlib import Path
import pcbnew

PCB=Path(sys.argv[1]).resolve()
OUT=Path(sys.argv[2]).resolve()
b=pcbnew.LoadBoard(str(PCB))

def vv(points):
    v=pcbnew.VECTOR_VECTOR2I()
    for x,y in points:
        v.append(pcbnew.VECTOR2I_MM(x,y))
    return v

gnd=b.GetNetsByName()["GND"]
in1=b.GetLayerID("In1.Cu")
fps={fp.GetReference():fp for fp in b.GetFootprints()}

def pad(ref,num):
    for p in fps[ref].Pads():
        if p.GetNumber()==str(num):
            return p
    raise RuntimeError(f"pad missing {ref}.{num}")

def xy(item):
    p=item.GetPosition()
    return pcbnew.ToMM(p.x),pcbnew.ToMM(p.y)

def add_gnd_stitch(ref,num,at,w=0.30,diam=0.60,drill=0.30):
    p=pad(ref,num)
    if p.GetNetname()!="GND":
        raise RuntimeError(f"{ref}.{num} is {p.GetNetname()}, expected GND")
    t=pcbnew.PCB_TRACK(b)
    t.SetStart(p.GetPosition())
    t.SetEnd(pcbnew.VECTOR2I_MM(at[0],at[1]))
    t.SetWidth(pcbnew.FromMM(w))
    t.SetLayer(pcbnew.F_Cu)
    t.SetNet(gnd)
    t.SetLocked(True)
    b.Add(t)
    v=pcbnew.PCB_VIA(b)
    v.SetPosition(pcbnew.VECTOR2I_MM(at[0],at[1]))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    v.SetWidth(pcbnew.FromMM(diam))
    v.SetDrill(pcbnew.FromMM(drill))
    v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu)
    v.SetNetCode(gnd.GetNetCode())
    v.SetLocked(True)
    b.Add(v)
    print(f"GND stitch {ref}.{num} {xy(p)} -> {at}")

# L2: near-continuous GND plane.  Keep 0.50 mm off the 50 x 40 mm edge.
z=pcbnew.ZONE(b)
z.SetLayer(in1)
z.SetNetCode(gnd.GetNetCode())
z.SetZoneName("P21_L2_GND")
z.SetLocalClearance(pcbnew.FromMM(0.20))
z.SetMinThickness(pcbnew.FromMM(0.20))
try:
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    z.SetThermalReliefGap(pcbnew.FromMM(0.25))
    z.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.30))
except Exception:
    pass
z.AddPolygon(vv([(0.50,0.50),(49.50,0.50),(49.50,39.50),(0.50,39.50)]))
b.Add(z)

# High-dv/dt switch-node keepout on L2 only.
# Covers Q601/Q602 commutation copper and the GAN_SW fanout into L601.
ko=pcbnew.ZONE(b)
ko.SetLayer(in1)
ko.SetIsRuleArea(True)
ko.SetZoneName("P21_GAN_SW_L2_KEEPOUT")
ko.SetDoNotAllowZoneFills(True)
ko.AddPolygon(vv([(11.20,3.75),(18.70,3.75),(18.70,6.90),(11.20,6.90)]))
b.Add(ko)

# Critical GND drops into the L2 plane.  Keep the driver return local,
# give each LC shunt its own low-inductance return, and ground INA296 locally.
for args in [
    ("C601",2,(5.70,5.40)),
    ("C602",2,(5.60,7.80)),
    ("U6",9,(8.50,3.70)),
    ("R611",2,(17.175,11.00)),
    ("R612",2,(21.675,11.00)),
    ("R613",2,(26.175,11.00)),
    ("C310",2,(30.50,12.80)),
    ("U3",2,(38.00,12.325)),
    ("U3",4,(38.00,11.025)),
    ("U1",19,(14.25,37.70)),
    ("U1",23,(16.25,37.70)),
    ("U1",35,(19.05,30.45)),
    ("U1",47,(10.85,28.54)),
]:
    add_gnd_stitch(*args)

b.BuildConnectivity()
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(OUT),b)
print("P2.1 plane stage: L2 GND plane + GAN_SW keepout filled")
