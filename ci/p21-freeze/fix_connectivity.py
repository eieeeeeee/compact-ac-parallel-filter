#!/usr/bin/env python3
from pathlib import Path
import sys, uuid, re

p=Path(sys.argv[1])
s=p.read_text(encoding="utf-8")
NS=uuid.UUID("7f0c9a4e-63ad-4d89-8ee0-998cb2912345")

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

def remove_uuid(text,u,kind=None):
    tok=f'(uuid "{u}")'
    pos=text.find(tok)
    if pos<0: raise RuntimeError("missing UUID "+u)
    kinds=[kind] if kind else ["segment","via"]
    st=-1
    for k in kinds:
        q=text.rfind("("+k,0,pos)
        if q>st: st=q
    if st<0: raise RuntimeError("block start not found "+u)
    en=block_end(text,st)
    if tok not in text[st:en]: raise RuntimeError("UUID outside block "+u)
    return text[:st]+text[en:]

def find_fp(text,ref):
    pos=text.find(f'(property "Reference" "{ref}"')
    if pos<0: raise RuntimeError("ref not found "+ref)
    st=text.rfind("(footprint ",0,pos)
    en=block_end(text,st)
    return st,en,text[st:en]

def patch_fp_at(text,ref,new_at):
    st,en,b=find_fp(text,ref)
    m=re.search(r'\n\t\t\(at [^\n]+\)',b)
    if not m: raise RuntimeError("footprint at not found "+ref)
    b=b[:m.start()]+f'\n\t\t(at {new_at})'+b[m.end():]
    return text[:st]+b+text[en:]

def patch_pad_net_in_fp(text,ref,num,netname):
    st,en,b=find_fp(text,ref)
    marker=f'(pad "{num}" '
    q=b.find(marker)
    if q<0: raise RuntimeError(f"{ref} pad {num} not found")
    ps=b.rfind("\t\t(pad ",0,q+1)
    if ps<0: ps=q
    pe=block_end(b,ps)
    pb=b[ps:pe]
    if "(net " in pb:
        pb=re.sub(r'\n\t\t\t\(net "[^"]*"\)',f'\n\t\t\t(net "{netname}")',pb,count=1)
    else:
        u=pb.find("\n\t\t\t(uuid ")
        if u<0: raise RuntimeError(f"{ref}.{num} uuid anchor missing")
        pb=pb[:u]+f'\n\t\t\t(net "{netname}")'+pb[u:]
    b=b[:ps]+pb+b[pe:]
    return text[:st]+b+text[en:]

def patch_segment_endpoint(text,u,oldxy,newxy):
    tok=f'(uuid "{u}")'; pos=text.find(tok)
    if pos<0: raise RuntimeError("missing segment "+u)
    st=text.rfind("(segment",0,pos); en=block_end(text,st); b=text[st:en]
    old=f"({oldxy[0]} {oldxy[1]})"; new=f"({newxy[0]} {newxy[1]})"
    # endpoint fields are '(start x y)' or '(end x y)'
    changed=0
    for fld in ("start","end"):
        needle=f"({fld} {oldxy[0]} {oldxy[1]})"
        if needle in b:
            b=b.replace(needle,f"({fld} {newxy[0]} {newxy[1]})",1); changed+=1
    if changed!=1: raise RuntimeError(f"endpoint patch {u} changed={changed}")
    return text[:st]+b+text[en:]

def uid(label): return str(uuid.uuid5(NS,label))

def seg(label,net,a,c,width,layer="F.Cu"):
    return f'''\n\t(segment
\t\t(start {a[0]} {a[1]})
\t\t(end {c[0]} {c[1]})
\t\t(width {width})
\t\t(locked yes)
\t\t(layer "{layer}")
\t\t(net "{net}")
\t\t(uuid "{uid("seg:"+label)}")
\t)'''

def via(label,net,xy,size=0.5,drill=0.3):
    return f'''\n\t(via
\t\t(at {xy[0]} {xy[1]})
\t\t(size {size})
\t\t(drill {drill})
\t\t(layers "F.Cu" "B.Cu")
\t\t(locked yes)
\t\t(net "{net}")
\t\t(uuid "{uid("via:"+label)}")
\t)'''

# 1. Physical pad/net parity on PCB.
s=patch_fp_at(s,"Q101","14.9 23.6625 90")
for n,nn in [("1","Q101_GATE"),("2","12V_REV"),("3","12V_FUSED")]:
    s=patch_pad_net_in_fp(s,"Q101",n,nn)
for n,nn in [("1","GND"),("2","3V3"),("3","VLINE_BIAS")]:
    s=patch_pad_net_in_fp(s,"D201",n,nn)

# 2. Delete exact Q101 conflict-path objects by UUID.
REMOVE_SEG=[
# Q101_GATE lower serpentine
"c2ed973e-e2e3-401b-be03-00bc0f0251c5","0818cb2b-8392-475f-b1c6-af5a38a3ca93",
"03ff4175-329f-4ff0-82ed-90e11d7bd786","3bc9dd77-528a-40bd-a9fd-f7e1d427d1ce",
"eb9b7961-2a35-4300-9d1f-ecc69b2867c8","ea6c29fd-b88a-48a9-8cca-4eca388b3487",
"2b7bd42f-2bf6-417c-8335-f3664967be74","38220afd-3ad2-4de9-99f9-6456a323e3a2",
# BRANCH_EN F crossing chain + last B segment
"9a9ec0c9-57b5-43e4-bb31-c02563a529b4","62e63520-d409-48a7-bc84-a7815db4da67",
"f3f4d297-b721-4be6-bcf8-22601ecec26a","e1c81bb8-2658-48aa-a565-035d2ad6cbff",
"095546de-343c-4ba6-8be0-4de4e195e148","4bdaf3c9-900a-4471-89b3-838665741ab0",
"4731036a-bb06-4bd7-8faf-6da3810d7af0","a230f8dd-5fd4-49fa-9d24-65faf92e0952",
"48f6b885-a47c-4d47-832f-ec82e55a7e9a","3f795b0b-5c71-4d88-af73-b141aaa9292e",
"40c43245-6e14-4857-83d7-ccaf6af8591b","d4b570d0-4483-42cb-a5dc-a6730cc915d5",
"eeda7219-71c4-40d9-b0c4-4a3eec6ae676","1406b82f-6044-409e-b262-b205b3c4cea7",
"6c0b4cb3-681f-41df-8bbd-c5ffab983e05",
# ISENSE_COMP2 F crossing chain + last B segment
"390b4d11-fa8e-4fcf-bede-a4e04c490cf5","49734d92-ce61-4609-a8dc-0c1fed0c411a",
"d295842b-caec-4a1f-9c14-572c31155ff0","2eebb895-b880-42a5-a302-36964b90c71f",
"5113b932-4347-4f7c-b18e-1def4c9d41ba","607781ca-d5c7-4700-ba80-f43269fe0c41",
"88f51a9c-5bc1-4686-8a47-24171dcd066f","8a216ffc-9b24-41bc-b5d9-e6bb86e0f8a4",
"73f27399-eaac-436c-bd58-44f83b37b61a","2cc92eb3-0e90-4f2b-b8e0-95632fce7262",
"72e6345a-b76a-47e2-9ec9-0b3193e980e1","62937b37-fdc1-4dd9-ba5e-8c260f89933c",
"ece446b9-bd14-4d10-b7a5-d810897323fa","eed9bfac-6983-4a63-9888-439f54896e17",
"3800ffd6-434f-4f78-928a-de8896907288","f4e57ad9-e254-47f1-90d9-84eb24ea976f",
"41efb583-7222-4136-9bd3-ca3cb3d0526d",
# 12V_IN central path
"53aea10b-0310-4996-9eea-1d3d4ae409b6","a20c6722-c150-4a5f-9c2e-090876b3e656",
"e46463e3-87c2-4bc6-9e40-e4e75597b4f9",
# 12V_FUSED B backbone (split below)
"e01b5c62-cc44-4164-af80-a5cf6bbf6297",
# D201 VLINE_FINE crossing
"18fd1d6a-cfa1-4a48-8bd4-6dc9fdf1cafa","4eafe467-ae05-48d3-b253-45c9fb98ba43",
"a796a3d7-309d-413e-9117-4c23c6443862","26708c9d-ace9-4108-9862-f5fca251ae80",
# X1 HSE_PF0 crossing
"661da9ff-1dd0-446d-a3af-04c5ebd5235e","652cd806-8026-41aa-a313-791effa95604",
"a04c39ed-9d97-4957-8269-88e844374f75",
]
for u in REMOVE_SEG: s=remove_uuid(s,u,"segment")
for u in ["ca0bb152-89a7-4ac1-bbcc-e8cc596fbc06","c3e8cde2-216c-4d18-a382-4d2685d874a2"]:
    s=remove_uuid(s,u,"via")

# 3. R205 +0.20 mm and drag exactly the two attached segment endpoints.
s=patch_fp_at(s,"R205","21 38.5")
s=patch_segment_endpoint(s,"487737a2-5752-4358-8659-48438e9026eb",(20.175,38.3),(20.175,38.5))
s=patch_segment_endpoint(s,"322800a6-f495-455c-92b4-620240764456",(21.825,38.3),(21.825,38.5))

# 4. Add replacement routing.
new=[]
# Q101 gate/source/drain
for i,(a,c) in enumerate([
((16.15,22.0),(16.7,20.9)),((16.7,20.9),(14.3,20.9)),
((14.3,20.9),(14.3,24.6)),((14.3,24.6),(13.95,24.6)),
((13.95,24.6),(15.25,24.625)),
]): new.append(seg(f"qgate{i}","Q101_GATE",a,c,0.15))
new.append(seg("qsource","12V_REV",(15.85,24.6),(16.525,24.6),0.35))
new.append(seg("qdrain_f","12V_FUSED",(14.9,22.725),(14.9,21.5),0.35))
new.append(via("qdrain","12V_FUSED",(14.9,21.5),0.6,0.3))
new.append(seg("qdrain_b","12V_FUSED",(14.9,21.5),(14.9,22.75),0.35,"B.Cu"))
new.append(seg("12vfused_l","12V_FUSED",(10.0,22.75),(14.9,22.75),0.35,"B.Cu"))
new.append(seg("12vfused_r","12V_FUSED",(14.9,22.75),(20.25,22.75),0.35,"B.Cu"))

# BRANCH transition left
new.append(via("branch_new","BRANCH_EN",(10.5,22.0),0.5,0.3))
for i,(a,c,lay) in enumerate([
((14.5,21.75),(14.5,21.2),"B.Cu"),((14.5,21.2),(10.5,21.2),"B.Cu"),
((10.5,21.2),(10.5,22.0),"B.Cu"),((10.5,22.0),(10.5,25.25),"F.Cu"),
((10.5,25.25),(10.75,25.25),"F.Cu"),
]): new.append(seg(f"branch{i}","BRANCH_EN",a,c,0.15,lay))

# ISENSE transition left
new.append(via("isense_new","ISENSE_COMP2",(11.6,21.6),0.5,0.3))
for i,(a,c,lay) in enumerate([
((15.5,22.0),(15.5,20.9),"B.Cu"),((15.5,20.9),(11.6,20.9),"B.Cu"),
((11.6,20.9),(11.6,21.6),"B.Cu"),((11.6,21.6),(11.6,25.75),"F.Cu"),
((11.6,25.75),(11.25,25.75),"F.Cu"),
]): new.append(seg(f"isense{i}","ISENSE_COMP2",a,c,0.12,lay))

# 12V_IN lowered
for i,(a,c) in enumerate([
((16.875,20.125),(16.5,20.2)),((16.5,20.2),(10.5,20.2)),((10.5,20.2),(11.0,21.25)),
]): new.append(seg(f"12vin{i}","12V_IN",a,c,0.35))

# D201 VLINE_FINE detour
for i,(a,c) in enumerate([
((32.75,28.0),(32.75,27.25)),((32.75,27.25),(34.75,27.25)),
((34.75,27.25),(34.75,29.0)),((34.75,29.0),(33.75,29.0)),
]): new.append(seg(f"d201fine{i}","VLINE_FINE_VINM",a,c,0.12))

# X1 DNP keepout detour
for i,(a,c) in enumerate([
((5.25,33.0),(4.35,32.5)),((4.35,32.5),(4.35,30.0)),((4.35,30.0),(5.625,29.2)),
]): new.append(seg(f"x1hse{i}","HSE_PF0",a,c,0.12))

# Explicit R605.2 -> GND via closure.
new.append(seg("r605gnd","GND",(16.325,11.7),(17.175,11.0),0.15))

anchor=s.find("\n\t(zone")
if anchor<0: raise RuntimeError("zone insertion anchor not found")
s=s[:anchor]+"".join(new)+s[anchor:]

p.write_text(s,encoding="utf-8")
print("CONNECTIVITY_TEXT_PATCH_APPLIED",len(REMOVE_SEG),"segments removed,",len(new),"items added")
