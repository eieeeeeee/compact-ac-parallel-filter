#!/usr/bin/env python3
"""YK66 R9 ideal phasor cancellation vs phase lag. NOT a mains design."""
import cmath, csv, math
from pathlib import Path

FREQUENCIES_HZ=(5000,10000,30000)
DELAYS_US=(0.0,0.1,0.5,1.0,5.0,10.0)
FRACTIONS=(0.2920542156,0.5,1.0)

def attenuation_db(alpha, phase_rad):
    residual=abs(1-alpha*cmath.exp(-1j*phase_rad))
    return float('inf') if residual<1e-14 else -20*math.log10(residual)

def phase_budget_degrees(target_db, alpha=1.0):
    if alpha<=0: return 0.0
    eps=10**(-target_db/20)
    cos_term=(1+alpha**2-eps**2)/(2*alpha)
    if cos_term>1: return 0.0
    return math.degrees(math.acos(max(-1.0,cos_term)))

def sweep_rows():
    return [dict(frequency_hz=f,delay_us=t,
                 phase_deg=round(360*f*t*1e-6,6),
                 cancelled_fraction=a,
                 ideal_attenuation_db=round(attenuation_db(a,2*math.pi*f*t*1e-6),6))
            for f in FREQUENCIES_HZ for t in DELAYS_US for a in FRACTIONS]

def test():
    assert math.isclose(attenuation_db(.5,0),6.020599913,abs_tol=1e-7)
    assert math.isclose(attenuation_db(.5,math.pi/3),1.249387366,abs_tol=1e-5)
    assert attenuation_db(.5,math.pi/2)<0
    assert math.isclose(360*30000*1e-6,10.8)
    assert math.isclose(360*30000*5e-6,54.0)
    ns=phase_budget_degrees(50)/(360*30000)*1e9
    assert 16<ns<17
    assert 0.18<phase_budget_degrees(50)<0.182
    assert phase_budget_degrees(50,.5)==0
    assert len(sweep_rows())==54
    return ns

if __name__=="__main__":
    ns=test()
    rows=sweep_rows()
    fn=Path("yk66_r9_phase_sweep.csv")
    with fn.open("w",encoding="utf-8",newline="") as fh:
        writer=csv.DictWriter(fh,fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    print("R9: 9 theoretical phase regression checks PASS; nonfab/mains HOLD")
    print(f"30kHz ideal 50dB effective lag bound: {ns:.4f} ns")
