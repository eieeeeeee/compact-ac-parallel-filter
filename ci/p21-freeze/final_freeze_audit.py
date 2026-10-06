#!/usr/bin/env python3
from pathlib import Path
import json,re,sys,xml.etree.ElementTree as ET,math

proj=Path(sys.argv[1])
pcb=proj/"RC18_RevB_SI.kicad_pcb"
pro=proj/"RC18_RevB_SI.kicad_pro"
netxml=Path(sys.argv[2])

s=pcb.read_text(encoding="utf-8")
j=json.loads(pro.read_text(encoding="utf-8"))

def bend(text,st):
    d=0;ins=False;esc=False
    for i in range(st,len(text)):
        c=text[i]
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

def footprint_blocks():
    out=[];pos=0
    while True:
        st=s.find("(footprint",pos)
        if st<0:break
        en=bend(s,st);b=s[st:en];pos=en
        m=re.search(r'\(property "Reference" "([^"]+)"',b)
        if m:out.append((m.group(1),b))
    return out

fps=dict(footprint_blocks())
pcb_refs=set(fps)

root=ET.parse(netxml).getroot()
sch_refs={c.attrib["ref"] for c in root.findall(".//components/comp")}
missing=sch_refs-pcb_refs
extra=pcb_refs-sch_refs
assert missing=={"U901","K301"}, f"unexpected schematic-only refs: {sorted(missing)}"
assert not extra, f"unexpected PCB-only refs: {sorted(extra)}"
assert len(sch_refs)==135, len(sch_refs)
assert len(pcb_refs)==133, len(pcb_refs)

def pad_nets(ref):
    b=fps[ref]; out={}
    pos=0
    while True:
        st=b.find("(pad ",pos)
        if st<0:break
        en=bend(b,st);pb=b[st:en];pos=en
        m=re.match(r'\(pad\s+"?([^"\s]+)',pb)
        n=re.search(r'\(net "([^"]+)"\)',pb)
        if m:out[m.group(1)]=n.group(1) if n else None
    return out

assert pad_nets("Q101")["1"]=="Q101_GATE"
assert pad_nets("Q101")["2"]=="12V_REV"
assert pad_nets("Q101")["3"]=="12V_FUSED"
assert pad_nets("D201")["1"]=="GND"
assert pad_nets("D201")["2"]=="3V3"
assert pad_nets("D201")["3"]=="VLINE_BIAS"
x=pad_nets("X1")
assert x["1"]=="HSE_PF0" and x["2"]=="GND" and x["3"]=="HSE_PF1" and x["4"]=="GND"

rules=j["board"]["design_settings"]["rules"]
expect={
 "min_clearance":0.1,
 "min_copper_edge_clearance":0.5,
 "min_hole_clearance":0.2,
 "min_hole_to_hole":0.25,
 "min_through_hole_diameter":0.2,
 "min_track_width":0.1,
 "min_via_annular_width":0.1,
 "min_via_diameter":0.45,
}
for k,v in expect.items():
    assert abs(float(rules[k])-v)<1e-9, (k,rules[k],v)
sev=j["board"]["design_settings"]["rule_severities"]
assert sev.get("courtyards_overlap")=="ignore"

# Verify all through vias respect final 0.45/0.20 / annular 0.10 rule.
pos=0;vias=0
while True:
    st=s.find("(via",pos)
    if st<0:break
    if s[st+4:st+5] not in " \n\t":
        pos=st+4;continue
    en=bend(s,st);b=s[st:en];pos=en
    ms=re.search(r'\(size ([\d.]+)\)',b); md=re.search(r'\(drill ([\d.]+)\)',b)
    if not (ms and md):continue
    size=float(ms.group(1)); drill=float(md.group(1)); vias+=1
    assert size>=0.45-1e-9, size
    assert drill>=0.2-1e-9, drill
    assert (size-drill)/2>=0.1-1e-9, (size,drill)

# Intentional courtyard-overlap body audit using actual F.Fab rectangles.
def fp_geom(ref):
    b=fps[ref]
    a=re.search(r'\\n\\s*\\(at ([\\d.\\-]+) ([\\d.\\-]+)(?: ([\\d.\\-]+))?',b)
    x,y=float(a.group(1)),float(a.group(2));rot=float(a.group(3) or 0)
    pos=0; rect=None
    while True:
        st=b.find("(fp_rect",pos)
        if st<0:break
        en=bend(b,st); rb=b[st:en]; pos=en
        if '(layer "F.Fab")' not in rb:continue
        m=re.search(r'\\(start ([\\d.\\-]+) ([\\d.\\-]+)\\)',rb)
        n=re.search(r'\\(end ([\\d.\\-]+) ([\\d.\\-]+)\\)',rb)
        if m and n:
            rect=tuple(map(float,m.groups()+n.groups()))
            break
    assert rect is not None, ref
    x1,y1,x2,y2=rect;hx=abs(x2-x1)/2;hy=abs(y2-y1)/2
    if int(rot)%180==90:hx,hy=hy,hx
    return x,y,hx,hy
def body_gap(a,b):
    x1,y1,hx1,hy1=fp_geom(a);x2,y2,hx2,hy2=fp_geom(b)
    dx=abs(x1-x2)-hx1-hx2;dy=abs(y1-y2)-hy1-hy2
    if dx>0 and dy>0:return math.hypot(dx,dy)
    if dx>0:return dx
    if dy>0:return dy
    return -min(-dx,-dy)
pairs=[("R201","R204"),("R201","R206"),("R204","R211"),("C6","R205")]
gaps={f"{a}-{b}":body_gap(a,b) for a,b in pairs}
assert min(gaps.values())>0, gaps

print("PARITY_PASS sch_refs=135 pcb_refs=133 schematic_only=U901,K301")
print("PINMAP_PASS Q101 D201 X1")
print("RULES_PASS",expect)
print("VIA_PASS count=",vias)
print("COURTYARD_BODY_GAPS_MM",gaps)
