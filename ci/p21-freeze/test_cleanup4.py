#!/usr/bin/env python3
from pathlib import Path
import sys

p=Path(sys.argv[1])
s=p.read_text(encoding="utf-8")

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

def find_fp(ref):
    pos=s.find(f'(property "Reference" "{ref}"')
    if pos<0:raise RuntimeError("missing ref "+ref)
    st=s.rfind("(footprint",0,pos); en=bend(s,st)
    return st,en,s[st:en]

def move_fp(ref,old,new):
    global s
    st,en,b=find_fp(ref)
    needle=f"(at {old})"
    if needle not in b:raise RuntimeError(f"{ref} old at missing: {old}")
    b=b.replace(needle,f"(at {new})",1)
    s=s[:st]+b+s[en:]

def field(block,name):
    q=block.find("("+name+" ")
    if q<0:return None,None,None
    r=block.find(")",q)
    vals=block[q+len(name)+2:r].split()
    return q,r+1,(float(vals[0]),float(vals[1]))

def drag(uuid,old,new):
    global s
    pos=s.find(f'(uuid "{uuid}")')
    if pos<0:raise RuntimeError("segment missing "+uuid)
    st=s.rfind("(segment",0,pos); en=bend(s,st); b=s[st:en]; n=0
    for fld in ("start","end"):
        q,r,xy=field(b,fld)
        if xy and abs(xy[0]-old[0])<1e-6 and abs(xy[1]-old[1])<1e-6:
            b=b[:q]+f"({fld} {new[0]} {new[1]})"+b[r:]; n+=1
    if n!=1:raise RuntimeError(f"drag {uuid} changed={n}")
    s=s[:st]+b+s[en:]

# Re-space lower VLINE component rows.
move_fp("R203","27.83 35.83","27.83 35.3")
drag("8e37ec0c-99cd-4b03-9afb-e39605f9cc73",(27.005,35.83),(27.005,35.3))
drag("c8d02c3d-6e0c-4be8-844c-ebc30f43d58a",(27.005,35.83),(27.005,35.3))
drag("cbb76204-d9ec-405a-893c-0ed3ae980acb",(28.655,35.83),(28.655,35.3))

move_fp("C220","31.08 35.83","31.08 35.3")
drag("0c2e185a-ff5b-42c5-b3eb-fe4c2e4484de",(30.305,35.83),(30.305,35.3))

move_fp("R201","27.83 37.4","27.83 36.8")
drag("6609d90f-829b-44fb-90f2-90be56653d0e",(27.005,37.4),(27.005,36.8))
drag("99d81289-6201-4e11-a042-819ea26a2581",(28.655,37.4),(28.655,36.8))

move_fp("R211","31.08 37.4","31.08 36.8")
drag("bd7f23e3-7491-4894-9794-63a64195e1e2",(30.255,37.4),(30.255,36.8))

# Resolve C6/R205 courtyard overlap by moving C6 left.
move_fp("C6","20.08 36.65 90","18.78 36.65 90")
drag("c368bece-cdc4-401e-9975-20f51d7f5590",(20.08,37.425),(18.78,37.425))

if s.count("(")!=s.count(")"):raise RuntimeError("parenthesis mismatch")
p.write_text(s,encoding="utf-8")
print("CLEANUP4_APPLIED")
