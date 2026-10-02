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

def seg(netitem,a,c,w=0.20,layer=pcbnew.F_Cu):
    t=pcbnew.PCB_TRACK(b)
    t.SetStart(pcbnew.VECTOR2I_MM(a[0],a[1]))
    t.SetEnd(pcbnew.VECTOR2I_MM(c[0],c[1]))
    t.SetWidth(pcbnew.FromMM(w))
    t.SetLayer(layer)
    t.SetNet(netitem.GetNet())
    t.SetLocked(True)
    b.Add(t)

def via(netitem,at,diam=0.60,drill=0.30):
    v=pcbnew.PCB_VIA(b)
    v.SetPosition(pcbnew.VECTOR2I_MM(at[0],at[1]))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    v.SetWidth(pcbnew.FromMM(diam))
    v.SetDrill(pcbnew.FromMM(drill))
    v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu)
    v.SetNet(netitem.GetNet())
    v.SetLocked(True)
    b.Add(v)

def poly(netitem,pts,w=0.20,layer=pcbnew.F_Cu):
    for a,c in zip(pts,pts[1:]):
        seg(netitem,a,c,w,layer)

def b_escape(ref,num,vat,w=0.18):
    p=pad(ref,num)
    seg(p,xy(p),vat,w,pcbnew.F_Cu)
    via(p,vat)
    return p

def assert_net(a_ref,a_pin,b_ref,b_pin):
    a=pad(a_ref,a_pin); z=pad(b_ref,b_pin)
    if a.GetNetname()!=z.GetNetname():
        raise RuntimeError(f"net mismatch {a_ref}.{a_pin}={a.GetNetname()} {b_ref}.{b_pin}={z.GetNetname()}")
    return a,z

# ---------------------------------------------------------------------------
# SI PWM inputs: long runs on B.Cu, only short endpoint escapes on F.Cu.
# Keep them away from the F.Cu gate/output and GAN_SW loops.
# ---------------------------------------------------------------------------
hi,_=assert_net("U1",30,"R601",1)
hi_mcu=(20.50,32.950)
hi_r=(7.00,10.70)
b_escape("U1",30,hi_mcu)
b_escape("R601",1,hi_r)
poly(hi,[hi_mcu,(20.50,24.00),(7.00,24.00),hi_r],0.18,pcbnew.B_Cu)

lo,_=assert_net("U1",31,"R602",1)
lo_mcu=(19.30,32.450)
lo_r=(2.70,10.80)
b_escape("U1",31,lo_mcu)
b_escape("R602",1,lo_r)
poly(lo,[lo_mcu,(19.30,26.00),(2.70,26.00),lo_r],0.18,pcbnew.B_Cu)

# Driver input resistors to U6: short F.Cu approaches from below.
hid,_=assert_net("R601",2,"U6",7)
poly(hid,[xy(hid),(9.40,8.35),(8.50,8.05),xy(pad("U6",7))],0.15,pcbnew.F_Cu)

lod,_=assert_net("R602",2,"U6",8)
poly(lod,[xy(lod),(5.65,8.00),(8.00,8.00),xy(pad("U6",8))],0.15,pcbnew.F_Cu)

# MCU driver-enable command to R606, separate left-edge B.Cu corridor.
en_cmd,_=assert_net("U1",40,"R606",1)
en_mcu=(15.25,27.30)
en_r=(1.20,7.85)
b_escape("U1",40,en_mcu)
b_escape("R606",1,en_r)
poly(en_cmd,[en_mcu,(1.20,27.30),en_r],0.18,pcbnew.B_Cu)

# U6_EN node: R606 -> U6 -> R605.  Keep it local and under the top-left
# power/control region on B.Cu, avoiding the LO_DRV B.Cu diagonal.
uen,_=assert_net("R606",2,"U6",6)
assert_net("U6",6,"R605",1)
uen_r606=(1.20,4.00)
uen_u6=(9.00,6.40)
uen_r605=(15.30,12.80)
b_escape("R606",2,uen_r606)
b_escape("U6",6,uen_u6)
b_escape("R605",1,uen_r605)
poly(uen,[uen_r606,(1.20,3.70),(9.00,3.70),uen_u6],0.18,pcbnew.B_Cu)
poly(uen,[uen_u6,(9.00,3.70),(15.30,3.70),uen_r605],0.18,pcbnew.B_Cu)

b.BuildConnectivity()
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(OUT),b)
print("P2.1 control stage A saved: SI_HI/SI_LO + driver inputs + enable")
