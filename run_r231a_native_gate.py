#!/usr/bin/env python3
from __future__ import annotations
import hashlib, re, shutil, subprocess, sys, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SCH=ROOT/'RC18_RevB_SI.kicad_sch'
PCB=ROOT/'RC18_RevB_SI.kicad_pcb'
PRO=ROOT/'RC18_RevB_SI.kicad_pro'
OUT=ROOT/'R2_3_1A_NATIVE_RESULTS'
EXPECTED='10.0.6'
class GateFail(RuntimeError): pass

def sha256(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def run(cmd,name):
    q=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    OUT.mkdir(exist_ok=True)
    (OUT/name).write_text('$ '+' '.join(map(str,cmd))+'\n\n'+q.stdout+f'\nEXIT_CODE={q.returncode}\n',encoding='utf-8')
    if q.returncode: raise GateFail(f'{name}: exit {q.returncode}')
    return q.stdout

def report_zero(p,erc=False):
    t=p.read_text(encoding='utf-8',errors='replace')
    if erc:
        bad=bool(re.search(r'\b([1-9][0-9]*)\s+(?:Errors?|Warnings?)\b',t,re.I))
        if bad: raise GateFail(f'ERC report nonzero marker: {p}')
    else:
        for pat in [r'Found 0 DRC violations',r'Found 0 unconnected pads',r'Found 0 Footprint errors']:
            if not re.search(pat,t,re.I): raise GateFail(f'Missing DRC zero marker {pat}: {p}')

def main():
    OUT.mkdir(exist_ok=True)
    exe=shutil.which('kicad-cli')
    if not exe: raise GateFail('kicad-cli missing')
    ver=subprocess.run([exe,'--version'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.strip()
    (OUT/'KICAD_NATIVE_VERSION.txt').write_text(ver+'\n')
    if EXPECTED not in ver: raise GateFail(f'Expected {EXPECTED}, got {ver}')
    for p in (SCH,PCB,PRO):
        if not p.is_file(): raise GateFail(f'Missing {p.name}')
    pre={p.name:sha256(p) for p in (SCH,PCB,PRO)}
    (OUT/'PRE_NATIVE_SHA256.txt').write_text(''.join(f'{h}  {n}\n' for n,h in pre.items()))
    erc=OUT/'R2_3_1A_NATIVE_ERC.rpt'
    dr1=OUT/'R2_3_1A_NATIVE_DRC_REFILL_SAVE.rpt'
    dr2=OUT/'R2_3_1A_NATIVE_DRC_FINAL.rpt'
    run([exe,'sch','erc','--format','report','--severity-error','--severity-warning','--exit-code-violations','--output',str(erc),str(SCH)],'ERC_CLI.log')
    report_zero(erc,erc=True)
    run([exe,'pcb','drc','--format','report','--all-track-errors','--schematic-parity','--severity-error','--severity-warning','--exit-code-violations','--refill-zones','--save-board','--output',str(dr1),str(PCB)],'DRC_REFILL_SAVE_CLI.log')
    report_zero(dr1)
    run([exe,'pcb','drc','--format','report','--all-track-errors','--schematic-parity','--severity-error','--severity-warning','--exit-code-violations','--output',str(dr2),str(PCB)],'DRC_FINAL_CLI.log')
    report_zero(dr2)
    post={p.name:sha256(p) for p in (SCH,PCB,PRO)}
    (OUT/'POST_NATIVE_SHA256.txt').write_text(''.join(f'{h}  {n}\n' for n,h in post.items()))
    (OUT/'R2_3_1A_NATIVE_GATE_PASS.txt').write_text('R2.3.1A NATIVE GATE PASS\nKiCad 10.0.6\nERC 0 error/warning via --exit-code-violations\nDRC 0 violations / 0 unconnected / 0 footprint errors\n')
    zip_path=ROOT.parent/'RC18_R2_3_1A_NATIVE_PASS_MASTER.zip'
    with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(ROOT.rglob('*')):
            if f.is_file() and '.git' not in f.parts:
                z.write(f,Path('RC18_R2_3_1A_NATIVE_PASS_MASTER')/f.relative_to(ROOT))
    (ROOT.parent/'RC18_R2_3_1A_NATIVE_PASS_MASTER_SHA256.txt').write_text(sha256(zip_path)+'  '+zip_path.name+'\n')
    print('R2_3_1A_NATIVE_GATE_PASS')

if __name__=='__main__':
    try: main()
    except Exception as e:
        OUT.mkdir(exist_ok=True)
        (OUT/'R2_3_1A_NATIVE_GATE_FAIL.txt').write_text(type(e).__name__+': '+str(e)+'\n')
        print('R2_3_1A_NATIVE_GATE_FAIL',e,file=sys.stderr)
        raise
