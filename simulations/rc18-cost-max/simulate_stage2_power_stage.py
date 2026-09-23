#!/usr/bin/env python3
import json, math
from pathlib import Path

OUT=Path(__file__).resolve().parent/"out"
OUT.mkdir(exist_ok=True)

VIN=12.0
CURRENTS=[0.5,1.0,2.0,3.0,4.5]
FSW=[250e3,500e3,1e6,1.5e6]

# System-level RC18 acceptance gates.
MAX_LOSS_W=1.0
MAX_DROOP_PCT=0.35
MIN_CURRENT_A=10.0
MIN_FSW_HZ=1.0e6
MAX_PROP_NS=35.0

def lmg_loss(i,f):
    r=4.4e-3
    coss_er=441e-12
    qg=7.3e-9
    # TI first-order guidance: transition time ~ VIN / 25 V/ns.
    ttr=(VIN/25.0)*1e-9
    pcond=i*i*r
    psw=VIN*i*ttr*f + VIN*VIN*coss_er*f
    pdrv=2*qg*5.0*f
    return pcond+psw+pdrv

def csd87330_loss(i,f):
    # TI typical effective AC on-impedance at 12 V/5 V drive:
    # HS 9.45 mOhm, LS 3.6 mOhm. Use 50% modulation as conservative symmetric RC18 case.
    reff=0.5*(9.45e-3+3.6e-3)
    # Dynamic values: HS tr/tf 6.8/1.7 ns, LS 7.5/1.6 ns.
    trtf=(6.8+1.7)*1e-9
    qrr=15e-9       # conservative larger LS reverse recovery value
    coss=(310+580)*1e-12
    qg=(4.8+9.6)*1e-9
    pcond=i*i*reff
    poverlap=0.5*VIN*i*trtf*f
    pqrr=VIN*qrr*f
    pcoss=0.5*coss*VIN*VIN*f
    pgate=qg*5.0*f
    return pcond+poverlap+pqrr+pcoss+pgate

devices={
 "LMG2100R044":{
   "cost_10_usd":7.53,"area_mm2":24.75,"current_A":35.0,"max_fsw_Hz":10e6,
   "prop_ns":35.0,"loss":lmg_loss,"architecture":"integrated GaN + driver"},
 "CSD87330Q3D+DGD0507A":{
   "cost_10_usd":1.0496+0.5205,"area_mm2":10.89+9.0,"current_A":20.0,"max_fsw_Hz":1.5e6,
   "prop_ns":23.0,"loss":csd87330_loss,"architecture":"30V NexFET power block + dual-input driver"}
}

results={}
for name,d in devices.items():
    rows=[]
    worst=0
    for f in FSW:
        for i in CURRENTS:
            p=d["loss"](i,f); worst=max(worst,p)
            rows.append({"current_A":i,"fsw_Hz":f,"loss_W":round(p,6)})
    droop=4.5*(4.4e-3 if name.startswith("LMG") else 0.5*(9.45e-3+3.6e-3))/VIN*100
    gates={
      "current_margin":d["current_A"]>=MIN_CURRENT_A,
      "frequency":d["max_fsw_Hz"]>=MIN_FSW_HZ,
      "propagation":d["prop_ns"]<=MAX_PROP_NS,
      "worst_loss_under_1W":worst<=MAX_LOSS_W,
      "droop_under_0p35pct":droop<=MAX_DROOP_PCT,
    }
    results[name]={
      "cost_10_usd":d["cost_10_usd"],"area_mm2":d["area_mm2"],
      "worst_loss_W":round(worst,4),"droop_pct_at_4p5A":round(droop,4),
      "gates":gates,"system_pass":all(gates.values()),"points":rows
    }

cand=results["CSD87330Q3D+DGD0507A"]
base=results["LMG2100R044"]
summary={
 "stage":"RC18-COST-MAX S2 power-stage qualification",
 "reference":"LMG2100R044",
 "candidate":"CSD87330Q3D + DGD0507A",
 "candidate_system_pass":cand["system_pass"],
 "cost_reduction_pct":round((1-cand["cost_10_usd"]/base["cost_10_usd"])*100,1),
 "area_reduction_pct":round((1-cand["area_mm2"]/base["area_mm2"])*100,1),
 "important_note":"Candidate is not lower-loss than GaN; pass means RC18 system electrical/thermal gates are met, not that silicon loss beats LMG2100.",
 "results":results
}
(OUT/"stage2_power_stage.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
if not cand["system_pass"]: raise SystemExit(2)
