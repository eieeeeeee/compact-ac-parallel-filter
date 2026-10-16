"""Tests for a math model. Tests never approve hardware or mains operation."""
import math
import unittest
from tools.yk66_bench_r3 import (STATUS, bandpass, build_report,
                                  passive_shunt_db, reduction_db, residual)
class R3Tests(unittest.TestCase):
    def test_center_bpf(self):
        self.assertAlmostEqual(bandpass(10000).real,1.0)
        self.assertAlmostEqual(bandpass(10000).imag,0.0)
    def test_center_six_db(self):
        x=build_report()["center"]
        self.assertAlmostEqual(x["baseline_voltage_peak_mv"],100)
        self.assertTrue(6<x["reduction_db_positive_means_better"]<6.03)
        self.assertTrue(49<x["controlled_voltage_peak_mv"]<52)
    def test_ideal_passive_10khz(self):
        self.assertAlmostEqual(passive_shunt_db(10000,10,1e-6),1.445070116,places=6)
        self.assertAlmostEqual(passive_shunt_db(10000,10,0.1e-6),.017111504,places=6)
    def test_ideal_passive_1mhz(self):
        self.assertAlmostEqual(passive_shunt_db(1e6,50,1e-6),49.943041456,places=6)
        self.assertAlmostEqual(passive_shunt_db(1e6,50,0.1e-6),29.947395549,places=6)
    def test_guard(self):
        x=build_report()["guard"]
        self.assertEqual(x["points"],671)
        self.assertEqual(x["worst_frequency_hz"],105000)
        self.assertGreater(x["worst_reduction_db"],-0.5)
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): bandpass(0)
        with self.assertRaises(ValueError): reduction_db(0)
        with self.assertRaises(ValueError): passive_shunt_db(0,1,1e-6)
    def test_safe_hold(self):
        x=build_report()
        self.assertEqual(STATUS,"NONFAB_HOLD_MAINS_HOLD")
        self.assertFalse(x["mains_authorized"])
        self.assertFalse(x["kicad_manufacturing_release"])
        self.assertTrue(x["model_only"])
if __name__=="__main__":
    unittest.main()
