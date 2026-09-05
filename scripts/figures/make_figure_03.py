#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from export_formats import save_formats

FIG_BLUE = '#245B78'
FIG_TEAL = '#2F7C78'
FIG_GRAY = '#6F7478'
FIG_GRID = '#D9DEE2'

def configure() -> None:
    mpl.rcParams.update({
        'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix', 'font.size': 9.4,
        'axes.labelsize': 9.7, 'axes.titlesize': 9.7, 'xtick.labelsize': 8.8, 'ytick.labelsize': 8.8,
        'axes.linewidth': 0.75, 'xtick.major.width': 0.75, 'ytick.major.width': 0.75,
        'xtick.major.size': 3.0, 'ytick.major.size': 3.0, 'lines.linewidth': 1.05,
        'pdf.fonttype': 42, 'ps.fonttype': 42,
    })

def draw_protocol(ax, df, protocol: str, color: str, title: str, show_y: bool) -> None:
    sub = df[df['protocol'] == protocol]
    xline = np.linspace(0.0, 1.0/32.0, 200)
    styles = {
        'primary': dict(marker='o', mfc=color, mec=color, ls='-', zorder=4),
        'replication': dict(marker='s', mfc='white', mec=color, ls='--', zorder=3),
    }
    for run in ['primary','replication']:
        s = sub[sub['run'] == run]
        finite = s[s['kind'] == 'finite_size'].sort_values('inv_n')
        thermo = s[s['kind'] == 'thermodynamic_limit'].iloc[0]
        style = styles[run]
        yline = float(thermo['beta']) + float(thermo['a_over_n']) * xline
        ax.plot(xline, yline, color=color, ls=style['ls'], lw=1.15, alpha=0.90, zorder=1)
        x = finite['inv_n'].to_numpy(float)
        y = finite['beta'].to_numpy(float)
        yerr = np.vstack([y - finite['ci_low'].to_numpy(float), finite['ci_high'].to_numpy(float) - y])
        ax.errorbar(x, y, yerr=yerr, fmt=style['marker'], ms=5.0,
                    mfc=style['mfc'], mec=style['mec'], mew=1.0,
                    ecolor=color, elinewidth=0.95, capsize=2.0, capthick=0.9,
                    linestyle='none', zorder=style['zorder'])
        y0 = float(thermo['beta'])
        y0err = np.array([[y0 - float(thermo['ci_low'])], [float(thermo['ci_high']) - y0]])
        ax.errorbar([0.0], [y0], yerr=y0err, fmt=style['marker'], ms=5.3,
                    mfc=style['mfc'], mec=style['mec'], mew=1.0,
                    ecolor=color, elinewidth=1.0, capsize=2.1, capthick=0.95,
                    linestyle='none', zorder=5)
    ax.axhline(0.0, color=FIG_GRAY, lw=0.70, zorder=0)
    ax.set_title(title, pad=4.0)
    ax.set_xlim(-0.0012, 0.0330)
    ax.set_ylim(-0.061, 0.002)
    ax.set_yticks([0.0, -0.02, -0.04, -0.06])
    ax.set_yticklabels([r'$0$', r'$-0.02$', r'$-0.04$', r'$-0.06$'])
    ax.set_xticks([0.0, 1/256, 1/128, 1/64, 1/32], labels=[r'$\infty$', r'$256$', r'$128$', r'$64$', r'$32$'])
    ax.grid(axis='y', color=FIG_GRID, lw=0.55, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if show_y:
        ax.set_ylabel(r'$\beta_n=\partial\chi_{\rm rel}/\partial(p/0.02)$')
    else:
        ax.tick_params(axis='y', labelleft=False)
        ax.set_ylabel('')

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=Path, required=True)
    parser.add_argument('--pdf', type=Path, required=True)
    parser.add_argument('--png', type=Path, required=True)
    args = parser.parse_args()
    configure()
    df = pd.read_csv(args.csv)
    fig, axes = plt.subplots(1, 2, figsize=(5.16, 2.72), sharey=True)
    draw_protocol(axes[0], df, 'z_projective', FIG_BLUE, r'projective $Z$', True)
    draw_protocol(axes[1], df, 'random_pauli', FIG_TEAL, r'random Pauli', False)
    fig.supxlabel(r'system size $n$ (positions linear in $1/n$)', x=0.545, y=0.046, fontsize=10.1)
    fig.subplots_adjust(left=0.165, right=0.992, bottom=0.235, top=0.89, wspace=0.10)
    save_formats(fig, args.pdf, args.png)
    plt.close(fig)

if __name__ == '__main__':
    main()
