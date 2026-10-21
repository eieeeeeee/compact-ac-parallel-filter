#!/usr/bin/env python3
"""Restore YK66 Rev.AT KiCad source from integrity-checked compressed payload.
The original KiCad UUIDs are systematically remapped to deterministic UUIDv5
while preserving cross-document identity and all other serialized source text.
This is a NONFAB research candidate; not certified or safe for AC mains use.
"""
from pathlib import Path
import base64, hashlib, json, lzma, re, uuid

ROOT = Path(__file__).resolve().parent
PARTS = sorted((ROOT / "payload").glob("part*.b64"))
EXPECTED_SHA256 = "7ff3910f3398f9fc1e717fadc6a25ba665ed0ca2d09e768fa560a85b3ee92fb2"
if len(PARTS) != 8:
    raise SystemExit(f"FAIL: expected 8 payload parts, got {len(PARTS)}")
encoded = "".join(p.read_text(encoding="ascii").strip() for p in PARTS)
if len(encoded) != 12488 or hashlib.sha256(encoded.encode()).hexdigest() != EXPECTED_SHA256:
    raise SystemExit("FAIL: payload length or SHA256 mismatch")
files = json.loads(lzma.decompress(base64.b64decode(encoded)).decode("utf-8"))
if len(files) != 19:
    raise SystemExit(f"FAIL: expected 19 source files, got {len(files)}")
ns = uuid.UUID("99e82e8e-0a42-4a5f-95d9-43f651ac1990")
uuid_cache = {}
def restore_id(match):
    index = int(match.group(1))
    if index not in uuid_cache:
        uuid_cache[index] = str(uuid.uuid5(ns, f"YK66-RevAT-source-UUID-{index}"))
    return uuid_cache[index]
for rel, text in files.items():
    path = ROOT.parent / rel
    if not path.resolve().is_relative_to(ROOT.parent.resolve()):
        raise SystemExit("FAIL: unsafe path")
    path.parent.mkdir(parents=True, exist_ok=True)
    if rel.endswith((".kicad_pcb", ".kicad_sch", ".kicad_sym", ".kicad_mod")):
        text = re.sub(r"UU(\d+)U", restore_id, text)
    path.write_text(text, encoding="utf-8")
    print(f"restored {rel}: {path.stat().st_size} bytes")
required = ["YK66_RevAT.kicad_sch", "YK66_RevAT.kicad_pcb", "sym-lib-table", "fp-lib-table"]
for name in required:
    if not (ROOT / name).is_file():
        raise SystemExit(f"FAIL: missing {name}")
print("PASS: integrity-checked source reconstructed (UUID-remapped; NONFAB)")
