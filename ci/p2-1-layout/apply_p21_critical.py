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
# Existing critical copper is locked so the remaining autorouter may not rip it.
# ---------------------------------------------------------------------------

# 7 V local driver supply / bootstrap source.
route("D601",1,"C601",1,0.30,mids=[(3.10,4.15),(3.05,4.15)],label="7V bootstrap source")
route("C601",1,"U6",1,0.30,mids=[(3.05,4.15),(7.00,4.15)],label="U6 7V local decoupling")
route("C602",1,"C601",1,0.25,mids=[(2.25,7.80),(2.25,4.15),(3.05,4.15)],label="U6 100n 7V local")

# Bootstrap loop.
route("D601",2,"C604",1,0.25,label="bootstrap diode to Cboot")
route("C604",1,"U6",3,0.20,mids=[(7.725,3.30),(8.00,3.30)],label="HB_BOOT")
route("C604",2,"U6",5,0.20,mids=[(9.275,3.30),(9.00,3.30)],label="Cboot switch return")

# High-side gate.  Enter the tiny gate copper from the side away from source.
route("U6",4,"R603",1,0.20,mids=[(8.50,1.35),(12.625,1.35)],label="HO_DRV")
r603=pad("R603",2)
p=xy(r603)
pts=[p,(10.70,2.30),(10.70,5.30),(12.60,5.30),(12.60,4.98)]
for aa,bb in zip(pts,pts[1:]): seg(r603,aa,bb,0.20)
log.append(("Q601_G","R603","2","Q601 landing","1",0.20,len(pts)-1))

# Low-side gate.  Route below the driver input resistor corridor, then approach
# the gate from above (opposite Q602 source).
route("U6",10,"R604",1,0.20,
      mids=[(7.00,7.80),(9.40,7.80),(9.40,10.40),(12.625,10.40)],
      label="LO_DRV")
r604=pad("R604",2)
p=xy(r604)
pts=[p,(10.20,9.00),(10.20,5.55),(11.80,5.55),(11.80,6.02)]
for aa,bb in zip(pts,pts[1:]): seg(r604,aa,bb,0.10)
log.append(("Q602_G","R604","2","Q602 landing","1",0.10,len(pts)-1))

# Driver command local high-side series resistor.
route("R601",2,"U6",7,0.20,label="SI_HI_DRV")

# GAN_SW: U6 HS sense enters the upper/source side of Q601.  The commutation
# trunk then goes right, down to Q602 drain, and straight to L601.
u6hs=pad("U6",5)
p0=xy(u6hs)
qsrc_land=(12.60,4.42)
pts=[p0,(9.00,3.70),(13.90,3.70),(13.90,4.42),qsrc_land]
for aa,bb in zip(pts,pts[1:]): seg(u6hs,aa,bb,0.20)
qsw=pad("Q601",2)
qlo=pad("Q602",3)
l1=pad("L601",1)
p_qlo=xy(qlo); p_l1=xy(l1)
junction=(14.00,4.42); lower=(14.00,p_qlo[1])
seg(qsw,qsrc_land,junction,0.20)
seg(qsw,junction,lower,0.80)
seg(qsw,lower,p_qlo,0.20)
seg(qsw,junction,(p_l1[0],junction[1]),0.80)
seg(qsw,(p_l1[0],junction[1]),p_l1,0.80)
log.append(("GAN_SW","Q601","2","Q602/L601","3/1",0.80,5))

# Closest 12 V ceramic to high-side drain.
route("C605",1,"Q601",3,0.60,
      mids=[(14.305,3.70),(13.40,3.70),(13.40,4.70)],
      label="12V local halfbridge decoupling")

# Three-stage reconstruction path and local damping branches.
route("L601",2,"L602",1,0.60,label="F1_NODE series")
route("L602",2,"L603",1,0.60,label="F2_NODE series")
route("L601",2,"C611",1,0.40,label="F1 shunt")
route("C611",2,"R611",1,0.40,label="C611_RET")
route("L602",2,"C612",1,0.40,label="F2 shunt")
route("C612",2,"R612",1,0.40,label="C612_RET")
route("L603",2,"C613",1,0.40,label="ACTIVE_OUT shunt")
route("C613",2,"R613",1,0.40,label="C613_RET")

# Injection current path.
route("C301",2,"R301",1,0.60,label="1uF to 4R7")
route("R301",2,"R302",1,0.60,label="4R7 to shunt")

# True Kelvin pair: independent from load-current copper.
route("R302",1,"R311",1,0.15,label="Kelvin P pickup")
route("R311",2,"U3",8,0.15,label="Kelvin P INA input")
route("R302",2,"R312",1,0.15,label="Kelvin N pickup")
route("R312",2,"U3",1,0.15,label="Kelvin N INA input")

# INA296 100 nF supply cap is now on the supply-pin side.
route("C310",1,"U3",6,0.20,label="INA296 local 100n")

# STM32 local VDD decoupling, top/bottom entries only; GND sides will connect
# to the continuous In1 GND plane after routing.
route("C1",1,"U1",48,0.20,label="MCU VDD decouple top-left")
route("C3",1,"U1",24,0.20,label="MCU VDD decouple bottom-right")
route("C4",1,"U1",21,0.20,label="MCU VDD decouple bottom-left")

# TLV9062 local 100 nF supply side.
route("C220",1,"U2",8,0.20,label="VLINE opamp local 100n")

pcbnew.SaveBoard(str(OUT),b)
print(f"P2.1 critical board saved: {OUT}")
print(f"protected route groups={len(log)}")
for x in log: print("ROUTE",x)
