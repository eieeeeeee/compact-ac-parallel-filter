#!/usr/bin/env python3
from pathlib import Path
import sys, uuid
p=Path(sys.argv[1]); s=p.read_text(encoding="utf-8")
NS=uuid.UUID("53f3ce8e-1a1d-4eb5-a5e4-c8fcb85ab317")
def uid(label): return str(uuid.uuid5(NS,label))
def seg(label,a,b,net,layer="F.Cu",width=0.1):
    return f'''\n\t(segment
\t\t(start {a[0]} {a[1]})
\t\t(end {b[0]} {b[1]})
\t\t(width {width})
\t\t(locked yes)
\t\t(layer "{layer}")
\t\t(net "{net}")
\t\t(uuid "{uid("seg:"+label)}")
\t)\n'''
def via(label,xy,net):
    return f'''\n\t(via
\t\t(at {xy[0]} {xy[1]})
\t\t(size 0.45)
\t\t(drill 0.2)
\t\t(layers "F.Cu" "B.Cu")
\t\t(locked yes)
\t\t(net "{net}")
\t\t(uuid "{uid("via:"+label)}")
\t)\n'''
new=[]
# Q101_GATE: F -> B -> F
qf1=[(12.6,22.9675),(13.05,22.9675),(13.4,23.3)]
for i,(a,b) in enumerate(zip(qf1,qf1[1:])): new.append(seg(f"qf1-{i}",a,b,"Q101_GATE"))
new.append(via("q-v1",(13.4,23.3),"Q101_GATE"))
new.append(seg("qb",(13.4,23.3),(15.65,23.3),"Q101_GATE","B.Cu"))
new.append(via("q-v2",(15.65,23.3),"Q101_GATE"))
qf2=[(15.65,23.3),(15.5,23.15),(15.5,23.125)]
for i,(a,b) in enumerate(zip(qf2,qf2[1:])): new.append(seg(f"qf2-{i}",a,b,"Q101_GATE"))

# D201.2 3V3: F -> B -> F
df1=[(33.8425,30.25),(33.75,30.25),(33.7,30.2),(33.5,30.2),(33.2,29.9)]
for i,(a,b) in enumerate(zip(df1,df1[1:])): new.append(seg(f"df1-{i}",a,b,"3V3"))
new.append(via("d-v1",(33.2,29.9),"3V3"))
db=[(33.2,29.9),(32.4,29.9),(32.15,29.65),(31.9,29.65),(31.65,29.4),(31.55,29.4),(31.1,28.95)]
for i,(a,b) in enumerate(zip(db,db[1:])): new.append(seg(f"db-{i}",a,b,"3V3","B.Cu"))
new.append(via("d-v2",(31.1,28.95),"3V3"))
df2=[(31.1,28.95),(30.55,29.5),(30.55,29.55),(30.5,29.6),(30.5,29.7),(30.45,29.75),(30.45,29.8),(30.4,29.85),(30.4,29.9),(30.35,29.95),(30.35,30.0),(30.305,30.08)]
for i,(a,b) in enumerate(zip(df2,df2[1:])): new.append(seg(f"df2-{i}",a,b,"3V3"))

anchor=s.find("\n\t(zone")
if anchor<0: raise SystemExit("zone anchor missing")
s=s[:anchor]+"".join(new)+s[anchor:]
if s.count("(")!=s.count(")"): raise SystemExit("paren mismatch")
p.write_text(s,encoding="utf-8")
print("CONNECT2_GND045_ADDED",len(new))
