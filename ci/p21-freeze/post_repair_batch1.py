#!/usr/bin/env python3
from pathlib import Path
import sys, uuid

p=Path(sys.argv[1])
s=p.read_text(encoding="utf-8")
NS=uuid.UUID("7e2af0bc-8c6f-4a62-aa03-64d94676b83e")

GND_POINTS=[
(17.8,21.55),(23.2,34.5),(23.8,28.75),(6.5,14.0),(16.2,32.1),
(18.0,13.6),(21.0,32.05),(42.1,15.25),(14.65,24.5),(30.85,24.6),
(35.65,2.15),(42.5,32.05),(31.65,28.4),(16.15,35.6),(12.25,14.2),
(31.3,35.5),(32.0,37.4),(14.188,39.0),(31.7,30.6),(33.55,32.0)
]

def uid(label):
    return str(uuid.uuid5(NS,label))

def via(label,x,y):
    return f'''\n\t(via
\t\t(at {x} {y})
\t\t(size 0.5)
\t\t(drill 0.3)
\t\t(layers "F.Cu" "B.Cu")
\t\t(locked yes)
\t\t(net "GND")
\t\t(uuid "{uid(label)}")
\t)\n'''

def seg(label,a,b,net="VLINE_FINE_VINM"):
    return f'''\n\t(segment
\t\t(start {a[0]} {a[1]})
\t\t(end {b[0]} {b[1]})
\t\t(width 0.1)
\t\t(locked yes)
\t\t(layer "F.Cu")
\t\t(net "{net}")
\t\t(uuid "{uid(label)}")
\t)\n'''

def block_end(text,start):
    d=0; ins=False; esc=False
    for i in range(start,len(text)):
        ch=text[i]
        if ins:
            if esc: esc=False
            elif ch=="\\": esc=True
            elif ch=='"': ins=False
        else:
            if ch=='"': ins=True
            elif ch=='(': d+=1
            elif ch==')':
                d-=1
                if d==0: return i+1
    raise RuntimeError("unbalanced")

def remove_uuid(text,u):
    tok=f'(uuid "{u}")'
    pos=text.find(tok)
    if pos<0:
        raise RuntimeError("missing segment "+u)
    st=text.rfind("(segment",0,pos)
    en=block_end(text,st)
    return text[:st]+text[en:]

new=[]
for i,(x,y) in enumerate(GND_POINTS):
    u=uid(f"gnd-stitch-{i}")
    if f'(uuid "{u}")' not in s:
        new.append(via(f"gnd-stitch-{i}",x,y))

# Re-route VLINE_FINE_VINM around D201.1 GND instead of crossing its pad.
# Remove the two short stubs that terminate inside the D201 clearance envelope.
for old_uuid in [
    "26708c9d-ace9-4108-9862-f5fca251ae80",
    "18fd1d6a-cfa1-4a48-8bd4-6dc9fdf1cafa",
]:
    s=remove_uuid(s,old_uuid)

for label,a,b in [
    ("vline-fine-detour-a",(33.75,29.0),(34.75,29.0)),
    ("vline-fine-detour-b",(34.75,29.0),(34.75,27.8)),
    ("vline-fine-detour-c",(34.75,27.8),(32.9,27.8)),
    ("vline-fine-detour-d",(32.9,27.8),(32.75,28.0)),
]:
    u=uid(label)
    if f'(uuid "{u}")' not in s:
        new.append(seg(label,a,b))

anchor=s.find("\n\t(zone")
if anchor<0:
    raise SystemExit("zone anchor missing")
s=s[:anchor]+"".join(new)+s[anchor:]
if s.count("(")!=s.count(")"):
    raise SystemExit("parenthesis mismatch")
p.write_text(s,encoding="utf-8")
print("POST_REPAIR_BATCH1_ADDED",len(new))
