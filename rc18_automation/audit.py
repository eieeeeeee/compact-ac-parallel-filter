import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
base=Path(__file__).resolve().parent
manifest=base/"inputs/manifest.json"
result={"utc":datetime.now(timezone.utc).isoformat(),"status":"ERROR_HOLD","manufacturing":"HOLD","checks":[],"errors":[]}
try:
 entries=json.loads(manifest.read_text())["files"]
 if not entries: result["errors"].append("No RC18 source files installed; verification unavailable")
 for e in entries:
  p=Path(e["path"])
  if p.is_absolute() or ".." in p.parts: raise ValueError("unsafe input path")
  f=(base/"inputs"/p).resolve()
  if not f.is_relative_to((base/"inputs").resolve()) or not f.is_file(): raise ValueError("missing "+str(p))
  digest=hashlib.sha256(f.read_bytes()).hexdigest()
  result["checks"].append({"path":str(p),"sha256":digest})
  if digest!=e["sha256"]: result["errors"].append("SHA256 mismatch "+str(p))
except (ValueError,KeyError,OSError,TypeError) as exc: result["errors"].append(str(exc))
if not result["errors"]:result["status"]="INTEGRITY_OK_DESIGN_HOLD"
(base/"report.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result))
if result["errors"]:raise SystemExit(1)
