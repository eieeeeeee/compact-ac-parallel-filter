#!/usr/bin/env python3
"""Rev45U: ordinary plated-through-hole PCB manufacturing candidate.
Research only: pin insertion/fit, solder, creepage, and enclosure not approved.
"""
from pathlib import Path
p=Path("verify/src/YK66_Rev41_RESEARCH_ONLY.kicad_pcb")
data=p.read_text()
a=data.index('(footprint "YK66:Phoenix_1711725_MKDS3_2_5p08_PRELIM"')
b=data.index("\n(footprint ",a+1)
f=data[a:b]
assert f.count('(drill 1.4)')==2,f.count('(drill 1.4)')
assert f.count('(size 2.50 2.08)')==2,f.count('(size 2.50 2.08)')
assert f.count('thru_hole oval')==2
f=f.replace('(drill 1.4)','(drill 1.3)').replace('(size 2.50 2.08)','(size 2.50 1.90)')
out=data[:a]+f+data[b:]
assert out != data
p.write_text(out)
print("Rev45U no-special-process candidate: Phoenix 1711725, PTH 1.30mm, oval pad 2.50x1.90mm")
print("Two terminals 5.08mm pitch, J1 x42.40 y18.60mm; all other footprint and copper unchanged.")
print("Annular ring nominal min = (1.90-1.30)/2 = 0.300mm")
print("L-N pad nominal clearance = 5.08-1.90 = 3.180mm")
print("JLC published PTH +0.13/-0.08 & hole position ±0.05: worst assumed ring = (1.90-1.43)/2-0.05 = 0.185mm")
print("PCBWay published PTH ±0.08 & hole position ±0.05 assumption: ring = (1.90-1.38)/2-0.05 = 0.210mm")
print("WARNING: JLC minimum finished hole 1.22mm below nominal square pin diagonal 1.273mm; physical fit test mandatory.")
print("WARNING: Pad-to-pad solder fillet margin and CTI-based functional/basic insulation requirements remain open.")
