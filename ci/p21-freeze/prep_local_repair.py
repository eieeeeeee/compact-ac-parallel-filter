#!/usr/bin/env python3
from pathlib import Path
import re, sys

p=Path(sys.argv[1])
s=p.read_text(encoding="utf-8")

def block_end(text,start):
    d=0; ins=False; esc=False
    for i in range(start,len(text)):
        c=text[i]
        if ins:
            if esc: esc=False
            elif c=="\\": esc=True
            elif c=='"': ins=False
        else:
            if c=='"': ins=True
            elif c=='(': d+=1
            elif c==')':
                d-=1
                if d==0: return i+1
    raise RuntimeError("unbalanced")

def find_fp(ref):
    pos=s.find(f'(property "Reference" "{ref}"')
    if pos<0: raise RuntimeError("ref not found "+ref)
    st=s.rfind("(footprint",0,pos); en=block_end(s,st)
    return st,en,s[st:en]

def set_pad_net(ref,num,net):
    global s
    st,en,b=find_fp(ref)
    q=b.find(f'(pad "{num}" ')
    if q<0: raise RuntimeError(f"{ref}.{num} missing")
    ps=q; pe=block_end(b,ps); pb=b[ps:pe]
    pb=re.sub(r'\n\s*\(net "[^"]*"\)','',pb)
    u=pb.find("\n\t\t\t(uuid ")
    if u<0: raise RuntimeError("uuid anchor missing")
    pb=pb[:u]+f'\n\t\t\t(net "{net}")'+pb[u:]
    b=b[:ps]+pb+b[pe:]
    s=s[:st]+b+s[en:]

def remove_uuid(u,kind="segment"):
    global s
    pos=s.find(f'(uuid "{u}")')
    if pos<0: raise RuntimeError("missing "+u)
    st=s.rfind("("+kind,0,pos); en=block_end(s,st)
    s=s[:st]+s[en:]

def move_fp(ref,old,new):
    global s
    st,en,b=find_fp(ref)
    needle=f"(at {old})"
    if needle not in b: raise RuntimeError(ref+" at mismatch")
    b=b.replace(needle,f"(at {new})",1)
    s=s[:st]+b+s[en:]

def drag_endpoint(u,old,new):
    global s
    pos=s.find(f'(uuid "{u}")'); st=s.rfind("(segment",0,pos); en=block_end(s,st); b=s[st:en]
    changed=0
    for fld in ("start","end"):
        a=f"({fld} {old[0]} {old[1]})"
        if a in b:
            b=b.replace(a,f"({fld} {new[0]} {new[1]})",1); changed+=1
    if changed!=1: raise RuntimeError(f"{u} endpoint changed={changed}")
    s=s[:st]+b+s[en:]

# Physical pin/net parity
for n,net in [(1,"Q101_GATE"),(2,"12V_REV"),(3,"12V_FUSED")]: set_pad_net("Q101",n,net)
for n,net in [(1,"GND"),(2,"3V3"),(3,"VLINE_BIAS")]: set_pad_net("D201",n,net)
for n,net in [(1,"HSE_PF0"),(2,"GND"),(3,"HSE_PF1"),(4,"GND")]: set_pad_net("X1",n,net)

# Remove only the copper that physically collides with newly-correct pads.
# Q101 / 12V_IN
remove_uuid("a20c6722-c150-4a5f-9c2e-090876b3e656")
# Q101 / BRANCH_EN local chain and transition via
for u in [
"9a9ec0c9-57b5-43e4-bb31-c02563a529b4","62e63520-d409-48a7-bc84-a7815db4da67",
"f3f4d297-b721-4be6-bcf8-22601ecec26a","e1c81bb8-2658-48aa-a565-035d2ad6cbff",
"095546de-343c-4ba6-8be0-4de4e195e148","4bdaf3c9-900a-4471-89b3-838665741ab0",
"4731036a-bb06-4bd7-8faf-6da3810d7af0","a230f8dd-5fd4-49fa-9d24-65faf92e0952"]:
    remove_uuid(u)
remove_uuid("ca0bb152-89a7-4ac1-bbcc-e8cc596fbc06","via")
# Q101 / ISENSE_COMP2 local chain
for u in [
"390b4d11-fa8e-4fcf-bede-a4e04c490cf5","49734d92-ce61-4609-a8dc-0c1fed0c411a",
"d295842b-caec-4a1f-9c14-572c31155ff0","2eebb895-b880-42a5-a302-36964b90c71f",
"5113b932-4347-4f7c-b18e-1def4c9d41ba","607781ca-d5c7-4700-ba80-f43269fe0c41"]:
    remove_uuid(u)

# D201 VINM crossing: create a small local ratsnest for router
for u in ["4eafe467-ae05-48d3-b253-45c9fb98ba43","a796a3d7-309d-413e-9117-4c23c6443862"]:
    remove_uuid(u)

# X1: remove branches tied to pads that change function.
for u in ["661da9ff-1dd0-446d-a3af-04c5ebd5235e","652cd806-8026-41aa-a313-791effa95604","a04c39ed-9d97-4957-8269-88e844374f75"]:
    remove_uuid(u)
for u in ["3a12b577-05bf-4b4e-ab8d-ed489f9d2ad2","8299d42a-f89d-4b6c-afca-7389e0b0ae71",
          "fd57a0e7-70f9-4c38-98bc-467432ef67ad","d2f2020e-3536-4389-bbb4-c395ad0a7d07",
          "caccb88d-09f9-4487-ae58-d057aad94e55","6676aa40-9ae6-4e0d-b2a7-f0835fa1842b"]:
    remove_uuid(u)

# True R205/C6 physical short
move_fp("R205","21 38.3","21 38.5")
drag_endpoint("487737a2-5752-4358-8659-48438e9026eb",(20.175,38.3),(20.175,38.5))
drag_endpoint("322800a6-f495-455c-92b4-620240764456",(21.825,38.3),(21.825,38.5))

if s.count("(")!=s.count(")"): raise RuntimeError("paren mismatch")
p.write_text(s,encoding="utf-8")
print("P21_REPAIR_PREPARED")
