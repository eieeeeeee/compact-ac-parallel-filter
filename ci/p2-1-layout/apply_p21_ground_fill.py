#!/usr/bin/env python3
import sys,math
from pathlib import Path
import pcbnew

PCB=Path(sys.argv[1]).resolve()
OUT=Path(sys.argv[2]).resolve()
b=pcbnew.LoadBoard(str(PCB))
gnd=b.GetNetsByName()["GND"]

def vv(points):
    v=pcbnew.VECTOR_VECTOR2I()
    for x,y in points: v.append(pcbnew.VECTOR2I_MM(x,y))
    return v

def add_zone(name,pts):
    z=pcbnew.ZONE(b)
    z.SetLayer(pcbnew.F_Cu)
    z.SetNetCode(gnd.GetNetCode())
    z.SetZoneName(name)
    z.SetLocalClearance(pcbnew.FromMM(0.20))
    z.SetMinThickness(pcbnew.FromMM(0.20))
    try:
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        z.SetThermalReliefGap(pcbnew.FromMM(0.25))
        z.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.30))
    except Exception:
        pass
    z.AddPolygon(vv(pts)); b.Add(z)

# Keep the switching cell and first LC section free of top-layer ground pour.
# Lower control/analog area gets one continuous top-side return fill.
add_zone("P21_F_GND_LOWER",[(0.50,12.00),(49.50,12.00),(49.50,39.50),(0.50,39.50)])
# Right-upper passive/monitor area can also carry quiet ground; stop before LC.
add_zone("P21_F_GND_UPPER_RIGHT",[(31.00,0.50),(49.50,0.50),(49.50,12.00),(31.00,12.00)])

# Geometry helpers for safe stitching-via placement.
fps=list(b.GetFootprints())
pad_xy=[]
for fp in fps:
    for p in fp.Pads():
        q=p.GetPosition()
        pad_xy.append((pcbnew.ToMM(q.x),pcbnew.ToMM(q.y)))

tracks=[]
for t in b.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA): continue
    try:
        a=t.GetStart(); c=t.GetEnd()
        tracks.append((pcbnew.ToMM(a.x),pcbnew.ToMM(a.y),pcbnew.ToMM(c.x),pcbnew.ToMM(c.y)))
    except Exception:
        pass

def dist_seg(px,py,x1,y1,x2,y2):
    dx=x2-x1; dy=y2-y1
    if dx==0 and dy==0: return math.hypot(px-x1,py-y1)
    u=((px-x1)*dx+(py-y1)*dy)/(dx*dx+dy*dy)
    u=max(0,min(1,u)); x=x1+u*dx; y=y1+u*dy
    return math.hypot(px-x,py-y)

def safe(x,y):
    if x<0.9 or x>49.1 or y<0.9 or y>39.1: return False
    # Only stitch where F.Cu GND zone exists.
    in_lower=(12.0<=y<=39.5 and 0.5<=x<=49.5)
    in_upper=(0.5<=y<=12.0 and 31.0<=x<=49.5)
    if not (in_lower or in_upper): return False
    if any(math.hypot(x-px,y-py)<0.85 for px,py in pad_xy): return False
    if any(dist_seg(x,y,*s)<0.55 for s in tracks): return False
    for fp in fps:
        bb=fp.GetBoundingBox()
        x0=pcbnew.ToMM(bb.GetX())-0.35; y0=pcbnew.ToMM(bb.GetY())-0.35
        x1=pcbnew.ToMM(bb.GetRight())+0.35; y1=pcbnew.ToMM(bb.GetBottom())+0.35
        if x0<=x<=x1 and y0<=y<=y1: return False
    return True

added=[]
for y in [13.0,17.0,21.0,25.0,29.0,33.0,37.0]:
    for x in [2.0,6.0,10.0,14.0,18.0,22.0,26.0,30.0,34.0,38.0,42.0,46.0,48.0]:
        if not safe(x,y): continue
        v=pcbnew.PCB_VIA(b)
        v.SetPosition(pcbnew.VECTOR2I_MM(x,y))
        v.SetViaType(pcbnew.VIATYPE_THROUGH)
        v.SetWidth(pcbnew.FromMM(0.60))
        v.SetDrill(pcbnew.FromMM(0.30))
        v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu)
        v.SetNetCode(gnd.GetNetCode())
        v.SetLocked(True)
        b.Add(v); added.append((x,y))

for y in [2.0,6.0,10.0]:
    for x in [32.0,36.0,40.0,44.0,48.0]:
        if not safe(x,y): continue
        v=pcbnew.PCB_VIA(b)
        v.SetPosition(pcbnew.VECTOR2I_MM(x,y))
        v.SetViaType(pcbnew.VIATYPE_THROUGH)
        v.SetWidth(pcbnew.FromMM(0.60))
        v.SetDrill(pcbnew.FromMM(0.30))
        v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu)
        v.SetNetCode(gnd.GetNetCode())
        v.SetLocked(True)
        b.Add(v); added.append((x,y))

b.BuildConnectivity()
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(OUT),b)
print(f"P2.1 F.Cu ground fill + stitching vias={len(added)}")
print(added)
