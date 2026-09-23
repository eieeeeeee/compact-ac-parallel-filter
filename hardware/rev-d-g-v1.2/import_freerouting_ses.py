#!/usr/bin/env python3
import sys, re
from pathlib import Path
import pcbnew

if len(sys.argv) != 4:
    raise SystemExit("usage: import_freerouting_ses.py <input.kicad_pcb> <input.ses> <output.kicad_pcb>")

board_path=Path(sys.argv[1])
ses_path=Path(sys.argv[2])
out_path=Path(sys.argv[3])

# ---------- tiny Specctra S-expression parser ----------
def tokenize(text):
    out=[]; i=0; n=len(text)
    while i<n:
        c=text[i]
        if c.isspace():
            i+=1; continue
        if c in "()":
            out.append(c); i+=1; continue
        if c=='"':
            i+=1; s=[]
            while i<n:
                if text[i]=='\\' and i+1<n:
                    s.append(text[i+1]); i+=2; continue
                if text[i]=='"':
                    i+=1; break
                s.append(text[i]); i+=1
            out.append("".join(s)); continue
        j=i
        while j<n and (not text[j].isspace()) and text[j] not in "()":
            j+=1
        out.append(text[i:j]); i=j
    return out

def parse(tokens):
    stack=[]; root=None
    for tok in tokens:
        if tok=="(":
            node=[]
            if stack: stack[-1].append(node)
            else:
                if root is not None: raise ValueError("multiple roots")
                root=node
            stack.append(node)
        elif tok==")":
            if not stack: raise ValueError("extra )")
            stack.pop()
        else:
            if not stack: raise ValueError("atom outside list")
            stack[-1].append(tok)
    if stack: raise ValueError("unclosed (")
    return root

tree=parse(tokenize(ses_path.read_text(encoding="utf-8",errors="replace")))
if not tree or tree[0]!="session":
    raise SystemExit("not a Specctra session")

def children(node, tag):
    return [x for x in node[1:] if isinstance(x,list) and x and x[0]==tag]

def child(node, tag):
    xs=children(node,tag)
    return xs[0] if xs else None

routes=child(tree,"routes")
if routes is None: raise SystemExit("SES has no routes")
res=child(routes,"resolution")
if res is None or len(res)<3:
    raise SystemExit("SES routes has no resolution")
unit=res[1]
resolution=float(res[2])
if unit!="um":
    raise SystemExit(f"unsupported SES unit {unit}")

# Specctra (resolution um N) means N integer database units per micrometre.
# Therefore 1 coordinate unit = 1/N um = 1/(N*1000) mm.
# Example: 1085000 at resolution 10 -> 108.5 mm.
scale_mm=1.0/(resolution*1000.0)

board=pcbnew.LoadBoard(str(board_path))
if board is None: raise SystemExit("cannot load board")
netmap={n.GetNetname():n for n in board.GetNetInfo().NetsByNetcode().values()}

layer_map={
    "F.Cu":pcbnew.F_Cu,
    "In1.Cu":pcbnew.In1_Cu,
    "In2.Cu":pcbnew.In2_Cu,
    "B.Cu":pcbnew.B_Cu,
}

def mm(v): return pcbnew.FromMM(float(v))
def pos(x,y):
    # Specctra y axis is inverted relative to KiCad board coordinates.
    return pcbnew.VECTOR2I(int(mm(float(x)*scale_mm)), int(mm(-float(y)*scale_mm)))

# Replace only autorouter-owned copper.  RC3 deliberately contains locked
# topology-critical GaN/LC/Kelvin/HRTIM tracks that must survive SES import.
locked_kept=0
removed=0
for t in list(board.Tracks()):
    is_locked = bool(t.IsLocked()) if hasattr(t, "IsLocked") else False
    if is_locked:
        locked_kept += 1
    else:
        board.Remove(t)
        removed += 1
print("LOCKED_TRACKS_KEPT", locked_kept)
print("UNLOCKED_TRACKS_REMOVED", removed)

network_out=child(routes,"network_out")
if network_out is None: raise SystemExit("SES has no network_out")

track_count=0; via_count=0; net_count=0
missing_nets=[]
for net_node in children(network_out,"net"):
    if len(net_node)<2: continue
    netname=net_node[1]
    net=netmap.get(netname)
    if net is None:
        missing_nets.append(netname)
        continue
    net_count += 1
    for item in net_node[2:]:
        if not isinstance(item,list) or not item: continue
        if item[0]=="wire":
            p=child(item,"path")
            if p is None or len(p)<6: continue
            layer_name=p[1]
            if layer_name not in layer_map:
                raise SystemExit(f"unsupported layer {layer_name}")
            width_mm=float(p[2])*scale_mm
            coords=p[3:]
            if len(coords)%2:
                raise SystemExit(f"odd path coordinate count in net {netname}")
            pts=[pos(coords[i],coords[i+1]) for i in range(0,len(coords),2)]
            for a,b in zip(pts,pts[1:]):
                tr=pcbnew.PCB_TRACK(board)
                tr.SetNet(net)
                tr.SetLayer(layer_map[layer_name])
                tr.SetWidth(mm(width_mm))
                tr.SetStart(a); tr.SetEnd(b)
                board.Add(tr); track_count+=1
        elif item[0]=="via":
            # (via "Via[0-3]_600:300_um" x y ...)
            if len(item)<4: continue
            stack=item[1]
            x,y=item[2],item[3]
            m=re.search(r'_([0-9.]+):([0-9.]+)_um$',stack)
            if m:
                dia_mm=float(m.group(1))/1000.0
                drill_mm=float(m.group(2))/1000.0
            else:
                dia_mm=0.60; drill_mm=0.30
            v=pcbnew.PCB_VIA(board)
            v.SetNet(net)
            v.SetPosition(pos(x,y))
            v.SetWidth(mm(dia_mm))
            v.SetDrill(mm(drill_mm))
            v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu)
            board.Add(v); via_count+=1

if missing_nets:
    raise SystemExit("SES nets missing on KiCad board: "+", ".join(missing_nets))

# Board design rules are supplied by the paired .kicad_pro and validated by kicad-cli DRC.
# Do not mutate the SWIG design-settings object here; its Python API shape varies across KiCad builds.
pcbnew.SaveBoard(str(out_path),board)
print("SES_MANUAL_IMPORT_OK")
print("NETS_IMPORTED",net_count)
print("TRACK_SEGMENTS",track_count)
print("VIAS",via_count)
print("OUTPUT",out_path)
