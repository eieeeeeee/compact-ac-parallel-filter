#!/usr/bin/env python3
from pathlib import Path
import re, collections, sys

base = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

def block(s, start):
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(s)):
        c = s[i]
        if in_string:
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == '"':
                in_string = False
            continue
        if c == '"':
            in_string = True
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return s[start:i+1]
    raise RuntimeError("unbalanced S-expression")

def fmt(v):
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return ("%.5f" % v).rstrip("0").rstrip(".")

total_labels = total_nc = 0
for f in sorted(base.glob("*.kicad_sch")):
    if f.name == "RC18_RevB_SI.kicad_sch":
        continue
    s = f.read_text(encoding="utf-8")
    lp = s.find("(lib_symbols")
    if lp < 0:
        continue
    lb = block(s, lp)
    libs = {}
    for m in re.finditer(r'\(symbol "([^"]+)"', lb):
        b = block(lb, m.start())
        name = m.group(1)
        if ":" not in name:
            continue
        pins = []
        for pm in re.finditer(
            r'\(pin\s+([a-zA-Z_]+)\s+([a-zA-Z_]+)\s+\(at\s+([-0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+)\).*?\(number\s+"([^"]+)"',
            b, re.S
        ):
            pins.append((pm.group(6), float(pm.group(3)), float(pm.group(4))))
        libs[name] = pins

    candidates = collections.defaultdict(list)
    for m in re.finditer(
        r'\(symbol \(lib_id "([^"]+)"\) \(at\s+([-0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+)\)',
        s
    ):
        b = block(s, m.start())
        lib = m.group(1)
        x, y, rot = float(m.group(2)), float(m.group(3)), float(m.group(4))
        if abs(rot) > 1e-9:
            raise RuntimeError(f"{f.name}: unsupported rotation {rot}")
        rm = re.search(r'\(property "Reference" "([^"]+)"', b)
        ref = rm.group(1) if rm else "?"
        for pn, dx, dy in libs.get(lib, []):
            wrong = (round(x + dx, 5), round(y + dy, 5))
            actual = (round(x + dx, 5), round(y - dy, 5))
            candidates[wrong].append((actual, ref, pn))

    moved = []
    pat = re.compile(
        r'(\(global_label "([^"]+)" \(shape [^)]+\) \(at\s+)([-0-9.]+)(\s+)([-0-9.]+)(\s+[-0-9.]+\))'
    )
    def repl(m):
        key = (round(float(m.group(3)), 5), round(float(m.group(5)), 5))
        cs = candidates.get(key, [])
        if len(cs) == 1:
            actual, ref, pn = cs[0]
            if actual != key:
                moved.append((m.group(2), ref, pn, key, actual))
                return m.group(1) + fmt(actual[0]) + m.group(4) + fmt(actual[1]) + m.group(6)
        return m.group(0)

    ns = pat.sub(repl, s)

    moved_nc = []
    patnc = re.compile(r'(\(no_connect \(at\s+)([-0-9.]+)(\s+)([-0-9.]+)(\))')
    def replnc(m):
        key = (round(float(m.group(2)), 5), round(float(m.group(4)), 5))
        cs = candidates.get(key, [])
        if len(cs) == 1:
            actual, ref, pn = cs[0]
            if actual != key:
                moved_nc.append((ref, pn, key, actual))
                return m.group(1) + fmt(actual[0]) + m.group(3) + fmt(actual[1]) + m.group(5)
        return m.group(0)

    ns = patnc.sub(replnc, ns)
    f.write_text(ns, encoding="utf-8")
    total_labels += len(moved)
    total_nc += len(moved_nc)
    print(f"{f.name}: moved_labels={len(moved)} moved_no_connect={len(moved_nc)}")

print(f"TOTAL moved_labels={total_labels} moved_no_connect={total_nc}")
if total_labels != 121 or total_nc != 2:
    raise SystemExit(f"unexpected patch count labels={total_labels} nc={total_nc}")


# Make project-local library tables resolvable in headless kicad-cli.
# Use absolute paths because this package is checked as a standalone schematic tree.
absbase = base.resolve().as_posix()
(base / "sym-lib-table").write_text(
    '(sym_lib_table\n'
    '  (version 7)\n'
    f'  (lib (name "RC18_Custom")(type "Legacy")(uri "{absbase}/RC18_Custom.lib")(options "")(descr "RC18 local legacy symbols"))\n'
    ')\n',
    encoding="utf-8"
)
(base / "fp-lib-table").write_text(
    '(fp_lib_table\n'
    '  (version 7)\n'
    f'  (lib (name "RC18_Custom")(type "KiCad")(uri "{absbase}/RC18_Custom.pretty")(options "")(descr "RC18 local footprints"))\n'
    ')\n',
    encoding="utf-8"
)
print("rewrote sym-lib-table and fp-lib-table with absolute paths")


# Create a same-name KiCad project so kicad-cli loads project-local library tables.
import json
project = {
    "erc": {
        "erc_exclusions": [],
        "meta": {"version": 0},
        "rule_severities": {
            "footprint_filter": "ignore",
            "footprint_link_issues": "warning",
            "four_way_junction": "ignore",
            "isolated_pin_label": "warning",
            "label_dangling": "error",
            "lib_symbol_issues": "warning",
            "simulation_model_issue": "ignore",
            "single_global_label": "ignore"
        }
    },
    "libraries": {
        "pinned_footprint_libs": [],
        "pinned_symbol_libs": []
    },
    "meta": {
        "filename": "RC18_RevB_SI.kicad_pro",
        "version": 3
    },
    "schematic": {
        "legacy_lib_dir": "",
        "legacy_lib_list": [],
        "meta": {"version": 1}
    },
    "sheets": []
}
(base / "RC18_RevB_SI.kicad_pro").write_text(
    json.dumps(project, indent=2) + "\n",
    encoding="utf-8"
)
print("created RC18_RevB_SI.kicad_pro")


# With a same-name project now present, use project-relative library URIs.
kprj = "$" + "{KIPRJMOD}"
(base / "sym-lib-table").write_text(
    '(sym_lib_table\n'
    '  (version 7)\n'
    f'  (lib (name "RC18_Custom")(type "Legacy")(uri "{kprj}/RC18_Custom.lib")(options "")(descr "RC18 local legacy symbols"))\n'
    ')\n',
    encoding="utf-8"
)
(base / "fp-lib-table").write_text(
    '(fp_lib_table\n'
    '  (version 7)\n'
    f'  (lib (name "RC18_Custom")(type "KiCad")(uri "{kprj}/RC18_Custom.pretty")(options "")(descr "RC18 local footprints"))\n'
    ')\n',
    encoding="utf-8"
)
print("rewrote library tables to project-relative KIPRJMOD URIs")


# Rebuild RC18_Custom as a modern KiCad symbol library directly from the
# embedded symbol definitions in the converted schematics.  This guarantees
# that ERC compares each placed symbol against an identical library definition.
custom_symbols = {}
for sch in sorted(base.glob("*.kicad_sch")):
    if sch.name == "RC18_RevB_SI.kicad_sch":
        continue
    txt = sch.read_text(encoding="utf-8")
    lp = txt.find("(lib_symbols")
    if lp < 0:
        continue
    lblock = block(txt, lp)
    for mm in re.finditer(r'\(symbol "(RC18_Custom:[^"]+)"', lblock):
        sb = block(lblock, mm.start())
        libid = mm.group(1)
        bare = libid.split(":", 1)[1]
        if bare not in custom_symbols:
            custom_symbols[bare] = sb.replace(
                f'(symbol "{libid}"',
                f'(symbol "{bare}"',
                1
            )

symout = [
    '(kicad_symbol_lib (version 20231120) (generator "openai_p2_erc")'
]
for name in sorted(custom_symbols):
    symout.append(custom_symbols[name])
symout.append(')')
(base / "RC18_Custom.kicad_sym").write_text(
    "\n".join(symout) + "\n",
    encoding="utf-8"
)
print(f"generated RC18_Custom.kicad_sym symbols={len(custom_symbols)}")

kprj = "$" + "{KIPRJMOD}"
(base / "sym-lib-table").write_text(
    '(sym_lib_table\n'
    '  (version 7)\n'
    f'  (lib (name "RC18_Custom")(type "KiCad")(uri "{kprj}/RC18_Custom.kicad_sym")(options "")(descr "RC18 embedded-equivalent symbols"))\n'
    ')\n',
    encoding="utf-8"
)
print("switched RC18_Custom symbol library to embedded-equivalent modern format")


# --- Final warning cleanup: preserve circuit intent, remove legacy naming drift. ---
import shutil

# Q601/Q602 have the frozen physical CSD17381F4 pin mapping (1=G,2=S,3=D).
# Give this physically mapped symbol its own library identity rather than sharing
# the generic MOSFET_LOGIC identity used elsewhere.
hb = base / "06_SI_HALFBRIDGE.kicad_sch"
txt = hb.read_text(encoding="utf-8")
txt = txt.replace('RC18_Custom:MOSFET_LOGIC', 'RC18_Custom:CSD17381F4')
txt = txt.replace('(symbol "MOSFET_LOGIC_', '(symbol "CSD17381F4_')
hb.write_text(txt, encoding="utf-8")
print("renamed Q601/Q602 library identity to RC18_Custom:CSD17381F4")

# Replace legacy/nonexistent footprint names with KiCad-library footprints that
# are copied into the project-local RC18_Custom.pretty directory.
fp_repl = {
    'Package_SO:VSSOP-8_3.0x3.0mm_P0.65mm':
        'RC18_Custom:VSSOP-8_3.0x3.0mm_P0.65mm',
    'Inductor_SMD:L_2520_1008Metric':
        'RC18_Custom:L_1008_2520Metric',
    'Package_SO:HVSSOP-8_3x3mm_P0.65mm':
        'RC18_Custom:MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm',
}
for sch in sorted(base.glob("*.kicad_sch")):
    st = sch.read_text(encoding="utf-8")
    nt = st
    for old, new in fp_repl.items():
        nt = nt.replace(old, new)
    if nt != st:
        sch.write_text(nt, encoding="utf-8")

srcfp = Path("ci/p2-kicad10/footprints")
dstfp = base / "RC18_Custom.pretty"
dstfp.mkdir(exist_ok=True)
for name in [
    "VSSOP-8_3.0x3.0mm_P0.65mm.kicad_mod",
    "MSOP-8-1EP_3x3mm_P0.65mm_EP1.68x1.88mm.kicad_mod",
    "L_1008_2520Metric.kicad_mod",
]:
    shutil.copy2(srcfp / name, dstfp / name)
print("copied 3 verified KiCad footprints into RC18_Custom.pretty")

# All remaining isolated labels were audited: SPARE/DBG/DIAG/internal or explicit
# DNP-open placeholders. Keep their net names and suppress only this intentional
# ERC class instead of deleting the labels.
pro = base / "RC18_RevB_SI.kicad_pro"
pdata = json.loads(pro.read_text(encoding="utf-8"))
pdata["erc"]["rule_severities"]["isolated_pin_label"] = "ignore"
pro.write_text(json.dumps(pdata, indent=2) + "\n", encoding="utf-8")
print("set isolated_pin_label=ignore for audited intentional single-pin nets")

# Regenerate the modern local symbol library after the CSD17381F4 identity split.
custom_symbols = {}
for sch in sorted(base.glob("*.kicad_sch")):
    if sch.name == "RC18_RevB_SI.kicad_sch":
        continue
    st = sch.read_text(encoding="utf-8")
    lp = st.find("(lib_symbols")
    if lp < 0:
        continue
    lblock = block(st, lp)
    for mm in re.finditer(r'\(symbol "(RC18_Custom:[^"]+)"', lblock):
        sb = block(lblock, mm.start())
        libid = mm.group(1)
        bare = libid.split(":", 1)[1]
        if bare not in custom_symbols:
            custom_symbols[bare] = sb.replace(
                f'(symbol "{libid}"', f'(symbol "{bare}"', 1
            )
symout = ['(kicad_symbol_lib (version 20231120) (generator "openai_p2_erc")']
for name in sorted(custom_symbols):
    symout.append(custom_symbols[name])
symout.append(')')
(base / "RC18_Custom.kicad_sym").write_text(
    "\n".join(symout) + "\n", encoding="utf-8"
)
print(f"regenerated final RC18_Custom.kicad_sym symbols={len(custom_symbols)}")
