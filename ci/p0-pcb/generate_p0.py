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

def make_pogo5():
    fp = pcbnew.FOOTPRINT()
    fp.SetReference("J201")
    fp.SetValue("SWD POGO 5")
    # 1.27 mm pitch, five round SMD contact pads, total length 5.08 mm.
    for i in range(5):
        p = pcbnew.PAD(fp)
        p.SetNumber(str(i+1))
        p.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
        p.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        p.SetSize(pcbnew.VECTOR2I_MM(1.4, 1.4))
        p.SetPosition(pcbnew.VECTOR2I_MM((i-2)*1.27, 0))
        p.SetLayerSet(pcbnew.LSET(pcbnew.F_Cu, pcbnew.F_Paste, pcbnew.F_Mask))
        fp.Add(p)
    return fp

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

# zone allocations in millimeters inside a 50 x 40 board.
zones = {
    "01_POWER_INPUT": (1.2, 1.2, 12.0, 11.5),
    "02_POWER_RAILS": (12.2, 1.2, 23.5, 11.5),
    "03_MCU_DIGITAL": (23.7, 1.2, 38.2, 15.5),
    "04_VLINE_ANALOG": (1.2, 11.7, 13.5, 23.5),
    "05_CURRENT_SENSE_TRIP": (13.7, 15.7, 25.0, 27.0),
    "06_SI_HALFBRIDGE": (25.2, 15.7, 39.0, 28.8),
    "07_RECONSTRUCTION_LC": (1.2, 27.2, 25.0, 38.8),
    "08_INJECTION_DISCONNECT": (25.2, 29.0, 39.0, 38.8),
    "09_MONITOR_THERMAL_UI": (39.2, 1.2, 48.8, 38.8),
}
def sheetkey(s):
    for k in zones:
        if k in s: return k
    return "09_MONITOR_THERMAL_UI"

# Approximate placement envelopes by footprint family, intentionally conservative.
def env(fpname, ref):
    if ref == "J201": return (8.0, 2.2)
    s = fpname.lower()
    if "jst_xh" in s: return (6.0, 7.0)
    if "lqfp-48" in s: return (10.0, 10.0)
    if "crystal_smd_3225" in s: return (4.5, 4.0)
    if "sma" in s: return (6.0, 4.0)
    if "2512" in s: return (7.0, 4.0)
    if "1206" in s: return (4.0, 2.8)
    if "0805" in s: return (3.4, 2.5)
    if "sot-23" in s: return (3.5, 3.4)
    if "msop" in s or "vssop" in s or "ucc27282" in s: return (7.2, 4.3)
    if "csd17381" in s: return (2.2, 1.8)
    if "l_1008" in s: return (4.3, 3.2)
    if "sod-123" in s: return (4.5, 3.0)
    if "rect_l7" in s: return (8.0, 4.0)
    return (2.8, 2.2)

# Group components and sort large-first to reduce overlap.
groups = {k:[] for k in zones}
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
    groups[k].append((-(w*h), ref, c, fpname, w, h))
for k in groups:
    groups[k].sort()

# Shelf pack within each functional zone.
placements = {}
for k, items in groups.items():
    x0,y0,x1,y1 = zones[k]
    x=x0; y=y0; rowh=0
    for _,ref,c,fpname,w,h in items:
        if x + w > x1:
            x=x0; y += rowh + 0.35; rowh=0
        if y + h > y1 + 1e-6:
            raise RuntimeError(f"zone overflow {k} at {ref}: y={y:.2f}, h={h:.2f}, ymax={y1:.2f}")
        placements[ref] = (x+w/2, y+h/2, 0)
        x += w + 0.35
        rowh=max(rowh,h)

# Create and place footprints, assign nets.
for ref,c in comps.items():
    if ref.startswith("#") or ref in SKIP:
        continue
    if ref == "J201":
        fp=make_pogo5()
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
