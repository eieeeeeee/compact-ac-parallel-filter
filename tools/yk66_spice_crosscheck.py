#!/usr/bin/env python3
"""Compare ngspice linear R-C outputs with independent closed-form calculation."""
import math
from pathlib import Path

def verify(path, amplitude, required):
    rows=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith(("#", "*")):
            continue
        parts=line.strip().split()
        try:
            values=list(map(float, parts))
        except ValueError:
            continue
        if len(values)<2:
            continue
        rows.append((values[0],values[1]))
    if not rows:
        raise AssertionError(f"No numeric data rows in {path}")
    for expected_f in required:
        closest=min(rows,key=lambda x: abs(x[0]-expected_f))
        f,mag=closest
        if abs(f-expected_f)>0.1:
            raise AssertionError(f"Missing requested frequency {expected_f} in {path}; closest {f}")
        z=math.hypot(5.03,1/(2*math.pi*f*1e-6))
        expected=amplitude/z
        if not math.isclose(mag,expected,rel_tol=1e-4,abs_tol=1e-8):
            raise AssertionError(f"ngspice disagreement f={f}: measured={mag}, math={expected}")
        print(f"PASS {path}: {f:g} Hz {mag:.7g} A equivalent (ideal model)")
verify("results/yk66_ngspice_12v_tone.dat",12,[5000,10000,20000,30000])
verify("results/yk66_ngspice_100v_passive.dat",100,[50,60])
print("CROSSCHECK_PASS: mathematical/small-signal passive network only; FAB_HOLD")
