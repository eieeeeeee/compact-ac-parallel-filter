#!/usr/bin/env python3
from pathlib import Path
import sys,uuid
p=Path(sys.argv[1]); s=p.read_text(encoding="utf-8")
NS=uuid.UUID("626a87b0-3e4f-4e8f-91e6-1129636d4f1c")
def uid(x): return str(uuid.uuid5(NS,x))
def bend(t,st):
    d=0;ins=False;esc=False
    for i in range(st,len(t)):
        c=t[i]
        if ins:
            if esc:esc=False
            elif c=="\\":esc=True
            elif c=='"':ins=False
        else:
            if c=='"':ins=True
            elif c=='(':d+=1
            elif c==')':
                d-=1
                if d==0:return i+1
    raise RuntimeError("unbalanced")
def field(block,name):
    q=block.find("(" + name + " ")
    if q<0:return None,None,None
    r=block.find(")",q); vals=block[q+len(name)+2:r].split()
    return q,r+1,(float(vals[0]),float(vals[1]))
def drag(u,old,new):
    global s
    pos=s.find(f'(uuid "{u}")')
    if pos<0:raise RuntimeError("seg missing "+u)
    st=s.rfind("(segment",0,pos);en=bend(s,st);b=s[st:en];n=0
    for fld in ("start","end"):
        q,r,xy=field(b,fld)
        if xy and abs(xy[0]-old[0])<1e-6 and abs(xy[1]-old[1])<1e-6:
            b=b[:q]+f"({fld} {new[0]} {new[1]})"+b[r:];n+=1
    if n!=1:raise RuntimeError(f"drag {u} changed={n}")
    s=s[:st]+b+s[en:]
def remove(u,kind="segment"):
    global s
    pos=s.find(f'(uuid "{u}")')
    if pos<0:raise RuntimeError("missing "+u)
    st=s.rfind("("+kind,0,pos);en=bend(s,st)
    s=s[:st]+s[en:]
def seg(label,a,b,net,width,layer):
    return f'''\n\t(segment
\t\t(start {a[0]} {a[1]})
\t\t(end {b[0]} {b[1]})
\t\t(width {width})
\t\t(locked yes)
\t\t(layer "{layer}")
\t\t(net "{net}")
\t\t(uuid "{uid(label)}")
\t)\n'''

# U901_UVLO: shift only shared bend away from U3_INN via.
drag("32c384ad-78f4-4962-90f2-fe29593d0b75",(30.0,13.0),(30.05,12.95))
drag("1a729c06-e65f-46ad-8b95-406a132a124f",(30.0,13.0),(30.05,12.95))

# VREF_FILT: remove diagonal pair beside VLINE_FINE_OUT via; use upper horizontal branch.
remove("a7f4994d-58a8-4f20-9ac9-464c2204fb4c")
remove("ef832d6a-5754-4431-90e4-d7c675bd3555")
new=[seg("vref-upper",(11.75,36.75),(11.25,36.75),"VREF_FILT",0.15,"B.Cu")]

# D201: move two bends away from pad2 3V3 while retaining endpoints.
drag("8204c115-a984-4049-9754-3623cc1397b5",(34.75,30.0),(34.9,29.95))
drag("3eae1290-5bc0-4bf7-97a9-9a9a438db651",(34.75,30.0),(34.9,29.95))
drag("3eae1290-5bc0-4bf7-97a9-9a9a438db651",(34.5,29.75),(34.65,29.65))
drag("591862a5-f4f0-4282-b6d7-431b7782a74f",(34.5,29.75),(34.65,29.65))

# X1 HSE_PF0: lift shared bend away from HSE_PF1 pad.
drag("58af632e-231b-4797-8e17-ea5175bcbf11",(8.125,32.0),(8.5,32.25))
drag("f9fcd7ed-130f-4185-ae6c-e5740620edb1",(8.125,32.0),(8.5,32.25))

anchor=s.find("\n\t(zone")
if anchor<0:raise RuntimeError("zone anchor missing")
s=s[:anchor]+"".join(new)+s[anchor:]
if s.count("(")!=s.count(")"):raise RuntimeError("paren mismatch")
p.write_text(s,encoding="utf-8")
print("CLEANUP3_APPLIED",len(new))
