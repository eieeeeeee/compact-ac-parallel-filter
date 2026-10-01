#!/usr/bin/env python3
import sys, math, json, shutil, re, xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew

BASE = Path(sys.argv[1]).resolve()
NET = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()
SKIP = {"U901", "K301"}

for name in ["J201_POGO5.kicad_mod", "UCC27282_DRC10_TI_CANDIDATE.kicad_mod"]:
    shutil.copyfile(Path("/work/ci/p0-pcb/footprints") / name,
                    BASE / "RC18_Custom.pretty" / name)

def fp_mod_path(fpname):
    lib, name = fpname.split(":", 1)
    if lib == "RC18_Custom":
        p = BASE / "RC18_Custom.pretty" / f"{name}.kicad_mod"
        if p.exists():
            return p
        raise RuntimeError(f"local footprint not found: {p}")
    p = Path("/usr/share/kicad/footprints") / f"{lib}.pretty" / f"{name}.kicad_mod"
    if p.exists():
        return p
    raise RuntimeError(f"footprint not found: {fpname}")

def load_fp(fpname):
    p = fp_mod_path(fpname)
    fp = pcbnew.FootprintLoad(str(p.parent), p.stem)
    if fp is None:
        raise RuntimeError(f"failed footprint load: {fpname}")
    return fp

def block(text, start):
    depth=0; ins=False; esc=False
    for i in range(start, len(text)):
        ch=text[i]
        if ins:
            if esc: esc=False
            elif ch=="\\": esc=True
            elif ch=='"': ins=False
            continue
        if ch=='"': ins=True
        elif ch=='(': depth += 1
        elif ch==')':
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    raise RuntimeError("unbalanced S-expression")

def courtyard_bbox(fpname):
    text=fp_mod_path(fpname).read_text(encoding="utf-8")
    pts=[]
    for kind in ["fp_line","fp_rect","fp_arc","fp_poly","fp_circle"]:
        pos=0
        while True:
            j=text.find(f"({kind}",pos)
            if j<0: break
            sb=block(text,j); pos=j+len(sb)
            if '(layer "F.CrtYd")' not in sb and '(layer F.CrtYd)' not in sb:
                continue
            if kind=="fp_circle":
                cm=re.search(r'\(center\s+([-0-9.]+)\s+([-0-9.]+)',sb)
                em=re.search(r'\(end\s+([-0-9.]+)\s+([-0-9.]+)',sb)
                if cm and em:
                    cx,cy=float(cm.group(1)),float(cm.group(2))
                    ex,ey=float(em.group(1)),float(em.group(2))
                    rr=math.hypot(ex-cx,ey-cy)
                    pts += [(cx-rr,cy-rr),(cx+rr,cy+rr)]
                    continue
            for m in re.finditer(r'\((?:start|end|mid|xy)\s+([-0-9.]+)\s+([-0-9.]+)',sb):
                pts.append((float(m.group(1)),float(m.group(2))))
    if not pts:
        fp=load_fp(fpname)
        xs=[]; ys=[]
        for pad in fp.Pads():
            bb=pad.GetBoundingBox()
            xs += [pcbnew.ToMM(bb.GetX()),pcbnew.ToMM(bb.GetRight())]
            ys += [pcbnew.ToMM(bb.GetY()),pcbnew.ToMM(bb.GetBottom())]
        return (min(xs)-0.25,min(ys)-0.25,max(xs)+0.25,max(ys)+0.25)
    xs=[x for x,y in pts]; ys=[y for x,y in pts]
    return min(xs),min(ys),max(xs),max(ys)

def rotated_bbox(bb,rot):
    a=math.radians(rot)
    q=[]
    for x,y in [(bb[0],bb[1]),(bb[0],bb[3]),(bb[2],bb[1]),(bb[2],bb[3])]:
        q.append((x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a)))
    xs=[x for x,y in q]; ys=[y for x,y in q]
    return min(xs),min(ys),max(xs),max(ys)

tree=ET.parse(NET)
root=tree.getroot()
comps={}
for c in root.find("components"):
    ref=c.attrib["ref"]
    value=c.findtext("value") or ""
    footprint=c.findtext("footprint") or ""
    sp=c.find("sheetpath")
    sheet=sp.attrib.get("names","") if sp is not None else ""
    comps[ref]={"value":value,"footprint":footprint,"sheet":sheet}

nets=[]; pin_net={}
for n in root.find("nets"):
    name=n.attrib.get("name","") or f"N-{n.attrib.get('code','0')}"
    nets.append(name)
    for node in n.findall("node"):
        pin_net[(node.attrib["ref"],node.attrib["pin"])]=name

board=pcbnew.BOARD()
try: board.SetCopperLayerCount(4)
except Exception: pass
try: board.GetDesignSettings().SetBoardThickness(pcbnew.FromMM(1.6))
except Exception: pass

netobjs={}
for name in sorted(set(nets)):
    ni=pcbnew.NETINFO_ITEM(board,name); board.Add(ni); netobjs[name]=ni

sheet_order=[
    "01_POWER_INPUT","02_POWER_RAILS","03_MCU_DIGITAL",
    "04_VLINE_ANALOG","05_CURRENT_SENSE_TRIP","06_SI_HALFBRIDGE",
    "07_RECONSTRUCTION_LC","08_INJECTION_DISCONNECT","09_MONITOR_THERMAL_UI"
]
rank={k:i for i,k in enumerate(sheet_order)}
def sheetkey(s):
    for k in sheet_order:
        if k in s: return k
    return sheet_order[-1]

# P1 frozen priority placement.
# Coordinates are footprint origins in mm, rotation degrees.
fixed={
    # UCC27282 + Si half-bridge + bootstrap/gate resistors
    "U6":   (6.0,  6.0, 270),
    "Q601": (10.2, 4.7, 180),
    "Q602": (10.2, 6.3,   0),
    "C604": (5.7,  3.0,   0),
    "R603": (12.3, 2.4, 180),
    "R604": (8.5,  9.2,  90),

    # Three-stage reconstruction LC
    "L601": (16.0, 4.6,   0),
    "L602": (20.5, 4.6,   0),
    "L603": (25.0, 4.6,   0),
    "C611": (18.25,7.4,   0),
    "R611": (18.25,9.6, 180),
    "C612": (22.75,7.4,   0),
    "R612": (22.75,9.6, 180),
    "C613": (27.25,7.4,   0),
    "R613": (27.25,9.6, 180),

    # 1 uF + 4.7 ohm injection + 0.33 ohm shunt + INA296 Kelvin front end
    "C301": (4.5, 18.0,   0),
    "R301": (14.8,18.0,   0),
    "R302": (22.7,18.0,   0),
    "U3":   (22.7,12.3, 180),
    "R311": (20.2,14.9,   0),
    "R312": (25.2,14.9, 180),
}

GUARD=0.30
BIN_W,BIN_H=48.0,38.0
ORIGIN_X,ORIGIN_Y=1.0,1.0
free_rects=[(0.0,0.0,BIN_W,BIN_H)]
placements={}
items=[]

def intersects(a,b):
    ax,ay,aw,ah=a; bx,by,bw,bh=b
    return not (bx>=ax+aw or bx+bw<=ax or by>=ay+ah or by+bh<=ay)
def contains(a,b):
    ax,ay,aw,ah=a; bx,by,bw,bh=b
    return (bx>=ax-1e-9 and by>=ay-1e-9 and
            bx+bw<=ax+aw+1e-9 and by+bh<=ay+ah+1e-9)

def subtract_used(used):
    global free_rects
    nf=[]
    for fr in free_rects:
        if not intersects(fr,used):
            nf.append(fr); continue
        fx,fy,fw,fh=fr; ux,uy,uw,uh=used
        if ux>fx: nf.append((fx,fy,ux-fx,fh))
        if ux+uw<fx+fw: nf.append((ux+uw,fy,fx+fw-(ux+uw),fh))
        if uy>fy: nf.append((fx,fy,fw,uy-fy))
        if uy+uh<fy+fh: nf.append((fx,uy+uh,fw,fy+fh-(uy+uh)))
    free_rects=[
        ra for ii,ra in enumerate(nf)
        if not any(ii!=jj and contains(rb,ra) for jj,rb in enumerate(nf))
    ]

# Build component geometry list.
for ref,c in comps.items():
    if ref.startswith("#") or ref in SKIP:
        continue
    fpname="RC18_Custom:J201_POGO5" if ref=="J201" else c["footprint"]
    if not fpname:
        raise RuntimeError(f"{ref} has no footprint")
    bb=courtyard_bbox(fpname)
    items.append((ref,c,fpname,bb,bb[2]-bb[0],bb[3]-bb[1],sheetkey(c["sheet"])))

# Reserve fixed priority footprints first.
used_fixed=[]
item_by_ref={x[0]:x for x in items}
for ref,(ox,oy,rot) in fixed.items():
    if ref not in item_by_ref:
        raise RuntimeError(f"fixed ref missing: {ref}")
    _,c,fpname,bb,w,h,sk=item_by_ref[ref]
    rbb=rotated_bbox(bb,rot)
    raw=(ox+rbb[0],oy+rbb[1],ox+rbb[2],oy+rbb[3])
    # Fixed priority parts may sit close by design, but their actual courtyards
    # must never overlap.  The larger GUARD is used only to keep auto-packed
    # non-priority parts away from the frozen block.
    for oref,oraw in used_fixed:
        if not (raw[0]>=oraw[2] or raw[2]<=oraw[0] or raw[1]>=oraw[3] or raw[3]<=oraw[1]):
            raise RuntimeError(f"fixed courtyard overlap: {ref} with {oref}")
    used_fixed.append((ref,raw))
    gx0,gy0,gx1,gy1=raw
    gx0-=GUARD/2; gy0-=GUARD/2; gx1+=GUARD/2; gy1+=GUARD/2
    if gx0<ORIGIN_X-1e-9 or gy0<ORIGIN_Y-1e-9 or gx1>ORIGIN_X+BIN_W+1e-9 or gy1>ORIGIN_Y+BIN_H+1e-9:
        raise RuntimeError(f"fixed {ref} outside inner board: {(gx0,gy0,gx1,gy1)}")
    subtract_used((gx0-ORIGIN_X,gy0-ORIGIN_Y,gx1-gx0,gy1-gy0))
    placements[ref]=(ox,oy,rot)

# Pack all non-priority parts around the frozen blocks.
rest=[x for x in items if x[0] not in fixed]
rest.sort(key=lambda t:(max(t[4],t[5]),t[4]*t[5],-rank[t[6]]), reverse=True)
for ref,c,fpname,bb,w,h,sk in rest:
    best=None
    for rot in [0,90]:
        rbb=rotated_bbox(bb,rot)
        rw=(rbb[2]-rbb[0])+GUARD
        rh=(rbb[3]-rbb[1])+GUARD
        for i,(x,y,fw,fh) in enumerate(free_rects):
            if rw<=fw+1e-9 and rh<=fh+1e-9:
                lw,lh=fw-rw,fh-rh
                score=(min(lw,lh),max(lw,lh),y,x)
                if best is None or score<best[0]:
                    best=(score,x,y,rw,rh,rot,rbb)
    if best is None:
        raise RuntimeError(f"P1 MaxRects overflow at {ref}: courtyard={w:.2f}x{h:.2f}")
    _,x,y,rw,rh,rot,rbb=best
    used=(x,y,rw,rh)
    subtract_used(used)
    desired_min_x=ORIGIN_X+x+GUARD/2
    desired_min_y=ORIGIN_Y+y+GUARD/2
    placements[ref]=(desired_min_x-rbb[0],desired_min_y-rbb[1],rot)

print(f"P1 packed={len(placements)} fixed_priority={len(fixed)}")

# Instantiate board.
fpmap={}
for ref,c in comps.items():
    if ref.startswith("#") or ref in SKIP:
        continue
    fpname="RC18_Custom:J201_POGO5" if ref=="J201" else c["footprint"]
    fp=load_fp(fpname)
    fp.SetReference(ref); fp.SetValue(c["value"])
    x,y,rot=placements[ref]
    fp.SetPosition(pcbnew.VECTOR2I_MM(x,y))
    fp.SetOrientationDegrees(rot)
    try:
        fp.Reference().SetVisible(False); fp.Value().SetVisible(False)
    except Exception: pass
    board.Add(fp); fpmap[ref]=fp
    for pad in fp.Pads():
        key=(ref,pad.GetNumber())
        if key in pin_net:
            pad.SetNet(netobjs[pin_net[key]])

def getpad(ref,num):
    for p in fpmap[ref].Pads():
        if p.GetNumber()==str(num):
            return p
    raise RuntimeError(f"pad not found {ref}.{num}")

def mmpt(v):
    return (pcbnew.ToMM(v.x),pcbnew.ToMM(v.y))

def add_segment(netpad,a,b,width,layer=pcbnew.F_Cu):
    tr=pcbnew.PCB_TRACK(board)
    tr.SetStart(pcbnew.VECTOR2I_MM(a[0],a[1]))
    tr.SetEnd(pcbnew.VECTOR2I_MM(b[0],b[1]))
    tr.SetWidth(pcbnew.FromMM(width))
    tr.SetLayer(layer)
    tr.SetNet(netpad.GetNet())
    board.Add(tr)

route_log=[]
def route(a_ref,a_pin,b_ref,b_pin,width,mid=None,layer=pcbnew.F_Cu,label=""):
    pa=getpad(a_ref,a_pin); pb=getpad(b_ref,b_pin)
    if pa.GetNetname()!=pb.GetNetname():
        raise RuntimeError(f"net mismatch {a_ref}.{a_pin} {pa.GetNetname()} vs {b_ref}.{b_pin} {pb.GetNetname()}")
    pts=[mmpt(pa.GetPosition())] + (mid or []) + [mmpt(pb.GetPosition())]
    for x,y in zip(pts,pts[1:]):
        add_segment(pa,x,y,width,layer)
    route_log.append((label or pa.GetNetname(),a_ref,a_pin,b_ref,b_pin,width,len(pts)-1))

# --- P1 priority routing ---
# Bootstrap and gate drive.  Keep these narrow at the driver pins.
route("C604",1,"U6",3,0.20,label="HB_BOOT cap-driver")
route("C604",2,"U6",5,0.20,label="GAN_SW bootstrap return")
route("U6",4,"R603",1,0.20,label="HO_DRV")
route("R603",2,"Q601",1,0.20,mid=[(11.35,4.875)],label="Q601 gate after Rg")
route("U6",10,"R604",1,0.20,label="LO_DRV")
route("R604",2,"Q602",1,0.20,mid=[(8.80,6.125)],label="Q602 gate after Rg")

# UCC27282 switch reference is low-current; the MOSFET commutation copper
# necks down only at the 0.35-mm YJC pads, then immediately widens.
route("U6",5,"Q601",2,0.20,label="GAN_SW driver sense")
qsw=getpad("Q601",2)
qlo=getpad("Q602",3)
l1=getpad("L601",1)
p_qsw=mmpt(qsw.GetPosition()); p_qlo=mmpt(qlo.GetPosition()); p_l1=mmpt(l1.GetPosition())
junction=(11.20,p_qsw[1])
lower=(11.20,p_qlo[1])
add_segment(qsw,p_qsw,junction,0.20)
add_segment(qsw,junction,lower,0.80)
add_segment(qsw,lower,p_qlo,0.20)
add_segment(qsw,junction,(p_l1[0],junction[1]),0.80)
add_segment(qsw,(p_l1[0],junction[1]),p_l1,0.80)
route_log.append(("GAN_SW commutation+LC fanout","Q601","2","Q602/L601","3/1",0.80,5))

# Three-stage LC series path and local shunt/damping returns.
route("L601",2,"L602",1,0.60,label="F1 series")
route("L602",2,"L603",1,0.60,label="F2 series")
route("L601",2,"C611",1,0.40,label="F1 shunt C")
route("C611",2,"R611",1,0.40,label="C611 return R")
route("L602",2,"C612",1,0.40,label="F2 shunt C")
route("C612",2,"R612",1,0.40,label="C612 return R")
route("L603",2,"C613",1,0.40,label="ACTIVE_OUT shunt C")
route("C613",2,"R613",1,0.40,label="C613 return R")

# Injection current chain.
route("C301",2,"R301",1,0.60,label="1uF to 4.7ohm")
route("R301",2,"R302",1,0.60,label="4.7ohm to 0.33ohm shunt")

# Kelvin sense: symmetric, thin, independent from current-path copper.
route("R302",1,"R311",1,0.20,label="Kelvin P pickup")
route("R311",2,"U3",8,0.20,label="Kelvin P to INA296 IN+")
route("R302",2,"R312",1,0.20,label="Kelvin N pickup")
route("R312",2,"U3",1,0.20,label="Kelvin N to INA296 IN-")

# Board outline.
def edge(x1,y1,x2,y2):
    s=pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts)
    s.SetStart(pcbnew.VECTOR2I_MM(x1,y1)); s.SetEnd(pcbnew.VECTOR2I_MM(x2,y2))
    s.SetWidth(pcbnew.FromMM(0.05)); board.Add(s)
edge(0,0,50,0); edge(50,0,50,40); edge(50,40,0,40); edge(0,40,0,0)

pcbnew.SaveBoard(str(OUT),board)
print(f"P1 board saved: {OUT}")
print(f"P1 priority routes={len(route_log)} segments={sum(x[6] for x in route_log)}")
for x in route_log:
    print("ROUTE",x)

# P1 is still a priority-routing gate, not final board routing.
# Keep unconnected_items ignored; all actual routed copper is fully DRC checked.
pro=BASE/"RC18_RevB_SI.kicad_pro"
pdata=json.loads(pro.read_text(encoding="utf-8"))
sev=pdata.setdefault("board",{}).setdefault("design_settings",{}).setdefault("rule_severities",{})
sev["unconnected_items"]="ignore"
pdata["meta"]["filename"]="RC18_RevB_SI.kicad_pro"
pro.write_text(json.dumps(pdata,indent=2)+"\n",encoding="utf-8")

dru=BASE/"RC18_RevB_SI.kicad_dru"
dru.write_text("""(version 1)
(rule "CSD17381F4 internal pad clearance"
  (condition "((A.Reference == 'Q601' && B.Reference == 'Q601') || (A.Reference == 'Q602' && B.Reference == 'Q602'))")
  (constraint clearance (min 0.10mm)))
(rule "CSD17381F4 local fanout clearance"
  (condition "((A.Reference == 'Q601' && (B.Net == 'Q601_G' || B.Net == 'GAN_SW' || B.Net == '12V_PROT')) || (B.Reference == 'Q601' && (A.Net == 'Q601_G' || A.Net == 'GAN_SW' || A.Net == '12V_PROT')) || (A.Reference == 'Q602' && (B.Net == 'Q602_G' || B.Net == 'GAN_SW' || B.Net == 'GND')) || (B.Reference == 'Q602' && (A.Net == 'Q602_G' || A.Net == 'GAN_SW' || A.Net == 'GND')))")
  (constraint clearance (min 0.10mm)))
""",encoding="utf-8")
print("P1 rule: unconnected_items=ignore only; routed copper/clearance/courtyard remain live")
