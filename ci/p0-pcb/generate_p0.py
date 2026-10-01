#!/usr/bin/env python3
import sys, math, json, shutil, re, xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew

BASE = Path(sys.argv[1]).resolve()
NET = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()
SKIP = {"U901", "K301"}   # explicit DNP logical fallbacks at P0

# Install the two P0-local physical footprints needed by the board build.
for name in ["J201_POGO5.kicad_mod", "UCC27282_DRC10_TI_CANDIDATE.kicad_mod"]:
    shutil.copyfile(Path("/work/ci/p0-pcb/footprints") / name,
                    BASE / "RC18_Custom.pretty" / name)

def fp_mod_path(fpname):
    lib, name = fpname.split(":", 1)
    if lib == "RC18_Custom":
        p = BASE / "RC18_Custom.pretty" / f"{name}.kicad_mod"
        if not p.exists():
            raise RuntimeError(f"local footprint file not found: {p}")
        return p
    for root in [Path("/usr/share/kicad/footprints")]:
        p = root / f"{lib}.pretty" / f"{name}.kicad_mod"
        if p.exists():
            return p
    raise RuntimeError(f"footprint file not found: {fpname}")

def load_fp(fpname):
    p = fp_mod_path(fpname)
    fp = pcbnew.FootprintLoad(str(p.parent), p.stem)
    if fp is None:
        raise RuntimeError(f"failed footprint load: {fpname} from {p}")
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
    """Return local (xmin,ymin,xmax,ymax) from the real F.CrtYd geometry."""
    text = fp_mod_path(fpname).read_text(encoding="utf-8")
    pts=[]
    for kind in ["fp_line","fp_rect","fp_arc","fp_poly","fp_circle"]:
        pos=0
        needle=f"({kind}"
        while True:
            j=text.find(needle,pos)
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
                    r=math.hypot(ex-cx,ey-cy)
                    pts += [(cx-r,cy-r),(cx+r,cy+r)]
                    continue
            for m in re.finditer(r'\((?:start|end|mid|xy)\s+([-0-9.]+)\s+([-0-9.]+)',sb):
                pts.append((float(m.group(1)),float(m.group(2))))
    if not pts:
        # Rare fallback: use pad copper bbox and add 0.25 mm each side.
        fp=load_fp(fpname)
        xs=[]; ys=[]
        for pad in fp.Pads():
            bb=pad.GetBoundingBox()
            xs += [pcbnew.ToMM(bb.GetX()), pcbnew.ToMM(bb.GetRight())]
            ys += [pcbnew.ToMM(bb.GetY()), pcbnew.ToMM(bb.GetBottom())]
        if not xs:
            raise RuntimeError(f"no courtyard or pads: {fpname}")
        return (min(xs)-0.25,min(ys)-0.25,max(xs)+0.25,max(ys)+0.25)
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    return (min(xs),min(ys),max(xs),max(ys))

def rotated_bbox(bb, rot):
    xmin,ymin,xmax,ymax=bb
    if rot==0:
        return bb
    if rot==90:
        # KiCad board coordinates use +Y downward; +90 rotates local
        # (x,y) -> (+y,-x).
        return (ymin, -xmax, ymax, -xmin)
    raise RuntimeError(f"unsupported P0 rotation {rot}")

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

# Use actual courtyard geometry. 0.30 mm total guard = 0.15 mm beyond each
# courtyard side, in addition to the assembly allowance already in the library.
GUARD=0.30
items=[]
for ref,c in comps.items():
    if ref.startswith("#") or ref in SKIP:
        continue
    fpname="RC18_Custom:J201_POGO5" if ref=="J201" else c["footprint"]
    if not fpname:
        raise RuntimeError(f"{ref} has no footprint")
    bb=courtyard_bbox(fpname)
    w=bb[2]-bb[0]; h=bb[3]-bb[1]
    items.append((ref,c,fpname,bb,w,h,sheetkey(c["sheet"])))

BIN_W,BIN_H=48.0,38.0
ORIGIN_X,ORIGIN_Y=1.0,1.0
free_rects=[(0.0,0.0,BIN_W,BIN_H)]
placements={}

def intersects(a,b):
    ax,ay,aw,ah=a; bx,by,bw,bh=b
    return not (bx>=ax+aw or bx+bw<=ax or by>=ay+ah or by+bh<=ay)
def contains(a,b):
    ax,ay,aw,ah=a; bx,by,bw,bh=b
    return (bx>=ax-1e-9 and by>=ay-1e-9 and
            bx+bw<=ax+aw+1e-9 and by+bh<=ay+ah+1e-9)

items.sort(key=lambda t:(max(t[4],t[5]),t[4]*t[5],-rank[t[6]]), reverse=True)

for ref,c,fpname,bb,w,h,sk in items:
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
                    best=(score,i,x,y,rw,rh,rot,rbb)
    if best is None:
        raise RuntimeError(f"MaxRects overflow at {ref}: courtyard={w:.2f}x{h:.2f}")
    _,idx,x,y,rw,rh,rot,rbb=best
    used=(x,y,rw,rh)

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

    # Put the *actual courtyard bbox* inside the guarded packing rectangle.
    desired_min_x=ORIGIN_X+x+GUARD/2
    desired_min_y=ORIGIN_Y+y+GUARD/2
    origin_x=desired_min_x-rbb[0]
    origin_y=desired_min_y-rbb[1]
    placements[ref]=(origin_x,origin_y,rot)

print(f"MaxRects actual-courtyard packed={len(placements)} inner={BIN_W}x{BIN_H}mm guard={GUARD}mm")

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
    board.Add(fp)
    for pad in fp.Pads():
        key=(ref,pad.GetNumber())
        if key in pin_net:
            pad.SetNet(netobjs[pin_net[key]])

def seg(x1,y1,x2,y2):
    s=pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts)
    s.SetStart(pcbnew.VECTOR2I_MM(x1,y1)); s.SetEnd(pcbnew.VECTOR2I_MM(x2,y2))
    s.SetWidth(pcbnew.FromMM(0.05)); board.Add(s)
seg(0,0,50,0); seg(50,0,50,40); seg(50,40,0,40); seg(0,40,0,0)

pcbnew.SaveBoard(str(OUT),board)
print(f"P0 board saved: {OUT}")
print(f"placed={len(placements)} skipped_DNP={sorted(SKIP)} size=50x40mm")
for k in sheet_order:
    print(k, sum(1 for ref,c,fp,bb,w,h,sk in items if sk==k))

# Placement-stage DRC: routing is intentionally absent. Ignore only the
# unconnected-items class. All geometric, copper, mask and courtyard checks stay live.
pro=BASE/"RC18_RevB_SI.kicad_pro"
pdata=json.loads(pro.read_text(encoding="utf-8"))
sev=pdata.setdefault("board",{}).setdefault("design_settings",{}).setdefault("rule_severities",{})
sev["unconnected_items"]="ignore"
pdata["meta"]["filename"]="RC18_RevB_SI.kicad_pro"
pro.write_text(json.dumps(pdata,indent=2)+"\n",encoding="utf-8")

# CSD17381F4 YJC land pattern is a TI-recommended fine-pitch pattern with
# 0.10 mm copper spacing between pads 1 and 2. Scope the reduced rule only
# to the two physical MOSFET footprints.
dru=BASE/"RC18_RevB_SI.kicad_dru"
dru.write_text("""(version 1)
(rule "CSD17381F4 internal pad clearance"
  (condition "((A.Reference == 'Q601' && B.Reference == 'Q601') || (A.Reference == 'Q602' && B.Reference == 'Q602'))")
  (constraint clearance (min 0.10mm)))
""",encoding="utf-8")
print("P0 project: unconnected_items=ignore; CSD17381F4 internal clearance=0.10mm")
