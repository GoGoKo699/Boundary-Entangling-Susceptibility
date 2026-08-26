#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def configure():
    mpl.rcParams.update({
        "font.family": "STIXGeneral",
        "mathtext.fontset": "stix",
        "font.size": 8.0,
        "axes.labelsize": 8.2,
        "xtick.labelsize": 7.2,
        "ytick.labelsize": 7.2,
        "legend.fontsize": 7.0,
        "axes.linewidth": 0.7,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "lines.linewidth": 1.0,
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
    order = (
        df[["family", "family_label", "family_order"]]
        .drop_duplicates()
        .sort_values("family_order")
    )
    labels = order["family_label"].tolist()
    families = order["family"].tolist()
    y_positions = np.arange(len(families))[::-1].astype(float)

    fig, ax = plt.subplots(figsize=(4.05, 2.45))
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
        xerr = np.vstack([x - sub["ci_low"].to_numpy(float),
                          sub["ci_high"].to_numpy(float) - x])
        st = styles[run]
        ax.errorbar(x, y, xerr=xerr, fmt=st["marker"], ms=4.4,
                    mfc=st["mfc"], mec=st["mec"], mew=0.9,
                    ecolor=st["ecolor"], elinewidth=1.0,
                    capsize=2.0, capthick=0.9, linestyle="none",
                    zorder=3)

    ax.axvline(0.0, color="0.35", linewidth=0.8, zorder=1)
    ax.set_xlim(-0.60, 0.035)
    ax.set_ylim(-0.55, len(families) - 0.45)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels)
    ax.set_xticks([-0.6, -0.4, -0.2, 0.0])
    ax.grid(axis="x", color="0.85", linewidth=0.55, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel(r"$\Delta\chi_{\rm rel}=\chi_{\rm rel}(0.24)-\chi_{\rm rel}(0.08)$")
    ax.tick_params(axis="y", pad=3.0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout(pad=0.4)
    args.pdf.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.pdf)
    fig.savefig(args.png, dpi=400)
    plt.close(fig)

if __name__ == "__main__":
    main()
