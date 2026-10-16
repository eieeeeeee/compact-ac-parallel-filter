#!/usr/bin/env python3
"""YK66 R3 analytical extra-low-voltage screening. NOT a mains or fabrication design."""
import argparse
import cmath
import csv
import json
import math

STATUS = "NONFAB_HOLD_MAINS_HOLD"
ASSUMPTIONS = dict(assumed_port_ohm=10.0, assumed_noise_current_peak_a=0.010,
                   nominal_compensation_ratio=0.5, bandpass_center_hz=10000.0,
                   bandpass_q=8.0, uncompensated_delay_s=0.5e-6)
SAMPLES = (5000,10000,20000,30000,100000,300000,700000)

def bandpass(f, f0=10000.0, q=8.0):
    if min(f,f0,q)<=0:
        raise ValueError("frequency and Q must be positive")
    x=f/f0
    return (1j*x/q)/(1-x*x+1j*x/q)

def residual(f, params=ASSUMPTIONS):
    if f<=0 or params["assumed_port_ohm"]<=0 or params["assumed_noise_current_peak_a"]<=0:
        raise ValueError("invalid frequency or port")
    k=params["nominal_compensation_ratio"]
    delay=params["uncompensated_delay_s"]
    if not 0<=k<=1 or delay<0:
        raise ValueError("invalid drive")
    b=bandpass(f,params["bandpass_center_hz"],params["bandpass_q"])
    return abs(1-k*b*cmath.exp(-2j*math.pi*f*delay))

def reduction_db(r):
    if r<=0: raise ValueError("invalid residual")
    return -20*math.log10(r)

def passive_shunt_db(f, r, c):
    """Ideal Norton port + parallel ideal C ONLY; no ESL, ESR or line rating."""
    if min(f,r,c)<=0: raise ValueError("invalid passive values")
    return 10*math.log10(1+(2*math.pi*f*r*c)**2)

def sample(f):
    r=residual(f)
    baseline=ASSUMPTIONS["assumed_port_ohm"]*ASSUMPTIONS["assumed_noise_current_peak_a"]*1000
    return dict(frequency_hz=int(f), baseline_voltage_peak_mv=round(baseline,6),
                controlled_voltage_peak_mv=round(baseline*r,6),
                reduction_db_positive_means_better=round(reduction_db(r),6))

def build_report():
    points=[sample(f) for f in SAMPLES]
    guard=[sample(1000*k) for k in range(30,701)]
    worst=min(guard,key=lambda x:x["reduction_db_positive_means_better"])
    center=sample(10000)
    return dict(project="YK66 R3 idealized 12V-or-less isolated bench screening",
                status=STATUS, model_only=True, mains_authorized=False,
                kicad_manufacturing_release=False, assumptions=ASSUMPTIONS,
                center=center, frequency_samples=points,
                guard=dict(points=len(guard), worst_frequency_hz=worst["frequency_hz"],
                           worst_reduction_db=worst["reduction_db_positive_means_better"],
                           model_only_pass=worst["reduction_db_positive_means_better"]>=-0.5),
                ideal_passive_comparison=[
                    dict(frequency_hz=f,port_ohm=r,capacitance_uf=c*1e6,
                         reduction_db=round(passive_shunt_db(f,r,c),6))
                    for f,r in ((10000,10),(1000000,50)) for c in (0.1e-6,1e-6)],
                release_note="NO AC100V CONNECTION. No real component / fault / stability validation.")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json",default="yk66_r3.json")
    ap.add_argument("--csv",default="yk66_r3_points.csv")
    args=ap.parse_args()
    r=build_report()
    with open(args.json,"w",encoding="utf-8") as f: json.dump(r,f,indent=2)
    with open(args.csv,"w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(r["frequency_samples"][0]))
        w.writeheader()
        w.writerows(r["frequency_samples"])
    print("10kHz theoretical reduction:",r["center"]["reduction_db_positive_means_better"],
          "dB; worst model guard:",r["guard"]["worst_reduction_db"],
          "dB; MAINS HOLD:",not r["mains_authorized"])

if __name__=="__main__":
    main()
