#!/usr/bin/env python3
import sys, os, math, xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew

BASE = Path(sys.argv[1]).resolve()
NET = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()

# P0 placement gate: DNP logical fallback devices without production-ready
# physical mapping stay out of the board for this pass. J201 gets a real pogo pad array.
SKIP = {"U901", "K301"}

def load_fp(fpname):
    lib, name = fpname.split(":", 1)
    if lib == "RC18_Custom":
        libpath = str(BASE / "RC18_Custom.pretty")
    else:
        candidates = [
            Path("/usr/share/kicad/footprints") / (lib + ".pretty"),
            Path("/usr/share/kicad/footprints") / lib,
        ]
        libpath = None
        for c in candidates:
            if c.exists():
                libpath = str(c); break
        if not libpath:
            raise RuntimeError(f"footprint lib not found: {lib}")
    fp = pcbnew.FootprintLoad(libpath, name)
    if fp is None:
        raise RuntimeError(f"failed footprint load: {fpname} from {libpath}")
    return fp

# J201 is loaded from a project-local .kicad_mod to avoid SWIG constructor differences.

# Install P0-only J201 footprint into the project-local footprint library.
import shutil
j201_src = Path("/work/ci/p0-pcb/footprints/J201_POGO5.kicad_mod")
j201_dst = BASE / "RC18_Custom.pretty" / "J201_POGO5.kicad_mod"
shutil.copyfile(j201_src, j201_dst)
ucc_src = Path("/work/ci/p0-pcb/footprints/UCC27282_DRC10_TI_CANDIDATE.kicad_mod")
ucc_dst = BASE / "RC18_Custom.pretty" / "UCC27282_DRC10_TI_CANDIDATE.kicad_mod"
shutil.copyfile(ucc_src, ucc_dst)

tree = ET.parse(NET)
root = tree.getroot()
comps = {}
for c in root.find("components"):
    ref = c.attrib["ref"]
    value = c.findtext("value") or ""
    footprint = c.findtext("footprint") or ""
    sp = c.find("sheetpath")
    sheet = sp.attrib.get("names","") if sp is not None else ""
    comps[ref] = {"value":value, "footprint":footprint, "sheet":sheet}

# Build net membership pin map.
nets = []
pin_net = {}
for n in root.find("nets"):
    name = n.attrib.get("name","")
    if not name:
        name = f"N-{n.attrib.get('code','0')}"
    nets.append(name)
    for node in n.findall("node"):
        pin_net[(node.attrib["ref"], node.attrib["pin"])] = name

board = pcbnew.BOARD()
try:
    board.SetCopperLayerCount(4)
except Exception:
    pass
ds = board.GetDesignSettings()
try:
    ds.SetBoardThickness(pcbnew.FromMM(1.6))
except Exception:
    pass

# nets
netobjs = {}
for name in sorted(set(nets)):
    ni = pcbnew.NETINFO_ITEM(board, name)
    board.Add(ni)
    netobjs[name] = ni

# Functional sheet order is retained as metadata, but P0 packing uses a
# MaxRects best-short-side-fit solver so the 50 x 40 mm board area is used
# efficiently. Rotation by 90 degrees is permitted.
sheet_order = [
    "01_POWER_INPUT","02_POWER_RAILS","03_MCU_DIGITAL",
    "04_VLINE_ANALOG","05_CURRENT_SENSE_TRIP","06_SI_HALFBRIDGE",
    "07_RECONSTRUCTION_LC","08_INJECTION_DISCONNECT","09_MONITOR_THERMAL_UI"
]
def sheetkey(s):
    for k in sheet_order:
        if k in s: return k
    return "09_MONITOR_THERMAL_UI"

# Conservative placement envelopes, roughly courtyard-sized.  A further
# 0.25 mm total guard is added to each rectangle before packing.
def env(fpname, ref):
    if ref == "J201": return (7.2, 1.8)
    s = fpname.lower()
    if "jst_xh" in s: return (6.5, 6.0)
    if "lqfp-48" in s: return (9.5, 9.5)
    if "3225" in s: return (4.0, 3.3)
    if "d_sma" in s: return (6.0, 3.8)
    if "2512" in s: return (7.0, 3.7)
    if "1206" in s: return (4.0, 2.5)
    if "0805" in s: return (3.1, 2.0)
    if "0603" in s: return (2.5, 1.6)
    if "sot-23" in s: return (3.4, 3.2)
    if "msop" in s or "vssop" in s or "ucc27282" in s: return (7.0, 3.8)
    if "csd17381" in s: return (1.8, 1.3)
    if "l_1008" in s: return (4.0, 3.0)
    if "sod-123" in s: return (4.5, 2.5)
    if "rect_l7" in s: return (8.0, 3.5)
    return (3.0, 2.0)

items = []
for ref,c in comps.items():
    if ref.startswith("#") or ref in SKIP:
        continue
    fpname = c["footprint"]
    if ref == "J201":
        fpname = "RC18_Custom:J201_POGO5"
    if not fpname:
        raise RuntimeError(f"{ref} has no footprint")
    w,h = env(fpname, ref)
    # packing rectangle adds 0.25 mm guard; actual footprint is centered inside.
    items.append((ref, c, fpname, w + 0.25, h + 0.25, sheetkey(c["sheet"])))

# MaxRects Best Short Side Fit in the 48 x 38 mm inner board region.
BIN_W, BIN_H = 48.0, 38.0
ORIGIN_X, ORIGIN_Y = 1.0, 1.0
free_rects = [(0.0, 0.0, BIN_W, BIN_H)]
placements = {}

def intersects(a,b):
    ax,ay,aw,ah=a; bx,by,bw,bh=b
    return not (bx >= ax+aw or bx+bw <= ax or by >= ay+ah or by+bh <= ay)

def contains(a,b):
    ax,ay,aw,ah=a; bx,by,bw,bh=b
    return (bx >= ax-1e-9 and by >= ay-1e-9 and
            bx+bw <= ax+aw+1e-9 and by+bh <= ay+ah+1e-9)

# Large-first; sheet order is the deterministic tie-breaker.
rank = {k:i for i,k in enumerate(sheet_order)}
items.sort(key=lambda t: (max(t[3],t[4]), t[3]*t[4], -rank[t[5]]), reverse=True)

for ref,c,fpname,w,h,sk in items:
    best = None
    candidates = [(w,h,0)]
    if abs(w-h) > 1e-9:
        candidates.append((h,w,90))
    for i,(x,y,fw,fh) in enumerate(free_rects):
        for rw,rh,rot in candidates:
            if rw <= fw+1e-9 and rh <= fh+1e-9:
                lw,lh = fw-rw, fh-rh
                score = (min(lw,lh), max(lw,lh), y, x)
                if best is None or score < best[0]:
                    best = (score,i,x,y,rw,rh,rot)
    if best is None:
        raise RuntimeError(f"MaxRects overflow at {ref}: envelope={w:.2f}x{h:.2f}")
    _,idx,x,y,rw,rh,rot = best
    used = (x,y,rw,rh)

    new_free=[]
    for fr in free_rects:
        if not intersects(fr, used):
            new_free.append(fr)
            continue
        fx,fy,fw,fh=fr; ux,uy,uw,uh=used
        if ux > fx: new_free.append((fx,fy,ux-fx,fh))
        if ux+uw < fx+fw: new_free.append((ux+uw,fy,fx+fw-(ux+uw),fh))
        if uy > fy: new_free.append((fx,fy,fw,uy-fy))
        if uy+uh < fy+fh: new_free.append((fx,uy+uh,fw,fy+fh-(uy+uh)))

    # Remove free rectangles fully contained by another free rectangle.
    pruned=[]
    for ii,ra in enumerate(new_free):
        if any(ii != jj and contains(rb,ra) for jj,rb in enumerate(new_free)):
            continue
        pruned.append(ra)
    free_rects = pruned

    # Actual footprint center is the center of the guarded rectangle.
    placements[ref] = (ORIGIN_X+x+rw/2, ORIGIN_Y+y+rh/2, rot)

max_x=max(placements[r][0] for r in placements)
print(f"MaxRects packed={len(placements)} inner={BIN_W}x{BIN_H}mm")

# Create and place footprints, assign nets.
for ref,c in comps.items():
    if ref.startswith("#") or ref in SKIP:
        continue
    if ref == "J201":
        fp=load_fp("RC18_Custom:J201_POGO5")
    else:
        fp=load_fp(c["footprint"])
    fp.SetReference(ref)
    fp.SetValue(c["value"])
    x,y,rot = placements[ref]
    fp.SetPosition(pcbnew.VECTOR2I_MM(x,y))
    fp.SetOrientationDegrees(rot)
    # Reduce reference/value text footprint in this dense P0.
    try:
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)
    except Exception:
        pass
    board.Add(fp)
    for pad in fp.Pads():
        key=(ref,pad.GetNumber())
        if key in pin_net:
            pad.SetNet(netobjs[pin_net[key]])

# Board outline 50 x 40 mm.
def seg(x1,y1,x2,y2):
    s=pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetLayer(pcbnew.Edge_Cuts)
    s.SetStart(pcbnew.VECTOR2I_MM(x1,y1))
    s.SetEnd(pcbnew.VECTOR2I_MM(x2,y2))
    s.SetWidth(pcbnew.FromMM(0.05))
    board.Add(s)
seg(0,0,50,0); seg(50,0,50,40); seg(50,40,0,40); seg(0,40,0,0)

pcbnew.SaveBoard(str(OUT), board)
print(f"P0 board saved: {OUT}")
print(f"placed={len(placements)} skipped_DNP={sorted(SKIP)} size=50x40mm")
for k in sheet_order:
    print(k, len(groups[k]))

# Placement-stage project rule: routing is intentionally not present yet.
# Ignore only unconnected-items for P0; all geometric/clearance/courtyard rules remain active.
import json
pro = BASE / "RC18_RevB_SI.kicad_pro"
pdata = json.loads(pro.read_text(encoding="utf-8"))
boardcfg = pdata.setdefault("board", {})
dsgn = boardcfg.setdefault("design_settings", {})
sev = dsgn.setdefault("rule_severities", {})
sev["unconnected_items"] = "ignore"
# Fine-pitch parts in this design (notably CSD17381F4) require 0.10 mm copper clearance.
for cls in pdata.setdefault("net_settings", {}).setdefault("classes", []):
    if cls.get("name") == "Default":
        cls["clearance"] = 0.10
pdata["meta"]["filename"] = "RC18_RevB_SI.kicad_pro"
pro.write_text(json.dumps(pdata, indent=2) + "\n", encoding="utf-8")
print("P0 project rule: unconnected_items=ignore (placement gate only)")
