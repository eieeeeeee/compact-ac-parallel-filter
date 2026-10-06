#!/usr/bin/env python3
from pathlib import Path
import re,sys
p=Path(sys.argv[1]); s=p.read_text(encoding="utf-8")

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

def remove_uuid(u,kind=None):
    global s
    pos=s.find(f'(uuid "{u}")')
    if pos<0: raise RuntimeError("missing "+u)
    kinds=[kind] if kind else ["segment","via"]
    st=max(s.rfind("("+k,0,pos) for k in kinds)
    en=bend(s,st)
    s=s[:st]+s[en:]

def move_via(u,old,new):
    global s
    pos=s.find(f'(uuid "{u}")'); st=s.rfind("(via",0,pos); en=bend(s,st); b=s[st:en]
    needle=f"(at {old[0]} {old[1]})"
    if needle not in b: raise RuntimeError("via at mismatch "+u)
    b=b.replace(needle,f"(at {new[0]} {new[1]})",1); s=s[:st]+b+s[en:]

def drag(u,old,new):
    global s
    pos=s.find(f'(uuid "{u}")')
    if pos<0: raise RuntimeError("seg missing "+u)
    st=s.rfind("(segment",0,pos);en=bend(s,st);b=s[st:en];n=0
    for fld in ["start","end"]:
        a=f"({fld} {old[0]} {old[1]})"
        if a in b:
            b=b.replace(a,f"({fld} {new[0]} {new[1]})",1); n+=1
    if n!=1: raise RuntimeError(f"drag {u} changed={n}")
    s=s[:st]+b+s[en:]

def move_fp(ref,old,new):
    global s
    pos=s.find(f'(property "Reference" "{ref}"')
    if pos<0: raise RuntimeError("ref missing "+ref)
    st=s.rfind("(footprint",0,pos); en=bend(s,st); b=s[st:en]
    needle=f"(at {old})"
    if needle not in b: raise RuntimeError("fp at mismatch "+ref)
    b=b.replace(needle,f"(at {new})",1);s=s[:st]+b+s[en:]

# dangling remnants
remove_uuid("88f51a9c-5bc1-4686-8a47-24171dcd066f","segment")
remove_uuid("48f6b885-a47c-4d47-832f-ec82e55a7e9a","segment")
remove_uuid("c65a9274-1f39-494f-816d-31cfd8e156b2","via")

# 3V3 close via pairs: keep one via and redirect branch
remove_uuid("65388c8c-e282-453c-a0fa-89a9f7d4c0d1","via")
drag("814e7380-ee72-41b5-b3fd-547470a80d56",(31.25,12.0),(31.5,11.75))
remove_uuid("e5378b02-b51f-4df6-9a5c-d3692431799f","via")
drag("7f53d461-1595-4347-8677-056721cad93c",(22.25,31.75),(22.25,31.25))

# VREF_FILT via spacing
move_via("3f1915de-1a27-434e-9c4b-4ce549bea210",(11.75,38.25),(12.0,38.25))
remove_uuid("aac23ca6-2cde-47b1-8de6-128ad0b9f10d","segment")
drag("aafe549c-7d55-47c5-9bbc-d813e8c53f75",(11.75,38.25),(12.0,38.25))
move_via("569d7b6d-48cb-4a4e-be8d-00a0398a7419",(11.5,38.0),(11.25,38.0))
drag("0fcbe5a9-6672-45dc-9947-70dd9908d3af",(11.5,38.0),(11.25,38.0))
drag("4f173c9f-d349-41ab-93dc-f0d95a8e5cf0",(11.5,38.0),(11.25,38.0))

# TEST_A: use PTH pad itself as layer transition
remove_uuid("ebaf5aa0-31d8-481c-8485-6a4b1353d75c","via")
remove_uuid("2bf9d278-4650-42b9-a268-c08837a6ba6b","segment")
drag("cf08e55b-9771-4638-a255-ce3cc851a59c",(47.25,20.0),(46.8,20.0))

# Move crowded upper resistors down while preserving edge clearance (pad edge 39.475 -> board edge 40 = 0.525 mm)
move_fp("R204","30.3 38.3","30.3 39")
drag("f00283e4-717c-472d-b24c-f151ad1c93ce",(29.475,38.3),(29.475,39.0))
drag("c33dfdcd-55ca-4b3e-b40d-ff5e746e632a",(31.125,38.3),(31.125,39.0))
move_fp("R205","21 38.5","21 39")
drag("487737a2-5752-4358-8659-48438e9026eb",(20.175,38.5),(20.175,39.0))
drag("322800a6-f495-455c-92b4-620240764456",(21.825,38.5),(21.825,39.0))
move_fp("R206","27.2 38.3","27.2 39")
drag("aac43a87-bf7f-475f-8bc1-597d9c217d2d",(26.375,38.3),(26.375,39.0))
drag("952e08cb-7132-4a6b-981a-14745cb90d06",(28.025,38.3),(28.025,39.0))

if s.count("(")!=s.count(")"): raise RuntimeError("paren mismatch")
p.write_text(s,encoding="utf-8")
print("CLEANUP1_APPLIED")
