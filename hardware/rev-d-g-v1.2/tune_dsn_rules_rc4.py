#!/usr/bin/env python3
from pathlib import Path
import sys

p=Path(sys.argv[1])
s=p.read_text(encoding="utf-8")
start=s.find("(class kicad_default ")
if start<0:
    raise SystemExit("kicad_default class not found")

depth=0; instr=False; esc=False; end=None
for i in range(start,len(s)):
    c=s[i]
    if instr:
        if esc: esc=False
        elif c=="\\": esc=True
        elif c=='"': instr=False
    else:
        if c=='"': instr=True
        elif c=='(': depth+=1
        elif c==')':
            depth-=1
            if depth==0:
                end=i+1
                break
if end is None:
    raise SystemExit("class block end not found")

# Widths are DSN micrometres.  Fine-pitch GaN/control nets stay narrow; the
# high-current LC/injection paths are widened only where their pads can support it.
classes=[
 ("revd_gan_fine",["GAN_SW","GAN_HB","GAN_HI","GAN_LI"],250),
 ("revd_lc",["GAN_F1","GAN_F2","ACTIVE_OUT"],600),
 ("revd_injection",["INJ_C_NODE","INJ_R_NODE","INJ_LINE"],600),
 ("revd_power12",["+12V"],500),
 ("revd_power5",["+5V","GND"],400),
 ("revd_power33",["+3V3","VDDA_FILT"],300),
 ("revd_buck",["BUCK_SW"],350),
 ("revd_sense",["VLINE_PRE","VLINE_BIAS","VLINE_BUF","VLINE_ADC","ISENSE_RAW","ISENSE_ADC","VMID","VMID_DIV","VTH_HI","VTH_LO"],200),
 ("revd_hrtim",["HRTIM_HI_RAW","HRTIM_LI_RAW"],200),
]
hdr=s[start:s.find("(circuit",start)]
tokens=hdr.replace("("," ").replace(")"," ").split()
allnets=tokens[2:]
assigned=set(n for _,ns,_ in classes for n in ns)
default=[n for n in allnets if n not in assigned]

def block(name,nets,width):
    return f'''(class {name} {' '.join(nets)}
      (circuit
        (use_via "Via[0-3]_600:300_um")
      )
      (rule
        (width {width})
        (clearance 150)
      )
    )'''

replacement="\n    ".join([block(n,ns,w) for n,ns,w in classes if ns]+[block("kicad_default",default,250)])
s=s[:start]+replacement+s[end:]
p.write_text(s,encoding="utf-8")
print("RC4_DSN_NETCLASS_TUNING_OK")
for name,nets,width in classes:
    print(name,width,",".join(nets))
print("kicad_default",250,",".join(default))
