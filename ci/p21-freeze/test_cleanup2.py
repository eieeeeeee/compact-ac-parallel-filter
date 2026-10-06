#!/usr/bin/env python3
from pathlib import Path
import sys
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

def field(block,name):
    q=block.find("(" + name + " ")
    if q<0:return None,None,None
    r=block.find(")",q); vals=block[q+len(name)+2:r].split()
    if len(vals)<2:return None,None,None
    return q,r+1,(float(vals[0]),float(vals[1]))

def move_via(u,old,new):
    global s
    pos=s.find(f'(uuid "{u}")')
    if pos<0: raise RuntimeError("via missing "+u)
    st=s.rfind("(via",0,pos);en=bend(s,st);b=s[st:en]
    q,r,xy=field(b,"at")
    if xy is None or abs(xy[0]-old[0])>1e-6 or abs(xy[1]-old[1])>1e-6: raise RuntimeError("via at mismatch "+u)
    b=b[:q]+f"(at {new[0]} {new[1]})"+b[r:];s=s[:st]+b+s[en:]

def drag(u,old,new):
    global s
    pos=s.find(f'(uuid "{u}")')
    if pos<0: raise RuntimeError("seg missing "+u)
    st=s.rfind("(segment",0,pos);en=bend(s,st);b=s[st:en];n=0
    for fld in ["start","end"]:
        q,r,xy=field(b,fld)
        if xy is not None and abs(xy[0]-old[0])<1e-6 and abs(xy[1]-old[1])<1e-6:
            b=b[:q]+f"({fld} {new[0]} {new[1]})"+b[r:];n+=1
    if n!=1: raise RuntimeError(f"drag {u} changed={n}")
    s=s[:st]+b+s[en:]

moves=[
("88f831cb-e0e1-4756-98a3-8a9b6a357dc0",(34.6,14.1),(34.6,14.15),["4c5024d6-deb9-477c-b005-570d225058e8","10851bb9-d95e-405a-9aa2-d58cda3a8f6f"]),
("c19144b4-c7d6-46d8-be1c-f5b87a9250cd",(33.6,10.9),(33.675,10.9),["d1a2e7f5-21fc-4abb-8d1b-7d0d4eebfcc2","80e5bf86-cfa3-49be-84cb-e80f3654bb3f"]),
("496bf6e3-70a9-4c03-90f3-cc5fb7f51406",(30.5,14.0),(30.5,14.075),["0c24fea6-11c2-4e81-95ef-0d4b1c5539dd","9ff3b0b6-0576-4828-a5e2-aa085fdbcfe6"]),
("c3963329-cff5-451f-a15b-0585acb57c3d",(19.5,38.25),(19.525,38.3),["1e088834-57c3-4042-97d9-a4aee476ee72","ff5e953e-79aa-4be8-956e-a62194baf229"]),
("a8ed9bfa-42dd-46ec-aeae-d174e38fe944",(18.25,36.5),(18.175,36.45),["4be67c1c-5f92-4f34-8ba4-b0323199a72b","7954d921-f003-4ea8-b0e6-bd2cee109bd3"]),
("57fb4a4b-9c4a-4908-963f-0518ce420546",(27.75,30.75),(27.75,30.7),["c1c78b05-109a-45a5-906d-06193f65dd36","f9a502ca-4987-4c58-a7f3-a78977efa362"]),
]
for u,old,new,segs in moves:
    move_via(u,old,new)
    for su in segs: drag(su,old,new)

move_via("3da12a12-52bf-5fae-84fc-3f7545c0620f",(17.8,21.55),(17.8,21.625))

if s.count("(")!=s.count(")"):raise RuntimeError("paren mismatch")
p.write_text(s,encoding="utf-8")
print("CLEANUP2_MOVED",len(moves)+1,"vias")
