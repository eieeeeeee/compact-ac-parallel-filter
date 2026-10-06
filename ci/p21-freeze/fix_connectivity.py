#!/usr/bin/env python3
from pathlib import Path
import re, sys

p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')

def block_end(text,start):
    d=0; ins=False; esc=False
    for i in range(start,len(text)):
        c=text[i]
        if ins:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c=='"': ins=False
        else:
            if c=='"': ins=True
            elif c=='(': d+=1
            elif c==')':
                d-=1
                if d==0:return i+1
    raise RuntimeError('unbalanced')

def footprint_block(ref):
    pos=s.find(f'(property "Reference" "{ref}"')
    if pos<0: raise RuntimeError(f'missing ref {ref}')
    st=s.rfind('(footprint',0,pos); en=block_end(s,st)
    return st,en,s[st:en]

def pad_blocks(b):
    out=[]; pos=0
    while True:
        st=b.find('(pad ',pos)
        if st<0: break
        en=block_end(b,st); out.append((st,en,b[st:en])); pos=en
    return out

def set_pad_net(ref,padnum,net):
    global s
    st,en,b=footprint_block(ref)
    found=False
    for ps,pe,pb in pad_blocks(b):
        m=re.match(r'\(pad\s+"?([^"\s]+)',pb)
        if not m or m.group(1)!=str(padnum): continue
        found=True
        pb2=re.sub(r'\n\s*\(net\s+"[^"]+"\)','',pb)
        u=pb2.find('\n\t\t\t(uuid ')
        if u<0: u=pb2.rfind('\n')
        indent='\n\t\t\t'
        pb2=pb2[:u]+f'{indent}(net "{net}")'+pb2[u:]
        b=b[:ps]+pb2+b[pe:]
        break
    if not found: raise RuntimeError(f'{ref} pad {padnum} not found')
    s=s[:st]+b+s[en:]

def remove_uuid(uuid, kind='segment'):
    global s
    tok=f'(uuid "{uuid}")'; pos=s.find(tok)
    if pos<0: raise RuntimeError(f'missing {uuid}')
    st=s.rfind('('+kind,0,pos); en=block_end(s,st)
    if tok not in s[st:en]: raise RuntimeError(f'{uuid} not in {kind}')
    while st>0 and s[st-1] in '\t ': st-=1
    if st>0 and s[st-1]=='\n': st-=1
    while en<len(s) and s[en] in '\t ': en+=1
    if en<len(s) and s[en]=='\n': en+=1
    s=s[:st]+s[en:]

def replace_segment_endpoint(uuid, oldpt, newpt):
    global s
    tok=f'(uuid "{uuid}")'; pos=s.find(tok)
    st=s.rfind('(segment',0,pos); en=block_end(s,st); b=s[st:en]
    old_start=f'(start {oldpt[0]} {oldpt[1]})'; old_end=f'(end {oldpt[0]} {oldpt[1]})'
    new_start=f'(start {newpt[0]} {newpt[1]})'; new_end=f'(end {newpt[0]} {newpt[1]})'
    if old_start in b: b=b.replace(old_start,new_start,1)
    elif old_end in b: b=b.replace(old_end,new_end,1)
    else: raise RuntimeError(f'endpoint {oldpt} missing in {uuid}')
    s=s[:st]+b+s[en:]

def move_footprint(ref, old_at, new_at):
    global s
    st,en,b=footprint_block(ref)
    old=f'(at {old_at})'; new=f'(at {new_at})'
    if old not in b: raise RuntimeError(f'{ref} old at not found')
    b=b.replace(old,new,1); s=s[:st]+b+s[en:]

def add_segment(a,b,w,layer,net,uuid):
    global s
    block=(f'\n\t(segment\n\t\t(start {a[0]} {a[1]})\n\t\t(end {b[0]} {b[1]})\n'
           f'\t\t(width {w})\n\t\t(locked yes)\n\t\t(layer "{layer}")\n'
           f'\t\t(net "{net}")\n\t\t(uuid "{uuid}")\n\t)\n')
    z=s.find('\n\t(zone')
    if z<0: z=s.rfind(')')
    s=s[:z]+block+s[z:]

def add_via(x,y,size,drill,net,uuid):
    global s
    block=(f'\n\t(via\n\t\t(at {x} {y})\n\t\t(size {size})\n\t\t(drill {drill})\n'
           f'\t\t(layers "F.Cu" "B.Cu")\n\t\t(net "{net}")\n\t\t(uuid "{uuid}")\n\t)\n')
    z=s.find('\n\t(zone')
    if z<0: z=s.rfind(')')
    s=s[:z]+block+s[z:]

set_pad_net('Q101',1,'Q101_GATE'); set_pad_net('Q101',2,'12V_REV'); set_pad_net('Q101',3,'12V_FUSED')
set_pad_net('D201',1,'GND'); set_pad_net('D201',2,'3V3'); set_pad_net('D201',3,'VLINE_BIAS')
set_pad_net('X1',1,'HSE_PF0'); set_pad_net('X1',2,'GND'); set_pad_net('X1',3,'HSE_PF1'); set_pad_net('X1',4,'GND')

for u in [
 'a20c6722-c150-4a5f-9c2e-090876b3e656',
 '9a9ec0c9-57b5-43e4-bb31-c02563a529b4','62e63520-d409-48a7-bc84-a7815db4da67',
 'f3f4d297-b721-4be6-bcf8-22601ecec26a','e1c81bb8-2658-48aa-a565-035d2ad6cbff',
 '095546de-343c-4ba6-8be0-4de4e195e148','4bdaf3c9-900a-4471-89b3-838665741ab0',
 '4731036a-bb06-4bd7-8faf-6da3810d7af0','a230f8dd-5fd4-49fa-9d24-65faf92e0952',
 '390b4d11-fa8e-4fcf-bede-a4e04c490cf5','49734d92-ce61-4609-a8dc-0c1fed0c411a',
 'd295842b-caec-4a1f-9c14-572c31155ff0','2eebb895-b880-42a5-a302-36964b90c71f',
 '5113b932-4347-4f7c-b18e-1def4c9d41ba','607781ca-d5c7-4700-ba80-f43269fe0c41']:
    remove_uuid(u)

add_segment((16.25,20.75),(16.25,19.75),0.35,'F.Cu','12V_IN','ed627ba6-5757-4672-b138-f5b68179d6f7')
add_segment((16.25,19.75),(11.5,19.75),0.35,'F.Cu','12V_IN','fdf377e0-09bd-4b9f-a063-f46e4d165058')
add_segment((11.5,19.75),(11.5,20.75),0.35,'F.Cu','12V_IN','e910174e-e0df-432c-9999-e8d61c96a620')
add_segment((14.25,22.0),(11.75,22.0),0.15,'F.Cu','BRANCH_EN','d265896b-ac3b-454a-9d0f-68b706e28a56')
add_segment((11.75,22.0),(11.75,24.0),0.15,'F.Cu','BRANCH_EN','edc10fba-6c40-48f3-8fbe-9547f8df3f3f')
add_segment((11.75,24.0),(12.25,24.0),0.15,'F.Cu','BRANCH_EN','a45f1386-c59f-4fa8-883b-55c02b5f776e')
add_segment((15.25,22.0),(15.25,24.0),0.12,'F.Cu','ISENSE_COMP2','fe183aa3-17c4-46c6-b62b-9764c50d75e5')
add_segment((15.25,24.0),(13.25,24.0),0.12,'F.Cu','ISENSE_COMP2','7a84920d-3440-4f9d-9416-1d6306835424')
add_segment((12.6,22.9675),(12.6,24.55),0.15,'F.Cu','Q101_GATE','75001066-5f4c-4737-8816-0ec24e3729e7')
add_segment((12.6,24.55),(15.5,24.55),0.15,'F.Cu','Q101_GATE','2ca16852-84ff-4978-867a-6406399710f5')
add_segment((15.5,24.55),(15.5,24.25),0.15,'F.Cu','Q101_GATE','74e49804-9a68-4d89-a8df-74de1e5268b1')
add_segment((14.5,22.9675),(15.8,22.9675),0.35,'F.Cu','12V_REV','f23681cc-2c3a-4b17-b183-0064bd127281')
add_segment((15.8,22.9675),(15.8,24.6),0.35,'F.Cu','12V_REV','88bececb-f742-4756-8ac5-605f76c36f9b')
add_segment((15.8,24.6),(16.525,24.6),0.35,'F.Cu','12V_REV','3613cc20-80cc-4f78-a256-ef471834463e')
add_segment((13.55,21.0925),(17.0,21.0925),0.35,'F.Cu','12V_FUSED','feea8cb5-12a9-45e5-8856-0e6019edff48')
add_segment((17.0,21.0925),(17.0,22.75),0.35,'F.Cu','12V_FUSED','ba7f72bb-d3ce-4d5c-9491-f093893663a1')
add_via(17.0,22.75,0.5,0.3,'12V_FUSED','0f521ffb-e6ce-4c36-a1c4-22e6b06edfd7')

for u in ['18fd1d6a-cfa1-4a48-8bd4-6dc9fdf1cafa','4eafe467-ae05-48d3-b253-45c9fb98ba43',
          'a796a3d7-309d-413e-9117-4c23c6443862','26708c9d-ace9-4108-9862-f5fca251ae80',
          'bdc192e6-f7b5-4ccf-ad2d-01aeec31e042','573438a0-6430-4903-ba50-dbfc929fd155',
          '591862a5-f4f0-4282-b6d7-431b7782a74f']:
    remove_uuid(u)
add_segment((32.75,28.0),(32.75,29.0),0.12,'F.Cu','VLINE_FINE_VINM','4a4a1999-6ba2-44ac-8ce1-f2f8f855e506')
add_segment((32.75,29.0),(34.75,29.0),0.12,'F.Cu','VLINE_FINE_VINM','746c84b9-9c1f-4dc2-8243-dbf957932210')
add_segment((34.75,29.0),(34.75,30.0),0.12,'F.Cu','VLINE_FINE_VINM','6a7a9a50-9234-44a9-a71b-2ba45f6c24c7')
add_segment((33.8425,28.35),(33.0,28.35),0.15,'F.Cu','GND','89752f44-a0f1-4676-b604-5d4ea588782d')
add_via(33.0,28.35,0.5,0.3,'GND','1aeead38-424b-4a41-b50f-c953bbfe9a68')
add_segment((33.8425,30.25),(33.0,30.25),0.15,'F.Cu','3V3','e7d58196-86a9-4e0b-9659-19f61618ef96')
add_via(33.0,30.25,0.5,0.3,'3V3','d7713e34-ca34-4c88-a3ba-4e0fdfc7d1e3')
add_segment((35.7175,29.3),(37.0,29.3),0.15,'F.Cu','VLINE_BIAS','66bfc2de-e05b-4ec1-a1a7-8e8084260f11')
add_segment((37.0,29.3),(37.0,33.25),0.15,'F.Cu','VLINE_BIAS','7cb8b794-e890-4611-9672-003efca06a38')
add_segment((37.0,33.25),(34.25,33.25),0.15,'F.Cu','VLINE_BIAS','4585bb00-492f-4856-98a8-31bc7a71088c')
add_segment((34.25,33.25),(34.25,33.0),0.15,'F.Cu','VLINE_BIAS','4548a91e-e38d-4927-bdda-1e2f8190ac95')

for u in ['0de4c0b9-daa7-4bfa-aa09-ef0ef57f51d2','468972ea-289b-43d8-bc3f-8355d849cd5e',
          '4afd6e78-94e9-4abc-af64-bbc1d9ba6f58','cf3961bc-a709-4795-91d2-4b8e57583a58',
          '661da9ff-1dd0-446d-a3af-04c5ebd5235e','652cd806-8026-41aa-a313-791effa95604',
          'a04c39ed-9d97-4957-8269-88e844374f75',
          '3a12b577-05bf-4b4e-ab8d-ed489f9d2ad2','8299d42a-f89d-4b6c-afca-7389e0b0ae71',
          'fd57a0e7-70f9-4c38-98bc-467432ef67ad','d2f2020e-3536-4389-bbb4-c395ad0a7d07',
          'caccb88d-09f9-4487-ae58-d057aad94e55','6676aa40-9ae6-4e0d-b2a7-f0835fa1842b']:
    remove_uuid(u)
add_segment((5.3,33.05),(4.4,33.05),0.12,'F.Cu','HSE_PF0','e91792bf-9f7f-4254-a4fa-e340946f31d4')
add_segment((4.4,33.05),(4.4,30.4),0.12,'F.Cu','HSE_PF0','590b9d88-79b5-49bd-bfc3-a80a3ee2b4e4')
add_segment((4.4,30.4),(5.625,30.4),0.12,'F.Cu','HSE_PF0','e3526d9c-e324-486c-a3a6-787e943870f8')
add_segment((5.625,30.4),(5.625,29.2),0.12,'F.Cu','HSE_PF0','be93fcff-c706-4876-896f-47f90c5094d6')
add_segment((7.5,31.35),(8.45,31.35),0.12,'F.Cu','HSE_PF1','c8ed4df2-33ff-4a2d-8d6c-6457274fdca2')
add_segment((8.45,31.35),(8.45,32.45),0.12,'F.Cu','HSE_PF1','2d703f87-dd95-4e65-85bd-0524680187d6')
add_segment((8.45,32.45),(8.5,32.5),0.12,'F.Cu','HSE_PF1','5a28d037-38fe-41a5-9501-c205688f692d')
add_segment((8.5,32.5),(8.5,34.0),0.12,'F.Cu','HSE_PF1','b1121106-b873-4ef1-b11e-a02db89026b5')
add_segment((8.5,34.0),(5.875,34.0),0.12,'F.Cu','HSE_PF1','94cd71ae-b81d-431b-b92d-79f7549da89b')
add_segment((5.875,34.0),(5.875,34.625),0.12,'F.Cu','HSE_PF1','293cbbcc-251d-4d63-9227-4ee551af8642')

move_footprint('R205','21 38.3','21 38.5')
replace_segment_endpoint('487737a2-5752-4358-8659-48438e9026eb',('20.175','38.3'),('20.175','38.5'))
replace_segment_endpoint('322800a6-f495-455c-92b4-620240764456',('21.825','38.3'),('21.825','38.5'))

add_segment((16.325,11.7),(17.175,11.0),0.15,'F.Cu','GND','3b195f1a-4e32-4494-b4fe-5cbcd495d68d')

if s.count('(')!=s.count(')'):
    raise SystemExit(f'paren mismatch {s.count("(")} {s.count(")")}')
p.write_text(s,encoding='utf-8')
print('CONNECTIVITY_FIXES_APPLIED')
