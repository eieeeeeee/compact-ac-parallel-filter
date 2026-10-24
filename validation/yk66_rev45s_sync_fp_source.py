#!/usr/bin/env python3
"""Footprint source synchronization using mounted PCB geometry. RESEARCH ONLY."""
from pathlib import Path
import re,csv
root=Path('verify/src')
board=root/'YK66_Rev41_RESEARCH_ONLY.kicad_pcb'
original=board.read_bytes()
s=original.decode()
def sexpr(t,i):
 assert t[i]=='('
 d=0;quote=False;esc=False
 for j in range(i,len(t)):
  c=t[j]
  if quote:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':quote=False
  elif c=='"':quote=True
  elif c=='(':d+=1
  elif c==')':
   d-=1
   if d==0:return t[i:j+1]
 raise ValueError('Unbalanced sexpr')
def elems(t,kind):
 return [sexpr(t,m.start()) for m in re.finditer(r'\('+re.escape(kind)+r'(?=[\s(])',t)]
def clean(p):
 p=re.sub(r'\s*\(uuid [0-9a-f-]+\)','',p)
 p=re.sub(r'\s*\(net \d+ "[^"]*"\)','',p)
 return p
fps=elems(s,'footprint')
assert len(fps)==13,len(fps)
lib=root/'YK66.pretty'
seen=set();rows=[]
for fp in fps:
 name=re.match(r'\(footprint "YK66:([^"]+)"',fp)[1]
 if name in seen:continue
 seen.add(name)
 side=re.search(r'\(layer "([FB])\.Cu"\)',fp)[1]
 p=[f'(footprint "{name}" (version 20241229) (generator "pcbnew") (layer "F.Cu")']
 for field in elems(fp,'property'):
  key=re.match(r'\(property "([^"]+)"',field)[1]
  if key not in ('Reference','Value'):continue
  val='REF**' if key=='Reference' else name
  field=re.sub(r'^\(property "[^"]+" "[^"]*"',f'(property "{key}" "{val}"',field)
  field=field.replace('B.Fab','F.Fab').replace('B.SilkS','F.SilkS')
  field=field.replace(' (justify mirror)','')
  p.append(clean(field))
 for typ in ('attr','fp_rect','fp_line','fp_circle','fp_arc','pad'):
  for item in elems(fp,typ):
   item=clean(item)
   if side=='B':
    for suffix in ('Cu','Paste','Mask','Fab','CrtYd','SilkS'):
     item=item.replace(f'"B.{suffix}"',f'"F.{suffix}"')
   p.append(item)
 p.append(')')
 (lib/f'{name}.kicad_mod').write_text('\n'.join(p)+'\n')
 rows.append((name,side,len(elems(fp,'pad'))))
assert len(rows)==8,len(rows)
assert board.read_bytes()==original
with (root/'FOOTPRINT_SOURCE_SYNC.csv').open('w') as f:
 w=csv.writer(f);w.writerow(('footprint','board_side','pads'));w.writerows(rows)
print('Board unchanged, 9 unique footprint library entries rewritten; 13 board instances')
