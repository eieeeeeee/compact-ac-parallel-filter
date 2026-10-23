#!/usr/bin/env python3
"""Rev35 mechanical clearance fix: move RB1/RB2 PTH pads from connector courtyard."""
from pathlib import Path
import re,uuid,hashlib,shutil
D=Path('rev35_terminal');D.mkdir(exist_ok=True)
SRC=Path('rev34_terminal/RC18_Lite_Rev34_2P_SCREW_1uF_DIRECT.kicad_pcb')
assert hashlib.sha256(SRC.read_bytes()).hexdigest()=='bafab06ee7815d5dc40a0082367bc54f2df3da3f3faf8fdc2f87b073fd61326c'
s=SRC.read_text()
def end(t,i):
 n=0;q=False;e=False
 for j in range(i,len(t)):
  c=t[j]
  if q:
   if e:e=False
   elif c=='\\':e=True
   elif c=='"':q=False
  elif c=='"':q=True
  elif c=='(':n+=1
  elif c==')':
   n-=1
   if not n:return j+1
 raise ValueError
mods={}
for ref,oldxy,newxy,oldpad,newpad,oldbody,newbody,oldcrt,newcrt in [
 ('RB1','(at 10.400 34.000)','(at 12.500 34.000)','(pad "2" thru_hole circle (at 10.000 0.000)','(pad "2" thru_hole circle (at 8.500 0.000)','(fp_rect (start 1.600 -1.300) (end 8.400 1.300)','(fp_rect (start 0.850 -1.300) (end 7.650 1.300)','(fp_rect (start 1.100 -1.800) (end 8.900 1.800)','(fp_rect (start 0.350 -1.800) (end 8.150 1.800)'),
 ('RB2','(at 20.400 40.000)','(at 21.000 40.000)','(pad "2" thru_hole circle (at -10.000 0.000)','(pad "2" thru_hole circle (at -8.500 0.000)','(fp_rect (start -8.400 -1.300) (end -1.600 1.300)','(fp_rect (start -7.650 -1.300) (end -0.850 1.300)','(fp_rect (start -8.900 -1.800) (end -1.100 1.800)','(fp_rect (start -8.150 -1.800) (end -0.350 1.800)')
]:
 i=s.index(f'(footprint "RC18_R34:{ref}_PHYSICAL_DRAFT"')
 j=end(s,i);part=s[i:j]
 for a,b in [(oldxy,newxy),(oldpad,newpad),(oldbody,newbody),(oldcrt,newcrt)]:
  assert part.count(a)==1,a
  part=part.replace(a,b,1)
 s=s[:i]+part+s[j:]
 mods[ref]=part
def replace(old,new):
 global s
 assert s.count(old)==1,old
 s=s.replace(old,new,1)
def remove(start):
 global s
 assert s.count(start)==1,start
 i=s.index(start);s=s[:i]+s[end(s,i):]
for a,b in [
 ('(segment (start 9.500 34.000) (end 10.400 34.000)','(segment (start 9.500 34.000) (end 12.500 34.000)'),
 ('(segment (start 20.400 34.000) (end 20.400 40.000)','(segment (start 21.000 34.000) (end 21.000 40.000)'),
 ('(segment (start 5.600 39.080) (end 10.400 40.000)','(segment (start 5.600 39.080) (end 12.500 40.000)'),
 ('(segment (start 10.400 40.000) (end 10.400 44.000)','(segment (start 12.500 40.000) (end 12.500 44.000)'),
 ('(segment (start 10.400 44.000) (end 21.500 44.000)','(segment (start 12.500 44.000) (end 21.500 44.000)')]:replace(a,b)
for old in [
 '(segment (start 23.500 31.500) (end 23.500 32.500)',
 '(segment (start 23.500 32.500) (end 24.000 32.500)',
 '(segment (start 24.000 32.500) (end 24.000 34.000)',
 '(segment (start 24.000 34.000) (end 25.500 34.000)',
 '(segment (start 24.000 40.000) (end 25.500 40.000)',
 '(segment (start 24.000 40.000) (end 24.000 41.500)',
 '(segment (start 23.500 41.500) (end 24.000 41.500)',
 '(segment (start 23.500 41.500) (end 23.500 42.500)',
 '(segment (start 23.000 42.500) (end 23.500 42.500)',
 '(segment (start 23.000 42.500) (end 23.000 43.000)',
 '(segment (start 22.500 43.000) (end 23.000 43.000)',
 '(segment (start 22.500 43.000) (end 22.500 43.500)',
 '(segment (start 21.500 43.500) (end 22.500 43.500)',
 '(segment (start 21.500 43.500) (end 21.500 44.000)',
 '(segment (start 23.000 31.000) (end 23.000 31.500)',
 '(segment (start 23.000 31.500) (end 23.500 31.500)',
 '(segment (start 21.500 30.500) (end 22.500 30.500)',
 '(segment (start 22.500 30.500) (end 22.500 31.000)',
 '(segment (start 22.500 31.000) (end 23.000 31.000)']:
 remove(old)
def segment(x1,y1,x2,y2,n):
 u=uuid.uuid5(uuid.NAMESPACE_DNS,f'rc18_rev35_{n}_{x1}_{y1}_{x2}_{y2}')
 return f'(segment (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (width 0.600) (layer "B.Cu") (net {n}) (tstamp "{u}"))'
v=[
 segment(21.5,30.5,23.5,30.5,2),
 segment(23.5,30.5,23.5,31.5,2),
 segment(23.5,31.5,25.5,31.5,2),
 segment(25.5,31.5,25.5,34.0,2),
 segment(21.5,44.0,25.5,44.0,3),
 segment(25.5,44.0,25.5,40.0,3)]
s=s[:-2]+'\n'.join(v)+'\n)\n'
s=s.replace('RC18_Rev34_MKDS3_2Pole_Terminal','RC18_Rev35_MKDS3_2Pole_Terminal')
out=D/'RC18_Lite_Rev35_2P_SCREW_1uF_DIRECT.kicad_pcb'
out.write_text(s)
sha=hashlib.sha256(out.read_bytes()).hexdigest()
print('Rev35 VERIFIED BOARD HASH:',sha)
if sha!='baf5d3616717381baecc632308e38a0f993e183bb9b2627bd46e1991a17fea23':raise SystemExit('Rev35 hash mismatch')
lib=D/'RC18_R34.pretty'
shutil.copytree('rev34_terminal/RC18_R34.pretty',lib,dirs_exist_ok=True)
for ref,part in mods.items():
 module=part.replace(f'"RC18_R34:{ref}_PHYSICAL_DRAFT"',f'"{ref}_PHYSICAL_DRAFT"',1)
 module=re.sub(r'\(at \d+\.\d+ \d+\.\d+\)','',module,count=1)
 module=re.sub(r' \(net \d+ "[^"]+"\)','',module)
 (lib/(ref+'_PHYSICAL_DRAFT.kicad_mod')).write_text(module)
shutil.copy('rev34_terminal/fp-lib-table',D/'fp-lib-table')
assert len(list(lib.glob('*.kicad_mod')))==11
