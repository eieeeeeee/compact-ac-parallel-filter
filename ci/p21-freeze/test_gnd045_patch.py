#!/usr/bin/env python3
from pathlib import Path
import sys, uuid
p=Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
NS=uuid.UUID('ad7ac245-2834-45dd-a433-f1232fd11eaa')
def uid(label): return str(uuid.uuid5(NS,label))
def bend(text,st):
 d=0;ins=False;esc=False
 for i in range(st,len(text)):
  c=text[i]
  if ins:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':ins=False
  else:
   if c=='"':ins=True
   elif c=='(':d+=1
   elif c==')':
    d-=1
    if d==0:return i+1
 raise RuntimeError('unbalanced')
def remove_uuid(u,kind='segment'):
 global s
 pos=s.find(f'(uuid "{u}")')
 if pos<0: raise RuntimeError('missing '+u)
 st=s.rfind('('+kind,0,pos); en=bend(s,st)
 if f'(uuid "{u}")' not in s[st:en]: raise RuntimeError('uuid not in block')
 s=s[:st]+s[en:]
def via(label,xy):
 return f'''\n\t(via\n\t\t(at {xy[0]} {xy[1]})\n\t\t(size 0.45)\n\t\t(drill 0.2)\n\t\t(layers "F.Cu" "B.Cu")\n\t\t(locked yes)\n\t\t(net "GND")\n\t\t(uuid "{uid('via:'+label)}")\n\t)\n'''
def seg(label,a,b):
 return f'''\n\t(segment\n\t\t(start {a[0]} {a[1]})\n\t\t(end {b[0]} {b[1]})\n\t\t(width 0.4)\n\t\t(locked yes)\n\t\t(layer "B.Cu")\n\t\t(net "12V_PROT")\n\t\t(uuid "{uid('seg:'+label)}")\n\t)\n'''
remove_uuid('2971a963-2da5-4ef3-9f09-c808bd54f543','segment')
route=[(33.0,30.5),(34.3,32.0),(34.4,32.4),(36.1,33.7),(36.25,33.75)]
new=[]
for i,(a,b) in enumerate(zip(route,route[1:])): new.append(seg(f'f14-12v-{i}',a,b))
pts=[
 ('f05',(14.25,37.195)),
 ('f11',(7.08368,33.03134)),
 ('f14',(34.9353,32.0518)),
 ('f16',(5.63951,31.59469)),
 ('f25',(32.74852,24.00376)),
 ('f29',(8.27161,15.61507)),
 ('f34',(13.56864,14.10721)),
]
for label,xy in pts:new.append(via(label,xy))
anchor=s.find('\n\t(zone')
if anchor<0:raise RuntimeError('zone anchor missing')
s=s[:anchor]+''.join(new)+s[anchor:]
if s.count('(')!=s.count(')'):raise RuntimeError('paren mismatch')
p.write_text(s,encoding='utf-8')
print('GND045_PATCH',len(new),'items')
