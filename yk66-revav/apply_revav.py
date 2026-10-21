#!/usr/bin/env python3
"""Generate Rev.AV experimental PCB routing from frozen Rev.AT; NOT FOR FAB."""
import base64, gzip, json, pathlib, re, uuid

root = pathlib.Path(__file__).resolve().parents[1]
source = root / "yk66-revat" / "YK66_RevAT.kicad_pcb"
datafile = root / "yk66-revav" / "ROUTES_GZIP_BASE64.txt"
outdir = root / "yk66-revav" / "project"
outdir.mkdir(parents=True, exist_ok=True)
for f in (root / "yk66-revat").iterdir():
    if f.suffix in (".kicad_sch", ".kicad_pro", ".kicad_sym") or f.name in ("sym-lib-table", "fp-lib-table"):
        (outdir / f.name).write_bytes(f.read_bytes())
import shutil
shutil.copytree(root / "yk66-revat" / "YK66_RevAT.pretty",
                outdir / "YK66_RevAT.pretty", dirs_exist_ok=True)

raw = gzip.decompress(base64.b64decode(datafile.read_text().strip(), validate=True))
routes = json.loads(raw)
assert sorted(map(int, routes["tracks"])) == list(range(1,12))
STEP = routes["gridstep"]
x0, y0 = routes["xmin"], routes["ymin"]
pcb = source.read_text(encoding="utf-8")
assert pcb.count("(segment (start") == 863
assert pcb.count("(via (at") == 8
pcb, numsegs = re.subn(r"(?m)^  \(segment \([^\n]*\)\n", "", pcb)
pcb, numvias = re.subn(r"(?m)^  \(via \([^\n]*\)\n", "", pcb)
assert (numsegs, numvias) == (863, 8)
netnames = dict((int(n), name) for n, name in re.findall(
    r'\(net (\d+) "([^"]+)"\)', pcb[:pcb.index('  (footprint')]))
assert len(netnames) == 11
for name in netnames.values():
    pcb = pcb.replace('"' + name + '"', '"/' + name + '"')
lines = []
v = s = 0

def stamp(name):
    return uuid.uuid5(uuid.NAMESPACE_URL, "YK66-RevAV-" + name)

for net, paths in routes["tracks"].items():
    for path_id, path in enumerate(paths):
        pts = [tuple(q) for q in path]
        pieces = []
        begin = 0
        for i in range(1, len(pts)):
            if pts[i][0] != pts[i-1][0]:
                if i - 1 > begin:
                    pieces.append((pts[begin], pts[i-1]))
                _, ix, iy = pts[i]
                x, y = x0 + ix * STEP, y0 + iy * STEP
                lines.append('  (via (at %.3f %.3f) (size 1.10) (drill 0.45) '
                             '(layers "F.Cu" "B.Cu") (net %d) (tstamp %s))' %
                             (x, y, int(net), stamp(f"via:{net}:{path_id}:{i}")))
                v += 1
                begin = i
            elif i < len(pts) - 1:
                la, xa, ya = pts[i-1]
                _, xb, yb = pts[i]
                _, xc, yc = pts[i+1]
                if pts[i+1][0] != la or (xb-xa)*(yc-yb) != (yb-ya)*(xc-xb):
                    pieces.append((pts[begin], pts[i]))
                    begin = i
        if len(pts)-1 > begin:
            pieces.append((pts[begin], pts[-1]))
        for j, (a, b) in enumerate(pieces):
            if a == b:
                continue
            layer, x1, y1 = a
            _, x2, y2 = b
            lines.append('  (segment (start %.3f %.3f) (end %.3f %.3f) '
                         '(width 0.34) (layer "%s") (net %d) (tstamp %s))' %
                         (x0 + x1*STEP, y0+y1*STEP,
                          x0+x2*STEP, y0+y2*STEP,
                          ("F.Cu", "B.Cu")[layer], int(net),
                          stamp(f"seg:{net}:{path_id}:{j}")))
            s += 1
# Rev.AV.1: correct two pad-copper collisions found by native KiCad DRC.
# Keep F.Cu, 2-layer PCB, and all net endpoints unchanged.
def detour(old_start, old_end, net, points):
    global lines
    matching=[i for i,line in enumerate(lines)
        if ("(start "+old_start+") (end "+old_end+")") in line
        and ("(net %s)"%net) in line
        and '(layer "F.Cu")' in line]
    assert len(matching)==1,(net,old_start,old_end,matching)
    pos=matching[0]
    amended=[]
    for i,(a,b) in enumerate(zip(points,points[1:])):
        amended.append('  (segment (start %.3f %.3f) (end %.3f %.3f) '
            '(width 0.34) (layer "F.Cu") (net %d) (tstamp %s))' %
            (a[0],a[1],b[0],b[1],net,stamp(f"detour:{net}:{i}")))
    lines[pos:pos+1]=amended

detour("143.000 102.500","124.500 102.500",5,
       [(143,102.5),(143,101.5),(124.5,101.5),(124.5,102.5)])
detour("130.500 118.000","136.500 118.000",10,
       [(130.5,118),(130.5,116.5),(136.5,116.5),(136.5,118)])
s += 4

assert pcb.rstrip().endswith(")")
pcb = pcb.rstrip()[:-1] + "\n" + "\n".join(lines) + "\n)\n"
# Reference text on these three instances had been printed outside allowed zones.
# Keep the reference on F.Fab for assembly while avoiding misprints on F.SilkS.
for reference in ("TMOV1", "RB3", "RB4"):
    marker = '(fp_text reference "' + reference + '"'
    original = next((line for line in pcb.splitlines() if marker in line), None)
    assert original and '(layer "F.SilkS")' in original, reference
    pcb = pcb.replace(original, original.replace('(layer "F.SilkS")', '(layer "F.Fab")'), 1)

# Synchronize the local experimental footprint library with the actual PCB
# so footprint-drift DRC reflects real divergence rather than stale handmade
# library drawings. This does NOT certify geometry against manufacturer specs.
def footprint_sections(source):
    for match in re.finditer(r'\(footprint "YK66_RevAT:([^"]+)"', source):
        begin = match.start()
        depth = 0
        quoted = False
        escaped = False
        for idx in range(begin, len(source)):
            ch = source[idx]
            if quoted:
                if escaped: escaped = False
                elif ch == "\\": escaped = True
                elif ch == '"': quoted = False
            elif ch == '"': quoted = True
            elif ch == "(": depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    yield match.group(1), source[begin:idx+1]
                    break

updated = set()
for name, block in footprint_sections(pcb):
    if name in updated: continue
    block = block.replace('(footprint "YK66_RevAT:'+name+'" (layer "F.Cu")',
        '(footprint "'+name+'" (version 20240108) (generator "pcbnew") (layer "F.Cu")',1)
    block, count = re.subn(r'\(at [-\d.]+ [-\d.]+(?: [-\d.]+)?\)', "", block, count=1)
    assert count==1,name
    block = re.sub(r'\(tstamp [0-9a-f-]+\)', "", block)
    block = re.sub(r'\(net \d+ "[^"]*"\)', "", block)
    block = re.sub(r'\(attr [^)]*\)', "", block, count=1)
    block = re.sub(r'\(fp_text reference "[^"]+"', '(fp_text reference "REF**"', block, count=1)
    block = re.sub(r'\(fp_text value "[^"]+"', '(fp_text value "'+name+'"', block, count=1)
    (outdir/"YK66_RevAT.pretty"/(name+".kicad_mod")).write_text(block+"\n",encoding="utf-8")
    updated.add(name)
print("Synced",len(updated),"experimental footprint templates with PCB geometry (manufacturer approval pending)")

(outdir / "YK66_RevAT.kicad_pcb").write_text(pcb, encoding="utf-8")
print(json.dumps({"removed_segments":numsegs,"removed_vias":numvias,
                  "new_segments":s,"new_vias":v,"nets":len(routes["tracks"]),
                  "status":"EXPERIMENTAL_NONFAB"},ensure_ascii=False))
