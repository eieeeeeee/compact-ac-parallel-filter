from pathlib import Path
import math,csv,json
p=Path(__file__).parent/'ngspice_decks'
def rd(name):
    filename=p/(name+'.dat')
    s=[]
    for line in filename.read_text().splitlines():
        a=line.strip().split()
        try:v=[float(x) for x in a]
        except ValueError:continue
        if len(v)>=3 and v[0]>0:
            s.append((v[0],complex(v[1],v[2])))
    if len(s)<100:raise SystemExit(f'Insufficient output {name}: {len(s)} rows; first lines {filename.read_text()[:600]}')
    return s
def ratio(a,b,f):
    k=min(range(len(a)),key=lambda i:abs(math.log(a[i][0]/f)))
    if abs(a[k][0]-b[k][0])/a[k][0]>1e-5:raise ValueError('Grid mismatch')
    return 20*math.log10(abs(a[k][1]/b[k][1])),a[k][0]
b2=rd('two_node_none')
b7=rd('seven_node_none')
records=[]
for name,base in [(x,b2) for x in ['two_node_rc18','two_node_rc22_330n','two_node_rc47_330n','two_node_c1u_direct']]+[(x,b7) for x in ['seven_node_rc18_n0','seven_node_rc18_n3','seven_node_rc18_n6']]:
    withf=rd(name)
    for hz in (50000,100000,1000000):
        db,actual=ratio(withf,base,hz)
        records.append({'model':name,'requested_hz':hz,'actual_hz':actual,'ratio_dB':db})
with (p/'ngspice_verification_summary.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
print(json.dumps(records,indent=2))
# For common reference, checks based on numerical independent MNA Python results.
reference={'two_node_rc18':{100000:-1.3136088691,1000000:-6.0479017356},
           'seven_node_rc18_n6':{100000:-5.5979219113,1000000:-13.8262246244}}
for name,points in reference.items():
    base=b2 if name.startswith('two') else b7
    for hz,expected in points.items():
        actual,_=ratio(rd(name),base,hz)
        print('CROSSCHECK',name,hz,'ngspice',actual,'scipy',expected,'difference',abs(actual-expected))
        if abs(actual-expected)>.22:raise SystemExit('SPICE / Python mismatch')
print('PASS: independent SPICE and numerical nodal models agree within 0.22 dB.')
