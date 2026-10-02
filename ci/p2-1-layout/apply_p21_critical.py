#!/usr/bin/env python3
import sys
from pathlib import Path
import pcbnew

PCB=Path(sys.argv[1]).resolve()
OUT=Path(sys.argv[2]).resolve()
b=pcbnew.LoadBoard(str(PCB))

fps={fp.GetReference():fp for fp in b.GetFootprints()}

def pad(ref,num):
    for p in fps[ref].Pads():
        if p.GetNumber()==str(num):
            return p
    raise RuntimeError(f"pad missing {ref}.{num}")

def xy(p):
    q=p.GetPosition()
    return pcbnew.ToMM(q.x),pcbnew.ToMM(q.y)

def seg(netpad,a,c,w,layer=pcbnew.F_Cu,lock=True):
    t=pcbnew.PCB_TRACK(b)
    t.SetStart(pcbnew.VECTOR2I_MM(a[0],a[1]))
    t.SetEnd(pcbnew.VECTOR2I_MM(c[0],c[1]))
    t.SetWidth(pcbnew.FromMM(w))
    t.SetLayer(layer)
    t.SetNet(netpad.GetNet())
    try: t.SetLocked(lock)
    except Exception: pass
    b.Add(t)
    return t

def via(netpad,at,diam=0.60,drill=0.30,lock=True):
    v=pcbnew.PCB_VIA(b)
    v.SetPosition(pcbnew.VECTOR2I_MM(at[0],at[1]))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    v.SetWidth(pcbnew.FromMM(diam))
    v.SetDrill(pcbnew.FromMM(drill))
    v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu)
    v.SetNet(netpad.GetNet())
    try: v.SetLocked(lock)
    except Exception: pass
    b.Add(v)
    return v

log=[]
def route(ar,ap,br,bp,w,mids=None,label="",layer=pcbnew.F_Cu):
    a=pad(ar,ap); z=pad(br,bp)
    if a.GetNetname()!=z.GetNetname():
        raise RuntimeError(f"net mismatch {ar}.{ap}={a.GetNetname()} {br}.{bp}={z.GetNetname()}")
    pts=[xy(a)]+(mids or [])+[xy(z)]
    for p,q in zip(pts,pts[1:]): seg(a,p,q,w,layer)
    log.append((label or a.GetNetname(),ar,ap,br,bp,w,len(pts)-1))

def route_to_point(ar,ap,pts,w,label=""):
    a=pad(ar,ap); p0=xy(a); full=[p0]+pts
    for p,q in zip(full,full[1:]): seg(a,p,q,w)
    log.append((label or a.GetNetname(),ar,ap,"POINT","",w,len(full)-1))

# ---------------------------------------------------------------------------
# P2.1 manually protected critical nets.
# Reuse the exact P1 DRC0 routing geometry, translated +2 mm in X for the
# U6/Q601/Q602/C604 cell.  Only the physically critical nets are frozen here.
# ---------------------------------------------------------------------------

# Bootstrap loop: P1 geometry +2 mm X.
route("C604",1,"U6",3,0.20,mids=[(7.725,3.30),(8.00,3.30)],label="HB_BOOT cap-driver")
route("C604",2,"U6",5,0.20,mids=[(9.275,3.30),(9.00,3.30)],label="GAN_SW bootstrap return")

# High-side gate.
route("U6",4,"R603",1,0.20,mids=[(8.50,1.40),(12.625,1.40)],label="HO_DRV")
r603_out=pad("R603",2)
p=xy(r603_out)
hi_gate_land=(12.60,4.98)
hi_pts=[p,(10.70,2.30),(10.70,5.30),(12.60,5.30),hi_gate_land]
for aa,bb in zip(hi_pts,hi_pts[1:]):
    seg(r603_out,aa,bb,0.20)
log.append(("Q601 gate after Rg","R603","2","Q601","1",0.20,len(hi_pts)-1))

# Low-side gate.  Pin 10 is the left-most pad of U6's lower row; never
# cross pins 9..6 on F.Cu.  Escape left, change to B.Cu, then return beside
# R604.  This preserves the future In1.Cu GND plane and avoids SI_HI/EN pads.
lo=pad("U6",10)
r604_in=pad("R604",1)
v1=(6.10,7.40)
v2=(13.70,9.00)
seg(lo,xy(lo),v1,0.20,pcbnew.F_Cu)
via(lo,v1)
seg(lo,v1,v2,0.20,pcbnew.B_Cu)
via(lo,v2)
seg(lo,v2,xy(r604_in),0.20,pcbnew.F_Cu)
log.append(("LO_DRV B.Cu escape","U6","10","R604","1",0.20,3))
r604_out=pad("R604",2)
p=xy(r604_out)
lo_gate_land=(11.80,6.10)
lo_pts=[p,(11.20,9.00),(11.20,6.10),lo_gate_land]
for aa,bb in zip(lo_pts,lo_pts[1:]):
    seg(r604_out,aa,bb,0.10)
log.append(("Q602 gate after Rg","R604","2","Q602","1",0.10,len(lo_pts)-1))

# Low-current U6 HS/switch reference.  P1 DRC0 corridor +2 mm X.
route("U6",5,"Q602",3,0.20,
      mids=[(9.60,4.60),(9.60,5.70),(13.10,5.70),(13.10,6.30)],
      label="GAN_SW driver sense")

# High-current switch node: source/drain commutation plus direct fanout to L601.
qsw=pad("Q601",2)
qlo=pad("Q602",3)
l1=pad("L601",1)
p_qlo=xy(qlo); p_l1=xy(l1)
p_qsw=(12.60,4.42)
junction=(14.00,p_qsw[1])
lower=(14.00,p_qlo[1])
seg(qsw,p_qsw,junction,0.20)
seg(qsw,junction,lower,0.80)
seg(qsw,lower,p_qlo,0.20)
seg(qsw,junction,(p_l1[0],junction[1]),0.80)
seg(qsw,(p_l1[0],junction[1]),p_l1,0.80)
log.append(("GAN_SW commutation+LC fanout","Q601","2","Q602/L601","3/1",0.80,5))

# Three-stage reconstruction path and local damping branches.
route("L601",2,"L602",1,0.60,label="F1 series")
route("L602",2,"L603",1,0.60,label="F2 series")
route("L601",2,"C611",1,0.40,label="F1 shunt C")
route("C611",2,"R611",1,0.40,label="C611 return R")
route("L602",2,"C612",1,0.40,label="F2 shunt C")
route("C612",2,"R612",1,0.40,label="C612 return R")
route("L603",2,"C613",1,0.40,label="ACTIVE_OUT shunt C")
route("C613",2,"R613",1,0.40,label="C613 return R")

# Injection current path.
route("C301",2,"R301",1,0.60,label="1uF to 4R7")
route("R301",2,"R302",1,0.60,label="4R7 to 0R33 shunt")

# True Kelvin pair.  Keep separate from the 0.60-mm load-current copper.
route("R302",1,"R311",1,0.15,label="Kelvin P pickup")
route("R311",2,"U3",8,0.15,label="Kelvin P INA296 IN+")
route("R302",2,"R312",1,0.15,label="Kelvin N pickup")
route("R312",2,"U3",1,0.15,label="Kelvin N INA296 IN-")

pcbnew.SaveBoard(str(OUT),b)
print(f"P2.1 critical board saved: {OUT}")
print(f"protected route groups={len(log)}")
for x in log:
    print("ROUTE",x)
