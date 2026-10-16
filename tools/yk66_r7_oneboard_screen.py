#!/usr/bin/env python3
"""R7 cost-first one-board YK66 analytical screening. NOT electrical approval."""
import cmath, json, math
from itertools import product
R_SOURCE=(0.1,1,5)
R_LOAD=(5,10,20)
F_MID=(5000,10000,20000,30000)
F_GUARD=(1000,1500,2000,3000,4000,5000,*range(30000,700001,10000))
def y(f,g,hp,lp,delay,order):
    s=2j*math.pi*f
    return g*(s/(s+2*math.pi*hp))**order*(
        2*math.pi*lp/(s+2*math.pi*lp))*(
        2*math.pi*1e6/(s+2*math.pi*1e6))*cmath.exp(-s*delay*1e-6)
def db(rs,rl,yval):
    return 20*math.log10(abs(1+yval/(1/rs+1/rl)))
def main():
    ports=[{"Rs":rs,"Rl":rl,
        "S_ideal_for_3dB":(10**(3/20)-1)*(1/rs+1/rl),
        "baseline_mV_for_hypothetical_10mA":10/(1/rs+1/rl)}
        for rs,rl in product(R_SOURCE,R_LOAD)]
    caps=[{"nF":c,"mA_100Vac_50Hz":100*2*math.pi*50*c*1e-6,
           "mA_100Vac_60Hz":100*2*math.pi*60*c*1e-6,
           "dB_10kHz_10ohm_ideal_only":10*math.log10(
                1+(2*math.pi*10000*10*c*1e-9)**2)}
          for c in (22,47,100,1000)]
    count=0;passed=[]
    for order,hp,g,delay,lp in product((2,3,4),(300,600,1200,2400,4800),
                                      (.02,.1,.5,1,2,5),(.1,.5,1),
                                      (40000,100000,250000)):
        count+=1
        act=lambda f:y(f,g,hp,lp,delay,order)
        mains60=100*abs(act(60))*1000
        mid=min(db(rs,rl,act(f)) for rs,rl in product(R_SOURCE,R_LOAD) for f in F_MID)
        guard=min(db(rs,rl,act(f)) for rs,rl in product(R_SOURCE,R_LOAD) for f in F_GUARD)
        if mains60<=1 and mid>=3 and guard>=-.5: passed.append((order,hp,g,delay,lp))
    d={"status":"NONFAB_MAINS_HOLD","cases":len(ports),
       "min_S_for_3db":min(x["S_ideal_for_3dB"] for x in ports),
       "max_S_for_3db":max(x["S_ideal_for_3dB"] for x in ports),
       "model_sweeps":count,"ideal_screen_passes":len(passed),
       "passive_comparators":caps,
       "not_tested":["qualified mains barrier","fault disconnection","real loop stability",
                    "complex plant","current drive limits","prototype","PSE"],
       "manufacturing_allowed":False,"mains_connection_allowed":False}
    assert count==810 and len(passed)==0
    print(json.dumps(d,indent=2))
if __name__=="__main__":main()
