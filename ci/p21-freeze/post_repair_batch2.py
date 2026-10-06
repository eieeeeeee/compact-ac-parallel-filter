#!/usr/bin/env python3
from pathlib import Path
import sys, uuid

p=Path(sys.argv[1])
s=p.read_text(encoding="utf-8")
NS=uuid.UUID("df96179c-cb65-4e72-90f9-25d0ba8e0e2d")

def uid(label): return str(uuid.uuid5(NS,label))

def seg(label,a,b,net,width=0.1,layer="F.Cu"):
    return f'''\n\t(segment
\t\t(start {a[0]} {a[1]})
\t\t(end {b[0]} {b[1]})
\t\t(width {width})
\t\t(locked yes)
\t\t(layer "{layer}")
\t\t(net "{net}")
\t\t(uuid "{uid("seg:"+label)}")
\t)\n'''

def via(label,xy,net="GND",size=0.5,drill=0.3):
    return f'''\n\t(via
\t\t(at {xy[0]} {xy[1]})
\t\t(size {size})
\t\t(drill {drill})
\t\t(layers "F.Cu" "B.Cu")
\t\t(locked yes)
\t\t(net "{net}")
\t\t(uuid "{uid("via:"+label)}")
\t)\n'''

new=[]

# Q101_GATE: escape between Q101 pads, then join D102.1 (same net).
for i,(a,b) in enumerate([
    ((12.6,22.9675),(12.6,22.03)),
    ((12.6,22.03),(14.025,22.03)),
    ((14.025,22.03),(14.025,21.75)),
    ((14.025,21.75),(16.0,21.75)),
]):
    new.append(seg(f"q101-gate-{i}",a,b,"Q101_GATE",0.1))

# D201.2 3V3: route above THERM/VMID congestion into C221.1.
for i,(a,b) in enumerate([
    ((33.8425,30.25),(33.8425,29.45)),
    ((33.8425,29.45),(32.55,29.45)),
    ((32.55,29.45),(32.4,29.3)),
    ((32.4,29.3),(30.9,29.3)),
    ((30.9,29.3),(30.9,29.8)),
    ((30.9,29.8),(30.305,30.08)),
]):
    new.append(seg(f"d201-3v3-{i}",a,b,"3V3",0.1))

# Six F.Cu GND islands with adequate interior margin and L2 overlap.
for i,xy in enumerate([
    (6.974,33.045),
    (35.776,32.250),
    (5.515,30.731),
    (32.581,24.847),
    (9.673,13.350),
    (13.345,13.155),
]):
    new.append(via(f"gnd-island-{i}",xy))

anchor=s.find("\n\t(zone")
if anchor<0: raise SystemExit("zone anchor missing")
s=s[:anchor]+''.join(new)+s[anchor:]
if s.count("(")!=s.count(")"): raise SystemExit("parenthesis mismatch")
p.write_text(s,encoding="utf-8")
print("POST_REPAIR_BATCH2_ADDED",len(new))
