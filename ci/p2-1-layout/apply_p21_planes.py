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

b.BuildConnectivity()
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(OUT),b)
print("P2.1 plane stage: L2 GND plane + GAN_SW keepout filled")
