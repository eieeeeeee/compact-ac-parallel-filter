#!/usr/bin/env python3
"""YK66 R5 replay of archived P15 ideal shunt results, extra-frequency
regression and changed source/load check. This NEVER validates real hardware.
"""
import argparse
import cmath
import csv
import json
import math
from pathlib import Path

COLUMNS = ["rs_ohm","rl_ohm","conductance_S","hp_hz","delay_us",
 "min_reduction_5_30_dB","max_amplification_5_700_dB","current_30k_mA",
 "mains_50Hz_current_100Vrms_mA","mains_60Hz_current_100Vrms_mA",
 "reduction_5k_dB","reduction_10k_dB","reduction_30k_dB"]

def y(f,g,hp,delay_us):
    s=1j*2*math.pi*f
    w=2*math.pi*hp
    wlp=2*math.pi*100000
    return g*(s/(s+w))**4*(wlp/(s+wlp))*cmath.exp(-s*delay_us*1e-6)

def attenuation_db(f,rs,rl,g,hp,delay_us):
    b=1/rs+1/rl
    return 20*math.log10(abs(1+y(f,g,hp,delay_us)/b))

def screen(source):
    with Path(source).open(encoding="utf-8",newline="") as stream:
        rows_reader=csv.DictReader(stream)
        assert rows_reader.fieldnames==COLUMNS, "Unexpected source CSV fields"
        rows=[{k:float(v) for k,v in row.items()} for row in rows_reader]
    assert len(rows)==324, "Unexpected archive case count"
    count50=0
    both=[]
    for idx,row in enumerate(rows):
        rs,rl,g,hp,t=(row[k] for k in COLUMNS[:5])
        for f,col in [(5000,"reduction_5k_dB"),(10000,"reduction_10k_dB"),(30000,"reduction_30k_dB")]:
            assert abs(attenuation_db(f,rs,rl,g,hp,t)-row[col])<1e-8, "Source-to-model discrepancy"
        for f,col in [(50,"mains_50Hz_current_100Vrms_mA"),(60,"mains_60Hz_current_100Vrms_mA")]:
            assert abs(100e3*abs(y(f,g,hp,t))-row[col])<1e-8, "Mains ideal data discrepancy"
        sparse=(row["min_reduction_5_30_dB"]>=3 and row["max_amplification_5_700_dB"]<=.5)
        if sparse and row["mains_50Hz_current_100Vrms_mA"]<=1:count50+=1
        if sparse and row["mains_50Hz_current_100Vrms_mA"]<=1 and row["mains_60Hz_current_100Vrms_mA"]<=1:
            both.append((idx,row))
    assert count50==21 and len(both)==15, "Changed original screening output"
    amplified_below5k=0
    full_impedance_count=0
    details=[]
    for idx,r in both:
        rs,rl,g,hp,t=(r[k] for k in COLUMNS[:5])
        low=min(attenuation_db(f,rs,rl,g,hp,t) for f in range(1000,5000,100))
        mid=min(attenuation_db(f,rs,rl,g,hp,t) for f in range(5000,30001,1000))
        high=min(attenuation_db(f,rs,rl,g,hp,t) for f in range(30000,700001,1000))
        if low<0:amplified_below5k+=1
        robust=True
        for alt_rs in (0.1,1.0,5.0):
            for alt_rl in (5.0,10.0,20.0):
                alt_min=min(attenuation_db(f,alt_rs,alt_rl,g,hp,t) for f in range(5000,30001,1000))
                alt_guard=min(attenuation_db(f,alt_rs,alt_rl,g,hp,t) for f in range(30000,700001,10000))
                if alt_min<3 or alt_guard<-.5:robust=False
        if robust:full_impedance_count+=1
        details.append({"source_index":idx,"original_source_ohm":rs,"original_load_ohm":rl,
            "G_siemens":g,"hp_hz":hp,"delay_us":t,
            "min_db_1to5khz":round(low,8),"min_atten_5to30khz_db":round(mid,8),
            "worst_gain_30to700khz_db":round(-high,8),
            "stable_3db_across_9_source_load_combinations":robust})
    assert amplified_below5k==15, "Recheck low band finding"
    assert full_impedance_count==0, "Recheck 9 impedance robustness finding"
    return {"status":"HISTORICAL_BEHAVIORAL_MODEL_ONLY_PASS_NONFAB_HOLD",
      "total_historical_cases":len(rows),"50hz_only_pass":count50,
      "50hz_and_60hz_pass":len(both),"cases_amplifying_1_to_5khz":amplified_below5k,
      "cases_robust_over_all_9_source_load_pairs":full_impedance_count,
      "mains_authorized":False,"manufacturing_authorized":False,"hardware_validated":False,
      "limitation":"Y is an ideal actuator; no driver, stability, faults, AC100V insulation or physical plant",
      "cases":details}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--csv",default="historical/YK66_P15_BANDPASS_SHUNT_SWEEP_20261015.csv")
    ap.add_argument("--out",default="yk66_r5_gate.json")
    args=ap.parse_args()
    info=screen(args.csv)
    Path(args.out).write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in info.items() if k!="cases"},ensure_ascii=False))
if __name__=="__main__":main()
