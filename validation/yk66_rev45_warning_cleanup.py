#!/usr/bin/env python3
"""Non-release PCB/schematic notation corrections. Routing and pads unchanged."""
from pathlib import Path
import re

root=Path("verify/src")
pcb=root/"YK66_Rev41_RESEARCH_ONLY.kicad_pcb"
sch=root/"YK66_Rev41_RESEARCH_ONLY.kicad_sch"

def blocks(src,prefix):
    i=0
    while True:
        i=src.find(prefix,i)
        if i<0:return
        dep=0; quoted=False; esc=False
        for j in range(i,len(src)):
            c=src[j]
            if quoted:
                if esc:esc=False
                elif c=="\\":esc=True
                elif c=='"':quoted=False
            else:
                if c=='"':quoted=True
                elif c=='(':dep+=1
                elif c==')':
                    dep-=1
                    if dep==0:
                        yield i,j+1,src[i:j+1]
                        i=j+1
                        break
        else:raise RuntimeError("Unclosed expression")

s=pcb.read_text()
count=0
for a,b,part in reversed(list(blocks(s,'(footprint '))):
    m=re.search(r'\(layer "(F.Cu|B.Cu)"\)',part)
    if not m:continue
    side=m.group(1)[0]
    part=part.replace(f'(layer "{side}.SilkS") (effects ',f'(layer "{side}.Fab") (effects ')
    if side=='B':
        part,n=re.subn(r'(\(property "(?:Reference|Value)"[^\n]*?\(effects \(font \(size [^)]+\) \(thickness [^)]+\)\))\)',r'\1 (justify mirror))',part)
        assert n==2,(n,part[:150])
    s=s[:a]+part+s[b:];count+=1
assert count==13,count
s=s.replace('(gr_text "YK66 Rev45 ROUTED RESEARCH HOLD / NO MAINS" (at 26 1.3) (layer "F.SilkS")','(gr_text "YK66 Rev45 ROUTED RESEARCH HOLD / NO MAINS" (at 26 1.3) (layer "F.Fab")')
pcb.write_text(s)
s=sch.read_text();q=1.27
groups=[]
for a,b,part in reversed(list(blocks(s,'(symbol (lib_id '))):
    p=re.search(r'\(at ([\d.]+) ([\d.]+) 0\)',part)
    x,y=map(float,p.groups());dx=round(x/q)*q-x;dy=round(y/q)*q-y
    def tr(m):
        return f'(at {float(m[1])+dx:.4f} {float(m[2])+dy:.4f} {m[3]})'
    part,n=re.subn(r'\(at ([\d.]+) ([\d.]+) (0)\)',tr,part)
    assert n>=5
    groups.append((x,y,dx,dy))
    s=s[:a]+part+s[b:]
assert len(groups)==13,len(groups)
nr=0
for a,b,part in reversed(list(blocks(s,'(label '))):
    p=re.search(r'\(at ([\d.]+) ([\d.]+) 0\)',part)
    x,y=map(float,p.groups())
    matches=[u for u in groups if abs(y-u[1])<.001 and abs(abs(x-u[0])-5.08)<.001]
    assert len(matches)==1,(x,y,matches)
    _,_,dx,dy=matches[0]
    part=part.replace(p.group(),f'(at {x+dx:.4f} {y+dy:.4f} 0)')
    s=s[:a]+part+s[b:];nr+=1
assert nr==26,nr
sch.write_text(s)
print("Removed unsuitable silk text from 13 board footprints; mirrored back Fab values.")
print("Moved 13 schematic symbol groups and 26 pins' net labels onto 1.27 mm grid.")
print("Copper, pads, nets and components are deliberately unchanged.")
