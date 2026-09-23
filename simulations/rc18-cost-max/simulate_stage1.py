#!/usr/bin/env python3
import cmath, csv, json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"out"
OUT.mkdir(exist_ok=True)

BASE={
 "L1":0.56e-6,"L2":0.56e-6,"L3":0.56e-6,
 "C1":68e-9,"C2":68e-9,"C3":68e-9,
 "Cinj":1.0e-6,"Rinj":2.20,"Rsh":0.330,
}
# Stage 1 changes only MCU ordering code (RCT6 -> RCT3).
# Power stage, reconstruction filter and injection path are intentionally identical.
RC18=dict(BASE)

def solve(a,b):
    n=len(b)
    a=[list(row) for row in a]; b=list(b)
    for i in range(n):
        p=max(range(i,n), key=lambda r: abs(a[r][i]))
        if abs(a[p][i])<1e-30: raise RuntimeError("singular matrix")
        a[i],a[p]=a[p],a[i]; b[i],b[p]=b[p],b[i]
        piv=a[i][i]
        for j in range(i,n): a[i][j]/=piv
        b[i]/=piv
        for r in range(n):
            if r==i: continue
            f=a[r][i]
            if f==0: continue
            for j in range(i,n): a[r][j]-=f*a[i][j]
            b[r]-=f*b[i]
    return b

def response(p,f,zline):
    w=2*math.pi*f
    # Nodes: n1,n2,n3,n4,n5,line. Source GAN_SW is fixed at 1 V AC.
    Y=[[0j]*6 for _ in range(6)]; I=[0j]*6
    def branch(i,j,y):
        if i is not None: Y[i][i]+=y
        if j is not None: Y[j][j]+=y
        if i is not None and j is not None:
            Y[i][j]-=y; Y[j][i]-=y
    # L1 from fixed 1 V source to n1
    y=1/(1j*w*p["L1"]); Y[0][0]+=y; I[0]+=y*1.0
    branch(0,1,1/(1j*w*p["L2"]))
    branch(1,2,1/(1j*w*p["L3"]))
    branch(0,None,1j*w*p["C1"])
    branch(1,None,1j*w*p["C2"])
    branch(2,None,1j*w*p["C3"])
    branch(2,3,1j*w*p["Cinj"])
    branch(3,4,1/p["Rinj"])
    branch(4,5,1/p["Rsh"])
    branch(5,None,1/zline)
    v=solve(Y,I)
    return v[5]

freqs=[10**(2+i*(5/250)) for i in range(251)] # 100 Hz .. 10 MHz
zlines=[0.2,1.0,5.0,10.0,20.0]
rows=[]
max_mag=0.0; max_phase=0.0
for z in zlines:
    for f in freqs:
        hb=response(BASE,f,z); hr=response(RC18,f,z)
        mb=20*math.log10(max(abs(hb),1e-300))
        mr=20*math.log10(max(abs(hr),1e-300))
        pb=math.degrees(cmath.phase(hb)); pr=math.degrees(cmath.phase(hr))
        dm=abs(mr-mb); dp=abs(pr-pb)
        max_mag=max(max_mag,dm); max_phase=max(max_phase,dp)
        rows.append((z,f,mb,mr,dm,pb,pr,dp))

with (OUT/"stage1_plant_equivalence.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["zline_ohm","freq_hz","rc17_mag_db","rc18_mag_db","delta_mag_db","rc17_phase_deg","rc18_phase_deg","delta_phase_deg"]); w.writerows(rows)
summary={
 "stage":"RC18-COST-MAX S1",
 "change":"STM32G474RCT6 -> STM32G474RCT3 only",
 "sweep_hz":[100,10000000],
 "line_impedance_ohm":zlines,
 "max_magnitude_delta_db":max_mag,
 "max_phase_delta_deg":max_phase,
 "pass": max_mag < 1e-12 and max_phase < 1e-12
}
(OUT/"stage1_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
if not summary["pass"]: raise SystemExit(2)
