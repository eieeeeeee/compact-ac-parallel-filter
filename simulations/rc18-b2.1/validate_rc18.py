#!/usr/bin/env python3
"""RC18-B2.1 reproducibility gate.

This script is intentionally self-contained. It recomputes the RC18 electrical
simulation gate from disclosed equations and constants and exits non-zero if a
gate fails.

Scope: low-voltage architecture simulation only. It does not define or validate
an AC-mains coupling/isolation implementation.
"""
from __future__ import annotations

import argparse
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------- Frozen gate inputs ----------------------------
FS = 2_000_000.0
VS = 0.300
I_MAX = 0.120
VMAX = 3.39411255
BASE_CONTROL_DELAY = 2.005e-6  # tuned deterministic control-path target
EPC23104_PROP_DELAY = 36e-9
TOTAL_DELAY = BASE_CONTROL_DELAY + EPC23104_PROP_DELAY
JITTER = 25e-9
G_STEP = 0.0005

F_TARGET = np.geomspace(5e3, 30e3, 241)
F_WATCH = np.geomspace(30e3, 100e3, 241)
F = np.concatenate([F_TARGET, F_WATCH[1:]])
NT = len(F_TARGET)
PHASES_DEG = np.arange(-60, 61, 15)
Z_MAG = np.array([0.2, 0.5, 1, 2, 5, 10, 20.0])

# Final tuned digital biquad, H(z)=(b0+b1 z^-1+b2 z^-2)/(1+a1 z^-1+a2 z^-2)
BIQUAD = np.array([1.96005549, -2.81840199, 0.92560172, -1.02969083, 0.09694605])

# Same-model RC17 fine-grid references used for strict equivalence testing.
RC17_FINE_DB = {
    0.2: -0.26369068846874283,
    0.5: -0.7091844043218214,
    1.0: -1.666710494730435,
    2.0: -3.2910560940707483,
    5.0: -7.191263752556715,
    10.0: -11.45696053552019,
    20.0: -16.49681184469315,
}

# B2.1 reconstruction network. DCR/ESR are model values disclosed with the gate.
LC_CORNERS = {
    "nom": (
        (0.82e-6, 0.47e-6, 0.68e-6),
        (150e-9, 100e-9, 82e-9),
        (0.048, 0.022, 0.028),
        (0.08, 0.08, 0.08),
    ),
    "low": (
        tuple(0.8 * x for x in (0.82e-6, 0.47e-6, 0.68e-6)),
        tuple(0.8 * x for x in (150e-9, 100e-9, 82e-9)),
        (0.048, 0.022, 0.028),
        (0.08, 0.08, 0.08),
    ),
    "high": (
        tuple(1.2 * x for x in (0.82e-6, 0.47e-6, 0.68e-6)),
        tuple(1.05 * x for x in (150e-9, 100e-9, 82e-9)),
        (0.048, 0.022, 0.028),
        (0.08, 0.08, 0.08),
    ),
}


def z_branch(f: np.ndarray, c: float, r: float, l: float) -> np.ndarray:
    return r + 1j * 2 * np.pi * f * l + 1 / (1j * 2 * np.pi * f * c)


def passive_admittance(f: np.ndarray) -> np.ndarray:
    # Frozen Candidate-A passive network used by RC17/RC18 same-model comparison.
    return (
        1 / z_branch(f, 330e-9, 0.066, 30e-9)
        + 1 / z_branch(f, 220e-9, 1.084, 17e-9)
        + 1 / z_branch(f, 22e-9, 1.123, 11e-9)
        + 1 / 660e3
    )


YP = passive_admittance(F)
ZI = 2.63 + 1 / (1j * 2 * np.pi * F * 1e-6)

# Passive baseline for each source impedance and phase.
PBASE: dict[tuple[float, float], tuple[complex, np.ndarray]] = {}
for zm in Z_MAG:
    for ph in PHASES_DEG:
        zs = float(zm) * np.exp(1j * np.deg2rad(ph))
        vp = VS / (1 + zs * YP)
        PBASE[(float(zm), float(ph))] = (zs, 20 * np.log10(np.abs(vp) / VS))


def ladder_affine(ls, cs, rls, rcs):
    """Return YA = y0 + y1*K for the 3-section reconstruction ladder."""
    y0 = np.empty(len(F), complex)
    y1 = np.empty(len(F), complex)
    for i, ff in enumerate(F):
        w = 2 * np.pi * ff
        zl = [rls[k] + 1j * w * ls[k] for k in range(3)]
        yc = [1 / (rcs[k] + 1 / (1j * w * cs[k])) for k in range(3)]
        zi = ZI[i]

        def solve_for(kdrive: int) -> complex:
            a = np.zeros((3, 3), complex)
            b = np.zeros(3, complex)
            a[0, 0] = 1 / zl[0] + yc[0] + 1 / zl[1]
            a[0, 1] = -1 / zl[1]
            b[0] = kdrive / zl[0]
            a[1, 0] = -1 / zl[1]
            a[1, 1] = 1 / zl[1] + yc[1] + 1 / zl[2]
            a[1, 2] = -1 / zl[2]
            a[2, 1] = -1 / zl[2]
            a[2, 2] = 1 / zl[2] + yc[2] + 1 / zi
            b[2] = 1 / zi
            nodes = np.linalg.solve(a, b)
            return (1 - nodes[2]) / zi

        y0[i] = solve_for(0)
        y1[i] = solve_for(1)
    return y0, y1 - y0


AFF = {name: ladder_affine(*cfg) for name, cfg in LC_CORNERS.items()}


def ideal_biquad_response(coeff: np.ndarray) -> np.ndarray:
    b0, b1, b2, a1, a2 = coeff
    z = np.exp(-1j * 2 * np.pi * F / FS)
    return (b0 + b1 * z + b2 * z * z) / (1 + a1 * z + a2 * z * z)


def estimate_complex(x, y, f, n0):
    t = np.arange(n0, len(y)) / FS
    yy = y[n0:]
    c = np.cos(2 * np.pi * f * t)
    s = np.sin(2 * np.pi * f * t)
    m = np.column_stack((c, s, np.ones_like(c)))
    fit = np.linalg.lstsq(m, yy, rcond=None)[0]
    amp = np.max(np.abs(x))
    return (fit[0] - 1j * fit[1]) / amp


def float32_runtime_response(coeff: np.ndarray) -> tuple[np.ndarray, dict]:
    b0, b1, b2, a1, a2 = coeff.astype(np.float32)
    h = np.empty(len(F), complex)
    max_y = 0.0
    for k, f in enumerate(F):
        per = FS / f
        n_samples = int(max(2500, math.ceil(18 * per + 500)))
        n = np.arange(n_samples)
        x = (0.125 * np.cos(2 * np.pi * f * n / FS)).astype(np.float32)
        y = np.zeros(n_samples, np.float32)
        x1 = x2 = y1 = y2 = np.float32(0)
        for i in range(n_samples):
            acc = np.float32(b0 * x[i])
            acc = np.float32(acc + np.float32(b1 * x1))
            acc = np.float32(acc + np.float32(b2 * x2))
            acc = np.float32(acc - np.float32(a1 * y1))
            acc = np.float32(acc - np.float32(a2 * y2))
            y[i] = acc
            x2, x1, y2, y1 = x1, x[i], y1, acc
        n0 = int(max(500, 5 * per))
        h[k] = estimate_complex(x.astype(float), y.astype(float), f, n0)
        max_y = max(max_y, float(np.max(np.abs(y))))
    return h, {"runtime_peak_fraction_fs": max_y}


def sat32(v: int) -> int:
    return max(-2147483648, min(2147483647, v))


def q31_runtime_response(coeff: np.ndarray) -> tuple[np.ndarray, dict]:
    # CMSIS-DSP DF1 convention: feedback signs reversed and postShift=2.
    b0, b1, b2, a1, a2 = coeff
    post_shift = 2
    scale = 2**post_shift
    q = 2**31
    eff = np.array([b0, b1, b2, -a1, -a2])
    qi = np.rint(eff / scale * q).astype(np.int64)
    qb0, qb1, qb2, qa1, qa2 = [int(v) for v in qi]
    h = np.empty(len(F), complex)
    max_y = 0.0
    max_acc_2p62 = 0.0
    shift = 31 - post_shift
    for k, f in enumerate(F):
        per = FS / f
        n_samples = int(max(2500, math.ceil(18 * per + 500)))
        n = np.arange(n_samples)
        xf = 0.125 * np.cos(2 * np.pi * f * n / FS)
        x = np.rint(xf * q).astype(np.int64)
        x = np.clip(x, -2**31, 2**31 - 1)
        y = np.zeros(n_samples, dtype=np.int64)
        x1 = x2 = y1 = y2 = 0
        for i in range(n_samples):
            acc = qb0 * int(x[i]) + qb1 * x1 + qb2 * x2 + qa1 * y1 + qa2 * y2
            max_acc_2p62 = max(max_acc_2p62, abs(acc) / (2**62))
            out = sat32(acc >> shift)
            y[i] = out
            x2, x1, y2, y1 = x1, int(x[i]), y1, out
        n0 = int(max(500, 5 * per))
        h[k] = estimate_complex(x.astype(float) / q, y.astype(float) / q, f, n0)
        max_y = max(max_y, float(np.max(np.abs(y))) / q)
    return h, {
        "runtime_peak_fraction_fs": max_y,
        "accumulator_peak_2p62": max_acc_2p62,
        "post_shift": post_shift,
        "q31_coefficients": [qb0, qb1, qb2, qa1, qa2],
    }


def evaluate(a_aff, b_aff, h, zmag, jitter=JITTER):
    gv = np.arange(0, 0.5000001, G_STEP)
    g = gv[:, None]
    valid = np.ones(len(gv), bool)
    phase_worst = np.full((len(gv), len(PHASES_DEG)), -1e99)
    phase_mean = np.full_like(phase_worst, -1e99)
    worst_jitter = np.zeros_like(phase_worst)
    watchdog = np.full(len(gv), -1e99)
    target_extra = np.full(len(gv), -1e99)
    max_i = np.zeros(len(gv))
    max_v = np.zeros(len(gv))

    for dj in (-jitter, 0.0, jitter):
        e = np.exp(-1j * 2 * np.pi * F * (TOTAL_DELAY + dj))
        k = e[None, :] * (1 - ZI[None, :] * g * h[None, :])
        ya = a_aff[None, :] + b_aff[None, :] * k
        valid &= ya.real.min(axis=1) >= -1e-12

        for ip, ph in enumerate(PHASES_DEG):
            zs, passive_db = PBASE[(float(zmag), float(ph))]
            va = VS / (1 + zs * (YP[None, :] + ya))
            atten = 20 * np.log10(np.abs(va) / VS)
            extra = atten - passive_db[None, :]
            ia = np.abs(ya * va)
            vcmd = np.abs(k * va)
            valid &= (
                (ia.max(axis=1) <= I_MAX + 1e-12)
                & (vcmd.max(axis=1) <= VMAX + 1e-12)
                & (extra.max(axis=1) <= 0.5 + 1e-12)
            )
            wc = atten[:, :NT].max(axis=1)
            mc = atten[:, :NT].mean(axis=1)
            replace = wc > phase_worst[:, ip]
            phase_worst[replace, ip] = wc[replace]
            phase_mean[replace, ip] = mc[replace]
            worst_jitter[replace, ip] = dj
            watchdog = np.maximum(watchdog, extra[:, NT - 1 :].max(axis=1))
            target_extra = np.maximum(target_extra, extra[:, :NT].max(axis=1))
            max_i = np.maximum(max_i, ia.max(axis=1))
            max_v = np.maximum(max_v, vcmd.max(axis=1))

    idx = np.where(valid)[0]
    if len(idx) == 0:
        return None
    worst_by_g = phase_worst[idx].max(axis=1)
    pidx = phase_worst[idx].argmax(axis=1)
    means = phase_mean[idx, pidx]
    order = np.lexsort((means, worst_by_g))
    j = idx[order[0]]
    ip = pidx[order[0]]
    return {
        "G_S": gv[j],
        "worst_5_30k_dB": phase_worst[j, ip],
        "worst_phase_deg": PHASES_DEG[ip],
        "worst_jitter_ns": worst_jitter[j, ip] * 1e9,
        "mean_5_30k_dB": phase_mean[j, ip],
        "watchdog_max_extra_dB": watchdog[j],
        "target_max_extra_dB": target_extra[j],
        "max_Iactive_mArms": max_i[j] * 1000,
        "max_command_Vrms": max_v[j],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="validation/rc18-b2.1/generated")
    parser.add_argument("--formats", default="float32,q31", help="comma-separated: float32,q31")
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    formats = [x.strip() for x in args.formats.split(",") if x.strip()]
    runtime = {}
    meta = {}
    if "float32" in formats:
        runtime["float32_runtime"], meta["float32_runtime"] = float32_runtime_response(BIQUAD)
    if "q31" in formats:
        runtime["q31_runtime"], meta["q31_runtime"] = q31_runtime_response(BIQUAD)

    rows = []
    for fmt, h in runtime.items():
        for corner, (aa, bb) in AFF.items():
            for zm in Z_MAG:
                result = evaluate(aa, bb, h, float(zm))
                if result is None:
                    rows.append({"format": fmt, "corner": corner, "Zmag_ohm": zm, "valid": False})
                    continue
                delta = result["worst_5_30k_dB"] - RC17_FINE_DB[float(zm)]
                rows.append(
                    {
                        "format": fmt,
                        "corner": corner,
                        "Zmag_ohm": zm,
                        "valid": True,
                        **result,
                        "RC17_fine_dB": RC17_FINE_DB[float(zm)],
                        "delta_vs_RC17_fine_dB": delta,
                    }
                )

    detail = pd.DataFrame(rows)
    detail.to_csv(out / "detail.csv", index=False)

    summary_rows = []
    all_pass = True
    for fmt in runtime:
        d = detail[(detail["format"] == fmt) & (detail["valid"] == True)]
        if len(d) != len(AFF) * len(Z_MAG):
            all_pass = False
            summary_rows.append({"format": fmt, "strict_PASS": False, "reason": "invalid operating point"})
            continue
        worst_delta = d.loc[d["delta_vs_RC17_fine_dB"].idxmax()]
        worst_watch = d.loc[d["watchdog_max_extra_dB"].idxmax()]
        strict = bool(
            (d["delta_vs_RC17_fine_dB"].max() <= 0)
            and (d["watchdog_max_extra_dB"].max() <= 0.5)
            and (d["max_Iactive_mArms"].max() <= 120)
            and (d["max_command_Vrms"].max() <= VMAX)
        )
        all_pass &= strict
        summary_rows.append(
            {
                "format": fmt,
                "maxdef_dB": d["delta_vs_RC17_fine_dB"].max(),
                "def_corner": worst_delta["corner"],
                "def_Z_ohm": worst_delta["Zmag_ohm"],
                "maxwatch_dB": d["watchdog_max_extra_dB"].max(),
                "watch_corner": worst_watch["corner"],
                "watch_Z_ohm": worst_watch["Zmag_ohm"],
                "maxI_mArms": d["max_Iactive_mArms"].max(),
                "maxV": d["max_command_Vrms"].max(),
                "runtime_peak_fraction_fs": meta[fmt]["runtime_peak_fraction_fs"],
                "strict_PASS": strict,
            }
        )

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(out / "summary.csv", index=False)
    print(summary.to_string(index=False))
    print(f"elapsed_s={time.time()-t0:.2f}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
