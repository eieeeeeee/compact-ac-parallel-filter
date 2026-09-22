#!/usr/bin/env python3
import csv, uuid, re
from pathlib import Path
from collections import defaultdict

ROOT=Path(__file__).resolve().parent
NET=ROOT/"NETLIST_v1.2.csv"
NS=uuid.UUID("d3791df4-8b62-4ae1-8e92-0f3854a17eb6")
def uid(name): return str(uuid.uuid5(NS,name))

PARTS_DATA="""U1|STM32G474RCT6|Package_QFP:LQFP-64_10x10mm_P0.5mm
U2|TLV9062|Package_SO:SOIC-8_3.9x4.9mm_P1.27mm
U3|INA240A1|Package_SO:SOIC-8_3.9x4.9mm_P1.27mm
U4|TLV3202|Package_SO:VSSOP-8_3x3mm_P0.65mm
U5|SN74LVC1G332|Package_TO_SOT_SMD:SOT-23-6
U6|LMG2100R044|
U7|TPS62163|Package_SON:Texas_DSG0008A_WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm
U8|TLV75533P|Package_TO_SOT_SMD:SOT-23-5
J1|TEST_A / GND|
J2|+12V / GND|
J3|SWD 1x5|Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical
K1|G5V-1 DC12|Relay_THT:Relay_SPDT_Omron_G5V-1
Q1|2N7002|Package_TO_SOT_SMD:SOT-23
Q2|2N7002|Package_TO_SOT_SMD:SOT-23
R101|10k 1%|Resistor_SMD:R_0603_1608Metric
C101|100nF|Capacitor_SMD:C_0603_1608Metric
R102|100k 1%|Resistor_SMD:R_0603_1608Metric
C110|100nF|Capacitor_SMD:C_0603_1608Metric
C111|100nF|Capacitor_SMD:C_0603_1608Metric
C112|100nF|Capacitor_SMD:C_0603_1608Metric
C113|100nF|Capacitor_SMD:C_0603_1608Metric
C114|4.7uF 6.3V+|Capacitor_SMD:C_0805_2012Metric
FB101|Ferrite bead 600R@100MHz|Inductor_SMD:L_0603_1608Metric
C115|1uF|Capacitor_SMD:C_0805_2012Metric
C116|100nF|Capacitor_SMD:C_0603_1608Metric
R201|1.00k 1%|Resistor_SMD:R_0805_2012Metric
C201|100nF 50V|Capacitor_SMD:C_0805_2012Metric
R202|100k 1%|Resistor_SMD:R_0805_2012Metric
D201|BAT54H|Diode_SMD:D_SOD-323
D202|BAT54H|Diode_SMD:D_SOD-323
R203|100R 1%|Resistor_SMD:R_0603_1608Metric
C203|470pF C0G|Capacitor_SMD:C_0603_1608Metric
R210|10.0k 0.1%|Resistor_SMD:R_0805_2012Metric
R211|10.0k 0.1%|Resistor_SMD:R_0805_2012Metric
C210|10uF 10V|Capacitor_SMD:C_1206_3216Metric
C211|100nF|Capacitor_SMD:C_0603_1608Metric
C212|100nF|Capacitor_SMD:C_0603_1608Metric
C301|1.0uF 63V film 5%|Capacitor_THT:C_Rect_L7.2mm_W5.0mm_P5.00mm
R301|2.20R 1.5W pulse|Resistor_SMD:R_2512_6332Metric
R302|0.330R 1W 1%|Resistor_SMD:R_2512_6332Metric
R303|100R 1%|Resistor_SMD:R_0603_1608Metric
C303|470pF C0G|Capacitor_SMD:C_0603_1608Metric
C304|100nF|Capacitor_SMD:C_0603_1608Metric
R401|10.0k 0.1%|Resistor_SMD:R_0603_1608Metric
R402|61.9k 0.1%|Resistor_SMD:R_0603_1608Metric
R403|61.9k 0.1%|Resistor_SMD:R_0603_1608Metric
R404|10.0k 0.1%|Resistor_SMD:R_0603_1608Metric
R405|100k 1%|Resistor_SMD:R_0603_1608Metric
C405|100nF|Capacitor_SMD:C_0603_1608Metric
C406|100nF|Capacitor_SMD:C_0603_1608Metric
C501|330nF 50V X7R|Capacitor_SMD:C_1206_3216Metric
R501|1.00R 1% 2512|Resistor_SMD:R_2512_6332Metric
C502|220nF 50V X7R|Capacitor_SMD:C_0805_2012Metric
R502|1.00R 1% 2512|Resistor_SMD:R_2512_6332Metric
C503|22nF 50V X7R|Capacitor_SMD:C_0603_1608Metric
R503|660k 1%|Resistor_SMD:R_0805_2012Metric
R601|33R|Resistor_SMD:R_0603_1608Metric
R602|33R|Resistor_SMD:R_0603_1608Metric
R603|10k 1%|Resistor_SMD:R_0603_1608Metric
R604|10k 1%|Resistor_SMD:R_0603_1608Metric
C601|100nF 16V X7R 0402|Capacitor_SMD:C_0402_1005Metric
C602|100nF 16V X7R 0402|Capacitor_SMD:C_0402_1005Metric
C603|1uF 16V X7R 0603|Capacitor_SMD:C_0603_1608Metric
C604|2.2uF 25V X7R 0805|Capacitor_SMD:C_0805_2012Metric
C605|2.2uF 25V X7R 0805|Capacitor_SMD:C_0805_2012Metric
C606|100nF 50V X7R 0603|Capacitor_SMD:C_0603_1608Metric
L601|0.56uH|Inductor_SMD:L_Bourns_SRP7028A_7.3x6.6mm
L602|0.56uH|Inductor_SMD:L_Bourns_SRP7028A_7.3x6.6mm
L603|0.56uH|Inductor_SMD:L_Bourns_SRP7028A_7.3x6.6mm
C611|68nF 50V X7R 0603|Capacitor_SMD:C_0603_1608Metric
C612|68nF 50V X7R 0603|Capacitor_SMD:C_0603_1608Metric
C613|68nF 50V X7R 0603|Capacitor_SMD:C_0603_1608Metric
R701|1k|Resistor_SMD:R_0603_1608Metric
R702|100k|Resistor_SMD:R_0603_1608Metric
D701|SS14|Diode_SMD:D_SMA
L801|2.2uH >=1.3A|
C801|10uF 25V X7R|Capacitor_SMD:C_0805_2012Metric
C802|100nF 25V+|Capacitor_SMD:C_0603_1608Metric
C803|22uF 10V X7R|Capacitor_SMD:C_1206_3216Metric
C804|100nF|Capacitor_SMD:C_0603_1608Metric
R805|100k|Resistor_SMD:R_0603_1608Metric
C901|1uF 10V X7R|Capacitor_SMD:C_0805_2012Metric
C902|2.2uF 6.3V+ X7R|Capacitor_SMD:C_0805_2012Metric
C903|100nF|Capacitor_SMD:C_0603_1608Metric
TP1|TestPoint|TestPoint:TestPoint_Pad_D1.5mm
TP2|TestPoint|TestPoint:TestPoint_Pad_D1.5mm
TP3|TestPoint|TestPoint:TestPoint_Pad_D1.5mm
TP4|TestPoint|TestPoint:TestPoint_Pad_D1.5mm
TP5|TestPoint|TestPoint:TestPoint_Pad_D1.5mm
TP6|TestPoint|TestPoint:TestPoint_Pad_D1.5mm
TP7|TestPoint|TestPoint:TestPoint_Pad_D1.5mm
TP8|TestPoint|TestPoint:TestPoint_Pad_D1.5mm
TP9|TestPoint|TestPoint:TestPoint_Pad_D1.5mm
TP10|TestPoint|TestPoint:TestPoint_Pad_D1.5mm"""

PARTS={}
for line in PARTS_DATA.splitlines():
    ref,val,fp=line.split("|",2); PARTS[ref]={"Value":val,"Footprint":fp}

def read_netlist():
    pin_net={}; net_pins=defaultdict(list)
    with NET.open(encoding="utf-8-sig") as f:
        rd=csv.reader(f); next(rd)
        for row in rd:
            net=row[0].strip()
            for p in row[1:]:
                p=p.strip()
                if not p: continue
                if p in pin_net and pin_net[p]!=net:
                    raise SystemExit(f"DUPLICATE PIN NET: {p} {pin_net[p]} {net}")
                pin_net[p]=net; net_pins[net].append(p)
    return pin_net,net_pins

U1_NAMES={1:"VBAT",2:"PC13",3:"PC14-OSC32_IN",4:"PC15-OSC32_OUT",5:"PF0-OSC_IN",6:"PF1-OSC_OUT",7:"PG10-NRST",8:"PC0",9:"PC1",10:"PC2",11:"PC3",12:"PA0",13:"PA1",14:"PA2",15:"VSS",16:"VDD",17:"PA3",18:"PA4",19:"PA5",20:"PA6",21:"PA7",22:"PC4",23:"PC5",24:"PB0",25:"PB1",26:"PB2",27:"VSSA",28:"VREF+",29:"VDDA",30:"PB10",31:"VSS",32:"VDD",33:"PB11",34:"PB12",35:"PB13",36:"PB14",37:"PB15",38:"PC6",39:"PC7",40:"PC8",41:"PC9",42:"PA8",43:"PA9",44:"PA10",45:"PA11",46:"PA12",47:"VSS",48:"VDD",49:"PA13",50:"PA14",51:"PA15",52:"PC10",53:"PC11",54:"PC12",55:"PD2",56:"PB3",57:"PB4",58:"PB5",59:"PB6",60:"PB7",61:"PB8-BOOT0",62:"PB9",63:"VSS",64:"VDD"}
U1_TYPES={i:"bidirectional" for i in range(1,65)}
for i in (1,15,16,27,29,32,48,64): U1_TYPES[i]="power_in"
U1_TYPES[28]="input"
for i in (31,47,63): U1_TYPES[i]="passive"

SYMS={
"STM32G474RCT6":[(str(i),U1_NAMES[i],U1_TYPES[i]) for i in range(1,65)],
"TLV9062":[("1","OUTA","output"),("2","-INA","input"),("3","+INA","input"),("4","V-","power_in"),("5","+INB","input"),("6","-INB","input"),("7","OUTB","output"),("8","V+","power_in")],
"INA240A1":[("1","IN-","input"),("2","GND","power_in"),("3","REF2","passive"),("4","GND","passive"),("5","OUT","output"),("6","VS","power_in"),("7","REF1","passive"),("8","IN+","input")],
"TLV3202":[("1","1OUT","output"),("2","1IN-","input"),("3","1IN+","input"),("4","GND","power_in"),("5","2IN+","input"),("6","2IN-","input"),("7","2OUT","output"),("8","VCC","power_in")],
"SN74LVC1G332":[("1","A","input"),("2","B","input"),("3","GND","power_in"),("4","Y","output"),("5","C","input"),("6","VCC","power_in")],
"LMG2100R044":[("1","NC","no_connect"),("2","NC","no_connect"),("3","NC","no_connect"),("4","NC","no_connect"),("5","SW","power_out"),("6","PGND","power_in"),("7","VIN","power_in"),("8","NC","no_connect"),("9","NC","no_connect"),("10","HB","power_in"),("11","HS","passive"),("12","HI","input"),("13","LI","input"),("14","VCC","power_in"),("15","AGND","power_in"),("16","NC","no_connect"),("17","PGND","power_in")],
"TPS62163":[("1","PGND","power_in"),("2","VIN","power_in"),("3","EN","input"),("4","AGND","power_in"),("5","FB","input"),("6","VOS","input"),("7","SW","power_out"),("8","PG","open_collector"),("9","EP","power_in")],
"TLV75533P":[("1","IN","power_in"),("2","GND","power_in"),("3","EN","input"),("4","NC","no_connect"),("5","OUT","power_out")],
"CONN2":[("1","1","passive"),("2","2","passive")],
"CONN5":[(str(i),str(i),"passive") for i in range(1,6)],
"G5V1":[("1","NC","passive"),("2","COIL+","passive"),("5","COM","passive"),("6","COM","passive"),("9","COIL-","passive"),("10","NO","passive")],
"NMOS":[("1","G","input"),("2","S","passive"),("3","D","passive")],
"R":[("1","1","passive"),("2","2","passive")],
"C":[("1","1","passive"),("2","2","passive")],
"L":[("1","1","passive"),("2","2","passive")],
"D":[("1","K","passive"),("2","A","passive")],
"TP":[("1","TP","passive")],
"PWR_FLAG":[("1","pwr","power_out")],
}
PREFIX={"R":"R","C":"C","L":"L","FB":"L","D":"D","TP":"TP"}

def kind_for(ref):
    if ref=="U1": return "STM32G474RCT6"
    if ref=="U2": return "TLV9062"
    if ref=="U3": return "INA240A1"
    if ref=="U4": return "TLV3202"
    if ref=="U5": return "SN74LVC1G332"
    if ref=="U6": return "LMG2100R044"
    if ref=="U7": return "TPS62163"
    if ref=="U8": return "TLV75533P"
    if ref in ("J1","J2"): return "CONN2"
    if ref=="J3": return "CONN5"
    if ref=="K1": return "G5V1"
    if ref in ("Q1","Q2"): return "NMOS"
    for p,k in PREFIX.items():
        if ref.startswith(p): return k
    raise KeyError(ref)

EXPECTED_NC={
"U1":set(map(str,[2,3,4,5,6,8,9,10,11,14,17,18,19,20,21,22,23,24,25,26,30,33,34,35,36,37,38,39,40,41,44,45,51,52,53,54,55,56,60,62])),
"U6":{"1","2","3","4","8","9","16"},"U8":{"4"},"K1":{"1"}}

def ref_prefix(kind):
    return {"R":"R","C":"C","L":"L","D":"D","TP":"TP","CONN2":"J","CONN5":"J","G5V1":"K","NMOS":"Q","PWR_FLAG":"#FLG"}.get(kind,"U")

def symbol_expr(libname,kind,pins,qualified=False):
    nm=f"{libname}:{kind}" if qualified else kind
    pref=ref_prefix(kind); n=len(pins); y0=(n-1)*2.54/2
    top=max(2.54,y0+1.27); bottom=-top
    lines=[f'    (symbol "{nm}" (pin_names (offset 0.508)) (in_bom {"no" if kind=="PWR_FLAG" else "yes"}) (on_board {"no" if kind=="PWR_FLAG" else "yes"})',
           f'      (property "Reference" "{pref}" (at 0 {bottom-2.54:.2f} 0) (effects (font (size 1.0 1.0))))',
           f'      (property "Value" "{kind}" (at 0 {top+2.54:.2f} 0) (effects (font (size 1.0 1.0))))',
           '      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.0 1.0)) hide))',
           '      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.0 1.0)) hide))',
           f'      (symbol "{kind}_0_1" (rectangle (start -5.08 {top:.2f}) (end 5.08 {bottom:.2f}) (stroke (width 0.254) (type default)) (fill (type none))))',
           f'      (symbol "{kind}_1_1"']
    for idx,(num,name,etype) in enumerate(pins):
        py=y0-idx*2.54; safe=name.replace('"',"'")
        lines.append(f'        (pin {etype} line (at -7.62 {py:.2f} 0) (length 2.54) (name "{safe}" (effects (font (size 0.8 0.8)))) (number "{num}" (effects (font (size 0.8 0.8)))))')
    return lines+["      )","    )"]

def pin_y(kind,num):
    pins=SYMS[kind]; y0=(len(pins)-1)*2.54/2
    for i,(p,_,_) in enumerate(pins):
        if p==str(num): return y0-i*2.54
    raise KeyError((kind,num))

def validate(pin_net):
    refs={p.split(".",1)[0] for p in pin_net}|set(EXPECTED_NC)
    if refs!=set(PARTS):
        raise SystemExit(f"PARTS mismatch missing={set(PARTS)-refs} extra={refs-set(PARTS)}")
    errs=[]
    for full in pin_net:
        ref,pin=full.split(".",1); valid={p[0] for p in SYMS[kind_for(ref)]}
        if pin not in valid: errs.append(f"invalid physical pin {full}")
        if pin in EXPECTED_NC.get(ref,set()): errs.append(f"connected but expected NC {full}")
    actual_nc={}
    for ref in PARTS:
        valid={p[0] for p in SYMS[kind_for(ref)]}
        actual_nc[ref]={p for p in valid if f"{ref}.{p}" not in pin_net}
        allowed=EXPECTED_NC.get(ref,set())
        if actual_nc[ref]!=allowed:
            errs.append(f"NC mismatch {ref}: actual={sorted(actual_nc[ref])} expected={sorted(allowed)}")
    if errs: raise SystemExit("\n".join(errs))
    return actual_nc

def write_outputs():
    pin_net,net_pins=read_netlist(); nc=validate(pin_net)
    lib="RevDGSem"
    ext=['(kicad_symbol_lib (version 20220914) (generator "revdg_semantic_v12")']
    for kind,pins in SYMS.items():
        for line in symbol_expr(lib,kind,pins,False): ext.append("  "+line[4:] if line.startswith("    ") else line)
    ext.append(")")
    (ROOT/"RevDG_Semantic.kicad_sym").write_text("\n".join(ext)+"\n",encoding="utf-8")
    (ROOT/"sym-lib-table").write_text('(sym_lib_table\n  (lib (name "RevDGSem")(type "KiCad")(uri "${KIPRJMOD}/RevDG_Semantic.kicad_sym")(options "")(descr "Rev.D-G v1.2 semantic device symbols"))\n)\n',encoding="utf-8")

    (ROOT/"fp-lib-table").write_text('(fp_lib_table\n  (lib (name "RevC")(type "KiCad")(uri "${KIPRJMOD}/RevC.pretty")(options "")(descr "Validated Rev.C shared footprints"))\n)\n',encoding="utf-8")
    pending=[("J1","Wurth 691253510002","Exact manufacturer footprint freeze pending PCB stage"),("J2","Wurth 691253510002","Exact manufacturer footprint freeze pending PCB stage"),("U6","LMG2100R044","TI RAR land pattern pending exact vendor-footprint freeze"),("L801","VLF3012ST-2R2M1R4","TDK VLF3012 land pattern pending exact vendor-footprint freeze")]
    with (ROOT/"FOOTPRINT_PENDING_v1.2.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f); w.writerow(["Ref","Part","Status"]); w.writerows(pending)
    out=['(kicad_sch (version 20220904) (generator "revdg_semantic_v12")',f'  (uuid {uid("root")})','  (paper "A0")','  (lib_symbols']
    for kind,pins in SYMS.items(): out+=symbol_expr(lib,kind,pins,True)
    out+=['  )']; inst=[]
    special=["U1","U2","U3","U4","U5","U6","U7","U8","J1","J2","J3","K1","Q1","Q2"]
    places={"U1":(101.60,106.68),"U2":(330.20,50.80),"U3":(431.80,50.80),"U4":(533.40,50.80),"U5":(635.00,50.80),"U6":(736.60,63.50),"U7":(838.20,50.80),"U8":(939.80,50.80),"J1":(330.20,139.70),"J2":(431.80,139.70),"J3":(533.40,139.70),"K1":(635.00,139.70),"Q1":(736.60,139.70),"Q2":(838.20,139.70)}
    others=[r for r in PARTS if r not in special]
    for i,ref in enumerate(sorted(others)):
        places[ref]=(76.20+(i%8)*127.00,254.00+(i//8)*33.02)

    for ref,info in PARTS.items():
        kind=kind_for(ref); pins=SYMS[kind]; x,y=places[ref]; suid=uid("sym:"+ref)
        val=info["Value"].replace('"',"'"); fp=info["Footprint"].replace('"',"'")
        out += [f'  (symbol (lib_id "{lib}:{kind}") (at {x:.2f} {y:.2f} 0) (unit 1)',f'    (in_bom yes) (on_board yes) (uuid {suid})',
                f'    (default_instance (reference "{ref}") (unit 1) (value "{val}") (footprint "{fp}"))',
                f'    (property "Reference" "{ref}" (id 0) (at {x:.2f} {y-5.08:.2f} 0) (effects (font (size 0.9 0.9))))',
                f'    (property "Value" "{val}" (id 1) (at {x:.2f} {y+5.08:.2f} 0) (effects (font (size 0.8 0.8))))',
                f'    (property "Footprint" "{fp}" (id 2) (at {x:.2f} {y:.2f} 0) (effects (font (size 0.8 0.8)) hide))',
                f'    (property "Datasheet" "~" (id 3) (at {x:.2f} {y:.2f} 0) (effects (font (size 0.8 0.8)) hide))']
        for pn,_,_ in pins: out.append(f'    (pin "{pn}" (uuid {uid("pin:"+ref+":"+pn)}))')
        out.append("  )")
        for pn,_,_ in pins:
            cx=x-7.62; cy=y-pin_y(kind,pn); full=f"{ref}.{pn}"
            if full in pin_net:
                net=pin_net[full].replace('"',"'")
                out.append(f'  (label "{net}" (at {cx:.2f} {cy:.2f} 0) (effects (font (size 0.75 0.75)) (justify left bottom)) (uuid {uid("label:"+full)}))')
            else:
                out.append(f'  (no_connect (at {cx:.2f} {cy:.2f}) (uuid {uid("nc:"+full)}))')
        inst.append(f'    (path "/{suid}" (reference "{ref}") (unit 1) (value "{val}") (footprint "{fp}"))')

    flags=[("#FLG01","+12V","external isolated bench supply"),("#FLG02","GND","external isolated bench return"),("#FLG03","+5V","regulated output after L801"),("#FLG04","VDDA_FILT","filtered analog supply after FB101"),("#FLG05","GAN_HB","LMG2100 internal bootstrap diode")]
    for i,(ref,net,reason) in enumerate(flags):
        kind="PWR_FLAG"; x=1041.40; y=50.80+i*25.40; suid=uid("sym:"+ref); cx=x-7.62
        out += [f'  (symbol (lib_id "{lib}:{kind}") (at {x:.2f} {y:.2f} 0) (unit 1)',f'    (in_bom no) (on_board no) (uuid {suid})',
                f'    (default_instance (reference "{ref}") (unit 1) (value "{reason}") (footprint ""))',
                f'    (property "Reference" "{ref}" (id 0) (at {x:.2f} {y-2.54:.2f} 0) (effects (font (size 0.7 0.7)) hide))',
                f'    (property "Value" "{reason}" (id 1) (at {x:.2f} {y+2.54:.2f} 0) (effects (font (size 0.7 0.7))))',
                f'    (property "Footprint" "" (id 2) (at {x:.2f} {y:.2f} 0) (effects (font (size 0.8 0.8)) hide))',
                f'    (property "Datasheet" "~" (id 3) (at {x:.2f} {y:.2f} 0) (effects (font (size 0.8 0.8)) hide))',
                f'    (pin "1" (uuid {uid("pin:"+ref+":1")}))','  )',
                f'  (label "{net}" (at {cx:.2f} {y:.2f} 0) (effects (font (size 0.75 0.75)) (justify left bottom)) (uuid {uid("label:"+ref)}))']
        inst.append(f'    (path "/{suid}" (reference "{ref}") (unit 1) (value "{reason}") (footprint ""))')

    out += ['  (text "LOW-VOLTAGE LAB HARDWARE ONLY - NOT FOR DIRECT AC100V CONNECTION" (at 50.80 810.26 0) (effects (font (size 2.0 2.0)) (justify left bottom)))',
            '  (sheet_instances (path "/" (page "1")))','  (symbol_instances',*inst,'  )',')']
    (ROOT/"RevD_G_v1_2_FULL.kicad_sch").write_text("\n".join(out)+"\n",encoding="utf-8")

    with (ROOT/"BOM_v1.2_FULL.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f); w.writerow(["Ref","Value","Footprint"])
        for ref,info in PARTS.items(): w.writerow([ref,info["Value"],info["Footprint"]])
    with (ROOT/"NC_PINS_v1.2_FULL.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f); w.writerow(["Ref","NC pins"])
        for ref in sorted(nc):
            if nc[ref]: w.writerow([ref,",".join(sorted(nc[ref],key=lambda x:int(x) if x.isdigit() else 999))])
    pinmap=[("U1","7","PG10-NRST","NRST"),("U1","12","PA0","VLINE_ADC"),("U1","13","PA1","ISENSE_ADC"),("U1","42","PA8","HRTIM_HI_RAW"),("U1","43","PA9","HRTIM_LI_RAW"),("U1","46","PA12","FORCE_SAFE"),("U1","49","PA13","SWDIO"),("U1","50","PA14","SWCLK"),("U1","57","PB4","MCU_FORCE_SAFE"),("U1","58","PB5","RELAY_CMD"),("U1","59","PB6","PWR_GOOD_5V"),("U1","61","PB8-BOOT0","BOOT0"),
            ("U3","8","IN+","INJ_R_NODE"),("U3","1","IN-","INJ_LINE"),("U3","5","OUT","ISENSE_RAW"),
            ("U5","1","A","TRIP_HI"),("U5","2","B","TRIP_LO"),("U5","5","C","MCU_FORCE_SAFE"),("U5","4","Y","FORCE_SAFE"),("U5","6","VCC","+3V3"),("U5","3","GND","GND"),
            ("U6","5","SW","GAN_SW"),("U6","7","VIN","+12V"),("U6","10","HB","GAN_HB"),("U6","11","HS","GAN_SW"),("U6","12","HI","GAN_HI"),("U6","13","LI","GAN_LI"),("U6","14","VCC","+5V"),
            ("U7","2","VIN","+12V"),("U7","3","EN","+12V"),("U7","5","FB","GND"),("U7","6","VOS","+5V"),("U7","7","SW","BUCK_SW"),("U7","8","PG","PWR_GOOD_5V"),("U7","9","EP","GND"),
            ("U8","1","IN","+5V"),("U8","2","GND","GND"),("U8","3","EN","+5V"),("U8","4","NC","NC"),("U8","5","OUT","+3V3")]
    with (ROOT/"PINMAP_v1.2_FULL.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f); w.writerow(["Ref","Pin","PinName","Net"]); w.writerows(pinmap)
    (ROOT/"SEMANTIC_STATIC_CHECK.txt").write_text(f"BOM refs={len(PARTS)}\nConnected pins={len(pin_net)}\nExplicit NC pins={sum(len(v) for v in nc.values())}\nNets={len(net_pins)}\nPWR_FLAGs={len(flags)}\nPASS\n",encoding="utf-8")
    print((ROOT/"SEMANTIC_STATIC_CHECK.txt").read_text())

if __name__=="__main__": write_outputs()
