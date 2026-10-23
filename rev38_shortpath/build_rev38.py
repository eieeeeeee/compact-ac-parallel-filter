#!/usr/bin/env python3
"""Rev38: Reproducibly shorten the F1-to-C1 copper path on official Rev35 board.
This PCB is for review, not mains manufacturing or energization approval.
"""
from pathlib import Path
import re,uuid,hashlib,shutil
SRC=Path('rev35_terminal/RC18_Lite_Rev35_2P_SCREW_1uF_DIRECT.kicad_pcb')
OUT=Path('rev38_shortpath');OUT.mkdir(exist_ok=True)
s=SRC.read_text()
assert hashlib.sha256(SRC.read_bytes()).hexdigest()=='baf5d3616717381baecc632308e38a0f993e183bb9b2627bd46e1991a17fea23'
p=re.compile(r'^\s*\(segment \(start ([\d.]+) ([\d.]+)\) \(end ([\d.]+) ([\d.]+)\) \(width ([\d.]+)\) \(layer "([^"]+)"\) \(net (\d+)\)[^\n]*\n',re.M)
removed=[]
for m in p.finditer(s):
 if m.group(6)=='F.Cu' and m.group(7)=='2':
  a=(float(m.group(1)),float(m.group(2)))
  b=(float(m.group(3)),float(m.group(4)))
  keepable=({a,b}=={(37.,12.),(44.,12.)} or {a,b}=={(37.,12.),(37.,25.)})
  if not keepable:removed.append(m.group(0))
assert len(removed)==22,len(removed)
for item in removed:
 assert s.count(item)==1
 s=s.replace(item,'',1)
short_segments=[((34.,23.5),(34.,17.4)),((34.,17.4),(7.,17.4)),((7.,17.4),(7.,10.))]
new=[]
for i,(a,b) in enumerate(short_segments):
 new.append(f'\t(segment (start {a[0]:.3f} {a[1]:.3f}) (end {b[0]:.3f} {b[1]:.3f}) (width 0.600) (layer "F.Cu") (net 2) (tstamp "{uuid.uuid5(uuid.NAMESPACE_DNS,"rev38_1uF_F1_shunt_short_fcu_"+str(i))}"))\n')
pos=s.rfind(')');s=s[:pos]+''.join(new)+s[pos:]
s=s.replace('Rev35_2P','Rev38_shortpath')
path=OUT/'RC18_Lite_Rev38_2P_Screw_1uF_ShortPath.kicad_pcb'
path.write_text(s)
sha=hashlib.sha256(path.read_bytes()).hexdigest()
print('Rev38 SHA256',sha)
assert sha=='ec3a5a6711e7a7a65eeed0f59b762018b35cc759c9d829d45e3e27cc72cfa04e'
shutil.copytree('rev35_terminal/RC18_R34.pretty',OUT/'RC18_R34.pretty',dirs_exist_ok=True)
shutil.copy('rev35_terminal/fp-lib-table',OUT/'fp-lib-table')
print('Rev38 ready: 22 segments removed, 3 installed, 11 footprints')
