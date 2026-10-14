#!/usr/bin/env python3
"""Fail-closed RC18 gate audit. Never claims electrical design validation."""
import json, hashlib
from pathlib import Path
from datetime import datetime, timezone
base=Path(__file__).resolve().parent
report={"utc":datetime.now(timezone.utc).isoformat(),"manufacturing":"HOLD","status":"ERROR_HOLD","checks":[],"errors":[]}
try:
    gates=json.loads((base/"inputs/release_gates.json").read_text(encoding="utf-8"))
    expected={"project":"RC18","manufacturing":"HOLD","requirements":41,"missing_fit_parts":64,"release_blockers":17}
    for k,v in expected.items():
        if gates.get(k)!=v:report["errors"].append(f"unexpected {k}: {gates.get(k)!r}")
    if gates.get("native_erc_drc_verified_for_current_candidate") is not False:
        report["errors"].append("Native verification status changed; manual review required")
    vendor=gates.get("vendor_pin_audit",{})
    if (vendor.get("devices"),vendor.get("pins"),vendor.get("incorrect_electrical_types"))!=(3,21,12):
        report["errors"].append("vendor audit baseline changed; manual review required")
    report["checks"].append("RC18 public-safe HOLD gate baseline")
    manifest=json.loads((base/"inputs/manifest.json").read_text(encoding="utf-8"))
    entries=manifest["files"]
    for item in entries:
        rel=Path(item["path"])
        root=(base/"inputs").resolve()
        target=(root/rel).resolve()
        if rel.is_absolute() or not target.is_relative_to(root) or not target.is_file():
            report["errors"].append("invalid/missing input "+str(rel));continue
        digest=hashlib.sha256(target.read_bytes()).hexdigest()
        if digest!=item["sha256"]:report["errors"].append("hash mismatch "+str(rel))
        report["checks"].append(str(rel))
    if not entries:report["checks"].append("No design-source hash audit configured; baseline only")
except (OSError,ValueError,KeyError,TypeError) as exc:
    report["errors"].append(str(exc))
if not report["errors"]:report["status"]="BASELINE_OK_DESIGN_HOLD"
(base/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
if report["errors"]:raise SystemExit(1)
