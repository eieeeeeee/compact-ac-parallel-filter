"""R11 regression: mathematical models only, not a physical AC100V test."""
import json
import tempfile
import unittest
from pathlib import Path
from yk66_r11_dm_envelope import (
    FRACTION_3DB, RS, RL, port_y, ideal_current, ideal_limit_db,
    virtual_y, on_volts, db, main
)

class R11Regression(unittest.TestCase):
    def test_port(self):
        self.assertAlmostEqual(port_y(.1, 5), 10.2)
    def test_fraction(self):
        self.assertAlmostEqual(FRACTION_3DB, .292054215615, places=11)
    def test_required3(self):
        self.assertAlmostEqual(ideal_current(.1, .1, 5)*1000, 297.895300, places=5)
    def test_required50(self):
        self.assertAlmostEqual(ideal_current(.1, .1, 5, 50)*1000, 1016.774477, places=5)
    def test_norton(self):
        for a in RS:
            for b in RL:
                v = .01/port_y(a,b)
                self.assertAlmostEqual(ideal_current(v,a,b), FRACTION_3DB*.01, places=12)
    def test_ceiling(self):
        self.assertAlmostEqual(ideal_limit_db(.1,.1,5,.02), .172003, places=5)
    def test_limiter(self):
        v,current,alpha=on_volts(10.2,4.5,.1,.02)
        self.assertLessEqual(current,.02000001)
        self.assertLess(alpha,1)
        self.assertLess(db(.1,v),.2)
    def test_norton_ideal_target(self):
        vals=[]
        for a in RS:
            for b in RL:
                for x in (-1,0,1):
                    p=port_y(a,b,x);off=.01/p
                    on,current,_=on_volts(p,4.5,off,.02)
                    self.assertLess(current,.01)
                    vals.append(db(off,on))
        self.assertGreater(min(vals),3)
    def test_positive_real_port(self):
        for a in RS:
            for b in RL:
                for x in (-1,0,1):
                    p=port_y(a,b,x)
                    self.assertGreater(p.real,0)
                    self.assertLessEqual(abs(on_volts(p,4.5,.01,.02)[0]),.01+1e-12)
    def test_frequency_model(self):
        y=virtual_y(60,5,800,6,200000,250000,.1)
        self.assertLess(100*abs(y),.001)
        self.assertGreater(abs(virtual_y(10000,5,800,6,200000,250000,.1)),1)
    def test_negative_incremental_conductance(self):
        self.assertLess(virtual_y(300000,.1,1600,4,80000,250000,.5).real,0)
    def test_full_screen_hold(self):
        with tempfile.TemporaryDirectory() as d:
            data=main(d)
            self.assertEqual(data['cases'],9)
            self.assertEqual(data['model_variants'],64)
            self.assertEqual(data['passes_all_math_gates'],0)
            self.assertEqual(data['20mA_3db_100mV_cases'],3)
            self.assertFalse(data['mains_allowed'])
            self.assertFalse(data['manufacturing_allowed'])
            self.assertEqual(len(json.loads((Path(d)/'64_candidate_ideal_models.json').read_text())),64)

if __name__=='__main__':
    unittest.main()
