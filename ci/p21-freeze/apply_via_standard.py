#!/usr/bin/env python3
from pathlib import Path
import re, sys

TARGETS=set([
  "336e2cc4-d7ce-43d0-af21-aa1d2a6e614a",
  "4a03bd11-b4f0-4184-addd-4363083993c7",
  "57fb4a4b-9c4a-4908-963f-0518ce420546",
  "6e664564-7cba-40a1-9e39-7b3d4f490aa2",
  "a8ed9bfa-42dd-46ec-aeae-d174e38fe944",
  "056a8523-629d-4991-8e58-4ee606feba0f",
  "48966cb6-2ba6-4988-a0fa-1af8625f62a1",
  "8c88e2b6-db2b-42b8-b358-9ba4d58d0a40",
  "277d72cf-0ebb-4405-b388-802a8fd8542c",
  "67040e07-a2db-4b41-9d3a-1deb76de314c",
  "1bc0dbec-3028-489b-a44d-b5bd810cd127",
  "af91d810-fddd-49fc-b785-0295112b0ead",
  "b73d1a1f-8eba-4e3f-9f55-2a5285f49e79",
  "f3c166ca-66d0-4239-9c94-d83a6d461da8",
  "cd35add2-a7bd-4d08-b097-6a72087bf063",
  "e5e69435-f2b2-42f5-a20f-120f264437fc",
  "fcd7a5d7-bf8d-4289-96fc-afb7f29c2285",
  "07873bca-3ccf-48c3-89e3-491cc45728a6",
  "33bb3796-d847-471e-8d0e-660ca5ca6c56",
  "7010402b-bbed-4674-aab0-0daecabdcbc9",
  "f54aaaaf-275f-4a0b-96e9-020ae8fdf798",
  "252d4d78-e406-467c-8a0f-d17f1abd06dc",
  "500f5175-81bb-48ca-846f-e3d7e6c2610f",
  "96ec71a6-63f1-449f-9c95-d545e89cfe74",
  "f22ac8a3-cae6-415d-a77b-a1adc2b13ae7",
  "89508242-61d0-4283-8db7-3d0aaac032ee",
  "c3963329-cff5-451f-a15b-0585acb57c3d",
  "3f1915de-1a27-434e-9c4b-4ce549bea210",
  "569d7b6d-48cb-4a4e-be8d-00a0398a7419",
  "89df1565-d35b-43a1-8f16-76b85f964cbf",
  "1ebaaeb2-6da0-4d2d-a782-9c390ede37ff",
  "d454091c-e660-4974-9127-e848ec2a3480",
  "01f1288f-dd5f-43eb-914d-3a89fa6edda7",
  "023e0ccd-43a6-4c05-98bb-c1455061ac40",
  "10626083-9c0f-482a-93dc-e40ce323534c",
  "d3a220f7-6400-4396-9faa-474e310327b8",
  "ca0bb152-89a7-4ac1-bbcc-e8cc596fbc06",
  "9599c6a6-718c-44f0-9e2c-e153ce2e9c60",
  "5f4a2164-5434-452a-b062-39494ad7443f",
  "bdaa48ee-9ea6-4275-a474-66b07267b77c",
  "249c2e0a-56e8-479b-a1a9-8108ea5d65e5",
  "ebaf5aa0-31d8-481c-8485-6a4b1353d75c",
  "3d5369c8-a50f-40bf-8962-b90fc598f59b",
  "45682ff0-bf6a-44be-96e8-c95bb05cbaee",
  "54938e26-1148-4038-9029-922a340a9da7",
  "60dff402-4287-4ff1-a5e5-d3f6f682383e",
  "bd63a8e2-2a3c-4707-b339-b06c8ad195e4",
  "d29ffbef-48ab-40a3-b9eb-be85ea66dabf",
  "d3076201-5230-45e2-b84a-bfd734818b4d",
  "33b9ae64-1c34-44e3-93b7-183068952c86",
  "35195a7f-d2a1-46f1-96cc-e8fad58f927a",
  "496bf6e3-70a9-4c03-90f3-cc5fb7f51406",
  "88f831cb-e0e1-4756-98a3-8a9b6a357dc0",
  "c19144b4-c7d6-46d8-be1c-f5b87a9250cd",
  "5a2ecffd-cbd8-4016-8409-d71e394d6f29",
  "c689c5e7-5a8e-4c72-aa6e-cfac4aa38554",
  "d883f6eb-9d40-48ec-967e-39842c9db311",
  "f3b7969a-57ac-4107-8492-a92b5d9d5447"
])

def block_end(s,start):
    depth=0; ins=False; esc=False
    for i in range(start,len(s)):
        c=s[i]
        if ins:
            if esc: esc=False
            elif c=="\\": esc=True
            elif c=='"': ins=False
        else:
            if c=='"': ins=True
            elif c=='(': depth+=1
            elif c==')':
                depth-=1
                if depth==0: return i+1
    raise RuntimeError("unbalanced")

p=Path(sys.argv[1])
s=p.read_text(encoding="utf-8")
out=[]; pos=0; changed=[]
while True:
    m=re.search(r'(?m)^[ \\t]*\\(via\\b',s[pos:])
    if not m:
        out.append(s[pos:]); break
    st=pos+m.start(); en=block_end(s,st)
    out.append(s[pos:st])
    b=s[st:en]
    um=re.search(r'\\(uuid "([^"]+)"\\)',b)
    if um and um.group(1) in TARGETS:
        old_size=re.search(r'\\(size ([0-9.]+)\\)',b)
        old_drill=re.search(r'\\(drill ([0-9.]+)\\)',b)
        if not old_size or not old_drill:
            raise SystemExit("missing size/drill "+um.group(1))
        b=re.sub(r'\\(size [0-9.]+\\)','(size 0.5)',b,count=1)
        b=re.sub(r'\\(drill [0-9.]+\\)','(drill 0.3)',b,count=1)
        changed.append((um.group(1),old_size.group(1),old_drill.group(1)))
    out.append(b); pos=en
new=''.join(out)
missing=TARGETS-{x[0] for x in changed}
if missing:
    raise SystemExit("missing target UUIDs: "+",".join(sorted(missing)))
p.write_text(new,encoding="utf-8")
print("VIA_STANDARD_CHANGED",len(changed))
for u,sz,dr in changed:
    print(u,sz,dr,"-> 0.5 0.3")
