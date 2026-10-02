#!/usr/bin/env python3
import sys,math
from pathlib import Path
import pcbnew

PCB=Path(sys.argv[1]).resolve(); OUT=Path(sys.argv[2]).resolve()
b=pcbnew.LoadBoard(str(PCB))
fps={fp.GetReference():fp for fp in b.GetFootprints()}
nets=b.GetNetsByName()
gnd=nets["GND"]; p33=nets["3V3"]; p12=nets["12V_PROT"]
in2=b.GetLayerID("In2.Cu")

def pad(ref,num):
    for p in fps[ref].Pads():
        if p.GetNumber()==str(num): return p
    raise RuntimeError(f"pad missing {ref}.{num}")

def xy(item):
    p=item.GetPosition(); return pcbnew.ToMM(p.x),pcbnew.ToMM(p.y)

def seg(item,a,c,w=0.25,layer=pcbnew.F_Cu):
    t=pcbnew.PCB_TRACK(b)
    t.SetStart(pcbnew.VECTOR2I_MM(*a)); t.SetEnd(pcbnew.VECTOR2I_MM(*c))
    t.SetWidth(pcbnew.FromMM(w)); t.SetLayer(layer); t.SetNet(item.GetNet()); t.SetLocked(True); b.Add(t)

def via(item,at,diam=0.60,drill=0.30):
    v=pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I_MM(*at))
    v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetWidth(pcbnew.FromMM(diam)); v.SetDrill(pcbnew.FromMM(drill))
    v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu); v.SetNetCode(item.GetNetCode()); v.SetLocked(True); b.Add(v)

def in_plane(net,x,y):
    if net=="12V_PROT":
        ok=(0.50<=x<=27.80 and 0.50<=y<=20.00)
        if 11.20<=x<=18.70 and 3.75<=y<=6.90: ok=False
        return ok
    if net=="3V3":
        return ((0.50<=x<=49.50 and 24.00<=y<=39.50) or
                (29.00<=x<=39.00 and 7.00<=y<=24.00))
    return False

# Existing geometry for candidate screening.
allpads=[]
for fp in fps.values():
    for p in fp.Pads():
        x,y=xy(p); allpads.append((p,x,y))

def dseg(px,py,x1,y1,x2,y2):
    dx=x2-x1; dy=y2-y1
    if abs(dx)+abs(dy)<1e-12: return math.hypot(px-x1,py-y1)
    u=((px-x1)*dx+(py-y1)*dy)/(dx*dx+dy*dy); u=max(0,min(1,u))
    return math.hypot(px-(x1+u*dx),py-(y1+u*dy))

def candidate_for(fp,p):
    px,py=xy(p); fc=xy(fp)
    dx=px-fc[0]; dy=py-fc[1]
    if math.hypot(dx,dy)<0.05: dx,dy=1.0,0.0
    base=math.atan2(dy,dx)
    others=[q for q in allpads if q[0] is not p]
    for r in (0.85,1.05,1.25,1.45):
        for da in (0,math.radians(30),-math.radians(30),math.radians(60),-math.radians(60),math.radians(90),-math.radians(90),math.pi):
            a=base+da; x=px+r*math.cos(a); y=py+r*math.sin(a)
            if not (0.90<=x<=49.10 and 0.90<=y<=39.10): continue
            if not in_plane(p.GetNetname(),x,y): continue
            # Keep via and dogbone clear of other pad centers.
            if any(math.hypot(x-ox,y-oy)<0.75 for _,ox,oy in others): continue
            if any(dseg(ox,oy,px,py,x,y)<0.38 for _,ox,oy in others): continue
            return (x,y)
    return None

added=[]; failed=[]
for fp in fps.values():
    for p in fp.Pads():
        net=p.GetNetname()
        if net not in ("3V3","12V_PROT"): continue
        try:
            if p.IsOnLayer(in2):
                continue
        except Exception:
            pass
        at=candidate_for(fp,p)
        if at is None:
            failed.append((fp.GetReference(),p.GetNumber(),net,xy(p))); continue
        seg(p,xy(p),at,0.30 if net=="3V3" else 0.45)
        via(p,at,0.65 if net=="12V_PROT" else 0.60,0.30)
        added.append((fp.GetReference(),p.GetNumber(),net,at))

# Explicit GND returns remaining outside the quiet F.Cu pour.
def gdrop(ref,num,at,w=0.30):
    p=pad(ref,num)
    if p.GetNetname()!="GND": raise RuntimeError(f"{ref}.{num} not GND")
    seg(p,xy(p),at,w); via(p,at,0.60,0.30)

# C902/C602/C601 local driver/input return chain to an L2 via.
p=pad("C902",2); seg(p,xy(p),(2.20,8.20),0.25); seg(p,(2.20,8.20),xy(pad("C602",2)),0.25)
p2=pad("C602",2); seg(p2,xy(p2),xy(pad("C601",2)),0.30)
# Existing C601 return via at (5.70,5.40) is already present from plane stage.

# U6 local ground pins to C601 return, kept left of GAN_SW.
u11=pad("U6",11); seg(u11,xy(u11),(6.20,6.00),0.35); seg(u11,(6.20,6.00),(5.70,5.40),0.35)
u9=pad("U6",9); seg(u9,xy(u9),(6.20,7.40),0.30); seg(u9,(6.20,7.40),(5.70,5.40),0.30)
# Low-side source exits below the switch keepout to its own low-inductance via.
gdrop("Q602",2,(10.60,7.40),0.80)
# C605 ground is above the switch-node keepout; drop directly to L2.
gdrop("C605",2,(16.70,2.63),0.45)
# Quiet top-left/right option caps not covered by F.Cu GND pour.
gdrop("C620",2,(24.40,1.30),0.25)
gdrop("C614",2,(28.90,2.13),0.25)
gdrop("C310",2,(29.70,10.43),0.25)
# U701 exposed/ground pad gets an explicit L2 return.
gdrop("U701",6,(5.90,11.30),0.30)

b.BuildConnectivity(); pcbnew.ZONE_FILLER(b).Fill(b.Zones()); pcbnew.SaveBoard(str(OUT),b)
print(f"P2.1 power fanout added={len(added)} failed={len(failed)}")
print("ADDED",added)
print("FAILED",failed)
