#!/usr/bin/env python3
from pathlib import Path
P=Path(__file__).parent/'decks'
P.mkdir(exist_ok=True)
vals=[('C010',.1,0),('C022',.22,0),('C047',.47,0),('C100',1,0),('C220',2.2,0),('C470',4.7,0),('C500',5,0),('RC100',1,4.7)]
def make(label,s,base):
    path=P/(label+'.cir')
    # source/load synthetic, not household measurements
    path.write_text(f'''* RC18 Lite Rev29, AC small-signal, DM only, synthetic network
* {label} — ESR=0.05 ohm ESL=30 nH for all nominal capacitances
{base}
.control
set noaskquit
set wr_singlescale
set wr_vecnames
ac dec 150 10k 10Meg
wrdata {label}.dat v({s})
quit
.endc
.end
''')
def cap(net,c,r):
    if c==0:return ''
    start=net
    z=''
    if r:
        z=f'R_DAMP {net} CPIN {r}\n';start='CPIN'
    return z+f'''R_ESR {start} C_ESR 0.05
L_ESL C_ESR C_TOP 30n
C_FILTER C_TOP 0 {c}u
'''
for lbl,c,r in [('NONE',0,0)]+vals:
    two='''V_NOISE VIN 0 AC 1
R_SRC VIN NS1 1
L_SRC NS1 BUS 1u
R_LOAD BUS 0 50
C_LOAD BUS 0 3n
'''+cap('BUS',c,r)
    make('two_'+lbl,'BUS',two)
    seven='''I_NOISE 0 N6 AC 1m
R_GRID N0 GRID1 .3
L_GRID GRID1 0 1u
'''
    for i in range(6):
        seven+=f'R_LINE{i} N{i} W{i} 0.2\nL_LINE{i} W{i} N{i+1} 2u\n'
    for i in range(7):
        seven+=f'R_LOAD{i} N{i} 0 250\nC_LOAD{i} N{i} 0 2n\n'
    seven+=cap('N6',c,r)
    make('seven_'+lbl,'N6',seven)
print('Generated',len(list(P.glob('*.cir'))),'SPICE netlists')
