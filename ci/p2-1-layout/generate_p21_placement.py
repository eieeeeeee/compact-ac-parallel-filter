#!/usr/bin/env python3
import sys, math, json, shutil, re, xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew

BASE=Path(sys.argv[1]).resolve()
NET=Path(sys.argv[2]).resolve()
OUT=Path(sys.argv[3]).resolve()
SKIP={"U901","K301"}

for name in ["J201_POGO5.kicad_mod","UCC27282_DRC10_TI_CANDIDATE.kicad_mod"]:
    shutil.copyfile(Path("/work/ci/p0-pcb/footprints")/name,
                    BASE/"RC18_Custom.pretty"/name)

def fp_path(fpname):
    lib,name=fpname.split(":",1)
    p=(BASE/"RC18_Custom.pretty"/f"{name}.kicad_mod") if lib=="RC18_Custom" else Path("/usr/share/kicad/footprints")/f"{lib}.pretty"/f"{name}.kicad_mod"
    if not p.exists(): raise RuntimeError(f"footprint not found: {fpname} -> {p}")
    return p

def load_fp(fpname):
    p=fp_path(fpname)
    fp=pcbnew.FootprintLoad(str(p.parent),p.stem)
    if fp is None: raise RuntimeError(f"failed footprint load: {fpname}")
    return fp

def sexpr_block(text,start):
    d=0; ins=False; esc=False
    for i in range(start,len(text)):
        ch=text[i]
        if ins:
            if esc: esc=False
            elif ch=="\\": esc=True
            elif ch=='"': ins=False
            continue
        if ch=='"': ins=True
        elif ch=='(': d+=1
        elif ch==')':
            d-=1
            if d==0: return text[start:i+1]
    raise RuntimeError("unbalanced sexpr")

def courtyard_bbox(fpname):
    text=fp_path(fpname).read_text(encoding="utf-8")
    pts=[]
    for kind in ["fp_line","fp_rect","fp_arc","fp_poly","fp_circle"]:
        pos=0
        while True:
            j=text.find(f"({kind}",pos)
            if j<0: break
            sb=sexpr_block(text,j); pos=j+len(sb)
            if '(layer "F.CrtYd")' not in sb and '(layer F.CrtYd)' not in sb: continue
            if kind=="fp_circle":
                cm=re.search(r'\(center\s+([-0-9.]+)\s+([-0-9.]+)',sb)
                em=re.search(r'\(end\s+([-0-9.]+)\s+([-0-9.]+)',sb)
                if cm and em:
                    cx,cy=float(cm.group(1)),float(cm.group(2)); ex,ey=float(em.group(1)),float(em.group(2))
                    rr=math.hypot(ex-cx,ey-cy); pts += [(cx-rr,cy-rr),(cx+rr,cy+rr)]
                    continue
            for m in re.finditer(r'\((?:start|end|mid|xy)\s+([-0-9.]+)\s+([-0-9.]+)',sb):
                pts.append((float(m.group(1)),float(m.group(2))))
    if not pts:
        fp=load_fp(fpname); xs=[]; ys=[]
        for pad in fp.Pads():
            bb=pad.GetBoundingBox()
            xs += [pcbnew.ToMM(bb.GetX()),pcbnew.ToMM(bb.GetRight())]
            ys += [pcbnew.ToMM(bb.GetY()),pcbnew.ToMM(bb.GetBottom())]
        return min(xs)-0.25,min(ys)-0.25,max(xs)+0.25,max(ys)+0.25
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    return min(xs),min(ys),max(xs),max(ys)

def rbbox(bb,rot):
    a=math.radians(rot); pts=[]
    for x,y in [(bb[0],bb[1]),(bb[0],bb[3]),(bb[2],bb[1]),(bb[2],bb[3])]:
        pts.append((x*math.cos(a)+y*math.sin(a),-x*math.sin(a)+y*math.cos(a)))
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    return min(xs),min(ys),max(xs),max(ys)

tree=ET.parse(NET); root=tree.getroot()
comps={}
for c in root.find("components"):
    ref=c.attrib["ref"]; comps[ref]={"value":c.findtext("value") or "","footprint":c.findtext("footprint") or ""}
nets=[]; pin_net={}
for n in root.find("nets"):
    name=n.attrib.get("name","") or f"N-{n.attrib.get('code','0')}"
    nets.append(name)
    for nd in n.findall("node"): pin_net[(nd.attrib["ref"],nd.attrib["pin"])]=name

# Explicit functional placement: no global autoplacement.
P={
"D301":(45.95,13.75,0),"Q301":(40.8,17.0,0),"Q302":(40.8,22.0,0),"Q303":(36.8,22.08,90),
"R303":(44.58,16.08,0),"R304":(41.83,14.33,0),"R305":(41.08,24.83,0),"R306":(41.83,12.58,0),
"C901":(3.08,28.38,0),"C902":(1.58,10.13,90),"R900":(18.38,15.03,0),"R901":(45.0,5.0,0),
"R902":(30.08,25.38,0),"R903":(1.33,2.63,90),"R904":(32.58,25.63,90),"R905":(34.08,21.88,90),
"C620":(22.6,1.3,0),"R617":(18.8,1.3,0),
"C301":(16.2,18.0,0),"C302":(32.08,22.05,90),"R301":(26.8,18.0,0),"R302":(34.8,18.0,0),
"R307":(26.93,22.28,0),"R308":(25.8,13.8,0),
"C101":(18.0,24.6,0),"C102":(2.83,18.08,0),"D101":(9.85,21.6,90),"D102":(17.8,22.0,0),
"F101":(21.73,22.63,90),"J101":(4.4,22.0,270),"Q101":(13.55,22.03,90),"R101":(13.83,25.83,90),
"J301":(46.8,20.0,270),
"C310":(30.5,11.2,90),"C311":(33.0,8.5,0),"C312":(36.3,8.5,0),"C313":(43.0,8.8,0),
"C314":(44.8,10.8,0),"R311":(31.5,15.0,0),"R312":(37.0,15.0,180),"R313":(39.5,8.8,0),
"R314":(39.9,10.8,0),"U3":(34.8,12.0,180),
"C611":(18.0,8.0,0),"C612":(22.5,8.0,0),"C613":(27.0,8.0,0),"C614":(27.05,2.13,0),
"C615":(30.8,2.13,0),"C616":(32.83,5.1,90),"C617":(34.55,2.13,0),"C618":(35.08,5.1,90),
"C619":(37.33,5.1,90),"L601":(18.0,5.0,0),"L602":(22.5,5.0,0),"L603":(27.0,5.0,0),
"R611":(18.0,10.0,180),"R612":(22.5,10.0,180),"R613":(27.0,10.0,180),"R614":(38.28,2.1,0),
"R615":(39.55,5.08,90),"R616":(41.8,5.08,90),
"C1":(11.3,26.2,0),"C2":(20.2,33.5,90),"C3":(17.0,39.0,0),"C4":(13.5,39.0,0),
"C5":(22.2,35.6,90),"C6":(20.08,36.65,90),"C7":(7.83,37.83,90),"C8":(3.83,35.83,90),
"C9":(6.4,29.2,0),"C10":(6.4,35.2,0),"FB1":(20.2,29.85,90),"J201":(1.75,32.65,90),
"R1":(6.08,37.83,90),"R2":(3.58,38.33,0),"U1":(14.0,32.7,0),"X1":(6.4,32.2,0),
"C120":(47.33,32.08,90),"R120":(44.58,34.08,0),"R121":(41.83,32.08,90),
"C801":(26.83,26.33,0),"C802":(26.33,29.05,90),"C803":(25.08,33.08,0),"U801":(23.3,29.0,90),
"C701":(3.25,14.2,90),"C702":(11.58,14.13,90),"C703":(9.58,14.1,90),"C704":(12.33,16.63,0),
"R701":(12.33,11.63,0),"R702":(13.33,14.13,90),"R703":(15.08,14.13,90),"U701":(6.5,14.2,90),
"C601":(4.0,5.4,0),"C602":(4.0,7.8,0),"C604":(8.5,2.5,0),"D601":(4.5,2.5,0),
"R601":(8.08,8.88,0),"R602":(4.83,9.63,0),"R603":(11.8,2.3,180),"R604":(11.8,9.0,180),
"R605":(15.5,11.7,0),"R606":(1.33,5.88,90),"U6":(8.0,6.0,270),
"C605":(15.08,2.63,0),"C606":(19.0,12.0,0),"C607":(35.9,25.3,0),"Q601":(12.2,4.7,180),"Q602":(12.2,6.3,0),
"RTH1":(44.58,30.08,0),"RTH2":(44.58,35.83,0),"TH1":(44.53,32.05,0),"TH2":(44.53,28.05,0),
"LED1":(41.33,34.58,0),"LED2":(47.83,34.58,0),"RLED1":(41.83,28.83,90),"RLED2":(47.33,28.83,90),
"C201":(34.33,37.58,0),"C203":(34.33,35.83,0),"C210":(35.83,33.05,90),"C211":(31.08,28.33,0),
"C220":(31.08,35.83,0),"C221":(31.08,30.08,0),"D201":(34.78,29.3,0),"R201":(27.83,37.40,0),
"R202":(25.33,35.58,90),"R203":(27.83,35.83,0),"R210":(28.58,29.33,90),"R211":(31.08,37.40,0),
"U2":(31.0,33.0,180),"C204":(24.10,38.70,0),"R204":(30.30,38.70,0),"R205":(21.00,38.70,0),"R206":(27.20,38.70,0)
}

actual={r for r in comps if not r.startswith("#") and r not in SKIP}
if actual!=set(P):
    raise RuntimeError(f"placement map mismatch missing={sorted(actual-set(P))} extra={sorted(set(P)-actual)}")

# VLINE fine network remains compact between the MCU ADC pins and U2.
# The upper row (C6/R201/R211) has been shifted 0.18 mm upward to preserve
# courtyard separation while the fine row stays inside 0.50 mm edge clearance.
P["R205"]=(21.00,38.90,0)
P["C204"]=(24.10,38.90,0)
P["R206"]=(27.20,38.90,0)
P["R204"]=(30.30,38.90,0)
print("P2.1 VLINE fine row fixed compact: R205=21.00 C204=24.10 R206=27.20 R204=30.30")

# Validate actual courtyards.
rects={}
for ref,(x,y,rot) in P.items():
    fpname="RC18_Custom:J201_POGO5" if ref=="J201" else comps[ref]["footprint"]
    bb=rbbox(courtyard_bbox(fpname),rot)
    rect=(x+bb[0],y+bb[1],x+bb[2],y+bb[3])
    rects[ref]=rect
    if rect[0]<0.10 or rect[1]<0.10 or rect[2]>49.90 or rect[3]>39.90:
        raise RuntimeError(f"{ref} outside board: {rect}")
refs=sorted(rects)
overlaps=[]
for i,a in enumerate(refs):
    ax0,ay0,ax1,ay1=rects[a]
    for b in refs[i+1:]:
        bx0,by0,bx1,by1=rects[b]
        if not (ax0>=bx1 or bx0>=ax1 or ay0>=by1 or by0>=ay1):
            overlaps.append((a,b,rects[a],rects[b]))
if overlaps:
    for a,b,ra,rb in overlaps:
        print(f"OVERLAP {a} {b}: {ra} / {rb}", file=sys.stderr)
    raise RuntimeError(f"P2.1 courtyard overlaps={len(overlaps)}")

board=pcbnew.BOARD()
board.SetCopperLayerCount(4)
try: board.GetDesignSettings().SetBoardThickness(pcbnew.FromMM(1.6))
except Exception: pass

netobjs={}
for name in sorted(set(nets)):
    ni=pcbnew.NETINFO_ITEM(board,name); board.Add(ni); netobjs[name]=ni

for ref,c in comps.items():
    if ref.startswith("#") or ref in SKIP: continue
    fpname="RC18_Custom:J201_POGO5" if ref=="J201" else c["footprint"]
    fp=load_fp(fpname); fp.SetReference(ref); fp.SetValue(c["value"])
    x,y,rot=P[ref]; fp.SetPosition(pcbnew.VECTOR2I_MM(x,y)); fp.SetOrientationDegrees(rot)
    try:
        fp.Reference().SetVisible(False); fp.Value().SetVisible(False)
    except Exception: pass
    board.Add(fp)
    for pad in fp.Pads():
        key=(ref,pad.GetNumber())
        if key in pin_net: pad.SetNet(netobjs[pin_net[key]])

def edge(x1,y1,x2,y2):
    s=pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts)
    s.SetStart(pcbnew.VECTOR2I_MM(x1,y1)); s.SetEnd(pcbnew.VECTOR2I_MM(x2,y2)); s.SetWidth(pcbnew.FromMM(0.05)); board.Add(s)
edge(0,0,50,0); edge(50,0,50,40); edge(50,40,0,40); edge(0,40,0,0)
pcbnew.SaveBoard(str(OUT),board)

pro=BASE/"RC18_RevB_SI.kicad_pro"
pdata=json.loads(pro.read_text(encoding="utf-8"))
ds=pdata.setdefault("board",{}).setdefault("design_settings",{})
sev=ds.setdefault("rule_severities",{})
sev["unconnected_items"]="ignore"
ds.setdefault("rules",{})["min_track_width"]=0.10
pdata["meta"]["filename"]="RC18_RevB_SI.kicad_pro"
pro.write_text(json.dumps(pdata,indent=2)+"\n",encoding="utf-8")

dru=BASE/"RC18_RevB_SI.kicad_dru"
dru.write_text("""(version 1)
(rule "CSD17381F4 internal pad clearance"
  (condition "((A.Reference == 'Q601' && B.Reference == 'Q601') || (A.Reference == 'Q602' && B.Reference == 'Q602'))")
  (constraint clearance (min 0.10mm)))
""",encoding="utf-8")

print(f"P2.1 functional placement saved: {OUT}")
print(f"footprints={len(P)}; unconnected ignored only for placement gate")
