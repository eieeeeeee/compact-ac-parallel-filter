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
assert pcb.rstrip().endswith(")")
pcb = pcb.rstrip()[:-1] + "\n" + "\n".join(lines) + "\n)\n"
(outdir / "YK66_RevAT.kicad_pcb").write_text(pcb, encoding="utf-8")
print(json.dumps({"removed_segments":numsegs,"removed_vias":numvias,
                  "new_segments":s,"new_vias":v,"nets":len(routes["tracks"]),
                  "status":"EXPERIMENTAL_NONFAB"},ensure_ascii=False))
