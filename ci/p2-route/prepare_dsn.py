#!/usr/bin/env python3
import sys
from pathlib import Path
import pcbnew

pcb = Path(sys.argv[1]).resolve()
dsn = Path(sys.argv[2]).resolve()

board = pcbnew.LoadBoard(str(pcb))

# RC18 P2 manufacturing floor.  The CSD17381F4 YJC land pattern already
# requires 0.10 mm local copper spacing, so use the same floor in the DSN
# router model instead of forcing an impossible 0.20 mm default around it.
ds = board.GetDesignSettings()
ds.m_MinClearance = pcbnew.FromMM(0.10)
ds.m_TrackMinWidth = pcbnew.FromMM(0.10)
try:
    nc = ds.m_NetSettings.GetDefaultNetclass()
    nc.SetClearance(pcbnew.FromMM(0.10))
    nc.SetTrackWidth(pcbnew.FromMM(0.20))
except Exception as e:
    print(f"netclass update warning: {e}")

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
