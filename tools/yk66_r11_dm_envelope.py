#!/usr/bin/env python3
"""YK66 R11 Norton DM virtual resistor model. MODEL ONLY, NONFAB/MAINS HOLD."""
import cmath
import csv
import itertools
import json
import math
from pathlib import Path

RS = (.1, 1., 5.)
RL = (5., 10., 20.)
F_TARGET = (5000, 10000, 20000, 30000)
F_GUARD = (1000, 1500, 2000, 3000, 4000, 4500, 35000, 50000, 70000, 100000, 150000, 300000, 500000, 700000)
FRACTION_3DB = 1 - 10**(-3/20)

def port_y(rs, rl, reactive=0):
    return 1/(rs*(1+1j*reactive)) + 1/(rl*(1-.5j*reactive))

def ideal_current(v_off, rs, rl, attenuation=3, reactive=0):
    return abs(v_off*port_y(rs,rl,reactive))*(1-10**(-attenuation/20))

def ideal_limit_db(v_off, rs, rl, imax):
    Ioff=abs(v_off*port_y(rs,rl))
    remaining=max(0,1-imax/Ioff)
    return math.inf if remaining==0 else -20*math.log10(remaining)

def virtual_y(f, G, hp, order, lp, drv, delay_us):
    s=2j*math.pi*f
    return (G*(s/(s+2*math.pi*hp))**order *
            (2*math.pi*lp/(s+2*math.pi*lp)) *
            (2*math.pi*drv/(s+2*math.pi*drv)) *
            cmath.exp(-s*delay_us*1e-6))

def on_volts(port, virtual, v_off, imax):
    """Steady-state radially scaled admittance, not an actual driver or stable feedback."""
    source=port*v_off
    def f(alpha):
        den=port+alpha*virtual
        if abs(den)<1e-20:return complex(float('inf')), float('inf')
        v=source/den
        return v, abs(alpha*virtual*v)
    voltage,current=f(1)
    if current<=imax:return voltage,current,1.
    low,high=0.,1.
    for i in range(1,101):
        voltage,current=f(i/100)
        if current>=imax:
            low,high=(i-1)/100,i/100
            break
    for _ in range(45):
        mid=(low+high)/2
        if f(mid)[1]>=imax:high=mid
        else:low=mid
    alpha=(low+high)/2
    voltage,current=f(alpha)
    return voltage,current,alpha

def db(v_off,v_on):
    return 20*math.log10(abs(v_off)/abs(v_on)) if abs(v_on)>0 else math.inf

def main(outdir='results/yk66_r11'):
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    nine=[]
    for rs,rl in itertools.product(RS,RL):
        v_off=.1
        current3=ideal_current(v_off,rs,rl,3)
        current50=ideal_current(v_off,rs,rl,50)
        nine.append({'Rs_Ohm':rs,'Rl_Ohm':rl,
            'Zp_Ohm':round((1/port_y(rs,rl)).real,8),
            'I_3db_100mV_mA':round(1000*current3,6),
            'I_50db_100mV_mA':round(1000*current50,6),
            'I_3db_fixed_10mA_source_mA':round(FRACTION_3DB*10,6),
            'ceiling_20mA_dB':round(ideal_limit_db(v_off,rs,rl,.02),6) if .02<.1*abs(port_y(rs,rl)) else 'UNBOUNDED_IDEAL'})
    with (outdir/'nine_ports.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=nine[0].keys());w.writeheader();w.writerows(nine)
    candidates=[]
    for G,hp,order,lp,delay in itertools.product((.1,.5,2.,5.),(800.,1600.),(4,6),(80000.,200000.),(.1,.5)):
        m60=100*abs(virtual_y(60,G,hp,order,lp,250000.,delay))*1000
        lowdb=math.inf; maxgain=-math.inf; bad_real=[]
        for freq in F_TARGET+F_GUARD:
            y=virtual_y(freq,G,hp,order,lp,250000.,delay)
            if y.real<0:bad_real.append(freq)
            for rs,rl,reactive in itertools.product(RS,RL,(-1.,0.,1.)):
                p=port_y(rs,rl,reactive)
                value,_current,_alpha=on_volts(p,y,.1,.02)
                val=db(.1,value)
                if freq in F_TARGET:lowdb=min(lowdb,val)
                if freq in F_GUARD:maxgain=max(maxgain,-val)
        candidates.append({'gain_S':G,'hp_Hz':hp,'order':order,'lp_Hz':lp,
            'delay_us':delay,'I_limit_mA':20,
            'mains_60Hz_ideal_mA':round(m60,6),
            'min_5_30k_dB':round(lowdb,6),'max_guard_gain_dB':round(maxgain,6),
            'negative_real_Y_Hz':bad_real,
            'screen_pass':bool(m60<=1 and lowdb>=3 and maxgain<=.5 and not bad_real)})
    with (outdir/'64_candidate_ideal_models.json').open('w',encoding='utf8') as f:
        json.dump(candidates,f,indent=2)
    ref10=[];ref100=[]
    for rs,rl,x in itertools.product(RS,RL,(-1.,0.,1.)):
        p=port_y(rs,rl,x)
        v=.01/p
        ref10.append(db(v,on_volts(p,4.5,v,.02)[0]))
        ref100.append(db(.1,on_volts(p,4.5,.1,.02)[0]))
    summary={'status':'NONFAB_MAINS_HOLD','cases':len(nine),
        'worst_3db_100mV_mA':max(r['I_3db_100mV_mA'] for r in nine),
        'worst_50db_100mV_mA':max(r['I_50db_100mV_mA'] for r in nine),
        '20mA_3db_100mV_cases':sum(r['ceiling_20mA_dB']=='UNBOUNDED_IDEAL' or r['ceiling_20mA_dB']>=3 for r in nine),
        '20mA_all9_3db_max_noise_mV':round(1000*.02/(FRACTION_3DB*10.2),6),
        'ideal_real_4p5S_10mA_min_27case_dB':round(min(ref10),6),
        'ideal_real_4p5S_100mV_min_27case_dB':round(min(ref100),6),
        'model_variants':len(candidates),
        'passes_all_math_gates':sum(c['screen_pass'] for c in candidates),
        'physical_parts_confirmed':False,'hardware_stability_confirmed':False,
        'manufacturing_allowed':False,'mains_allowed':False}
    (outdir/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
    print(json.dumps(summary,indent=2))
    assert len(nine)==9 and len(candidates)==64 and summary['passes_all_math_gates']==0
    return summary

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--outdir',default='results/yk66_r11')
    main(p.parse_args().outdir)
