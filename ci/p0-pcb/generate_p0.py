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
shutil.copy2(j201_src, j201_dst)

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

# Functional sheet order; placement is globally shelf-packed inside the
# 50 x 40 mm board so unused area can be shared between blocks.
sheet_order = [
    "01_POWER_INPUT","02_POWER_RAILS","03_MCU_DIGITAL",
    "04_VLINE_ANALOG","05_CURRENT_SENSE_TRIP","06_SI_HALFBRIDGE",
    "07_RECONSTRUCTION_LC","08_INJECTION_DISCONNECT","09_MONITOR_THERMAL_UI"
]
def sheetkey(s):
    for k in sheet_order:
        if k in s: return k
    return "09_MONITOR_THERMAL_UI"

# Approximate courtyard envelopes by footprint family.
# Values include a small assembly margin; KiCad DRC is the final authority.
def env(fpname, ref):
    if ref == "J201": return (6.5, 2.0)
    s = fpname.lower()
    if "jst_xh" in s: return (5.2, 6.5)
    if "lqfp-48" in s: return (9.5, 9.5)
    if "crystal_smd_3225" in s: return (4.0, 3.5)
    if "sma" in s: return (6.0, 3.5)
    if "2512" in s: return (7.0, 3.0)
    if "1206" in s: return (4.0, 2.1)
    if "0805" in s: return (3.0, 1.9)
    if "sot-23" in s: return (3.2, 3.0)
    if "msop" in s or "vssop" in s or "ucc27282" in s: return (6.5, 3.5)
    if "csd17381" in s: return (1.8, 1.4)
    if "l_1008" in s: return (4.0, 2.6)
    if "sod-123" in s: return (4.0, 2.5)
    if "rect_l7" in s: return (8.0, 3.5)
    return (2.4, 1.5)

groups = {k:[] for k in sheet_order}
for ref,c in comps.items():
    if ref.startswith("#") or ref in SKIP:
        continue
    fpname = c["footprint"]
    if ref == "J201":
        fpname = "RC18_Custom:J201_POGO5"
    if not fpname:
        raise RuntimeError(f"{ref} has no footprint")
    k = sheetkey(c["sheet"])
    w,h = env(fpname, ref)
    groups[k].append((ref, c, fpname, w, h))
for k in groups:
    groups[k].sort(key=lambda z: (-(z[3]*z[4]), -max(z[3],z[4]), z[0]))

# MaxRects-style placement on the front side.  Items are processed in functional
# sheet order and large-first within each block.  0.22 mm pack gap + 0.7 mm edge margin.
free_rects = [(0.7, 0.7, 48.6, 38.6)]  # x,y,w,h
placements = {}
gap = 0.22

def intersects(a,b):
    ax,ay,aw,ah=a; bx,by,bw,bh=b
    return not (bx >= ax+aw or bx+bw <= ax or by >= ay+ah or by+bh <= ay)

def contained(a,b):
    ax,ay,aw,ah=a; bx,by,bw,bh=b
    return ax >= bx-1e-9 and ay >= by-1e-9 and ax+aw <= bx+bw+1e-9 and ay+ah <= by+bh+1e-9

def split_free(used):
    global free_rects
    ux,uy,uw,uh=used
    out=[]
    for fr in free_rects:
        if not intersects(fr, used):
            out.append(fr); continue
        fx,fy,fw,fh=fr
        if ux > fx:
            out.append((fx,fy,ux-fx,fh))
        if ux+uw < fx+fw:
            out.append((ux+uw,fy,fx+fw-(ux+uw),fh))
        if uy > fy:
            out.append((fx,fy,fw,uy-fy))
        if uy+uh < fy+fh:
            out.append((fx,uy+uh,fw,fy+fh-(uy+uh)))
    out=[r for r in out if r[2] > 0.15 and r[3] > 0.15]
    pruned=[]
    for i,r in enumerate(out):
        if any(i!=j and contained(r,q) for j,q in enumerate(out)):
            continue
        pruned.append(r)
    free_rects=pruned

for k in sheet_order:
    for ref,c,fpname,w,h in groups[k]:
        choices=[]
        for i,(fx,fy,fw,fh) in enumerate(free_rects):
            for rot,(rw,rh) in [(0,(w,h)),(90,(h,w))]:
                pw,ph=rw+gap,rh+gap
                if pw <= fw+1e-9 and ph <= fh+1e-9:
                    short=min(fw-pw,fh-ph)
                    long=max(fw-pw,fh-ph)
                    choices.append((short,long,fy,fx,i,rot,rw,rh,pw,ph))
        if not choices:
            raise RuntimeError(f"MaxRects placement overflow at {ref}; free={len(free_rects)}")
        _,_,fy,fx,i,rot,rw,rh,pw,ph=min(choices)
        placements[ref]=(fx+rw/2, fy+rh/2, rot)
        split_free((fx,fy,pw,ph))

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
for k in zones:
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
pdata["meta"]["filename"] = "RC18_RevB_SI.kicad_pro"
pro.write_text(json.dumps(pdata, indent=2) + "\n", encoding="utf-8")
print("P0 project rule: unconnected_items=ignore (placement gate only)")
