#!/usr/bin/env python3
from pathlib import Path
import sys

R303="198d641b-2f52-404c-ba27-5ad0e20e4acc"
OLD={
"3b8d62c5-ad05-41b9-a709-94f0a97cf089",
"e5ae09d1-3ffb-4eee-b38f-b003338d64da",
}
NEW=[
'''(segment
		(start 44.675 12.25)
		(end 43.5 12.5)
		(width 0.15)
		(locked yes)
		(layer "F.Cu")
		(net "BRANCH_EN")
		(uuid "37e17cc4-1964-4001-bd95-2078de3212a4")
	)''',
'''(segment
		(start 46.325 12.25)
		(end 46.5 12.5)
		(width 0.15)
		(locked yes)
		(layer "F.Cu")
		(net "BRANCH_GATE")
		(uuid "c707cc9f-4184-424a-9734-5de153873794")
	)''',
'''(segment
		(start 46.5 12.5)
		(end 46.5 15.25)
		(width 0.15)
		(locked yes)
		(layer "F.Cu")
		(net "BRANCH_GATE")
		(uuid "ca0db3df-0ed3-4f85-9a40-a3880dab0dd8")
	)''',
'''(segment
		(start 46.5 15.25)
		(end 45 15.75)
		(width 0.15)
		(locked yes)
		(layer "F.Cu")
		(net "BRANCH_GATE")
		(uuid "13235d7e-e52d-4159-a3b2-26c53b6afe84")
	)''',
'''(segment
		(start 45 15.75)
		(end 44.75 16)
		(width 0.15)
		(locked yes)
		(layer "F.Cu")
		(net "BRANCH_GATE")
		(uuid "555ef8ee-954a-402f-a63f-3164e0ace785")
	)'''
]
GND_VIA='''(via
		(at 43.29 11.46)
		(size 0.45)
		(drill 0.2)
		(layers "F.Cu" "B.Cu")
		(locked yes)
		(net "GND")
		(uuid "6e7a5b0d-4d48-4db2-ae3e-3061c21a8f95")
	)'''

def blocks(t):
    out=[]; dep=0; st=None
    for i,c in enumerate(t):
        if c=="(":
            if dep==1: st=i
            dep+=1
        elif c==")":
            dep-=1
            if dep==1 and st is not None:
                out.append((st,i+1,t[st:i+1])); st=None
    return out

def hit(t,u):
    q=f'(uuid "{u}")'
    return next(((a,b,x) for a,b,x in blocks(t) if q in x),None)

def main():
    p=Path(sys.argv[1]); t=p.read_text()
    h=hit(t,R303); assert h
    a,b,r=h
    r=r.replace('(layer "B.Cu")','(layer "F.Cu")',1)
    r=r.replace('(at 43.5 14)','(at 45.5 12.25)',1)
    for x,y in [('"B.SilkS"','"F.SilkS"'),('"B.Fab"','"F.Fab"'),('"B.CrtYd"','"F.CrtYd"'),('"B.Cu"','"F.Cu"'),('"B.Mask"','"F.Mask"')]:
        r=r.replace(x,y)
    r=r.replace('\n\t\t\t\t(justify mirror)','')
    r=r.replace('(property "MountSide" "BOTTOM_MANUAL_SMD"','(property "MountSide" "TOP_SMD"')
    r=r.replace('(attr smd exclude_from_pos_files)','(attr smd)')
    r=r.replace('(layers "F.Cu" "F.Mask")','(layers "F.Cu" "F.Mask" "F.Paste")')
    t=t[:a]+r+t[b:]
    for u in OLD:
        h=hit(t,u); assert h
        a,b,_=h
        if a and t[a-1]=="\t": a-=1
        if b<len(t) and t[b]=="\n": b+=1
        t=t[:a]+t[b:]
    z=t.find("\n\t(zone")
    assert z>0
    add="".join("\t"+x.replace("\n","\n\t")+"\n" for x in NEW+[GND_VIA])
    t=t[:z+1]+add+t[z+1:]
    p.write_text(t)
    q=p.read_text()
    r=hit(q,R303)[2]
    assert '(layer "F.Cu")' in r and '(at 45.5 12.25)' in r
    assert '(attr smd)' in r and 'exclude_from_pos_files' not in r
    for u in OLD: assert hit(q,u) is None
    for x in NEW+[GND_VIA]:
        u=x.split('(uuid "',1)[1].split('"',1)[0]
        assert hit(q,u)
    print("R303_AND_GND_STITCH_PATCH_PASS")

if __name__=="__main__": main()
