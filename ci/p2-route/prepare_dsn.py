#!/usr/bin/env python3
import sys
from pathlib import Path
import pcbnew

pcb = Path(sys.argv[1]).resolve()
dsn = Path(sys.argv[2]).resolve()

board = pcbnew.LoadBoard(str(pcb))
tracks = list(board.GetTracks())
for t in tracks:
    try:
        t.SetLocked(True)
    except Exception:
        pass

pcbnew.SaveBoard(str(pcb), board)
ok = pcbnew.ExportSpecctraDSN(board, str(dsn))
if not ok:
    raise SystemExit("ExportSpecctraDSN failed")

print(f"locked_existing_items={len(tracks)}")
print(f"dsn={dsn}")
