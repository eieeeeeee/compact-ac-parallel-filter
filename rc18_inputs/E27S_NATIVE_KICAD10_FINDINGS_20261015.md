# RC18 E27S Native KiCad 10.0.6 verification (NONFAB HOLD)

2026-10-15; exact source ZIP SHA256 ab240ce51e5d56b19caab85618319387f2a1d75d81dc31418c5fc1573ac367f3. Source 40/40 verified. Run https://github.com/eieeeeeee/compact-ac-parallel-filter/actions/runs/38709038314

## Real KiCad modifications
- U1 pin19 VSS => VSSA; existing GND net unchanged.
- U1 pin21 VDD => VDDA; existing 3V3 net unchanged.
- Both cached schematic symbol (03_MCU_DIGITAL.kicad_sch) and RC18_Custom.kicad_sym patched; two electrical design files modified, no net, footprint or copper changes.
- Source reverse-check to E27P passed; ST DS12288 Rev6 package authority https://www.st.com/resource/en/datasheet/stm32g474cb.pdf

## Native KiCad results
| Item | Result |
| --- | --- |
| KiCad version | 10.0.6 |
| ERC errors | 0 |
| ERC warnings | 3 (U1003, U1005, U1302 unresolved footprint IDs) |
| DRC geometric violations | 0 |
| PCB unconnected | 3 (SW_SOURCE, R302_KELVIN_N, TEST_A) |
| Missing PCB footprints | 64 |
| Full Native release | FAIL/HOLD |

See GitHub Actions artifact RC18-E27S-KICAD10-NATIVE-NONFAB-38709038314 (raw ERC, DRC, CLI and machine audit).

## Single-chip integration contract
Existing STM32G474CBT6 already supports HRTIM1 CHA1/2 at PA8/PA9, ADC3 IN5 at PB13 and OPAMP2 at PA5/PA6/PA7. Pin mapping alone does NOT verify ADC/COMP/OPAMP simultaneous configuration, FMAC/DMA 1.454545MHz latency or closed-loop noise performance. Theoretical CPU budgets 58.44 cycles per 2.90909MS/s ADC sample and 116.88 per 1.454545MHz control update.

Approved component removal 0 and verified savings JPY0. Independent 178mA physical current cutoff, physical PRE_VERIFIED producer, Q301/Q302 source-referenced fail-off, E-STOP and manual ARM must remain. Original 17 stop items: native tool technical obstacle overcome, 16 other items OPEN.

**HOLD_NO_POWER_NO_AC_NO_ORDER_NO_FAB.**
