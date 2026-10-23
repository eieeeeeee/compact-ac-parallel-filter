#!/usr/bin/env python3
from pathlib import Path
import csv,math
P=Path(__file__).parent/'decks'
names=['C010','C022','C047','C100','C220','C470','C500','RC100']
def rd(name):
    data=[]
    for line in (P/(name+'.dat')).read_text().splitlines():
        v=line.strip().split()
        try:a=[float(x) for x in v]
        except ValueError: continue
        if len(a)>=3 and a[0]>0:data.append((a[0],complex(a[1],a[2])))
    if len(data)<250:raise ValueError('SPICE output missing: '+name)
    return data
records=[]
for family in ['two','seven']:
    base=rd(family+'_NONE')
    for nm in names:
        result=rd(family+'_'+nm)
        for f in [100000,1000000]:
            i=min(range(len(result)),key=lambda x:abs(math.log(result[x][0]/f)))
            assert abs(result[i][0]-base[i][0])<1e-3
            d=20*math.log10(abs(result[i][1]/base[i][1]))
            records.append((family,nm,f,result[i][0],d))
with (P/'official_ngspice_key_results.csv').open('w',newline='') as out:
    w=csv.writer(out);w.writerow(['model','configuration','target_Hz','ngspice_actual_Hz','attenuation_dB']);w.writerows(records)
# Independent nodal reference from Rev29 Python analysis, fixed ESR .05 and ESL30n.
expected={('two','C100',100000):.88,('two','C100',1000000):-41.65,
          ('two','C500',100000):-11.05,('two','C500',1000000):-32.74,
          ('two','RC100',100000):-1.32,('two','RC100',1000000):-6.11}
for family,nm,f,_,d in records:
    k=(family,nm,f)
    if k in expected:
        delta=abs(d-expected[k])
        print('CROSSCHECK',family,nm,f,'SPICE=',round(d,4),'Python=',expected[k],'error=',round(delta,4))
        if delta>.15:raise SystemExit('Simulation discrepancy')
print('PASS: 18 ngspice networks; key points agree with independent calculation')
