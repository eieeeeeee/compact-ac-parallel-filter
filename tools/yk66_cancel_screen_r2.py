#!/usr/bin/env python3
"""YK66 R2 analytical differential-mode feedforward cancellation screen.

NON-FABRICATION model. It is NOT a mains injection design, safety approval,
control-loop stability analysis, or prediction of measured attenuation.
"""
import argparse
import csv
import json
import math
from pathlib import Path

FREQUENCIES_HZ = (5000, 10000, 20000, 30000)
DELAYS_US = (0.1, 0.5, 1.0)
GAIN_RATIOS = (0.99, 1.00)
NOISE_CURRENT_PEAK_A = (0.010, 0.030, 0.080)
HYPOTHETICAL_ENGINEERING_CURRENT_BUDGET_A = 0.050
HISTORICAL_HARD_TRIP_REFERENCE_A = 0.178
RELEASE_STATUS = "NONFAB_HOLD"


def residual_ratio(frequency_hz, gain_ratio, delay_s, phase_correction_rad=0.0):
    """|1 - gain*exp(j*(phase_correction - omega*delay))|."""
    if frequency_hz <= 0 or gain_ratio < 0 or delay_s < 0:
        raise ValueError("Invalid positive-frequency cancellation parameters")
    angle = phase_correction_rad - 2.0 * math.pi * frequency_hz * delay_s
    return math.hypot(
        1.0 - gain_ratio * math.cos(angle),
        gain_ratio * math.sin(angle),
    )


def attenuation_db(residual):
    if residual < 0:
        raise ValueError("Negative residual")
    if residual == 0:
        return None  # ideal mathematical zero; never report infinite physical dB
    return -20.0 * math.log10(residual)


def maximum_uncorrected_delay_us(frequency_hz, target_db):
    """Max pure delay for exact gain=1, no phase compensation, single tone."""
    if frequency_hz <= 0 or target_db < 0:
        raise ValueError("Invalid delay budget inputs")
    residual_allow = 10.0 ** (-target_db / 20.0)
    return 1.0e6 * math.asin(min(1.0, residual_allow / 2.0)) / (
        math.pi * frequency_hz
    )


def build_report():
    rows = []
    for f in FREQUENCIES_HZ:
        for delay_us in DELAYS_US:
            for gain in GAIN_RATIOS:
                residual = residual_ratio(f, gain, delay_us * 1e-6)
                rows.append({
                    "frequency_hz": f,
                    "latency_us": delay_us,
                    "cancellation_gain_ratio": gain,
                    "remaining_noise_ratio": round(residual, 9),
                    "ideal_small_signal_reduction_db": round(attenuation_db(residual), 5),
                })
    phase_budget = [
        {"target_db": db, "at_hz": 30000,
         "max_uncompensated_latency_us": round(
             maximum_uncorrected_delay_us(30000, db), 6)}
        for db in (10, 20, 30, 45, 50)
    ]
    current_cases = [
        {"assumed_noise_peak_a": current,
         "ideal_equal_and_opposite_injection_peak_a": current,
         "within_hypothetical_50ma_engineering_budget":
             current <= HYPOTHETICAL_ENGINEERING_CURRENT_BUDGET_A,
         "below_historical_178ma_trip_reference":
             current < HISTORICAL_HARD_TRIP_REFERENCE_A}
        for current in NOISE_CURRENT_PEAK_A
    ]
    return {
        "name": "YK66 R2",
        "status": RELEASE_STATUS,
        "scope": "ideal one-tone feedforward current cancellation, not closed-loop or mains",
        "assumptions": {
            "latency_model": "pure delay, no transfer-function magnitude or frequency dependence",
            "nominal_drive_gain": "relative to unknown actual noise current",
            "noise_current_cases_are_assumptions_not_measurements": True,
            "engineering_50ma_screen_is_hypothetical_not_an_approved_limit": True,
            "178ma_is_historical_FAULT_TRIP_not_continuous_rating": True,
            "isolation_transient_thermal_emc_feedback_and_source_impedance": "UNMODELED"
        },
        "phase_budget_at_30khz": phase_budget,
        "cancellation_scenarios": rows,
        "assumed_current_cases": current_cases,
        "release_gates": {
            "isolation_and_line_coupling_qualified": False,
            "fault_open_independent_protection_proven": False,
            "measured_noise_current_spectrum_available": False,
            "full_loop_stability_and_latency_verified": False,
            "full_one_off_bom_under_3500_yen": False,
            "kicad_same_variant_erc_drc_parity": False,
            "mains_energization_authorized": False
        }
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--json", type=Path, default=Path("yk66_r2.json"))
    p.add_argument("--csv", type=Path, default=Path("yk66_r2_scenarios.csv"))
    a = p.parse_args()
    report = build_report()
    a.json.parent.mkdir(parents=True, exist_ok=True)
    a.csv.parent.mkdir(parents=True, exist_ok=True)
    a.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    with a.csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(report["cancellation_scenarios"][0]))
        w.writeheader()
        w.writerows(report["cancellation_scenarios"])
    print(json.dumps({
        "status": report["status"],
        "latency_budget_us_30khz_20db": report["phase_budget_at_30khz"][1]["max_uncompensated_latency_us"],
        "mains_energization_authorized": False
    }))


if __name__ == "__main__":
    main()
