#!/usr/bin/env python3
import csv, os, sys, importlib.util
from pathlib import Path
import pcbnew

ROOT=Path(__file__).resolve().parent
BOARD_FILE=ROOT/"RevD_G_v1_2_PCB_RC1.kicad_pcb"
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
  (fp_rect (start -2.75 -2.25) (end 2.75 2.25) (stroke (width 0.15) (type default)) (fill none) (layer "F.SilkS"))
  (fp_rect (start -3.05 -2.55) (end 3.05 2.55) (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))
  (fp_line (start -2.75 -2.25) (end -2.05 -2.25) (stroke (width 0.35) (type default)) (layer "F.SilkS"))
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

# Board outline 100 x 75 mm, origin at 0,0.
for a,b in [((0,0),(100,0)),((100,0),(100,75)),((100,75),(0,75)),((0,75),(0,0))]:
    s=pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetStart(v(*a)); s.SetEnd(v(*b)); s.SetLayer(pcbnew.Edge_Cuts)
    s.SetWidth(mm(0.1)); board.Add(s)

# 4 x 3.2 mm NPTH mounting holes, kept outside the functional zones.
for i,(x,y) in enumerate([(3.5,3.5),(96.5,3.5),(96.5,71.5),(3.5,71.5)],1):
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
"J1":(5.5,60,0),"J2":(94,12,0),"J3":(32,6,90),
"U1":(48,19,0),"U2":(17,20,0),"U3":(32,62,0),"U4":(42,60,0),"U5":(50,60,0),
"U6":(87,36,0),"U7":(82,11,0),"U8":(64,11,0),"K1":(59,61,0),"Q1":(70,60,0),"Q2":(76,60,0),
"FB101":(31,29,0),
"R101":(39,7,0),"C101":(43,7,0),"R102":(57,7,0),
"C110":(39,29,0),"C111":(43,29,0),"C112":(47,29,0),"C113":(51,29,0),"C114":(55,29,0),"C115":(34,29,0),"C116":(36.5,29,0),
"R201":(8,31,0),"C201":(12,31,0),"R202":(16,31,0),"D201":(20,31,0),"D202":(24,31,0),"R203":(11,36,0),"C203":(15,36,0),
"R210":(10,10,0),"R211":(14,10,0),"C210":(10,15,0),"C211":(14,15,0),"C212":(22,15,0),
"C301":(11,68,0),"R301":(18,68,0),"R302":(26,68,0),"R303":(31,55,0),"C303":(35,55,0),"C304":(35,68,0),
"R401":(39,51,0),"R402":(43,51,0),"R403":(47,51,0),"R404":(51,51,0),"R405":(55,51,0),"C405":(54,55,0),"C406":(57,55,0),
"C501":(12,45,0),"R501":(17,45,0),"C502":(12,50,0),"R502":(17,50,0),"C503":(12,55,0),"R503":(17,55,0),
"R601":(91,29,0),"R602":(91,32,0),"R603":(96,29,0),"R604":(96,32,0),
"C601":(87,41,0),"C602":(92,40,0),"C603":(96,40,0),"C604":(82,44,0),"C605":(87,45,0),"C606":(92,45,0),
"L601":(74,37,0),"C611":(74,43,0),"L602":(61,37,0),"C612":(61,43,0),"L603":(48,37,0),"C613":(48,43,0),
"R701":(68,52,0),"R702":(72,52,0),"D701":(62,52,0),
"L801":(76,11,0),"C801":(88,18,0),"C802":(92,18,0),"C803":(74,17,0),"C804":(70,17,0),"R805":(80,6,0),
"C901":(59,7,0),"C902":(59,15,0),"C903":(64,17,0),
"TP1":(6,46,0),"TP2":(8,38,0),"TP3":(32,72,0),"TP4":(54,64,0),"TP5":(82,37,0),
"TP6":(42,37,0),"TP7":(72,11,0),"TP8":(59,24,0),"TP9":(23,20,0),"TP10":(6,41,0)
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

# RC1b placement-clean pass: routing intentionally disabled until geometry is clean.
critical=[]
for n,a,b,w in critical:
    try: direct(n,a,b,w)
    except Exception as e: print("CRITICAL_ROUTE_SKIPPED",n,a,b,e)

# Critical shunt capacitor returns to local GND pads by direct F.Cu segments.
for c_ref in ["C611","C612","C613","C602","C603","C604","C605","C606"]:
    # Do not guess a remote star; connect only when a nearby local GND pad exists later.
    pass

# Labels/notes on User.Comments
def text(txt,x,y,size=1.2):
    d=pcbnew.PCB_TEXT(board); d.SetText(txt); d.SetPosition(v(x,y)); d.SetLayer(pcbnew.Cmts_User)
    d.SetTextSize(v(size,size)); d.SetTextThickness(mm(0.18)); board.Add(d)
text("Rev.D-G v1.2 PCB RC1 - LOW VOLTAGE ONLY",45,63,1.3)
text("U6 footprint = RAR0017B INTEGRATION DRAFT - DO NOT FABRICATE UNTIL VERIFIED",45,59.5,0.9)
text("J1/J2 Wurth body/courtyard compare pending official model",45,57.5,0.8)

pcbnew.SaveBoard(str(BOARD_FILE),board)
print("BOARD",BOARD_FILE)
print("FOOTPRINTS",len(footprints))
print("NETS",len(nets))
print("COPPER_LAYERS",board.GetCopperLayerCount())
print("SIZE_MM","100 x 75")
