#!/usr/bin/env python3
import csv, os, sys, importlib.util, json
from pathlib import Path
import pcbnew

ROOT=Path(__file__).resolve().parent
BOARD_FILE=ROOT/"RevD_G_v1_2_PCB_RC18_COST_MAX_S2C.kicad_pcb"
CUSTOM=ROOT/"RevDG.pretty"
CUSTOM.mkdir(exist_ok=True)

# Import the frozen semantic/BOM generator as the single ref/value/footprint source.
spec=importlib.util.spec_from_file_location("sem", ROOT/"generate_semantic_schematic.py")
sem=importlib.util.module_from_spec(spec); spec.loader.exec_module(sem)

# RC18-COST-MAX Stage 2C:
# same STM32G474 silicon family, LQFP64 pinout and 170 MHz/HRTIM/analog features;
# keep 256 KiB Flash and the same LQFP64 electrical topology; RCT3 raises the rated ambient temperature ceiling to 125 C.
sem.PARTS["U1"]["Value"]="STM32G474RCT3"
sem.PARTS["U6"]={"Value":"LMG1205","Footprint":"RevDG:TI_YFX0012_LMG1205"}
sem.PARTS["Q3"]={"Value":"IRLHS6376","Footprint":"RevDG:Infineon_PG_TSDSON_6_900_IRLHS6376"}

# --- Custom RC18 footprints -------------------------------------------------
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

# U6: TI LMG1205 YFX0012.  TI 4215094/B specifies a 0.4-mm grid,
# 0.225-mm preferred NSMD copper lands and 0.25-mm stencil apertures.
(CUSTOM/"TI_YFX0012_LMG1205.kicad_mod").write_text(r'''(footprint "TI_YFX0012_LMG1205"
  (version 20240108) (generator pcbnew)
  (layer "F.Cu")
  (descr "TI LMG1205 YFX0012; 0.4mm grid; 0.225mm NSMD land; TI 4215094/B")
  (attr smd)
  (fp_rect (start -0.88 -0.96) (end 0.88 0.96)
    (stroke (width 0.10) (type default)) (fill none) (layer "F.Fab"))
  (fp_rect (start -1.10 -1.15) (end 1.10 1.15)
    (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))
  (pad "A1" smd circle (at -0.6 -0.6) (size 0.225 0.225) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (solder_paste_margin 0.0125))
  (pad "A2" smd circle (at -0.2 -0.6) (size 0.225 0.225) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (solder_paste_margin 0.0125))
  (pad "A3" smd circle (at 0.2 -0.6) (size 0.225 0.225) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (solder_paste_margin 0.0125))
  (pad "A4" smd circle (at 0.6 -0.6) (size 0.225 0.225) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (solder_paste_margin 0.0125))
  (pad "B1" smd circle (at -0.6 -0.2) (size 0.225 0.225) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (solder_paste_margin 0.0125))
  (pad "B4" smd circle (at 0.6 -0.2) (size 0.225 0.225) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (solder_paste_margin 0.0125))
  (pad "C1" smd circle (at -0.6 0.2) (size 0.225 0.225) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (solder_paste_margin 0.0125))
  (pad "C4" smd circle (at 0.6 0.2) (size 0.225 0.225) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (solder_paste_margin 0.0125))
  (pad "D1" smd circle (at -0.6 0.6) (size 0.225 0.225) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (solder_paste_margin 0.0125))
  (pad "D2" smd circle (at -0.2 0.6) (size 0.225 0.225) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (solder_paste_margin 0.0125))
  (pad "D3" smd circle (at 0.2 0.6) (size 0.225 0.225) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (solder_paste_margin 0.0125))
  (pad "D4" smd circle (at 0.6 0.6) (size 0.225 0.225) (layers "F.Cu" "F.Paste" "F.Mask") (solder_mask_margin 0.05) (solder_paste_margin 0.0125))
)''',encoding="utf-8")

# Q3: Infineon IRLHS6376, PG-TSDSON-6-900 (PQFN Dual 2x2).
# Edge terminals follow the official 0.65-mm pitch package.  The duplicated
# drain lands model the two bottom drain contacts.  This is an RC18 routing
# candidate; stencil segmentation remains a fabrication-stage audit item.
(CUSTOM/"Infineon_PG_TSDSON_6_900_IRLHS6376.kicad_mod").write_text(r'''(footprint "Infineon_PG_TSDSON_6_900_IRLHS6376"
  (version 20240108) (generator pcbnew)
  (layer "F.Cu")
  (descr "IRLHS6376 PG-TSDSON-6-900 / PQFN Dual 2x2; official Infineon package geometry")
  (attr smd)
  (fp_rect (start -1 -1) (end 1 1)
    (stroke (width 0.10) (type default)) (fill none) (layer "F.Fab"))
  (fp_rect (start -1.20 -1.20) (end 1.20 1.20)
    (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))
  (pad "4" smd roundrect (at -0.65 -0.735) (size 0.23 0.50) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.18) (solder_mask_margin 0.025))
  (pad "5" smd roundrect (at 0 -0.735) (size 0.23 0.50) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.18) (solder_mask_margin 0.025))
  (pad "6" smd roundrect (at 0.65 -0.735) (size 0.23 0.50) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.18) (solder_mask_margin 0.025))
  (pad "3" smd roundrect (at -0.65 0.735) (size 0.23 0.50) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.18) (solder_mask_margin 0.025))
  (pad "2" smd roundrect (at 0 0.735) (size 0.23 0.50) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.18) (solder_mask_margin 0.025))
  (pad "1" smd roundrect (at 0.65 0.735) (size 0.23 0.50) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.18) (solder_mask_margin 0.025))
  (pad "3" smd roundrect (at -0.45 0) (size 0.65 0.90) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.08) (solder_mask_margin 0.025))
  (pad "6" smd roundrect (at 0.45 0) (size 0.65 0.90) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.08) (solder_mask_margin 0.025))
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
with (ROOT/"NETLIST_RC18_COST_MAX_S2.csv").open(encoding="utf-8-sig") as f:
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
    "U6":"RevDG:TI_YFX0012_LMG1205",
    "Q3":"RevDG:Infineon_PG_TSDSON_6_900_IRLHS6376",
    "L801":"RevDG:L_TDK_VLS3012CX",
}

# Placement (mm), grouped by function.
P={
"J1":(6,70,0),"J2":(114,12,0),"J3":(27,8,90),
"U1":(58,20,0),"U2":(18,21,0),"U3":(30,48,0),"U4":(48,54,0),"U5":(57,54,0),
"U6":(90.2,38.0,0),"Q3":(88.0,38.0,0),"U7":(103,12,0),"U8":(83,12,0),"K1":(25,72,0),"Q1":(38,68,0),"Q2":(43,68,0),
"FB101":(40,34,0),
"R101":(42,8,0),"C101":(47,8,0),"R102":(72,8,0),
"C110":(54,31,0),"C111":(58,31,0),"C112":(62,31,0),"C113":(66,31,0),"C114":(70,31,0),"C115":(45,34,0),"C116":(50,34,0),
"R201":(8,34,0),"C201":(14,34,0),"R202":(20,34,0),"D201":(26,34,0),"D202":(30,34,0),"R203":(12,40,0),"C203":(18,40,0),
"R210":(10,9,0),"R211":(16,9,0),"C210":(10,15,0),"C211":(16,15,0),"C212":(25,15,0),
"C301":(50,40,180),"R301":(38.5,40,180),"R302":(28.5,40,0),"R303":(36,46,0),"C303":(41,46,0),"C304":(30,54,0),
"R401":(52,60,0),"R402":(57,60,0),"R403":(62,60,0),"R404":(67,60,0),"R405":(72,60,0),"C405":(76,60,0),"C406":(80,60,0),
"C501":(9,46,0),"R501":(20,46,0),"C502":(9,52,0),"R502":(20,52,0),"C503":(9,58,0),"R503":(20,58,0),
"R601":(70,22.0,180),"R602":(70,16.0,180),"R603":(93.0,36.0,0),"R604":(93.0,40.0,0),
"C601":(90.7,40.0,0),"C602":(90.2,35.5,180),"C603":(92.2,34.5,0),"C604":(85.2,35.5,0),"C605":(85.2,40.5,0),"C606":(85.5,38.0,90),
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

# Stage 2C half bridge: LMG1205 driver + IRLHS6376 dual MOSFET.
# Keep the actual power loop deterministic and compact.
_q1=pad("Q3","1").GetPosition()
_q3=pad("Q3","3").GetPosition()
_sw1=v(88.65,39.55)
_sw2=v(87.35,39.55)
locked_track("GAN_SW",_q1,_sw1,0.25)
locked_track("GAN_SW",_sw1,_sw2,0.50)
locked_track("GAN_SW",_sw2,_q3,0.25)
locked_track("GAN_SW",_sw2,pad("L601","1").GetPosition(),0.70)

# Split source/sink outputs are joined only at each MOSFET gate.
locked_direct("GAN_HG",("U6","D1"),("U6","D2"),0.15)
_hg0=pad("U6","D2").GetPosition()
_hg1=v(89.2,38.75)
locked_track("GAN_HG",_hg0,_hg1,0.15)
locked_track("GAN_HG",_hg1,pad("Q3","2").GetPosition(),0.18)

locked_direct("GAN_LG",("U6","A1"),("U6","B1"),0.15)
_lg0=pad("U6","B1").GetPosition()
_lg1=v(89.2,37.25)
locked_track("GAN_LG",_lg0,_lg1,0.15)
locked_track("GAN_LG",_lg1,pad("Q3","5").GetPosition(),0.18)

# Bootstrap and local supply bypass.
locked_direct("GAN_HB",("U6","D3"),("C601","1"),0.15)
locked_direct("GAN_SW",("U6","D4"),("C601","2"),0.15)
locked_direct("+5V",("U6","A3"),("C602","1"),0.15)
locked_direct("GND",("U6","A2"),("C602","2"),0.15)

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
# Only escape the fine-pitch VOS pin into open routing space.
# Freerouting then joins this stub to the post-inductor +5V network.
# Keeping this short avoids creating a fixed +5V island around the BUCK_SW trace.
_vos_a=v(104.60,12.25)
_vos_b=v(104.60,14.00)
locked_track("+5V",_u7_vos,_vos_a,0.20)
locked_track("+5V",_vos_a,_vos_b,0.20)

# U4 pad 2 (VTH_HI) is a fine-pitch VSSOP pad that Freerouting can
# occasionally leave isolated. Give it a short deterministic outward escape
# and a fixed via; the autorouter completes the remainder of the same VTH_HI net.
_u4_vth=pad("U4","2").GetPosition()
_vth_escape=v(44.80,53.675)
locked_track("VTH_HI",_u4_vth,_vth_escape,0.18)
_vth_via=pcbnew.PCB_VIA(board)
_vth_via.SetNet(nets["VTH_HI"])
_vth_via.SetPosition(_vth_escape)
_vth_via.SetWidth(mm(0.60))
_vth_via.SetDrill(mm(0.30))
_vth_via.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu)
_vth_via.SetLocked(True)
board.Add(_vth_via)

# U1 pin47 (VSS) was the remaining inaccessible MCU ground pad in RC14.
# Give it a short outward escape and let Freerouting join it to the GND network.
_u1_g47=pad("U1","47").GetPosition()
_g47_escape=v(65.20,16.75)
locked_track("GND",_u1_g47,_g47_escape,0.20)
# Terminate the fine-pitch escape in a fixed through-via so the autorouter can
# reach this MCU ground from either inner copper layer instead of treating the
# F.Cu stub as an isolated endpoint.
_g47_via=pcbnew.PCB_VIA(board)
_g47_via.SetNet(nets["GND"])
_g47_via.SetPosition(_g47_escape)
_g47_via.SetWidth(mm(0.60))
_g47_via.SetDrill(mm(0.30))
_g47_via.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu)
_g47_via.SetLocked(True)
board.Add(_g47_via)
# Fixed-output TPS62163 EN is tied to VIN in the schematic/netlist.
locked_direct("+12V",("U7","2"),("U7","3"),0.20)

# Labels/notes on User.Comments
def text(txt,x,y,size=1.2):
    d=pcbnew.PCB_TEXT(board); d.SetText(txt); d.SetPosition(v(x,y)); d.SetLayer(pcbnew.Cmts_User)
    d.SetTextSize(v(size,size)); d.SetTextThickness(mm(0.18)); board.Add(d)
text("Rev.D-G RC18-COST-MAX S2C - LOW VOLTAGE ONLY",50,82,1.3)
text("S2C: LMG1205 + IRLHS6376 candidate power stage; transient/bench qualification pending",50,79.5,0.9)
text("J1/J2 Wurth body/courtyard compare pending official model",50,77.5,0.8)

pcbnew.SaveBoard(str(BOARD_FILE),board)
# KiCad CLI DRC reads serialized Default netclass clearance; set RC2 to 0.15 mm.
txt=BOARD_FILE.read_text(encoding="utf-8")
txt=txt.replace('(clearance 0.2)', '(clearance 0.15)', 1)
BOARD_FILE.write_text(txt,encoding="utf-8")

# KiCad 9 stores the Default netclass in the project file, not in .kicad_pcb.
# Create an RC18 Stage-2C project alongside the board so kicad-cli DRC uses the intended rules.
PRO_FILE=ROOT/"RevD_G_v1_2_PCB_RC18_COST_MAX_S2C.kicad_pro"
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
