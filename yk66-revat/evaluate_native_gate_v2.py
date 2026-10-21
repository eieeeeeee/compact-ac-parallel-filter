#!/usr/bin/env python3
"""KiCad 10 JSON-native gate: count sheet ERC, PCB DRC, unconnected and parity.
All non-excluded violations are failures. Passing does not mean AC mains safe.
"""
import json, pathlib, sys, collections
p = pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "reports")
p.mkdir(parents=True, exist_ok=True)

def read_json(filename):
    f=p/filename
    if not f.is_file(): return None
    try: return json.loads(f.read_text(encoding="utf-8-sig"))
    except (ValueError, OSError): return None

def items(seq):
    if not isinstance(seq,list): return None
    return [v for v in seq if isinstance(v,dict) and not v.get("excluded",False)]

E = read_json("ERC_NATIVE.json")
D = read_json("DRC_NATIVE.json")
erc = None
if isinstance(E,dict):
    if isinstance(E.get("sheets"),list):
        pools=[sheet.get("violations") for sheet in E["sheets"] if isinstance(sheet,dict)]
        if all(isinstance(v,list) for v in pools):
            erc=[x for pool in pools for x in items(pool)]
    else:
        erc=items(E.get("violations"))
drc = items(D.get("violations")) if isinstance(D,dict) else None
unconnected = items(D.get("unconnected_items")) if isinstance(D,dict) else None
parity = items(D.get("schematic_parity")) if isinstance(D,dict) else None
sections={"ERC":erc,"DRC":drc,"Unconnected":unconnected,"Parity":parity}
counts={k:len(v) if isinstance(v,list) else None for k,v in sections.items()}
types={k:dict(collections.Counter(v0.get("type","unknown") for v0 in v)) if isinstance(v,list) else {} for k,v in sections.items()}
errors=[f"{k}: {v} violations or missing result" for k,v in counts.items() if v is None or v!=0]
exitcodes={}
for key in ("ERC","DRC"):
    try: val=int((p/f"{key}_EXIT_CODE.txt").read_text().strip())
    except (ValueError,OSError): val=None
    exitcodes[key]=val
    if val is None: errors.append(f"{key}: missing process exit status")
    elif val!=0 and counts[key]==0: errors.append(f"{key}: CLI error {val} despite zero reported violations")
status="PASS" if not errors else "FAIL"
report={"status":status,"tool":"KiCad 10.0.6 native CLI","counts":counts,"types":types,"exit_codes":exitcodes,
        "errors":errors,"safety_release":"HOLD_NONFAB_NOT_MAINS"}
(p/"RESULT_SUMMARY_V2.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
md=["# YK66 Rev.AT — KiCad native gate","",f"Result: **{status}**",""]
md += [f"- {k}: **{v}**" for k,v in counts.items()]
md += ["","## DRC violation categories",""]
md += [f"- {k}: {v}" for k,v in types.get("DRC",{}).items()]
md += ["","**Manufacturing, mains and PSE approval: HOLD.**",""]
(p/"RESULT_SUMMARY_V2.md").write_text("\n".join(md),encoding="utf-8")
print(json.dumps(report,indent=2,ensure_ascii=False))
sys.exit(0 if status=="PASS" else 1)
