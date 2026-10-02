#!/usr/bin/env python3
import sys
from pathlib import Path
import pcbnew

pcb=Path(sys.argv[1]).resolve()
dsn=Path(sys.argv[2]).resolve()
b=pcbnew.LoadBoard(str(pcb))

items=list(b.GetTracks())
for x in items:
    try: x.SetLocked(True)
    except Exception: pass

# Preserve the P2.1 manufacturing rules: default 0.20 mm clearance,
# with the existing .kicad_dru exception only for the CSD17381F4 internals.
pcbnew.SaveBoard(str(pcb),b)
if not pcbnew.ExportSpecctraDSN(b,str(dsn)):
    raise SystemExit("ExportSpecctraDSN failed")
print(f"P2.1 DSN exported; locked tracks/vias={len(items)}")
print(dsn)
