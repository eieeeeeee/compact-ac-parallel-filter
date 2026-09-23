#!/usr/bin/env python3
import csv, os, sys, importlib.util, json
from pathlib import Path
import pcbnew

ROOT=Path(__file__).resolve().parent
BOARD_FILE=ROOT/"RevD_G_v1_2_PCB_RC13.kicad_pcb"
CUSTOM=ROOT/"RevDG.pretty"
CUSTOM.mkdir(exist_ok=True)

# Import the frozen semantic/BOM generator as the single ref/value/footprint source.
spec=importlib.util.spec_from_file_location("sem", ROOT/"generate_semantic_schematic.py")
sem=importlib.util.module_from_spec(spec); spec.loader.exec_module(sem)

# --- Custom RC1 footprints -------------------------------------------------
# J1/J2: exact 5.08-mm electrical pitch and 1.2-mm drill from the validated
# Rev.C footprint. Body outline is deliberately conservative until the
# Würth official 691253510002 KiCad model is imported/compared.
(CUSTOM/"Wurth_691253510002_RC1.kicad_mod").write_text(r'''(footprint "Wurth_691253510002_RC1"
  (version 20240108) (generator pcbnew)
  (layer "F.Cu")
  (descr "RC1 electrical footprint for Wurth 691253510002; official body/courtyard compare pending")
  (attr through_hole)
  (fp_rect (start -3.6 -5.7) (end 3.6 5.7) (stroke (width 0.25) (type default)) (fill none) (layer "F.SilkS"))
  (fp_rect (start -3.85 -5.95) (end 3.85 5.95) (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))
  (pad "1" thru_hole rect (at 0 -2.54) (size 2.4 2.4) (drill 1.2) (layers "*.Cu" "*.Mask"))
  (pad "2" thru_hole circle (at 0 2.54) (size 2.4 2.4) (drill 1.2) (layers "*.Cu" "*.Mask"))
)''',encoding="utf-8")

# TDK VLS3012CX: TDK recommended land dimensions A=1.0, B=1.0, C=3.0 mm.
# Two 1.0 x 3.0 mm lands, 1.0 mm gap -> centers +/-1.0 mm.
(CUSTOM/"L_TDK_VLS3012CX.kicad_mod").write_text(r'''(footprint "L_TDK_VLS3012CX"
  (version 20240108) (generator pcbnew)
  (layer "F.Cu")
  (descr "TDK VLS3012CX recommended land: A=1.0 B=1.0 C=3.0mm")
  (attr smd)
  (fp_rect (start -1.7 -1.7) (end 1.7 1.7) (stroke (width 0.2) (type default)) (fill none) (layer "F.SilkS"))
  (fp_rect (start -1.85 -1.85) (end 1.85 1.85) (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))
  (pad "1" smd rect (at -1 0) (size 1 3) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "2" smd rect (at 1 0) (size 1 3) (layers "F.Cu" "F.Paste" "F.Mask"))
)''',encoding="utf-8")

# U6: integration-only RC1 draft. Logical pads follow TI RAR0017B pin table.
# The exact copper/mask geometry MUST be replaced/compared against TI/Ultra
# Librarian RAR0017B before fabrication. It is intentionally named DRAFT.
(CUSTOM/"TI_RAR0017B_LMG2100_DRAFT.kicad_mod").write_text(r'''(footprint "TI_RAR0017B_LMG2100_DRAFT"
  (version 20240108) (generator pcbnew)
  (layer "F.Cu")
  (descr "DRAFT integration footprint; logical pads only; replace/verify against TI RAR0017B before fabrication")
  (attr smd)
  (fp_rect (start -3.05 -2.55) (end 3.05 2.55) (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))
  (pad "1" smd rect (at -2.35 -0.75) (size 0.70 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "2" smd rect (at -2.35 -0.25) (size 0.70 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "3" smd rect (at -2.35 0.25) (size 0.70 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "4" smd rect (at -2.35 0.75) (size 0.70 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "5" smd rect (at -1.50 1.90) (size 0.25 0.70) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "6" smd rect (at -0.50 1.90) (size 0.25 0.70) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "7" smd rect (at 0.50 1.90) (size 0.25 0.70) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "8" smd rect (at 1.50 1.90) (size 0.25 0.70) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "9" smd rect (at 2.35 0.75) (size 0.70 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "10" smd rect (at 2.35 0.25) (size 0.70 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "11" smd rect (at 2.35 -0.25) (size 0.70 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "12" smd rect (at 2.35 -0.75) (size 0.70 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "13" smd rect (at 1.50 -1.90) (size 0.25 0.70) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "14" smd rect (at 0.50 -1.90) (size 0.25 0.70) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "15" smd rect (at -0.50 -1.90) (size 0.25 0.70) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "16" smd rect (at -1.50 -1.90) (size 0.25 0.70) (layers "F.Cu" "F.Paste" "F.Mask"))
  (pad "17" smd rect (at 0 0) (size 1.70 1.70) (layers "F.Cu" "F.Paste" "F.Mask"))
)''',encoding="utf-8")

def mm(x): return pcbnew.FromMM(float(x))
def v(x,y): return pcbnew.VECTOR2I(mm(x),mm(y))

board=pcbnew.BOARD()
board.SetCopperLayerCount(4)
ds=board.GetDesignSettings()
ds.m_MinClearance=mm(0.15)
ds.m_TrackMinWidth=mm(0.15)
ds.m_HoleClearance=mm(0.20)
ds.m_CopperEdgeClearance=mm(0.25)

# RC10 board outline 120 x 85 mm. Size is intentionally relaxed until routing is proven.
for a,b in [((0,0),(120,0)),((120,0),(120,85)),((120,85),(0,85)),((0,85),(0,0))]:
    s=pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(v(*a)); s.SetEnd(v(*b)); s.SetLayer(pcbnew.Edge_Cuts)
    s.SetWidth(mm(0.1)); board.Add(s)

# 4 x 3.2 mm NPTH mounting holes, kept outside the functional zones.
for i,(x,y) in enumerate([(3.5,3.5),(116.5,3.5),(116.5,81.5),(3.5,81.5)],1):
    fp=pcbnew.FOOTPRINT(board); fp.SetReference(f"H{i}"); fp.SetValue("M3_NPTH")
    fp.SetPosition(v(x,y))
    pad=pcbnew.PAD(fp); pad.SetNumber(""); pad.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
    pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE); pad.SetSize(v(3.2,3.2)); pad.SetDrillSize(v(3.2,3.2))
    pad.SetLayerSet(pcbnew.LSET.AllCuMask()); fp.Add(pad); board.Add(fp)

# Authoritative netlist
pin_net={}; netpins={}
with (ROOT/"NETLIST_v1.2.csv").open(encoding="utf-8-sig") as f:
    rd=csv.reader(f); next(rd)
    for row in rd:
        name=row[0].strip(); netpins[name]=[]
        for p in row[1:]:
            p=p.strip()
            if p: pin_net[p]=name; netpins[name].append(p)

nets={}
for name in netpins:
    ni=pcbnew.NETINFO_ITEM(board,name); board.Add(ni); nets[name]=ni

def load_fp(fpname):
    if fpname.startswith("RevDG:"):
        lib=str(CUSTOM); name=fpname.split(":",1)[1]
    else:
        libname,name=fpname.split(":",1)
        lib=f"/usr/share/kicad/footprints/{libname}.pretty"
    fp=pcbnew.FootprintLoad(lib,name)
    if fp is None: raise RuntimeError(f"FootprintLoad failed: {fpname} ({lib})")
    return fp

# Override unresolved semantic-stage footprints with explicit RC1 integration footprints.
override={
    "J1":"RevDG:Wurth_691253510002_RC1",
    "J2":"RevDG:Wurth_691253510002_RC1",
    "U6":"RevDG:TI_RAR0017B_LMG2100_DRAFT",
    "L801":"RevDG:L_TDK_VLS3012CX",
}

# Placement (mm), grouped by function.
P={
"J1":(6,70,0),"J2":(114,12,0),"J3":(27,8,90),
"U1":(58,20,0),"U2":(18,21,0),"U3":(30,48,0),"U4":(48,54,0),"U5":(57,54,0),
"U6":(88,38,0),"U7":(103,12,0),"U8":(83,12,0),"K1":(25,72,0),"Q1":(38,68,0),"Q2":(43,68,0),
"FB101":(40,34,0),
"R101":(42,8,0),"C101":(47,8,0),"R102":(72,8,0),
"C110":(54,31,0),"C111":(58,31,0),"C112":(62,31,0),"C113":(66,31,0),"C114":(70,31,0),"C115":(45,34,0),"C116":(50,34,0),
"R201":(8,34,0),"C201":(14,34,0),"R202":(20,34,0),"D201":(26,34,0),"D202":(30,34,0),"R203":(12,40,0),"C203":(18,40,0),
"R210":(10,9,0),"R211":(16,9,0),"C210":(10,15,0),"C211":(16,15,0),"C212":(25,15,0),
"C301":(50,40,180),"R301":(38.5,40,180),"R302":(28.5,40,0),"R303":(36,46,0),"C303":(41,46,0),"C304":(30,54,0),
"R401":(52,60,0),"R402":(57,60,0),"R403":(62,60,0),"R404":(67,60,0),"R405":(72,60,0),"C405":(76,60,0),"C406":(80,60,0),
"C501":(9,46,0),"R501":(20,46,0),"C502":(9,52,0),"R502":(20,52,0),"C503":(9,58,0),"R503":(20,58,0),
"R601":(70,22.0,180),"R602":(70,16.0,180),"R603":(91,34,0),"R604":(91,43,0),
"C601":(92,38,90),"C602":(93,31,0),"C603":(97,31,0),"C604":(84,31,0),"C605":(88,31,0),"C606":(92,28,0),
"L601":(78,40,180),"C611":(78,46,0),"L602":(68.5,40,180),"C612":(68.5,46,0),"L603":(59,40,180),"C613":(59,46,0),
"R701":(36,73,0),"R702":(42,73,0),"D701":(47,72,0),
"L801":(108,12,0),"C801":(108,22,0),"C802":(114,22,0),"C803":(103,20,0),"C804":(108,20,0),"R805":(100,6,0),
"C901":(78,7,0),"C902":(83,19,0),"C903":(87,24,0),
"TP1":(15,70,0),"TP2":(8,41,0),"TP3":(39,51,0),"TP4":(61,65,0),"TP5":(82,48,0),
"TP6":(55,35,0),"TP7":(91,12,0),"TP8":(75,20,0),"TP9":(28,21,0),"TP10":(5,41,0)
}

footprints={}
for ref,info in sem.PARTS.items():
    fpname=override.get(ref,info["Footprint"])
    if not fpname:
        raise RuntimeError(f"No RC1 footprint assigned for {ref}")
    fp=load_fp(fpname)
    fp.SetReference(ref); fp.SetValue(info["Value"])
    x,y,rot=P[ref]; fp.SetPosition(v(x,y)); fp.SetOrientationDegrees(rot)
    board.Add(fp); footprints[ref]=fp
    try:
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)
    except Exception:
        pass
    # Assign nets by physical pad number.
    for pad in fp.Pads():
        full=f"{ref}.{pad.GetNumber()}"
        if full in pin_net: pad.SetNet(nets[pin_net[full]])

# Short helper for locating assigned pads.
def pad(ref,num):
    p=footprints[ref].FindPadByNumber(str(num))
    if p is None: raise RuntimeError(f"Pad missing {ref}.{num}")
    return p

def track(netname,p1,p2,width=0.25,layer=pcbnew.F_Cu):
    t=pcbnew.PCB_TRACK(board); t.SetNet(nets[netname]); t.SetLayer(layer); t.SetWidth(mm(width))
    t.SetStart(p1); t.SetEnd(p2); board.Add(t); return t

def direct(netname,a,b,width=0.25,layer=pcbnew.F_Cu):
    track(netname,pad(*a).GetPosition(),pad(*b).GetPosition(),width,layer)

# RC3: lock the topology-critical analog/power paths before autorouting.
def locked_track(netname,p1,p2,width=0.25,layer=pcbnew.F_Cu):
    t=track(netname,p1,p2,width,layer)
    t.SetLocked(True)
    return t

def locked_direct(netname,a,b,width=0.25,layer=pcbnew.F_Cu):
    return locked_track(netname,pad(*a).GetPosition(),pad(*b).GetPosition(),width,layer)

# GaN switch node and bootstrap.
# Fine-pitch U6 pins escape at 0.20 mm; copper widens only after leaving the package.
p5=pad("U6","5").GetPosition()
l1=pad("L601","1").GetPosition()
esc5=pcbnew.VECTOR2I(p5.x-mm(1.40),p5.y)
locked_track("GAN_SW",p5,esc5,0.20)
locked_track("GAN_SW",esc5,l1,0.70)
# HS is a sense/source connection: keep it narrow and local.  Freerouting completes
# the local tie to the main GAN_SW network around, not through, the package.
locked_direct("GAN_SW",("U6","11"),("C601","2"),0.18)
locked_direct("GAN_HB",("C601","1"),("U6","10"),0.18)

# Three-section reconstruction ladder.
locked_direct("GAN_F1",("L601","2"),("L602","1"),0.60)
locked_direct("GAN_F1",("C611","1"),("L601","2"),0.40)
locked_direct("GAN_F2",("L602","2"),("L603","1"),0.60)
locked_direct("GAN_F2",("C612","1"),("L602","2"),0.40)
locked_direct("ACTIVE_OUT",("L603","2"),("C301","1"),0.60)
locked_direct("ACTIVE_OUT",("C613","1"),("L603","2"),0.40)

# Physical injection path: wide after the film capacitor, but respect SMD escape geometry.
locked_direct("INJ_C_NODE",("C301","2"),("R301","1"),0.60)
locked_direct("INJ_R_NODE",("R301","2"),("R302","2"),0.60)

# Kelvin sense: independent thin traces from the shunt pads to INA240 inputs.
locked_direct("INJ_R_NODE",("R302","2"),("U3","8"),0.18)
locked_direct("INJ_LINE",("R302","1"),("U3","1"),0.18)

# Source termination only: lock the short MCU-to-resistor section.
# The longer post-resistor HI/LI runs are left to the router to avoid crossings.

# Buck local loop: lock only the noisy switching edge U7 SW -> L801.
# Keep the switching edge short and give VOS a dedicated Kelvin-like sense connection
# to the post-inductor +5V node.  This also prevents the router from leaving VOS as a stub.
locked_direct("BUCK_SW",("U7","7"),("L801","1"),0.30)
# VOS must reach the post-inductor node without crossing the SW trace/pad.
# Route upward first, then across above L801 pad 1, then down to pad 2.
_u7_vos=pad("U7","6").GetPosition()
_l801_out=pad("L801","2").GetPosition()
# Exit pin 6 horizontally first so the trace clears adjacent pin 5 (GND),
# then move above the SW/inductor region and drop onto L801 pad 2.
_vos_a=v(105.50,12.25)
_vos_b=v(105.50,14.00)
_vos_c=v(109.00,14.00)
locked_track("+5V",_u7_vos,_vos_a,0.20)
locked_track("+5V",_vos_a,_vos_b,0.20)
locked_track("+5V",_vos_b,_vos_c,0.20)
locked_track("+5V",_vos_c,_l801_out,0.20)
# Fixed-output TPS62163 EN is tied to VIN in the schematic/netlist.
locked_direct("+12V",("U7","2"),("U7","3"),0.20)

# Labels/notes on User.Comments
def text(txt,x,y,size=1.2):
    d=pcbnew.PCB_TEXT(board); d.SetText(txt); d.SetPosition(v(x,y)); d.SetLayer(pcbnew.Cmts_User)
    d.SetTextSize(v(size,size)); d.SetTextThickness(mm(0.18)); board.Add(d)
text("Rev.D-G v1.2 PCB RC13 - LOW VOLTAGE ONLY",50,82,1.3)
text("U6 RAR0017B DRAFT - RC13 routing proof only; TI official land pattern freeze pending",50,79.5,0.9)
text("J1/J2 Wurth body/courtyard compare pending official model",50,77.5,0.8)

pcbnew.SaveBoard(str(BOARD_FILE),board)
# KiCad CLI DRC reads serialized Default netclass clearance; set RC2 to 0.15 mm.
txt=BOARD_FILE.read_text(encoding="utf-8")
txt=txt.replace('(clearance 0.2)', '(clearance 0.15)', 1)
BOARD_FILE.write_text(txt,encoding="utf-8")

# KiCad 9 stores the Default netclass in the project file, not in .kicad_pcb.
# Create an RC10 project alongside the board so kicad-cli DRC uses the intended rules.
PRO_FILE=ROOT/"RevD_G_v1_2_PCB_RC13.kicad_pro"
template=ROOT.parent/"rev-c-active-shunt"/"RevC_Active_Controller_v0.3.1.kicad_pro"
with template.open(encoding="utf-8") as f:
    pro=json.load(f)
pro["boards"]=[BOARD_FILE.name]
pro["meta"]["filename"]=PRO_FILE.name
default=pro["net_settings"]["classes"][0]
default["name"]="Default"
default["clearance"]=0.15
default["track_width"]=0.25
default["via_diameter"]=0.60
default["via_drill"]=0.30
pro["net_settings"]["classes"]=[default]
pro["net_settings"]["netclass_patterns"]=[]
pro["board"]["design_settings"]["rule_severities"]["silk_overlap"]="ignore"
pro["board"]["design_settings"]["rule_severities"]["silk_over_copper"]="ignore"
pro["board"]["design_settings"]["rule_severities"]["courtyards_overlap"]="error"
with PRO_FILE.open("w",encoding="utf-8") as f:
    json.dump(pro,f,indent=2)
print("BOARD",BOARD_FILE)
print("FOOTPRINTS",len(footprints))
print("NETS",len(nets))
print("COPPER_LAYERS",board.GetCopperLayerCount())
print("SIZE_MM","120 x 85")
