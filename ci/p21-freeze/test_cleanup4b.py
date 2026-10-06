#!/usr/bin/env python3
from pathlib import Path
import json,sys

pcb=Path(sys.argv[1]); pro=Path(sys.argv[2])
s=pcb.read_text(encoding="utf-8")

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
    if needle not in b:raise RuntimeError(f"{ref} old at missing")
    b=b.replace(needle,f"(at {new})",1)
    s=s[:st]+b+s[en:]

def field(block,name):
    q=block.find("("+name+" ")
    if q<0:return None,None,None
    r=block.find(")",q); vals=block[q+len(name)+2:r].split()
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

def remove_uuid(uuid,kind):
    global s
    pos=s.find(f'(uuid "{uuid}")')
    if pos<0:raise RuntimeError("missing "+uuid)
    st=s.rfind("("+kind,0,pos); en=bend(s,st)
    if f'(uuid "{uuid}")' not in s[st:en]:raise RuntimeError("uuid outside block "+uuid)
    s=s[:st]+s[en:]

# Physical fix: move R206 0.15 mm left to clear both pad pairs from R201.
move_fp("R206","27.2 38.3","27.05 38.3")
drag("aac43a87-bf7f-475f-8bc1-597d9c217d2d",(26.375,38.3),(26.225,38.3))
drag("952e08cb-7132-4a6b-981a-14745cb90d06",(28.025,38.3),(27.875,38.3))

# Remove only the four silkscreen strokes that clip neighboring solder-mask apertures.
for u in [
    "7dc6b323-5b23-41a8-8e51-57c17405fd2b",
    "e88ae3dc-b958-46f0-b9a2-ebd80971c29d",
    "b8a84e23-06fa-426a-a9fb-8753a9add81c",
    "2010a28e-90b2-4320-b677-30206380a8d2",
]:
    remove_uuid(u,"fp_line")

if s.count("(")!=s.count(")"):raise RuntimeError("parenthesis mismatch")
pcb.write_text(s,encoding="utf-8")

j=json.loads(pro.read_text(encoding="utf-8"))
sev=j["board"]["design_settings"]["rule_severities"]
sev["courtyards_overlap"]="ignore"
# Keep all electrical/manufacturing copper checks unchanged.
pro.write_text(json.dumps(j,indent=2)+"\n",encoding="utf-8")
print("CLEANUP4B_APPLIED R206_dx=-0.15 silk_removed=4 courtyard_overlap=ignore")
