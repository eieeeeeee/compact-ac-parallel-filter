#!/usr/bin/env python3
"""Generate pre-prototype simulation figures for the open-source shunt filter."""

from pathlib import Path
import csv
import math

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent

CAPS = {
    "0.10 uF": (0.10e-6, 0.15, 15e-9),
    "0.47 uF": (0.47e-6, 0.10, 20e-9),
    "1.00 uF": (1.00e-6, 0.08, 25e-9),
    "4.00 uF": (4.00e-6, 0.06, 40e-9),
}
COLORS = ["#2878b5", "#45a778", "#e5a33d", "#c65454"]


def z_cap(f, c, esr, esl):
    w = 2 * np.pi * f
    return esr + 1j * (w * esl - 1 / (w * c))


def style_axis(ax):
    ax.grid(True, which="both", color="#d8dee5", linewidth=0.65, alpha=0.85)
    ax.set_facecolor("#fbfcfd")
    for spine in ax.spines.values():
        spine.set_color("#9aa7b2")


def save_csv(path, header, columns):
    with path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        writer.writerow(header)
        writer.writerows(zip(*columns))


def plot_impedance(ax, f):
    cols = [f]
    header = ["frequency_hz"]
    for (label, (c, esr, esl)), color in zip(CAPS.items(), COLORS):
        z = np.abs(z_cap(f, c, esr, esl))
        ax.loglog(f, z, label=label, color=color, linewidth=2.2)
        cols.append(z)
        header.append(label.replace(" ", "_") + "_ohm")
    ax.set_title("A. Capacitor impedance model", loc="left", fontweight="bold")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("|Z| [ohm]")
    ax.set_xlim(10, 30e6)
    ax.set_ylim(0.04, 1e6)
    ax.legend(frameon=True, fontsize=9)
    style_axis(ax)
    save_csv(ROOT / "impedance_model_v0_1.csv", header, cols)


def plot_attenuation(ax, f):
    c, esr, esl = CAPS["1.00 uF"]
    z = z_cap(f, c, esr, esl)
    cols = [f]
    header = ["frequency_hz"]
    for rsrc, color in zip([0.1, 1, 10, 50], COLORS):
        h = np.abs(z / (rsrc + z))
        db = 20 * np.log10(h)
        ax.semilogx(f, db, label=f"Source R = {rsrc:g} ohm", color=color, linewidth=2.2)
        cols.append(db)
        header.append(f"source_{rsrc:g}_ohm_db")
    ax.axhline(0, color="#5d6872", linewidth=0.8)
    ax.set_title("B. Predicted shunt attenuation (1 uF)", loc="left", fontweight="bold")
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Vout / Vsource [dB]")
    ax.set_xlim(10, 30e6)
    ax.set_ylim(-65, 3)
    ax.legend(frameon=True, fontsize=8)
    style_axis(ax)
    save_csv(ROOT / "attenuation_model_v0_1.csv", header, cols)


def plot_discharge(ax):
    t = np.linspace(0, 2.5, 501)
    v0 = math.sqrt(2) * 100
    tau = 440e3 * 1e-6
    v = v0 * np.exp(-t / tau)
    t60 = tau * math.log(v0 / 60)
    ax.plot(t, v, color="#2878b5", linewidth=2.5)
    ax.axhline(60, color="#c65454", linestyle="--", linewidth=1.4, label="60 V")
    ax.axvline(t60, color="#c65454", linestyle=":", linewidth=1.4)
    ax.scatter([t60, 1.0], [60, v0 * math.exp(-1 / tau)], color=["#c65454", "#45a778"], zorder=3)
    ax.annotate(f"60 V at {t60:.2f} s", (t60, 60), xytext=(0.70, 91),
                arrowprops={"arrowstyle": "->", "color": "#6a737d"}, fontsize=9)
    ax.annotate(f"{v0 * math.exp(-1/tau):.1f} V at 1.00 s", (1, v0 * math.exp(-1/tau)),
                xytext=(1.28, 38), arrowprops={"arrowstyle": "->", "color": "#6a737d"}, fontsize=9)
    ax.set_title("C. Plug-removal discharge prediction", loc="left", fontweight="bold")
    ax.set_xlabel("Time after removal [s]")
    ax.set_ylabel("Capacitor voltage [V]")
    ax.set_xlim(0, 2.5)
    ax.set_ylim(0, 150)
    style_axis(ax)
    save_csv(ROOT / "discharge_model_v0_1.csv", ["time_s", "voltage_v"], [t, v])


def plot_line_current(ax):
    labels = list(CAPS.keys())
    currents = [2 * math.pi * 60 * c * 100 * 1000 for c, _, _ in CAPS.values()]
    bars = ax.bar(labels, currents, color=COLORS, edgecolor="#ffffff", linewidth=0.8)
    for bar, value in zip(bars, currents):
        ax.text(bar.get_x() + bar.get_width()/2, value + 3, f"{value:.1f}",
                ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("D. 60 Hz capacitive current at 100 V RMS", loc="left", fontweight="bold")
    ax.set_ylabel("RMS current [mA]")
    ax.set_ylim(0, 175)
    style_axis(ax)
    save_csv(ROOT / "line_current_v0_1.csv", ["capacitance", "current_ma"], [labels, currents])


def individual_plot(name, plotter, *args):
    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
    plotter(ax, *args)
    fig.savefig(ROOT / f"{name}.png", dpi=220, facecolor="white")
    fig.savefig(ROOT / f"{name}.svg", facecolor="white")
    plt.close(fig)


def main():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    f = np.logspace(1, math.log10(30e6), 601)

    individual_plot("01_impedance_model_v0_1", plot_impedance, f)
    individual_plot("02_attenuation_model_v0_1", plot_attenuation, f)
    individual_plot("03_discharge_model_v0_1", plot_discharge)
    individual_plot("04_line_current_v0_1", plot_line_current)

    fig, axes = plt.subplots(2, 2, figsize=(16, 10), constrained_layout=False)
    fig.subplots_adjust(left=0.07, right=0.97, bottom=0.09, top=0.84, wspace=0.23, hspace=0.34)
    plot_impedance(axes[0, 0], f)
    plot_attenuation(axes[0, 1], f)
    plot_discharge(axes[1, 0])
    plot_line_current(axes[1, 1])
    fig.suptitle("Open-source AC100V Shunt Noise Filter — Simulation v0.1",
                 x=0.07, y=0.965, ha="left", fontsize=21, fontweight="bold", color="#182532")
    fig.text(0.07, 0.915, "Pre-prototype prediction | Main capacitor: 1.0 uF X2 | Bleeder: 220 kohm x 2",
             fontsize=11.5, color="#4c5b66")
    fig.text(0.97, 0.95, "KiCad 10 DRC\n0 violations / 0 unconnected",
             ha="right", va="top", fontsize=11, fontweight="bold", color="#176b45",
             bbox={"boxstyle": "round,pad=0.55", "facecolor": "#eaf7f0", "edgecolor": "#79b797"})
    fig.text(0.07, 0.028,
             "SIMULATION — MEASUREMENT PENDING. Capacitor ESR/ESL and source resistance are explicit illustrative assumptions; raw CSV is included.",
             fontsize=10, color="#7b3f33", fontweight="bold")
    fig.savefig(ROOT / "shunt_filter_simulation_overview_v0_1.png", dpi=240, facecolor="white")
    fig.savefig(ROOT / "shunt_filter_simulation_overview_v0_1.svg", facecolor="white")
    plt.close(fig)
    print("Generated overview, four individual charts, and four CSV datasets")


if __name__ == "__main__":
    main()
