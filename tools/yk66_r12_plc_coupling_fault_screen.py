#!/usr/bin/env python3
"""YK66 R12: 5-30kHz ideal PLC transformer/capacitor fault and cost screening.
Not an electrical schematic, qualified part, AC100V safety test or fab release."""
import argparse, cmath, csv, json, math
from itertools import product
from pathlib import Path

N=1.307                 # 750510476 nominal primary / secondary turns ratio
LM=870e-6               # nominal primary magnetic inductance, no core loss
C=(22e-9,47e-9,100e-9,220e-9,470e-9,1e-6)
RS=(.1,1.,5.)
RL=(5.,10.,20.)
FS=(5000.,10000.,20000.,30000.)
RDRIVE=2.0              # ASSUMED, not an approved amplifier
VPEAK=5.0               # ASSUMED, not verified 12V supply swing

def cap_z(f,c):
    return 1/(2j*math.pi*f*c)

def zparallel(x,y):
    return x*y/(x+y)

def fres(c):
    return 1/(2*math.pi*math.sqrt(c*LM/N**2))

def off_branch(f,c,r_loss,primary_open):
    lm=2j*math.pi*f*LM
    mag=lm if primary_open else zparallel(lm,complex(RDRIVE))
    return r_loss+cap_z(f,c)+mag/N**2

def injected(f,c,rs,rl):
    # Ideal transformer+magnetizing branch, *no* core/winding/parasitic losses.
    zport=1/(1/rs+1/rl)
    zload=cap_z(f,c)+zport
    zm=2j*math.pi*f*LM
    zseen=zparallel(zm,N*N*zload)
    vp=VPEAK*zseen/(RDRIVE+zseen)
    return abs(vp/(N*zload)),abs((VPEAK-vp)/RDRIVE)

def make(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    resonances=[dict(C_nF=round(c*1e9),open_fault_resonance_kHz=round(fres(c)/1000,6),
                     line_branch_at_100V60Hz_mA=round(100/abs(off_branch(60,c,.2,True))*1000,6))
                for c in C]
    rows=[]
    for c,f,rs,rl in product(C,FS,RS,RL):
        il,ip=injected(f,c,rs,rl)
        req=.1*(1-10**(-3/20))*(1/rs+1/rl)
        rows.append(dict(C_nF=round(c*1e9),frequency_Hz=f,Rs_ohm=rs,Rl_ohm=rl,
                         ideal_line_Ipeak_mA=round(1000*il,6),ideal_driver_Ipeak_mA=round(1000*ip,6),
                         needed_3db_100mV_Ipeak_mA=round(1000*req,6),
                         theoretical_current_enough=il>=req))
    with (out/'coupler_9port_216_cases.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    fault=[]
    for c,r,f,rs,rl in product(C,(.2,2.,10.),(50.,60.,*FS),RS,RL):
        zp=1/(1/rs+1/rl)
        z_open=off_branch(f,c,r,True)
        z_short=off_branch(f,c,r,False)
        fault.append(dict(C_nF=round(c*1e9),loss_ohm=r,freq_Hz=f,Rs_ohm=rs,Rl_ohm=rl,
                          open_impedance_ohm=round(abs(z_open),6),
                          short_impedance_ohm=round(abs(z_short),6),
                          open_atten_dB=round(20*math.log10(abs(1+zp/z_open)),6),
                          short_atten_dB=round(20*math.log10(abs(1+zp/z_short)),6)))
    with (out/'fault_972_cases.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=fault[0]);w.writeheader();w.writerows(fault)
    cost={"target_JPY":3500,"IRM03_12_ex_tax_JPY":915,"Wurth750510476_ex_tax_JPY":872,
          "AFE031_ex_tax_JPY":1038,"OPA197_ex_tax_JPY":412,
          "AFE_3part_subtotal_tax_in_JPY":round((915+872+1038)*1.1,2),
          "AFE_3part_remaining_to_target_JPY":round(3500-(915+872+1038)*1.1,2),
          "OPA_3part_subtotal_tax_in_JPY":round((915+872+412)*1.1,2),
          "OPA_3part_remaining_to_target_JPY":round(3500-(915+872+412)*1.1,2),
          "all_safety_driver_PCB_SMT_shipping_priced":False}
    result={"status":"MAINS_FAB_HOLD","resonances":resonances,"driven_cases":len(rows),
        "off_fault_cases":len(fault),"cost":cost,"mains_allowed":False,
        "manufacturing_allowed":False,"real_controller_simulated":False,
        "transformer_core_loss_simulated":False,"isolation_certified_for_YK66":False}
    assert len(rows)==216 and len(fault)==972
    assert abs(fres(470e-9)-10287)<2
    assert abs(fres(100e-9)-22301.6)<2
    assert abs(1000*injected(10000,100e-9,.1,5)[0]-24)<.1
    assert cost["AFE_3part_remaining_to_target_JPY"]==392.5
    assert cost["OPA_3part_remaining_to_target_JPY"]==1081.1
    assert all(not result[k] for k in ("mains_allowed","manufacturing_allowed","isolation_certified_for_YK66"))
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print('R12 MODEL REGRESSION PASS; nine port + fault modes; MAINS & FAB HOLD')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--outdir',default='results/yk66_r12')
    make(ap.parse_args().outdir)
