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
