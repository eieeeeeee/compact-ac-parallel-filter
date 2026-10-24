#!/usr/bin/env python3
"""J1 prototype geometry candidate only, conditional on PCBWay advanced tolerances and Phoenix pin fit."""
from pathlib import Path
import re
pcb=Path('verify/src/YK66_Rev41_RESEARCH_ONLY.kicad_pcb')
s=pcb.read_text()
i=s.index('(footprint "YK66:Phoenix_1711725_MKDS3_2_5p08_PRELIM"')
j=s.index('\n(footprint ',i+1)
block=s[i:j]
assert '(at 42.4 18.6 0)' in block
assert block.count('(size 2.50 1.80)')==2
assert block.count('(drill 1.3)')==2
block=block.replace('(size 2.50 1.80)','(size 2.50 2.08)').replace('(drill 1.3)','(drill 1.4)')
s=s[:i]+block+s[j:]
pcb.write_text(s)
print("J1 conditional prototype: 1711725, holes FINISHED DIA 1.40mm; PTH oval 2.50 x 2.08mm; pitch 5.08mm")
print("Required special fabrication: finished hole ±0.05mm AND drill registration ±0.05mm.")
print("CHECK: nominal L/N gap 5.08-2.08=3.00mm; nominal ring (2.08-1.4)/2=0.34mm.")
print("CHECK: worst narrow ring (2.08-(1.4+0.05))/2-0.05=0.265mm.")
print("CHECK: min finished hole 1.35mm > square nominal pin diagonal 0.9*sqrt(2)=1.2728mm.")
print("HOLD: terminal pin tolerances, assembly insertion and solder joints remain unverified.")
