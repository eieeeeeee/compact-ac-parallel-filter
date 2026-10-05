#!/usr/bin/env python3
import sys
import pcbnew

P=sys.argv[1]
b=pcbnew.LoadBoard(P)

def mm(x): return pcbnew.FromMM(float(x))
def pt(x,y): return pcbnew.VECTOR2I(mm(x),mm(y))

def net(name):
    n=b.FindNet(name)
    if n is None: raise RuntimeError("net not found: "+name)
    return n

def fp(ref):
    for x in b.GetFootprints():
        if x.GetReference()==ref: return x
    raise RuntimeError("footprint not found: "+ref)

def pad(ref,num):
    for p in fp(ref).Pads():
        if p.GetNumber()==str(num): return p
    raise RuntimeError(f"pad {ref}.{num} not found")

def set_pad_net(ref,num,name):
    p=pad(ref,num); p.SetNet(net(name))
    print("PAD_NET",ref,num,name,pcbnew.ToMM(p.GetPosition()))

def find_track(name,a,c,layer="F.Cu"):
    aa=pt(*a); cc=pt(*c); lid=b.GetLayerID(layer); hits=[]
    tol=mm(0.005)
    def near(p,q):
        return abs(p.x-q.x)<=tol and abs(p.y-q.y)<=tol
    candidates=[]
    for t in b.GetTracks():
        if isinstance(t,pcbnew.PCB_VIA): continue
        if not isinstance(t,pcbnew.PCB_TRACK): continue
        if t.GetLayer()!=lid or t.GetNetname()!=name: continue
        ss=t.GetStart(); e=t.GetEnd()
        candidates.append((tuple(pcbnew.ToMM(ss)),tuple(pcbnew.ToMM(e))))
        if (near(ss,aa) and near(e,cc)) or (near(ss,cc) and near(e,aa)): hits.append(t)
    if len(hits)!=1:
        nearby=[x for x in candidates if min(abs(x[0][0]-a[0])+abs(x[0][1]-a[1]),abs(x[1][0]-a[0])+abs(x[1][1]-a[1]))<2.0]
        raise RuntimeError(f"track {name} {a}->{c} {layer}: {len(hits)} hits; nearby={nearby[:12]}")
    return hits[0]

def remove_track(name,a,c,layer="F.Cu"):
    t=find_track(name,a,c,layer); b.Remove(t)
    print("REMOVE",name,a,c,layer)

def add_track(name,a,c,width,layer="F.Cu"):
    t=pcbnew.PCB_TRACK(b)
    t.SetStart(pt(*a)); t.SetEnd(pt(*c))
    t.SetWidth(mm(width)); t.SetLayer(b.GetLayerID(layer)); t.SetNet(net(name))
    b.Add(t); print("ADD",name,a,c,width,layer); return t

def find_via(name,xy):
    q=pt(*xy); hits=[]
    for t in b.GetTracks():
        if not isinstance(t,pcbnew.PCB_VIA): continue
        if t.GetNetname()==name and t.GetPosition()==q: hits.append(t)
    if len(hits)!=1: raise RuntimeError(f"via {name} {xy}: {len(hits)} hits")
    return hits[0]

def remove_via(name,xy):
    v=find_via(name,xy); b.Remove(v); print("REMOVE_VIA",name,xy)

def add_via(name,xy,size=0.5,drill=0.3):
    v=pcbnew.PCB_VIA(b)
    v.SetPosition(pt(*xy)); v.SetWidth(mm(size)); v.SetDrill(mm(drill))
    v.SetLayerPair(b.GetLayerID("F.Cu"),b.GetLayerID("B.Cu"))
    v.SetNet(net(name)); b.Add(v)
    print("ADD_VIA",name,xy,size,drill); return v

def move_fp_with_tracks(ref,newxy):
    f=fp(ref); old={p.GetNumber():p.GetPosition() for p in f.Pads()}
    f.SetPosition(pt(*newxy)); new={p.GetNumber():p.GetPosition() for p in f.Pads()}
    changed=0
    for t in b.GetTracks():
        if isinstance(t,pcbnew.PCB_VIA) or not isinstance(t,pcbnew.PCB_TRACK): continue
        for n,o in old.items():
            nn=new[n]
            if t.GetStart()==o: t.SetStart(nn); changed+=1
            if t.GetEnd()==o: t.SetEnd(nn); changed+=1
    print("MOVE_FP",ref,pcbnew.ToMM(f.GetPosition()),"track_ends",changed)

# ---- Q101 cause group ----
# Keep SOT-23 rotation=90 deg, move so source is close to 12V_REV and drain is clear of D102.
q=fp("Q101")
q.SetPosition(pt(14.9,23.6625))
set_pad_net("Q101","1","Q101_GATE")
set_pad_net("Q101","2","12V_REV")
set_pad_net("Q101","3","12V_FUSED")
q1=tuple(pcbnew.ToMM(pad("Q101","1").GetPosition()))
q2=tuple(pcbnew.ToMM(pad("Q101","2").GetPosition()))
q3=tuple(pcbnew.ToMM(pad("Q101","3").GetPosition()))
print("Q101_PADS",q1,q2,q3)

# Remove the old lower Q101_GATE serpentine; retain the upper run from (15.25,24.625) to R101.
for a,c in [
 ((16.15,22.0),(16.5,22.0)),
 ((16.375,22.125),(16.5,22.0)),
 ((16.375,22.25),(16.375,22.125)),
 ((15.5,23.125),(16.375,22.25)),
 ((15.5,24.25),(15.5,23.125)),
 ((15.375,24.375),(15.5,24.25)),
 ((15.375,24.5),(15.375,24.375)),
 ((15.25,24.625),(15.375,24.5)),
]:
    remove_track("Q101_GATE",a,c)

# Gate: D102 -> below Q101 -> left side of drain -> Q101 gate; also join retained upper gate run.
for a,c in [
 ((16.15,22.0),(16.7,20.9)),
 ((16.7,20.9),(14.3,20.9)),
 ((14.3,20.9),(14.3,24.6)),
 ((14.3,24.6),q1),
 (q1,(15.25,24.625)),
]:
    add_track("Q101_GATE",a,c,0.15)

# Source: short direct join to existing 12V_REV endpoint.
add_track("12V_REV",q2,(16.525,24.6),0.35)

# Drain: drop to B.Cu below the package and join the existing 12V_FUSED backbone.
remove_track("12V_FUSED",(20.25,22.75),(10.0,22.75),"B.Cu")
add_track("12V_FUSED",(10.0,22.75),(14.9,22.75),0.35,"B.Cu")
add_track("12V_FUSED",(14.9,22.75),(20.25,22.75),0.35,"B.Cu")
add_via("12V_FUSED",(14.9,21.5),0.6,0.3)
add_track("12V_FUSED",q3,(14.9,21.5),0.35,"F.Cu")
add_track("12V_FUSED",(14.9,21.5),(14.9,22.75),0.35,"B.Cu")

# BRANCH_EN: move the F/B transition left of Q101 and bypass the former pad-crossing chain.
remove_via("BRANCH_EN",(14.25,22.0))
remove_track("BRANCH_EN",(14.5,21.75),(14.25,22.0),"B.Cu")
for a,c in [
 ((14.25,22.0),(14.0,22.25)),((14.0,22.25),(13.75,22.5)),
 ((13.75,22.5),(13.5,22.75)),((13.5,22.75),(13.25,23.0)),
 ((13.25,23.0),(13.0,23.25)),((13.0,23.25),(12.75,23.5)),
 ((12.75,23.5),(12.5,23.75)),((12.5,23.75),(12.25,24.0)),
 ((12.25,24.0),(12.0,24.25)),((12.0,24.25),(11.75,24.5)),
 ((11.75,24.5),(11.5,24.75)),((11.5,24.75),(11.25,25.0)),
 ((11.25,25.0),(11.0,25.25)),((11.0,25.25),(10.75,25.25)),
]:
    remove_track("BRANCH_EN",a,c)
add_via("BRANCH_EN",(10.5,22.0),0.5,0.3)
for a,c in [
 ((14.5,21.75),(14.5,21.2)),((14.5,21.2),(10.5,21.2)),((10.5,21.2),(10.5,22.0))
]:
    add_track("BRANCH_EN",a,c,0.15,"B.Cu")
add_track("BRANCH_EN",(10.5,22.0),(10.5,25.25),0.15,"F.Cu")
add_track("BRANCH_EN",(10.5,25.25),(10.75,25.25),0.15,"F.Cu")

# ISENSE_COMP2: move transition far left/below Q101, preserving the upstream B.Cu and downstream F.Cu chains.
remove_via("ISENSE_COMP2",(15.25,22.0))
remove_track("ISENSE_COMP2",(15.5,22.0),(15.25,22.0),"B.Cu")
for a,c in [
 ((15.25,22.0),(15.0,22.25)),((15.0,22.25),(14.75,22.5)),
 ((14.75,22.5),(14.5,22.75)),((14.5,22.75),(14.25,23.0)),
 ((14.25,23.0),(14.0,23.25)),((14.0,23.25),(13.75,23.5)),
 ((13.75,23.5),(13.5,23.75)),((13.5,23.75),(13.25,24.0)),
 ((13.25,24.0),(13.0,24.25)),((13.0,24.25),(12.75,24.5)),
 ((12.75,24.5),(12.5,24.75)),((12.5,24.75),(12.25,25.0)),
 ((12.25,25.0),(12.0,25.25)),((12.0,25.25),(11.75,25.5)),
 ((11.75,25.5),(11.5,25.5)),((11.5,25.5),(11.25,25.75)),
]:
    remove_track("ISENSE_COMP2",a,c)
add_via("ISENSE_COMP2",(11.6,21.6),0.5,0.3)
for a,c in [
 ((15.5,22.0),(15.5,20.9)),((15.5,20.9),(11.6,20.9)),((11.6,20.9),(11.6,21.6))
]:
    add_track("ISENSE_COMP2",a,c,0.12,"B.Cu")
add_track("ISENSE_COMP2",(11.6,21.6),(11.6,25.75),0.12,"F.Cu")
add_track("ISENSE_COMP2",(11.6,25.75),(11.25,25.75),0.12,"F.Cu")

# 12V_IN: lower the central run so it clears Q101 drain and the new gate route.
for a,c in [
 ((16.875,20.125),(16.25,20.75)),((16.25,20.75),(11.5,20.75)),((11.5,20.75),(11.0,21.25)),
]:
    remove_track("12V_IN",a,c)
for a,c in [
 ((16.875,20.125),(16.5,20.2)),((16.5,20.2),(10.5,20.2)),((10.5,20.2),(11.0,21.25)),
]:
    add_track("12V_IN",a,c,0.35,"F.Cu")

# ---- D201 / X1 / R205 / R605 closures retained from batch 1 ----
set_pad_net("D201","1","GND")
set_pad_net("D201","2","3V3")
set_pad_net("D201","3","VLINE_BIAS")
for a,c in [
 ((32.75,28.0),(33.0,28.25)),((33.0,28.25),(33.25,28.5)),
 ((33.25,28.5),(33.5,28.75)),((33.5,28.75),(33.75,29.0)),
]:
    remove_track("VLINE_FINE_VINM",a,c)
for a,c in [
 ((32.75,28.0),(32.75,27.25)),((32.75,27.25),(34.75,27.25)),
 ((34.75,27.25),(34.75,29.0)),((34.75,29.0),(33.75,29.0)),
]:
    add_track("VLINE_FINE_VINM",a,c,0.12)

for a,c in [
 ((5.25,33.0),(5.25,31.625)),((5.25,31.625),(5.625,31.25)),((5.625,31.25),(5.625,29.2)),
]:
    remove_track("HSE_PF0",a,c)
for a,c in [
 ((5.25,33.0),(4.35,32.5)),((4.35,32.5),(4.35,30.0)),((4.35,30.0),(5.625,29.2)),
]:
    add_track("HSE_PF0",a,c,0.12)

r=fp("R205"); rpos=pcbnew.ToMM(r.GetPosition())
move_fp_with_tracks("R205",(rpos[0],rpos[1]+0.20))

p605=tuple(pcbnew.ToMM(pad("R605","2").GetPosition()))
add_track("GND",p605,(17.175,11.0),0.15)

b.BuildConnectivity()
pcbnew.SaveBoard(P,b)
print("CONNECTIVITY_Q101_BATCH2_APPLIED")
