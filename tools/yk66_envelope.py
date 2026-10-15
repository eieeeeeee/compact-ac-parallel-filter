#!/usr/bin/env python3
"""YK66 non-fabrication analytical envelope. No mains-connected design is implied.

This is a deliberately small linear R-C sanity model, not electrical-safety,
EMC, closed-loop, transient, stability, or power-stage validation.
"""
import argparse
import csv
import json
import math
from pathlib import Path

CONFIG = {
    "name": "YK66",
    "release_status": "NONFAB_HOLD",
    "ac_supply_vrms": [100.0, 107.0],
    "fundamental_hz": [50, 60],
    "candidate_coupling_f": 1.0e-6,
    "candidate_damping_ohm": 4.7,
    "candidate_shunt_ohm": 0.33,
    "injection_limit_peak_a": 0.178,
    "ideal_injection_drive_peak_v": 12.0,
    "candidate_psu": {"model": "IRM-03-12", "v": 12.0, "max_current_a": 0.250, "rated_w": 3.0, "reference_price_yen": 915},
    "historical_mcu_unit_estimate_yen": 1300,
    "target_yen": 3500,
}

HF_HZ = [5000, 10000, 20000, 30000, 700000]


def series_z_magnitude(f_hz: float, c_f: float, series_ohm: float) -> float:
    """Magnitude |R + 1/(j 2 pi f C)|, for positive f, C and nonnegative R."""
    if not (f_hz > 0 and c_f > 0 and series_ohm >= 0):
        raise ValueError("Invalid passive R-C values")
    return math.hypot(series_ohm, 1.0 / (2.0 * math.pi * f_hz * c_f))


def amplitude_tolerance_for_attenuation_db(db: float) -> float:
    """Residual ratio needed for |Ierror/Iref| to reach attenuation db."""
    if db < 0:
        raise ValueError("db must be >= 0")
    return 10.0 ** (-db / 20.0)


def build_report() -> dict:
    cfg = CONFIG
    r = cfg["candidate_damping_ohm"] + cfg["candidate_shunt_ohm"]
    c = cfg["candidate_coupling_f"]
    lim = cfg["injection_limit_peak_a"]
    vinj = cfg["ideal_injection_drive_peak_v"]

    # Fundamental AC current below is a HYPOTHETICAL PASSIVE L-N series RC.
    # It is not the current or safe voltage of an active semiconductor bridge.
    mains = []
    for vrms in cfg["ac_supply_vrms"]:
        for f in cfg["fundamental_hz"]:
            z = series_z_magnitude(f, c, r)
            irms = vrms / z
            mains.append({
                "mains_vrms": vrms,
                "frequency_hz": f,
                "series_z_ohm": z,
                "passive_rc_rms_current_a": irms,
                "passive_rc_rms_damping_loss_w": irms**2 * cfg["candidate_damping_ohm"],
                "passive_rc_rms_shunt_loss_w": irms**2 * cfg["candidate_shunt_ohm"],
                "passive_rc_apparent_power_va": irms * vrms,
            })

    # These are differential injection drive test-tone calculations, NOT
    # mains fault/surge estimates and NOT a prediction of active noise reduction.
    hf = []
    for f in HF_HZ:
        z = series_z_magnitude(f, c, r)
        ideal_drive_current = vinj / z
        hf.append({
            "frequency_hz": f,
            "series_z_ohm": z,
            "ideal_12v_peak_tone_current_a": ideal_drive_current,
            "ratio_to_178ma_trip": ideal_drive_current / lim,
            "drive_peak_v_at_178ma_trip": z * lim,
            "12v_tone_exceeds_trip": ideal_drive_current > lim,
        })

    # 178mA is a hardware TRIP, not a permissible operating point.
    psu = cfg["candidate_psu"]
    power = {
        "psu_model": psu["model"],
        "nominal_output_power_w": psu["rated_w"],
        "psu_max_current_a": psu["max_current_a"],
        "12v_times_trip_current_w_not_continuous": psu["v"] * lim,
        "unallocated_nominal_w_after_hypothetical_trip_w": psu["rated_w"] - psu["v"] * lim,
        "qualification": "Trip current is not continuous draw; PSU transient behavior and loads remain unknown",
    }
    price = {
        "pcb_parts_assembly_budget_yen": cfg["target_yen"],
        "reference_psu_yen_ex_tax": psu["reference_price_yen"],
        "historical_mcu_estimate_yen_ex_tax": cfg["historical_mcu_unit_estimate_yen"],
        "priced_or_estimated_partial_yen": psu["reference_price_yen"] + cfg["historical_mcu_unit_estimate_yen"],
        "remaining_before_essential_unknown_costs_yen": cfg["target_yen"] - (psu["reference_price_yen"] + cfg["historical_mcu_unit_estimate_yen"]),
        "price_status": "INCOMPLETE; PSU quote date/vendor and MCU one-off price must be revalidated",
    }
    return {
        "scope": "Ideal linear single-branch R-C only; excludes physical HV connection, safety, enclosure, transformer, surge, EMI and control loop",
        "release_status": "NONFAB_HOLD",
        "configuration": cfg,
        "mains_passive_rc_only": mains,
        "hf_injection_tone_only": hf,
        "power_screen": power,
        "budget_screen": price,
        "reference_attenuation_error_ratio_45db": amplitude_tolerance_for_attenuation_db(45),
        "reference_attenuation_error_ratio_50db": amplitude_tolerance_for_attenuation_db(50),
        "blocking_gates": [
            "Mains-to-injection functional topology and approved isolation barrier unselected",
            "Line-sense measurement safety, protection coordination, and fail-open path unknown",
            "Certified X/Y component choices and single-fault current paths unverified",
            "MCU firmware/control stability and switching losses not simulated or measured",
            "Actual PCB placement and creepage/clearance for applicable standard not done",
            "Full 1-unit BOM plus PCB and assembly costs not quoted",
            "No built hardware; AC100V energization forbidden prior to review and test plan",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("yk66_envelope.json"))
    parser.add_argument("--csv", type=Path, default=Path("yk66_frequency_envelope.csv"))
    args = parser.parse_args()
    report = build_report()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with args.csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(report["hf_injection_tone_only"][0].keys()))
        writer.writeheader()
        writer.writerows(report["hf_injection_tone_only"])
    print(json.dumps({
        "status": report["release_status"],
        "min_peak_v_at_trip_5_to_30khz": min(x["drive_peak_v_at_178ma_trip"] for x in report["hf_injection_tone_only"] if x["frequency_hz"] <= 30000),
        "budget_unallocated_yen": report["budget_screen"]["remaining_before_essential_unknown_costs_yen"],
        "out": str(args.out),
        "csv": str(args.csv),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
