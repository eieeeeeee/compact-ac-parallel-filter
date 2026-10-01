#!/usr/bin/env python3
import re, sys
from pathlib import Path

pcb = Path(sys.argv[1]).resolve()
report = Path(sys.argv[2]).resolve()

rpt = report.read_text(encoding="utf-8", errors="replace")
targets=[]
lines=rpt.splitlines()
for i,line in enumerate(lines):
    if "[via_dangling]:" not in line:
        continue
    for j in range(i+1,min(i+6,len(lines))):
        m=re.search(r'@\(([-0-9.]+) mm, ([-0-9.]+) mm\): Via \[([^\]]+)\]', lines[j])
        if m:
            targets.append((float(m.group(1)),float(m.group(2)),m.group(3)))
            break

text=pcb.read_text(encoding="utf-8")

def sexpr_block(s,start):
    depth=0; ins=False; esc=False
    for k in range(start,len(s)):
        ch=s[k]
        if ins:
            if esc: esc=False
            elif ch=="\\": esc=True
            elif ch=='"': ins=False
            continue
        if ch=='"': ins=True
        elif ch=='(': depth+=1
        elif ch==')':
            depth-=1
            if depth==0:
                return k+1
    raise RuntimeError("unbalanced S-expression")

matches=[]
pos=0
while True:
    m=re.search(r'(?m)^[ \t]*\(via\b', text[pos:])
    if not m: break
    start=pos+m.start()
    end=sexpr_block(text,start)
    block=text[start:end]
    am=re.search(r'\(at\s+([-0-9.]+)\s+([-0-9.]+)',block)
    if am:
        x=float(am.group(1)); y=float(am.group(2))
        for tx,ty,net in targets:
            if abs(x-tx)<=0.03 and abs(y-ty)<=0.03:
                matches.append((start,end,x,y,net))
                break
    pos=end

if len(matches)!=len(targets):
    raise SystemExit(f"dangling-via text cleanup mismatch: targets={targets}, matches={[(x,y,n) for _,_,x,y,n in matches]}")

for start,end,x,y,net in sorted(matches,reverse=True):
    # Remove a preceding indentation-only slice only when it belongs to this line.
    line_start=text.rfind("\n",0,start)+1
    if text[line_start:start].strip()=="":
        start=line_start
    text=text[:start]+text[end:]

pcb.write_text(text,encoding="utf-8")
cats=re.findall(r'^\[([a-z0-9_]+)\]:',rpt,re.M)
print(f"preclean_categories={sorted(set(cats))}")
print(f"reported_dangling_vias={len(targets)} removed={[(x,y,n) for _,_,x,y,n in matches]}")
