#!/usr/bin/env python3
import sys,re
from pathlib import Path
import pcbnew

pcb=Path(sys.argv[1]).resolve()
dsn=Path(sys.argv[2]).resolve()
b=pcbnew.LoadBoard(str(pcb))

items=list(b.GetTracks())
for x in items:
    x.SetLocked(True)

pcbnew.SaveBoard(str(pcb),b)
if not pcbnew.ExportSpecctraDSN(b,str(dsn)):
    raise SystemExit("ExportSpecctraDSN failed")

# Existing copper is fixed at its actual widths.  Only newly autorouted repair
# copper uses 0.12 mm so the router can escape the dense Q101/D201/X1 areas.
s=dsn.read_text(encoding="utf-8")
count=s.count("(width 200)")
if count < 2:
    raise SystemExit(f"unexpected DSN width-200 count={count}")
s=s.replace("(width 200)","(width 100)")\ns=s.replace('(use_via "Via[0-3]_600:300_um")','(use_via "Via[0-3]_500:300_um")')
dsn.write_text(s,encoding="utf-8")
print(f"REPAIR_DSN locked={len(items)} width_200_to_100={count}; use_via=500:300")
print(dsn)
