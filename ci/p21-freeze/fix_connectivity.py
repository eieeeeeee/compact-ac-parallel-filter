#!/usr/bin/env python3
import sys
import pcbnew

P=sys.argv[1]
b=pcbnew.LoadBoard(P)

def mm(x): return pcbnew.FromMM(float(x))
def pt(x,y): return pcbnew.VECTOR2I(mm(x),mm(y))
def same(a,x,y): return a.x==mm(x) and a.y==mm(y)

def net(name):
    n=b.FindNet(name)
    if n is None:
        raise RuntimeError("net not found: "+name)
    return n

def fp(ref):
    for x in b.GetFootprints():
        if x.GetReference()==ref: return x
    raise RuntimeError("footprint not found: "+ref)

def pad(ref,num):
    f=fp(ref)
    for p in f.Pads():
        if p.GetNumber()==str(num): return p
    raise RuntimeError(f"pad {ref}.{num} not found")

def set_pad_net(ref,num,name):
    p=pad(ref,num)
    p.SetNet(net(name))
    print("PAD_NET",ref,num,name,pcbnew.ToMM(p.GetPosition()))

def find_track(name,a,c,layer="F.Cu"):
    aa=pt(*a); cc=pt(*c); lid=b.GetLayerID(layer)
    hits=[]
    for t in b.GetTracks():
        if not isinstance(t,pcbnew.PCB_TRACK): continue
        if t.GetLayer()!=lid or t.GetNetname()!=name: continue
        s=t.GetStart(); e=t.GetEnd()
        if (s==aa and e==cc) or (s==cc and e==aa): hits.append(t)
    if len(hits)!=1:
        raise RuntimeError(f"track {name} {a}->{c} {layer}: {len(hits)} hits")
    return hits[0]

def remove_track(name,a,c,layer="F.Cu"):
    t=find_track(name,a,c,layer)
    b.Remove(t)
    print("REMOVE",name,a,c,layer)

def add_track(name,a,c,width,layer="F.Cu"):
    t=pcbnew.PCB_TRACK(b)
    t.SetStart(pt(*a)); t.SetEnd(pt(*c))
    t.SetWidth(mm(width)); t.SetLayer(b.GetLayerID(layer)); t.SetNet(net(name))
    b.Add(t)
    print("ADD",name,a,c,width,layer)
    return t

def move_fp_with_tracks(ref,newxy):
    f=fp(ref)
    old={p.GetNumber():p.GetPosition() for p in f.Pads()}
    f.SetPosition(pt(*newxy))
    new={p.GetNumber():p.GetPosition() for p in f.Pads()}
    changed=0
    for t in b.GetTracks():
        if isinstance(t,pcbnew.PCB_VIA): continue
        if not isinstance(t,pcbnew.PCB_TRACK): continue
        for n,o in old.items():
            nn=new[n]
            if t.GetStart()==o:
                t.SetStart(nn); changed+=1
            if t.GetEnd()==o:
                t.SetEnd(nn); changed+=1
    print("MOVE_FP",ref,pcbnew.ToMM(f.GetPosition()),"track_ends",changed)

# 1) Q101 physical pin/net parity. Move it out of the BRANCH_EN/ISENSE crossing corridor.
q=fp("Q101")
q.SetPosition(pt(15.5,22.9))
set_pad_net("Q101","1","Q101_GATE")
set_pad_net("Q101","2","12V_REV")
set_pad_net("Q101","3","12V_FUSED")
q1=pcbnew.ToMM(pad("Q101","1").GetPosition())
q2=pcbnew.ToMM(pad("Q101","2").GetPosition())
q3=pcbnew.ToMM(pad("Q101","3").GetPosition())
# Exact existing anchors.
add_track("Q101_GATE",tuple(q1),(15.5,24.25),0.15)
add_track("12V_REV",tuple(q2),(16.525,24.6),0.35)
# Split the long 12V_FUSED run at x=15.5 and connect drain to the split point.
remove_track("12V_FUSED",(20.25,22.75),(10.0,22.75))
add_track("12V_FUSED",(10.0,22.75),(15.5,22.75),0.35)
add_track("12V_FUSED",(15.5,22.75),(20.25,22.75),0.35)
add_track("12V_FUSED",tuple(q3),(15.5,22.75),0.35)

# 2) D201 BAT54S physical pins: 1=LOW/GND, 2=HIGH/3V3, 3=SIG/VLINE_BIAS.
set_pad_net("D201","1","GND")
set_pad_net("D201","2","3V3")
set_pad_net("D201","3","VLINE_BIAS")
# Reroute only the VLINE_FINE_VINM portion that crossed pad 1.
for a,c in [
    ((32.75,28.0),(33.0,28.25)),
    ((33.0,28.25),(33.25,28.5)),
    ((33.25,28.5),(33.5,28.75)),
    ((33.5,28.75),(33.75,29.0)),
]:
    remove_track("VLINE_FINE_VINM",a,c)
for a,c in [
    ((32.75,28.0),(32.75,27.25)),
    ((32.75,27.25),(34.75,27.25)),
    ((34.75,27.25),(34.75,29.0)),
    ((34.75,29.0),(33.75,29.0)),
]:
    add_track("VLINE_FINE_VINM",a,c,0.12)

# 3) X1 remains DNP/TBD; preserve logical 1/2 mapping for now, but clear pad 4.
for a,c in [
    ((5.25,33.0),(5.25,31.625)),
    ((5.25,31.625),(5.625,31.25)),
    ((5.625,31.25),(5.625,29.2)),
]:
    remove_track("HSE_PF0",a,c)
for a,c in [
    ((5.25,33.0),(4.35,32.5)),
    ((4.35,32.5),(4.35,30.0)),
    ((4.35,30.0),(5.625,29.2)),
]:
    add_track("HSE_PF0",a,c,0.12)

# 4) R205/C6 real pad-to-pad short: move R205 +0.20 mm in Y and drag attached endpoints.
r=fp("R205")
rpos=pcbnew.ToMM(r.GetPosition())
move_fp_with_tracks("R205",(rpos[0],rpos[1]+0.20))

# 5) Close the explicit R605.2 -> GND via missing connection.
p605=pcbnew.ToMM(pad("R605","2").GetPosition())
add_track("GND",tuple(p605),(17.175,11.0),0.15)

b.BuildConnectivity()
pcbnew.SaveBoard(P,b)
print("CONNECTIVITY_BATCH1_APPLIED")
