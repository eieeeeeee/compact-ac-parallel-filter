#!/usr/bin/env python3
"""Traceable re-evaluation of the YK66 P15 archived ideal-model output.

A PASS here verifies only the 324 archived hypothetical rows and that BOTH
Japanese 50 and 60 Hz conditions are screened. It DOES NOT validate hardware,
safety, loop stability, performance, or authorize AC100V connection/fabrication.
The GitHub CSV is an accessible library-parsed EXPORT, not byte-identical
to the original Library CSV; consult source SHA in R4 handoff archive.
"""
import argparse
import csv
import json
from pathlib import Path

COLUMNS = ("rs_ohm","rl_ohm","conductance_S","hp_hz","delay_us",
           "min_reduction_5_30_dB","max_amplification_5_700_dB",
           "current_30k_mA","mains_50Hz_current_100Vrms_mA",
           "mains_60Hz_current_100Vrms_mA","reduction_5k_dB",
           "reduction_10k_dB","reduction_30k_dB")

def check(csv_path):
    with open(csv_path,encoding="utf-8",newline="") as fh:
        rd=csv.DictReader(fh)
        assert tuple(rd.fieldnames)==COLUMNS, "Unexpected CSV source or parsed index column"
        rows=[{k:float(v) for k,v in r.items()} for r in rd]
    assert len(rows)==324, "324-case historical provenance check failed"
    def meets_common(row):
        return row["min_reduction_5_30_dB"]>=3 and row["max_amplification_5_700_dB"]<=0.5
    f50=[r for r in rows if meets_common(r) and r["mains_50Hz_current_100Vrms_mA"]<=1]
    both=[r for r in f50 if r["mains_60Hz_current_100Vrms_mA"]<=1]
    assert len(f50)==21, "Historical 50Hz model count changed"
    assert len(both)==15, "50/60Hz dual-valid model count changed"
    return {
        "status":"HISTORICAL_IDEAL_CSV_INTEGRITY_PASS_ONLY",
        "all_cases":len(rows),
        "50Hz_ideal_candidates":len(f50),
        "50Hz_and_60Hz_ideal_candidates":len(both),
        "50Hz_only_candidates_rejected_for_dual_frequency":len(f50)-len(both),
        "model_validity":"ONLY_SPECIFIED_SOURCE_LOAD_AND_DISCRETE_TEST_FREQUENCIES",
        "physical_two_terminal_controller_exists":False,
        "ac100v_electrical_safety_validated":False,
        "measured_noise_reduction":False,
        "manufacturing_release":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--csv",default="historical/YK66_P15_BANDPASS_SHUNT_SWEEP_20261015.csv")
    p.add_argument("--out",default="yk66_r4_screen.json")
    a=p.parse_args()
    result=check(a.csv)
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":
    main()
