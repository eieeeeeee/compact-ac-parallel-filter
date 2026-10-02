#!/usr/bin/env python3
import sys,json
from pathlib import Path
p=Path(sys.argv[1])
d=json.loads(p.read_text(encoding="utf-8"))
sev=d.setdefault("board",{}).setdefault("design_settings",{}).setdefault("rule_severities",{})
sev["unconnected_items"]="error"
d["meta"]["filename"]=p.name
p.write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8")
print("P2.1 connectivity audit: unconnected_items=error")
