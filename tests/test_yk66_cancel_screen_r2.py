"""Analytical checks only; never authorize fabrication or mains operation."""
import math
import unittest
from tools.yk66_cancel_screen_r2 import (
    attenuation_db, build_report, maximum_uncorrected_delay_us, residual_ratio,
)


class ScreenR2Tests(unittest.TestCase):
    def test_perfect_ideal_cancel(self):
        self.assertAlmostEqual(residual_ratio(30000, 1.0, 0.0), 0.0, places=12)
        self.assertIsNone(attenuation_db(0.0))

    def test_one_percent_amplitude_error_caps_at_40db(self):
        r = residual_ratio(30000, 0.99, 0.0)
        self.assertAlmostEqual(attenuation_db(r), 40.0, places=6)

    def test_half_microsecond_at_30khz(self):
        r = residual_ratio(30000, 1.0, 0.5e-6)
        self.assertAlmostEqual(r, 2.0 * math.sin(math.pi * 30000 * 0.5e-6))
        self.assertTrue(20.0 < attenuation_db(r) < 21.0)

    def test_fifty_db_latency_budget_at_30khz(self):
        microseconds = maximum_uncorrected_delay_us(30000, 50)
        self.assertTrue(0.016 < microseconds < 0.017)

    def test_monotone_budget(self):
        self.assertGreater(maximum_uncorrected_delay_us(30000, 20),
                           maximum_uncorrected_delay_us(30000, 50))

    def test_invalid_data(self):
        with self.assertRaises(ValueError):
            residual_ratio(0, 1.0, 0.0)
        with self.assertRaises(ValueError):
            residual_ratio(5000, -1, 0.0)

    def test_mains_gates_must_remain_hold(self):
        report = build_report()
        self.assertEqual(report["status"], "NONFAB_HOLD")
        self.assertTrue(report["assumptions"][
            "noise_current_cases_are_assumptions_not_measurements"])
        self.assertFalse(any(report["release_gates"].values()))
        self.assertFalse(report["assumed_current_cases"][-1][
            "within_hypothetical_50ma_engineering_budget"])


if __name__ == "__main__":
    unittest.main()
