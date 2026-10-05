#!/usr/bin/env python3
from pathlib import Path
import re, sys

ROOT=Path(sys.argv[1])

def block_end(s,start):
    depth=0; ins=False; esc=False
    for i in range(start,len(s)):
        c=s[i]
        if ins:
            if esc: esc=False
            elif c=="\\": esc=True
            elif c=='"': ins=False
        else:
            if c=='"': ins=True
            elif c=='(': depth+=1
            elif c==')':
                depth-=1
                if depth==0: return i+1
    raise RuntimeError("unbalanced s-expression")

def symbol_block(s, marker):
    st=s.find(marker)
    if st<0: raise RuntimeError("missing symbol marker "+marker)
    return st, block_end(s,st)

def patch_def(path, marker, maps):
    s=path.read_text(encoding="utf-8")
    st,en=symbol_block(s,marker)
    b=s[st:en]
    for name,oldnum,newnum in maps:
        pat=r'(\\(name "'+re.escape(name)+r'"[^\\n]*\\)\\s*\\(number ")'+re.escape(oldnum)+r'(")'
        b2,n=re.subn(pat,lambda m:m.group(1)+newnum+m.group(2),b,count=1)
        if n!=1:
            raise RuntimeError(f"{path.name}: failed {name} {oldnum}->{newnum}")
        b=b2
    path.write_text(s[:st]+b+s[en:],encoding="utf-8")

def patch_instance(path, ref, pinmap):
    s=path.read_text(encoding="utf-8")
    key=f'(property "Reference" "{ref}"'
    p=s.find(key)
    if p<0: raise RuntimeError(f"{path.name}: ref {ref} not found")
    st=s.rfind('(symbol ',0,p)
    en=block_end(s,st)
    b=s[st:en]
    for old,new in pinmap.items():
        pat=r'\\(pin "'+re.escape(old)+r'"(\\s+\\(uuid [^)]+\\)\\))'
        b2,n=re.subn(pat,lambda m:f'(pin "{new}"'+m.group(1),b,count=1)
        if n!=1:
            raise RuntimeError(f"{path.name}: {ref} pin {old}->{new} failed")
        b=b2
    path.write_text(s[:st]+b+s[en:],encoding="utf-8")

# Project library
lib=ROOT/"RC18_Custom.kicad_sym"
patch_def(lib,'(symbol "MOSFET_LOGIC"',[
    ("G","G","1"),("D","D","3"),("S","S","2")
])
patch_def(lib,'(symbol "DUAL_CLAMP"',[
    ("SIG","SIG","3"),("HIGH","HIGH","2"),("LOW","LOW","1")
])

# Embedded library copies in native child sheets
p1=ROOT/"01_POWER_INPUT.kicad_sch"
patch_def(p1,'(symbol "RC18_Custom:MOSFET_LOGIC"',[
    ("G","G","1"),("D","D","3"),("S","S","2")
])
patch_instance(p1,"Q101",{"G":"1","D":"3","S":"2"})

p4=ROOT/"04_VLINE_ANALOG.kicad_sch"
patch_def(p4,'(symbol "RC18_Custom:DUAL_CLAMP"',[
    ("SIG","SIG","3"),("HIGH","HIGH","2"),("LOW","LOW","1")
])
patch_instance(p4,"D201",{"SIG":"3","HIGH":"2","LOW":"1"})

print("SCHEMATIC_PARITY_PATCHED Q101=1/3/2 D201=3/2/1 X1=DNP_TBD_EXCEPTION")
