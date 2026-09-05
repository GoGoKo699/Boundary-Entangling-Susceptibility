#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from export_formats import save_formats

def configure():
    mpl.rcParams.update({
        "font.family": "STIXGeneral",
        "mathtext.fontset": "stix",
        "font.size": 9.2,
        "axes.labelsize": 9.6,
        "xtick.labelsize": 8.6,
        "ytick.labelsize": 8.6,
        "legend.fontsize": 7.0,
        "axes.linewidth": 0.78,
        "xtick.major.width": 0.78,
        "ytick.major.width": 0.78,
        "xtick.major.size": 3.2,
        "ytick.major.size": 3.2,
        "lines.linewidth": 1.08,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--png", type=Path, required=True)
    args = parser.parse_args()
    configure()
    df = pd.read_csv(args.csv)
    order = df[["family", "family_label", "family_order"]].drop_duplicates().sort_values("family_order")
    labels = order["family_label"].tolist()
    families = order["family"].tolist()
    y_positions = np.arange(len(families))[::-1].astype(float)
    fig, ax = plt.subplots(figsize=(4.22, 2.70))
    for y in y_positions:
        ax.axhspan(y - 0.46, y + 0.46, color="0.97", zorder=0)
    offsets = {"primary": 0.12, "independent": -0.12}
    styles = {
        "primary": dict(marker="o", mfc="C0", mec="C0", ecolor="C0"),
        "independent": dict(marker="s", mfc="white", mec="C0", ecolor="C0"),
    }
    for run in ["primary", "independent"]:
        sub = df[df["run"] == run].set_index("family").loc[families]
        y = y_positions + offsets[run]
        x = sub["estimate"].to_numpy(float)
        xerr = np.vstack([x - sub["ci_low"].to_numpy(float), sub["ci_high"].to_numpy(float) - x])
        st = styles[run]
        ax.errorbar(x, y, xerr=xerr, fmt=st["marker"], ms=5.0,
                    mfc=st["mfc"], mec=st["mec"], mew=1.0,
                    ecolor=st["ecolor"], elinewidth=1.05,
                    capsize=2.15, capthick=0.98, linestyle="none", zorder=3)
    ax.axvline(0.0, color="0.35", linewidth=0.85, zorder=1)
    ax.set_xlim(-0.60, 0.035)
    ax.set_ylim(-0.55, len(families) - 0.45)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels)
    ax.set_xticks([-0.6, -0.4, -0.2, 0.0])
    ax.grid(axis="x", color="0.85", linewidth=0.55, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel(r"$\Delta\chi_{\rm rel}=\chi_{\rm rel}(0.24)-\chi_{\rm rel}(0.08)$", labelpad=3.8)
    ax.tick_params(axis="y", pad=3.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout(pad=0.48)
    save_formats(fig, args.pdf, args.png)
    plt.close(fig)

if __name__ == "__main__":
    main()
