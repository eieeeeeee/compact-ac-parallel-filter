# YK66 R14 — Seven global alternatives to passive-vs-active binary; small-parts first (2026-10-16)

**RESEARCH / NUMERICAL SCREEN ONLY. FAB HOLD, AC100V MAINS HOLD.** Japanese AC100V 50/60Hz, L-N 2-terminal parallel differential 5–30kHz, independent hard safety, first-one total ¥3500 (PCB+BOM+assembly+tax+shipping; stencil excluded) unproven. No separate LV product PCB.

## Research-backed candidate families, not just two
1. Original X2 shunt: one passive functional component, low part count; not wideband high reduction at low source impedance.
2. Series **R + X2 C** high-pass damper: just one added R; may reduce resonance interaction, can sacrifice narrow-frequency reduction.
3. Series **RLC tuned trap**: 3 passive parts, effective at tuned frequency but detunes badly.
4. **C + (L || R) second-order damped high-pass**: 3 passive parts; is the **preferred passive follow-up topology for measured source-impedance investigation**, not validated 5–30kHz 3dB. See PSCAD and APS sources.
5. Two parallel differently tuned RLC traps: six passive parts and extra core loss; still not a universal wideband filter.
6. **C-type high-pass**: low fundamental resistor loss but 50/60Hz tuning demands impractically high L at small C (e.g. C=1µF at 60Hz => ~7.04 H), not ideal for tiny PCB.
7. **Passive + minimum analog active damping / source-sensor-reduction**: research for broader performance; requires qualified high-voltage coupling, supply, current driver, independent fail-open; cannot yet fit price or safety.

Sources for filter taxonomy:
- https://www.pscad.com/webhelp/Master_Library_Models/Passive/Filters/Passive_Filter_Design.htm
- https://www.mathworks.com/help/simscape-electrical/ref/passiveharmonicfilterthreephase.html
- https://apseng.co.uk/Technical/passive-ac-harmonic-filters
- https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/pel2.12689
- https://www.jstage.jst.go.jp/article/ieejpes1990/119/2/119_2_204/_article/-char/ja/

## Actual supplier references, NOT full costed production
KEMET 0.47µF 310Vac X2 F861BP474K310A: **¥216 ex tax for one**, https://www.digikey.jp/en/products/detail/kemet/F861BP474K310A/8346543.
Würth 744743102 1mH inductor: **¥297 ex tax**, rated 420mA, Isat 550mA, maximum winding DCR 2.5Ω; https://www.digikey.jp/ja/products/detail/w%C3%BCrth-elektronik/744743102/3476775.
Two parts subtotal ¥513 ex tax; **no proof** of AC100V L–N branch short/surge/thermal safety, full protection, enclosure, PCB, SMT/shipping, or ¥3500 target. 1uF part of primary examples is a DIFFERENT cost item from the cited 0.47uF listing.

## R14 reproducing ORIGINAL vs new passive 32 variants
Independent Python+CSV/JSON and **7/7 local regression tests PASS** packaged separately in user ZIP. Formulas use small-signal Norton port, source Rs=.1/1/5Ω, load Rl=5/10/20Ω (9 purely resistive); optional synthetic impedances Rs*(1+jx), Rl*(1-jx/2) with x=-1/0/+1 (27 total hypothetical cases). Sample target: 5,7.5,10,15,20,25,30kHz; guard: 1,2,4,50,100,300,700kHz,1MHz. Original cap ESR=.08Ω ESL=25nH as *old guessed assumptions*, NOT manufacturer measured. For illustrative 1mH inductor, 2.5Ω winding DCR included.

| Small-signal example | Filter part count only | minimum 5–30kHz reduction across 9 resistive cases | minimum across 27 complex cases | maximum guard increase 27 complex cases |
|---|---:|---:|---:|---:|
| Original 1µF X2 | 1 | 0.000108 dB | -1.384 dB | +2.024dB |
| 1µF + series R=5Ω | 2 | 0.004202 dB | -0.452dB | +0.430dB |
| **1µF + series (1mH winding R2.5Ω || damping R20Ω)** | **3** | **0.016073dB** | **-0.0709dB** | **+0.287dB** |
| 2× 0.47µF series RLC 7/20kHz | 6 | 0.002538dB | -0.807dB | +0.639dB |

**0/32** candidates attained minimum 3dB reduction in all nine resistive source/load cases across 5–30kHz, **0/32** in 27 complex cases. Ideal loss and impedance stress are not measured household values. Reactive source/load interactions CAN make the terminal voltage rise in the purely passive network (negative reduction); no real oscillation claim. This is NOT proof that no possible other passive topology can work.

R14 research indicates 3-component damped high-pass is worth further **actual source/noise impedance evaluation**, BUT the modeled worst-case reduction is too small to promise a useful universal product. Source impedance at Rs=.1Ω and 5kHz is the main challenge. A single resonance can be excellent at one f but not 5–30kHz full-band.

## Product-development breakthrough that avoids double PCB rework
One AC100V final-design PCB with safety-approved protected L–N branches AND *optional DNP footprints* for a damped RC and shunt L||R C-network; fit only warranted parts after evidence. DNP variants need separate safety/fault qualification; empty footprints are not a substitute for approved electrical design. Prototype and product remain one PCB architecture, not separate low-voltage proof board.

**No final passive-vs-active user decision made.** Do not silently drop two-terminal active goal. R13 original archived parts stay reference; R14 becomes a measured-impedance-and-protection-driven design candidate, not fabrication sign-off. Any later active branch still needs an actual isolated safe mains injector and independent fault-disconnect; none chosen.

R13: docs/YK66_R13_ORIGINAL_10_PART_PASSIVE_VS_ACTIVE_COST_TRADE_20261016.md.
