# YK66 R22: Magnetic core feasibility gate — 2.75:1 target with E25/13/7 anchor
Date: 2026-10-16
Status: RESEARCH / ANALYTICAL ONLY — NOT RELEASED FOR AC100V FABRICATION OR ENERGIZATION

## 0. Executive result
R21 asked whether the 135–405 uH / 3:1 variable inductor is manufacturable and affordable.

R22 reduces the magnetic requirement further:
- target tuning ratio is reduced from 3.0:1 to approximately **2.75:1**
- coarse capacitor states are re-optimized to keep the resonant branch in the approximately 10–50 kHz region
- a catalog E25/13/7 ferrite set gives a credible zero-bias inductance and DC winding resistance with ~50 turns
- an experimentally published EE25-class DC-biased variable inductor has already demonstrated a **2.75:1** inductance ratio, which is now essentially the YK66 ratio target

The remaining hard problem is no longer inductance ratio. It is:
1. control-winding power,
2. AC/core-loss contribution to total series resistance,
3. manufacturability of the side control windings,
4. low-cost mains-derived control supply,
5. fault containment.

## 1. Coarse-C map re-optimized for 2.75:1 magnetic tuning
Instead of demanding 3:1 magnetic tuning, use a 2.75:1 variable inductance and slightly different capacitor values.

A mathematically exact low-part-count target is approximately:
- C0 = 75 nF
- CA = 130 nF
- CB = 480 nF

Four states:
- 75 nF
- 205 nF
- 555 nF
- 685 nF

With Lmax/Lmin = 2.75 and an E25-anchored target of about:
- Lmax = 377.5 uH
- Lmin = 137.3 uH

ideal resonance spans become:
- 685 nF: 9.90–16.41 kHz
- 555 nF: 11.00–18.23 kHz
- 205 nF: 18.09–30.00 kHz
- 75 nF: 29.91–49.60 kHz

The bands overlap continuously.
Therefore the published 2.75:1 tuning class is sufficient; YK66 no longer needs to exceed it.

Exact X2 values 75/130/480 nF are not frozen. They may be formed from standard safety-capacitor combinations or the crossover may be shifted slightly. This R22 result is a ratio/topology proof, not a released BOM.

## 2. Catalog ferrite anchor: TDK E25/13/7 N87
TDK E25/13/7 data:
- effective path length le = 57.5 mm
- effective cross section Ae = 52.5 mm^2
- effective volume Ve = 3020 mm^3
- one ungapped + one 0.50-mm-gapped N87 core half gives AL about 151 nH
- standard horizontal bobbin B66208B1110T001:
  - winding area AN = 61 mm^2
  - mean length per turn lN = 50 mm
  - winding resistance factor AR = 28 uohm

Sources:
https://www.tdk-electronics.tdk.com/inf/80/db/fer/e_25_13_7.pdf
https://www.digikey.jp/en/products/detail/tdk/B66317G0500X187/3914718
https://www.digikey.jp/en/products/detail/tdk/B66208B1110T001/3914554

### 50-turn main winding
Using L = AL*N^2:
L0 = 151 nH * 50^2 = **377.5 uH**

Using Rcu = AR*N^2:
RDC_est = 28 uohm * 50^2 = **70 mOhm**

This is a very useful result:
a commodity E25/13/7 core geometry naturally lands almost exactly on the new Lmax target and has an estimated DC copper resistance well below the R21 total-loss ceiling.

The AR-derived resistance is a winding-design estimate from the TDK bobbin geometry, NOT a measured finished-coil value. AC skin/proximity effects, lead/contact resistance and core loss must be added.

## 3. Material choice: N87 is preferred over N27 for this branch
TDK lists:
N87:
- optimum frequency range 25–500 kHz
- typical Pv = 57 kW/m^3 at 25 kHz / 200 mT / 100 C
- Bs about 490 mT at 25 C, 390 mT at 100 C

N27:
- optimum frequency range 25–150 kHz
- typical Pv = 155 kW/m^3 at 25 kHz / 200 mT / 100 C
- Bs about 500 mT at 25 C, 410 mT at 100 C

Sources:
https://www.tdk-electronics.tdk.com/download/540216/d6940b239127a8bab71b22168746021b/pdf-n87.pdf
https://www.tdk-electronics.tdk.com/download/540184/d7dcd087c9a2dbd3a81365841d4aa9a5/pdf-n27.pdf

Both are below their listed optimum range at the 10–20-kHz bottom end, but N87 has materially lower published 25-kHz loss at the same 200-mT benchmark.
R22 therefore selects **N87 as the first analytical material candidate**.

This does not establish actual YK66 loss because YK66 operates at much smaller AC flux in the normal-noise model and with DC bias.

## 4. Flux-density sanity check
Illustrative noise model only:
- open-circuit HF noise = 100 mV RMS
- Zs = 0.5 ohm
- 10-ohm load
- resonant branch Rtotal = 0.5 ohm
- around 20 kHz, L is approximately 300 uH class
- main winding N = 50
- Ae = 52.5 mm^2

The resonant-branch current is on the order of 0.1 A RMS in this model.
The resulting AC flux-density excursion is only tens of mT, not hundreds of mT.

Therefore the ordinary 100-mV noise model does not by itself require a huge core.
However large abnormal HF voltage/transients can drive the branch much harder, so current/thermal/fault protection remains mandatory.

## 5. Published small-core variable-inductor evidence is now directly aligned
He et al., Electronics 2026:
- EE25/20/6 PC40 ferrite
- center-leg gap = 1.04 mm
- main AC winding = 48 turns
- two side control windings = 30 turns each
- control current = 0–1.0 A
- measured/used inductance range = 40–110 uH
- ratio = **2.75:1**
- side control windings are series-opposed to cancel AC coupling into the control circuit

DOI:
https://doi.org/10.3390/electronics15142999

YK66 does NOT copy its absolute inductance, gap, winding or drive.
The important evidence is that:
- EE25-scale ferrite,
- ~50-turn AC winding,
- side DC control windings,
- 2.75:1 continuous inductance change
has been built and experimentally used.

R22's E25/13/7 anchor is therefore no longer relying on a speculative 3:1 extrapolation.

## 6. Preliminary control-MMF envelope
The published EE25-class experiment obtains 2.75:1 with:
30 turns per side * up to 1 A = about **30 A-turns per control leg**.

That does NOT prove YK66 needs exactly 30 A-turns because:
- core geometry differs,
- gap differs,
- material differs,
- target absolute inductance differs,
- flux path differs.

R22 uses **30–60 A-turns per side as an initial simulation envelope only**.

Examples:
- 60 turns -> 0.5–1.0 A for 30–60 At
- 90 turns -> 0.33–0.67 A for 30–60 At

Increasing turns does not magically eliminate copper power because resistance rises with turn count.
Therefore control winding design must optimize copper volume and thermal rise, not merely minimize current.

## 7. Control-power ceiling
YK66 is an always-plugged-in device.
A 1-A continuous magnetic-bias driver would be unattractive even if technically possible.

R22 sets a provisional product target:
- average control-winding electrical loss: **<=0.5 W preferred**
- absolute research gate: **<=1.0 W**
- if ordinary EE bias requires more, it loses first place for YK66

This ceiling is not a safety standard; it is a product/cost/thermal target.

## 8. Permanent-magnet-assisted orthogonal core: downgrade from "primary" to "high-upside secondary"
Aizu et al. (Tohoku University / Tohoku Electric Power) demonstrated an orthogonal-core variable inductor using permanent magnets in the DC-control magnetic path.
The permanent magnet establishes bias even at zero control current, and control current shifts the operating point.

DOI:
https://doi.org/10.20819/msjtmsj.23TR508

This remains highly relevant because it can potentially reduce continuous control power.
However the published device is not an E25-size 10–50-kHz YK66 part.

Therefore R22 corrects R21:
- **ordinary side-biased EE variable inductor = primary physical proof path**
- **PM-assisted orthogonal core = secondary power-reduction path**
until a small-core model demonstrates equivalent tuning range and loss.

## 9. Conventional saturable reactor: rejected as primary architecture
A single control winding strongly coupled to the AC winding tends to reproduce unwanted AC voltage in the bias/control circuit.
Suppressing that coupling generally adds blocking magnetics or more circuitry.

The side-winding / series-opposition EE structure is superior for YK66 because the published arrangement deliberately cancels high-frequency AC flux in the DC control circuit.

Therefore conventional same-flux-path saturable-reactor control is not the main path.

## 10. First-unit cost anchor
Current one-off Japan distributor anchors:
- N87 E25/13/7 core half, 0.5-mm gapped: about JPY210 before tax
- matching second core half: same-order cost
- E25/13/7 bobbin: about JPY206–240 before tax
- two G5Q-class coarse-selector relays from R20: about JPY580 before tax total

So:
core set + bobbin + 2 relays is roughly **JPY1,200 before tax**, before copper wire, X2 capacitors, controller, control driver, supply, protection, PCB, assembly and shipping.

This is not yet a comfortable JPY3,500 BOM, but it is much more plausible than a 6-relay tuning bank.

The largest remaining cost uncertainty is not the ferrite itself; it is:
- custom winding labor,
- low-voltage/control supply,
- protection and assembly.

## 11. R22 decision
### PASS to next analytical gate
The magnetic concept is NOT rejected.

The following candidate is technically credible enough for deeper modeling:
- TDK-class E25/13/7 N87 geometry
- nominal zero-bias AL around 151 nH
- ~50-turn main winding
- zero-bias L around 377.5 uH
- target biased L around 137 uH
- tuning ratio about 2.75:1
- DC main-winding resistance estimate around 70 mOhm before AC/core/contact effects
- two coarse capacitor switching functions
- passive HF branch above the adaptive-resonator range

### HOLD / not yet proven
- actual 2.75:1 tuning on this exact E25/13/7 geometry
- <=0.8-ohm total series loss over 10–50 kHz
- <=0.5-W control loss
- PM-assisted small-core implementation
- cost <=JPY3,500 after assembly/supply/protection/shipping
- product safety / mains suitability

## R23 gate
R23 must build a nonlinear analytical/behavioral magnetic model and answer:
1. How much DC control MMF is needed for the E25/13/7 50-turn candidate to move 377.5 -> ~137 uH?
2. What series resistance does copper + AC proximity + core loss contribute at 10/20/30/40/50 kHz?
3. Does Rtotal stay below 0.8 ohm?
4. What bias-driver voltage/current and power are required?
5. Can the control power be reduced by PM pre-bias without making temperature/tolerance unacceptable?
6. Does a cheaper two-range magnetic design beat continuous 2.75:1 tuning?

No AC100V fabrication or energization is authorized by R22.
