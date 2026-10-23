#!/usr/bin/env python3
"""Rebuild terminalized Rev34 from officially DRC-validated Rev31."""
from pathlib import Path
import re,uuid,hashlib,shutil
D=Path('rev34_terminal');D.mkdir(exist_ok=True)
P=Path('rev31_native_drc/RC18_Lite_Rev31_DIRECT_1uF_DRC_CANDIDATE.kicad_pcb')
s=P.read_text()
assert hashlib.sha256(P.read_bytes()).hexdigest()=='67b63bb7c672bfd5702e7ab90eb9519f6eabfc7c9f6c3dc9e2e7a55465a7d111'
def ending(t,i):
 depth=0;q=False;e=False
 for j in range(i,len(t)):
  c=t[j]
  if q:
   if e:e=False
   elif c=='\\':e=True
   elif c=='"':q=False
  elif c=='"':q=True
  elif c=='(':depth+=1
  elif c==')':
   depth-=1
   if not depth:return j+1
 raise ValueError('bad form')
i=s.index('(footprint "RC18_R26:J1_PHYSICAL_DRAFT"')
s=s[:i]+s[ending(s,i):]
for ref,old,new in [('RB1','(at 10.000 34.000)','(at 10.400 34.000)'),('RB2','(at 20.000 40.000)','(at 20.400 40.000)')]:
 i=s.index(f'(footprint "RC18_R26:{ref}_PHYSICAL_DRAFT"');j=ending(s,i)
 fp=s[i:j];assert old in fp
 s=s[:i]+fp.replace(old,new,1)+s[j:]
footprint='''(footprint "RC18_R34:Phoenix_1711725_MKDS3_2p_P5.08" (layer "F.Cu") (tstamp "'+str(uuid.uuid5(uuid.NAMESPACE_DNS,'rc18_rev34_J1'))+'") (at 5.600 34.000) (attr through_hole)
(property "Reference" "J1" (at 0.0 -3.0 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
(property "Value" "Phoenix_1711725_2P_5.08" (at 0 9.0 0) (layer "F.Fab") (effects (font (size 0.7 0.7) (thickness 0.1))))
(fp_rect (start -5.30 -2.24) (end 5.30 7.32) (stroke (width 0.10) (type default)) (fill none) (layer "F.Fab"))
(fp_rect (start -5.60 -2.54) (end 5.60 7.62) (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))
(fp_line (start -5.3 -2.24) (end -5.3 7.32) (stroke (width 0.10) (type default)) (layer "F.SilkS"))
(fp_line (start -5.3 -2.24) (end 5.3 -2.24) (stroke (width 0.10) (type default)) (layer "F.SilkS"))
(fp_line (start -5.3 7.32) (end 5.3 7.32) (stroke (width 0.10) (type default)) (layer "F.SilkS"))
(pad "1" thru_hole circle (at 0 0) (size 2.60 2.60) (drill 1.30) (layers "*.Cu" "*.Mask") (net 1 "A_IN"))
(pad "2" thru_hole circle (at 0 5.08) (size 2.60 2.60) (drill 1.30) (layers "*.Cu" "*.Mask") (net 3 "B_IN"))
)'''.replace("'+str(uuid.uuid5(uuid.NAMESPACE_DNS,'rc18_rev34_J1'))+'",str(uuid.uuid5(uuid.NAMESPACE_DNS,'rc18_rev34_J1')))
pos=s.index('(footprint "RC18_R26:F1_PHYSICAL_DRAFT"')
s=s[:pos]+footprint+'\n'+s[pos:]
s=s.replace('RC18_R26:','RC18_R34:')
replacements=[
 ('(segment (start 9.500 34.000) (end 10.000 34.000)','(segment (start 9.500 34.000) (end 10.400 34.000)'),
 ('(segment (start 20.000 34.000) (end 20.000 40.000)','(segment (start 20.400 34.000) (end 20.400 40.000)'),
 ('(segment (start 4.500 40.000) (end 10.000 40.000)','(segment (start 5.600 39.080) (end 10.400 40.000)'),
 ('(segment (start 10.000 40.000) (end 10.000 44.000)','(segment (start 10.400 40.000) (end 10.400 44.000)'),
 ('(segment (start 10.000 44.000) (end 21.500 44.000)','(segment (start 10.400 44.000) (end 21.500 44.000)')]
for old,new in replacements:
 assert s.count(old)==1,old
 s=s.replace(old,new,1)
i=s.index('(segment (start 4.500 40.000) (end 4.500 45.500)')
s=s[:i]+s[ending(s,i):]
segment=f'(segment (start 4.500 32.000) (end 5.600 34.000) (width 0.600) (layer "B.Cu") (net 1) (tstamp "{uuid.uuid5(uuid.NAMESPACE_DNS,"rc18_rev34_netA_terminal")}"))'
s=s[:-2]+segment+'\n)\n'
s=s.replace('RC18_Rev31_Direct_1uF_conversion','RC18_Rev34_MKDS3_2Pole_Terminal')
out=D/'RC18_Lite_Rev34_2P_SCREW_1uF_DIRECT.kicad_pcb'
out.write_text(s)
expected='bafab06ee7815d5dc40a0082367bc54f2df3da3f3faf8fdc2f87b073fd61326c'
got=hashlib.sha256(out.read_bytes()).hexdigest()
print('Generated PCB SHA256:',got)
if got!=expected:raise SystemExit('PCB does not match reviewed Rev34 local candidate')
lib=D/'RC18_R34.pretty';lib.mkdir(exist_ok=True)
for m in Path('rev31_native_drc/RC18_R26.pretty').glob('*.kicad_mod'):
 if m.name!='J1_PHYSICAL_DRAFT.kicad_mod':shutil.copyfile(m,lib/m.name)
module=footprint.replace('"RC18_R34:Phoenix_1711725_MKDS3_2p_P5.08"','"Phoenix_1711725_MKDS3_2p_P5.08"',1)
module=module.replace(' (net 1 "A_IN")','').replace(' (net 3 "B_IN")','')
module=re.sub(r'\(at 5\.600 34\.000\)','',module,count=1)
(lib/'Phoenix_1711725_MKDS3_2p_P5.08.kicad_mod').write_text(module)
(D/'fp-lib-table').write_text('(fp_lib_table\n  (lib (name "RC18_R34")(type "KiCad")(uri "$'+'{KIPRJMOD}/RC18_R34.pretty")(options "")(descr "RC18 Lite Rev34 footprints incl Phoenix 1711725"))\n)\n')
print('Footprint count:',len(list(lib.glob('*.kicad_mod'))))
assert len(list(lib.glob('*.kicad_mod')))==11
