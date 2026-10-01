#!/usr/bin/env python3
import re, sys
from pathlib import Path
import pcbnew

pcb = Path(sys.argv[1]).resolve()
report = Path(sys.argv[2]).resolve()

text = report.read_text(encoding="utf-8", errors="replace")
targets = []
lines = text.splitlines()
for i, line in enumerate(lines):
    if "[via_dangling]:" not in line:
        continue
    for j in range(i+1, min(i+6, len(lines))):
        m = re.search(r'@\(([-0-9.]+) mm, ([-0-9.]+) mm\): Via \[([^\]]+)\]', lines[j])
        if m:
            targets.append((m.group(3), float(m.group(1)), float(m.group(2))))
            break

board = pcbnew.LoadBoard(str(pcb))
removed=[]
for net,tx,ty in targets:
    hit=None
    for item in list(board.GetTracks()):
        if not isinstance(item, pcbnew.PCB_VIA):
            continue
        pos=item.GetPosition()
        x=pcbnew.ToMM(pos.x); y=pcbnew.ToMM(pos.y)
        if item.GetNetname()==net and abs(x-tx)<=0.03 and abs(y-ty)<=0.03:
            hit=item
            break
    if hit is None:
        raise SystemExit(f"KiCad-reported dangling via not found: {(net,tx,ty)}")
    board.Remove(hit)
    removed.append((net,tx,ty))

pcbnew.SaveBoard(str(pcb), board)
cats=re.findall(r'^\[([a-z0-9_]+)\]:', text, re.M)
print(f"preclean_categories={sorted(set(cats))}")
print(f"reported_dangling_vias={len(targets)} removed={removed}")
