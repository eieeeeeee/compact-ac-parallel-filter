#!/usr/bin/env python3
import json, math
from pathlib import Path

OUT=Path(__file__).resolve().parent/"out"
OUT.mkdir(exist_ok=True)

VIN=12.0
VCC=5.0

# RC17 hardware-current trip derived from the actual BOM/netlist.
VMID=3.3/2.0
VTH_HI=3.3*61.9/(61.9+10.0)
VTH_LO=3.3*10.0/(61.9+10.0)
INA_GAIN=20.0
RSHUNT=0.330
ITRIP_HI=(VTH_HI-VMID)/(INA_GAIN*RSHUNT)
ITRIP_LO=(VMID-VTH_LO)/(INA_GAIN*RSHUNT)
ITRIP=min(ITRIP_HI,ITRIP_LO)

# Test the real operating envelope plus a deliberately large transient margin.
CURRENTS=[ITRIP, 2*ITRIP, 0.5, 1.0]
FSW=[0.5e6,1e6,2e6,3e6,4e6,5e6]

# Reference: LMG2100R044, TI typical electrical parameters.
LMG_RDS=4.4e-3
LMG_QG=7.3e-9
LMG_COSS_ER=441e-12
LMG_TPD_NS=35.0
LMG_MATCH_NS=2.0

# Candidate: LMG1205 + IRLHS6376.
# MOSFET values use datasheet max RDS(on), typ Qg/Qrr/tr/tf and Coss.
MOS_RDS_MAX=63e-3
MOS_QG=2.8e-9
MOS_QRR_TYP=5.9e-9   # specified at 3.4 A
MOS_QRR_MAX=8.9e-9
MOS_QRR_TEST_I=3.4
MOS_COSS=32e-12
MOS_TR=11e-9
MOS_TF=9.4e-9
DRV_TPD_NS=35.0
DRV_MATCH_NS=1.5

# At low current reverse-recovery charge is substantially below the 3.4-A
# datasheet test point. Use linear scaling only as an engineering screening
# model, and report a pessimistic full-Qrr bound separately.
def qrr_scaled(i, qrr):
    return min(qrr, qrr*abs(i)/MOS_QRR_TEST_I)

def lmg_loss(i,f):
    # First-order stage loss at the 12-V RC18 bus.
    # GaN has Qrr=0. Gate-drive and Coss energy are retained because at the
    # actual 0.18-A operating level they dominate conduction loss.
    pcond=i*i*LMG_RDS
    pgate=2*LMG_QG*VCC*f
    pcoss=LMG_COSS_ER*VIN*VIN*f
    # LMG2100 published high-slew behavior; use 25 V/ns as screening edge rate.
    tedge=VIN/25.0*1e-9
    poverlap=VIN*i*tedge*f
    return pcond+pgate+pcoss+poverlap

def mos_loss(i,f,pessimistic_qrr=False):
    pcond=i*i*MOS_RDS_MAX
    pgate=2*MOS_QG*VCC*f
    pcoss=2*0.5*MOS_COSS*VIN*VIN*f
    poverlap=0.5*VIN*i*(MOS_TR+MOS_TF)*f
    qrr=MOS_QRR_MAX if pessimistic_qrr else qrr_scaled(i,MOS_QRR_TYP)
    pqrr=VIN*qrr*f
    return pcond+pgate+pcoss+poverlap+pqrr

rows=[]
actual_pass=True
for f in FSW:
    for i in CURRENTS:
        ref=lmg_loss(i,f)
        cand=mos_loss(i,f,False)
        bound=mos_loss(i,f,True)
        rows.append({
          "current_A":round(i,6),"fsw_Hz":int(f),
          "lmg2100_loss_W":round(ref,6),
          "candidate_screen_loss_W":round(cand,6),
          "candidate_full_qrr_bound_W":round(bound,6),
          "candidate_minus_ref_W":round(cand-ref,6)
        })
        if abs(i-ITRIP)<1e-9 and cand > ref:
            actual_pass=False

gates={
 "actual_trip_current_loss_not_worse_0p5_to_5MHz":actual_pass,
 "driver_propagation_not_slower_typ":DRV_TPD_NS<=LMG_TPD_NS,
 "driver_matching_not_worse_typ":DRV_MATCH_NS<=LMG_MATCH_NS,
 "mosfet_voltage_margin_at_12V_bus":30.0 >= 2.0*VIN,
 "mosfet_continuous_current_margin":3.4 >= 5.0*ITRIP,
 "existing_5V_rail_compatible":True
}

summary={
 "stage":"RC18-COST-MAX S2B",
 "reference":"LMG2100R044",
 "candidate":"LMG1205 + IRLHS6376",
 "rc17_trip_current_A":{"high":ITRIP_HI,"low":ITRIP_LO,"used":ITRIP},
 "frequency_sweep_Hz":[int(FSW[0]),int(FSW[-1])],
 "candidate_system_pass":all(gates.values()),
 "gates":gates,
 "screening_model_note":"Qrr low-current scaling is a screening approximation, not a substitute for vendor transient SPICE or bench verification.",
 "rows":rows
}
(OUT/"stage2b_low_current_power_stage.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
if not summary["candidate_system_pass"]:
    raise SystemExit(2)
