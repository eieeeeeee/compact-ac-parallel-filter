from pathlib import Path
p=Path(__file__).parent/'ngspice_decks'
p.mkdir(exist_ok=True)
def filt(n,kind):
    if kind=='none':return ''
    if kind=='rc18':
        return f'''R_FIL {n} RLC1 4.7
R_CESR RLC1 LC1 0.05
L_CESL LC1 CAPTOP 30n
C1 CAPTOP 0 1u
R_BLEED CAPTOP 0 220k
C_MOV {n} 0 700p
R_LED_AC {n} 0 150k
'''
    if kind=='c1u_direct':return f'R_CESR {n} LC1 0.05\nL_CESL LC1 CAPTOP 30n\nC1 CAPTOP 0 1u\n'
    x={'rc22_330n':22,'rc47_330n':47}[kind]
    return f'R_FIL {n} RLC1 {x}\nR_CESR RLC1 LC1 0.05\nL_CESL LC1 CAPTOP 30n\nC1 CAPTOP 0 330n\n'
def write(name,body,node):
    (p/(name+'.cir')).write_text(f'''* RC18-Lite Rev27 - {name} small-signal DM analysis only
* Synthetic wiring: NOT a mains safety test or real-house prediction
{body}
.control
set noaskquit
set wr_singlescale
set wr_vecnames
ac dec 150 1k 10Meg
wrdata {name}.dat v({node})
quit
.endc
.end
''')
for kind in ['none','rc18','rc22_330n','rc47_330n','c1u_direct']:
    v='V_NOISE VIN 0 AC 1\nR_SOURCE VIN NS1 1\nL_SOURCE NS1 BUS 1u\nR_LOAD BUS 0 50\nC_LOAD BUS 0 3n\n'+filt('BUS',kind)
    write('two_node_'+kind,v,'BUS')
for kind,node in [('none',6),('rc18_n0',0),('rc18_n3',3),('rc18_n6',6)]:
    v='I_NOISE 0 N6 AC 1m\nR_GRID N0 GRID1 .3\nL_GRID GRID1 0 1u\n'
    for i in range(6):v+=f'R_WIRE{i} N{i} W{i} .2\nL_WIRE{i} W{i} N{i+1} 2u\n'
    for i in range(7):v+=f'R_LOAD{i} N{i} 0 250\nC_LOAD{i} N{i} 0 2n\n'
    v+=filt('N'+str(node),'none' if kind=='none' else 'rc18')
    write('seven_node_'+kind,v,'N6')
print('Generated',len(list(p.glob('*.cir'))),'ngspice decks')
