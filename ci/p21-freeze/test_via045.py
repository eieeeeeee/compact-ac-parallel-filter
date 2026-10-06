#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

pcb=Path(sys.argv[1]); pro=Path(sys.argv[2])
s=pcb.read_text(encoding="utf-8")

def block_end(text,start):
    d=0; ins=False; esc=False
    for i in range(start,len(text)):
        c=text[i]
        if ins:
            if esc: esc=False
            elif c=="\\": esc=True
            elif c=='"': ins=False
        else:
            if c=='"': ins=True
            elif c=='(': d+=1
            elif c==')':
                d-=1
                if d==0: return i+1
    raise RuntimeError("unbalanced")

pos=0; changed=0; counts={}
while True:
    st=s.find("(via",pos)
    if st<0: break
    if s[st+4:st+5] not in " \n\t":
        pos=st+4; continue
    en=block_end(s,st); b=s[st:en]
    ms=re.search(r'\(size ([\d.]+)\)',b)
    md=re.search(r'\(drill ([\d.]+)\)',b)
    if ms and md:
        key=(float(ms.group(1)),float(md.group(1)))
        counts[key]=counts.get(key,0)+1
        if abs(key[0]-0.5)<1e-9 and abs(key[1]-0.3)<1e-9:
            b2=re.sub(r'\(size 0\.5\)','(size 0.45)',b,count=1)
            b2=re.sub(r'\(drill 0\.3\)','(drill 0.2)',b2,count=1)
            s=s[:st]+b2+s[en:]
            delta=len(b2)-len(b); en+=delta
            changed+=1
    pos=en
pcb.write_text(s,encoding="utf-8")

j=json.loads(pro.read_text(encoding="utf-8"))
rules=j.setdefault("board",{}).setdefault("design_settings",{}).setdefault("rules",{})
rules["min_via_diameter"]=0.45
rules["min_through_hole_diameter"]=0.2
rules["min_hole_clearance"]=0.2
# Keep hole-to-hole at 0.25 for now; PTH is audited separately.
pro.write_text(json.dumps(j,indent=2)+"\n",encoding="utf-8")
print("VIA045_CHANGED",changed)
print("OLD_SIZES",sorted((k,v) for k,v in counts.items()))
print("RULES min_via=0.45 min_hole=0.20 hole_clearance=0.20")
