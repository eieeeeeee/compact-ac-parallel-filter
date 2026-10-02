#!/usr/bin/env python3
import sys
from pathlib import Path
import pcbnew

PCB=Path(sys.argv[1]).resolve()
OUT=Path(sys.argv[2]).resolve()
b=pcbnew.LoadBoard(str(PCB))
fps={fp.GetReference():fp for fp in b.GetFootprints()}
gnd=b.GetNetsByName()["GND"]

def pad(ref,num):
    for p in fps[ref].Pads():
        if p.GetNumber()==str(num):
            return p
    raise RuntimeError(f"pad missing {ref}.{num}")

def xy(item):
    p=item.GetPosition()
    return pcbnew.ToMM(p.x),pcbnew.ToMM(p.y)

def seg(netitem,a,c,w=0.15,layer=pcbnew.F_Cu):
    t=pcbnew.PCB_TRACK(b)
    t.SetStart(pcbnew.VECTOR2I_MM(a[0],a[1]))
    t.SetEnd(pcbnew.VECTOR2I_MM(c[0],c[1]))
    t.SetWidth(pcbnew.FromMM(w))
    t.SetLayer(layer)
    t.SetNet(netitem.GetNet())
    t.SetLocked(True)
    b.Add(t)

def poly(netitem,pts,w=0.15,layer=pcbnew.F_Cu):
    for a,c in zip(pts,pts[1:]): seg(netitem,a,c,w,layer)

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

def assert_net(ar,ap,br,bp):
    a=pad(ar,ap); z=pad(br,bp)
    if a.GetNetname()!=z.GetNetname():
        raise RuntimeError(f"net mismatch {ar}.{ap}={a.GetNetname()} {br}.{bp}={z.GetNetname()}")
    return a,z

def gnd_drop(ref,num,at):
    p=pad(ref,num)
    if p.GetNetname()!="GND": raise RuntimeError(f"{ref}.{num} not GND")
    seg(p,xy(p),at,0.25,pcbnew.F_Cu)
    via(p,at,0.60,0.30)

# ---------------------------------------------------------------------------
# INA296 source-side analog: keep the raw output away from the long MCU runs.
# Escape U3.5 upward, cross above the U3 courtyard on B.Cu, then split locally.
# ---------------------------------------------------------------------------
raw,_=assert_net("U3",5,"R313",1)
assert_net("U3",5,"R314",1)
vraw1=(32.60,9.55)
vraw2=(37.60,7.50)
poly(raw,[xy(pad("U3",5)),vraw1],0.15,pcbnew.F_Cu)
via(raw,vraw1)
poly(raw,[vraw1,(32.60,7.50),vraw2],0.15,pcbnew.B_Cu)
via(raw,vraw2)
poly(raw,[vraw2,xy(pad("R313",1))],0.15,pcbnew.F_Cu)
poly(raw,[vraw2,(39.075,9.70),xy(pad("R314",1))],0.15,pcbnew.F_Cu)

# RC outputs remain local before the long filtered lines leave this island.
adc,_=assert_net("R313",2,"C313",1)
poly(adc,[xy(pad("R313",2)),xy(pad("C313",1))],0.15,pcbnew.F_Cu)
cmp2,_=assert_net("R314",2,"C314",1)
poly(cmp2,[xy(pad("R314",2)),xy(pad("C314",1))],0.15,pcbnew.F_Cu)
gnd_drop("C313",2,(44.60,8.80))
gnd_drop("C314",2,(46.40,10.80))

# ---------------------------------------------------------------------------
# VLINE local analog island.
# ---------------------------------------------------------------------------

# AC coupling resistor to C201.
acin,_=assert_net("R201",2,"C201",1)
# Thread between the 35.83 mm and 37.40 mm passive rows without vias.
poly(acin,[xy(pad("R201",2)),(28.655,36.60),(33.555,36.60),xy(pad("C201",1))],0.15,pcbnew.F_Cu)

# Wide ADC RC node: keep R203-C203 local.  MCU leg is added in stage B.
wide,_=assert_net("R203",2,"C203",1)
# Pass above the C220 pad row on F.Cu; the BUF crossover is moved to B.Cu.
poly(wide,[xy(pad("R203",2)),(28.655,34.90),(33.555,34.90),xy(pad("C203",1))],0.15,pcbnew.F_Cu)
gnd_drop("C203",2,(36.20,35.20))

# Op-amp buffer pins 1/2 are the same net. Join at the package edge, then
# leave below the U2 courtyard toward R203.1.
buf,_=assert_net("U2",1,"U2",2)
assert_net("U2",1,"R203",1)
assert_net("U2",1,"R206",1)
poly(buf,[xy(pad("U2",2)),xy(pad("U2",1))],0.15,pcbnew.F_Cu)
vb1=(34.20,34.45); vb2=(26.50,34.45)
poly(buf,[xy(pad("U2",1)),vb1],0.15,pcbnew.F_Cu)
via(buf,vb1)
poly(buf,[vb1,vb2],0.15,pcbnew.B_Cu)
via(buf,vb2)
poly(buf,[vb2,xy(pad("R203",1))],0.15,pcbnew.F_Cu)
poly(buf,[xy(pad("R203",1)),(26.30,36.60),(26.30,38.20),xy(pad("R206",1))],0.15,pcbnew.F_Cu)

# Fine compensation row: same-net passives are tied directly and compactly.
fout,_=assert_net("R205",1,"C204",1)
fo1=(19.20,38.90); fo2=(23.325,37.80)
poly(fout,[xy(pad("R205",1)),fo1],0.15,pcbnew.F_Cu)
via(fout,fo1)
poly(fout,[fo1,fo2],0.15,pcbnew.B_Cu)
via(fout,fo2)
poly(fout,[fo2,xy(pad("C204",1))],0.15,pcbnew.F_Cu)

# VINM uses a bottom B.Cu lane.  0.60/0.30 mm vias at y=39.20 land
# exactly at the 0.50 mm copper-to-edge manufacturing floor.
fvinm,_=assert_net("R205",2,"C204",2)
assert_net("R205",2,"R204",1)
fv1=(21.825,39.20); fv2=(24.875,39.20); fv3=(29.475,39.20)
poly(fvinm,[xy(pad("R205",2)),fv1],0.15,pcbnew.F_Cu); via(fvinm,fv1,0.60,0.30)
poly(fvinm,[xy(pad("C204",2)),fv2],0.15,pcbnew.F_Cu); via(fvinm,fv2,0.60,0.30)
poly(fvinm,[xy(pad("R204",1)),fv3],0.15,pcbnew.F_Cu); via(fvinm,fv3,0.60,0.30)
poly(fvinm,[fv1,fv2,fv3],0.15,pcbnew.B_Cu)

# Remaining U2/VMID ground stitching is added after the analog signal
# corridors are frozen, so return vias cannot force signal detours.

b.BuildConnectivity()
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(str(OUT),b)
print("P2.1 analog stage A saved: ISENSE source/RC + VLINE local island")
