#!/usr/bin/env python3
"""Reproduce Rev31 1uF X2 direct PCB deterministically from verified Rev27 input."""
from pathlib import Path
import re,hashlib,uuid,shutil
source=Path('rev27_native_drc/RC18_Lite_Rev26_ROUTED_DRAFT.kicad_pcb')
root=Path('rev31_native_drc')
root.mkdir(exist_ok=True)
data=source.read_bytes()
assert hashlib.sha256(data).hexdigest()=='710af374fd54fdae40df21c435d10b9e4e489b096224a8441e405cb257613bda'
s=data.decode('utf-8')
def form_end(t,i):
    depth=0;quote=False;esc=False
    for j in range(i,len(t)):
        c=t[j]
        if quote:
            if esc:esc=False
            elif c=='\\':esc=True
            elif c=='"':quote=False
        elif c=='"':quote=True
        elif c=='(':depth+=1
        elif c==')':
            depth-=1
            if not depth:return j+1
    raise ValueError('Unbalanced form')
i=s.index('(footprint "RC18_R26:R1_PHYSICAL_DRAFT"')
s=s[:i]+s[form_end(s,i):]
s,n=re.subn(r'\(segment \(start 47\.500 25\.000\) \(end 49\.000 25\.000\) [^\n]+\)','',s)
assert n==1
s=s.replace('(net 3 "RC_MID")\n','',1)
mapnet={0:0,1:1,2:2,3:2,4:3,5:4,6:5,7:6}
names={0:'',1:'A_IN',2:'A_FUSED',3:'B_IN',4:'B1',5:'B2',6:'LED_DRIVE'}
s=re.sub(r'\(net (\d+) "([^"\n]*)"\)',lambda m:f'(net {mapnet[int(m.group(1))]} "{names[mapnet[int(m.group(1))]]}")',s)
s=re.sub(r'\(net (\d+)\)',lambda m:f'(net {mapnet[int(m.group(1))]})',s)
bridge=f'(segment (start 37.000 25.000) (end 47.500 25.000) (width 0.600) (layer "F.Cu") (net 2) (tstamp "{uuid.uuid5(uuid.NAMESPACE_DNS,"rc18-lite-rev31-direct-bridge")}"))'
via=f'(via (at 37.000 25.000) (size 1.20) (drill 0.60) (layers "F.Cu" "B.Cu") (net 2) (tstamp "{uuid.uuid5(uuid.NAMESPACE_DNS,"rc18-lite-rev31-direct-via")}"))'
s=s[:-2]+bridge+'\n'+via+'\n)\n'
s=s.replace('(generator "RC18_Rev26_python_autorouter")','(generator "RC18_Rev31_Direct_1uF_conversion")')
assert form_end(s,0)==len(s.rstrip('\n'))
p=root/'RC18_Lite_Rev31_DIRECT_1uF_DRC_CANDIDATE.kicad_pcb'
p.write_text(s)
sha=hashlib.sha256(p.read_bytes()).hexdigest()
assert sha=='67b63bb7c672bfd5702e7ab90eb9519f6eabfc7c9f6c3dc9e2e7a55465a7d111',(sha,'unexpected board divergence')
shutil.copytree('rev27_native_drc/RC18_R26.pretty',root/'RC18_R26.pretty',dirs_exist_ok=True)
(root/'RC18_R26.pretty'/'R1_PHYSICAL_DRAFT.kicad_mod').unlink(missing_ok=True)
shutil.copyfile('rev27_native_drc/fp-lib-table',root/'fp-lib-table')
print('Rev31 board verified SHA256',sha)
print('Custom footprint count',len(list((root/'RC18_R26.pretty').glob('*.kicad_mod'))))
assert len(list((root/'RC18_R26.pretty').glob('*.kicad_mod')))==11
