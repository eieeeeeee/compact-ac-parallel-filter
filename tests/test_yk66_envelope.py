"""Unit tests for the YK66 non-fabrication R-C math envelope."""
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from yk66_envelope import CONFIG, HF_HZ, amplitude_tolerance_for_attenuation_db, build_report, series_z_magnitude


class EnvelopeTests(unittest.TestCase):
    def test_rc_impedance_exact(self):
        self.assertAlmostEqual(series_z_magnitude(50, 1e-6, 0), 3183.09886184, places=6)
        self.assertAlmostEqual(series_z_magnitude(30000, 1e-6, 5.03), math.hypot(5.03, 1/(2*math.pi*30000*1e-6)))

    def test_invalid_input_rejected(self):
        with self.assertRaises(ValueError):
            series_z_magnitude(0, 1e-6, 5.03)
        with self.assertRaises(ValueError):
            series_z_magnitude(50, -1e-6, 5.03)
        with self.assertRaises(ValueError):
            amplitude_tolerance_for_attenuation_db(-3)

    def test_fundamental_current(self):
        report = build_report()
        t = next(x for x in report["mains_passive_rc_only"] if x["mains_vrms"] == 100 and x["frequency_hz"] == 50)
        self.assertAlmostEqual(t["passive_rc_rms_current_a"], 0.0314155, delta=1e-6)
        self.assertLess(t["passive_rc_rms_damping_loss_w"], 0.005)
        self.assertGreater(t["passive_rc_apparent_power_va"], 3)

    def test_12v_tones_cross_hardware_trip(self):
        rows = build_report()["hf_injection_tone_only"]
        self.assertEqual(len(rows), len(HF_HZ))
        self.assertTrue(all(x["12v_tone_exceeds_trip"] for x in rows))
        self.assertGreater(rows[0]["drive_peak_v_at_178ma_trip"], rows[-1]["drive_peak_v_at_178ma_trip"])
        self.assertAlmostEqual(rows[3]["drive_peak_v_at_178ma_trip"], 1.3013, delta=0.0001)

    def test_limit_is_trip_not_continuous_power(self):
        power = build_report()["power_screen"]
        self.assertAlmostEqual(power["12v_times_trip_current_w_not_continuous"], 2.136)
        self.assertAlmostEqual(power["unallocated_nominal_w_after_hypothetical_trip_w"], 0.864)

    def test_budget_not_overclaimed(self):
        b = build_report()["budget_screen"]
        self.assertEqual(b["remaining_before_essential_unknown_costs_yen"], 1285)
        self.assertEqual(build_report()["release_status"], "NONFAB_HOLD")
        self.assertTrue(len(build_report()["blocking_gates"]) >= 6)

    def test_attenuation_error_needed(self):
        self.assertAlmostEqual(amplitude_tolerance_for_attenuation_db(50), 0.00316227766, places=8)
        self.assertAlmostEqual(amplitude_tolerance_for_attenuation_db(45), 0.00562341325, places=8)


if __name__ == "__main__":
    unittest.main()
