#!/usr/bin/env python3
from pathlib import Path
import argparse
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from export_formats import save_formats

FIG_BLUE = '#245B78'
FIG_ORANGE = '#B66A3C'
FIG_LIGHT = '#F3F4F4'
mpl.rcParams.update({
    'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix', 'font.size': 9.4,
    'xtick.labelsize': 9.2, 'ytick.labelsize': 9.2, 'axes.linewidth': 0.75,
    'xtick.major.size': 0, 'ytick.major.size': 0, 'pdf.fonttype': 42, 'ps.fonttype': 42,
})

def matrix_from_rows(frame, value_col):
    out = np.empty((3, 3), dtype=float)
    for i, dl in enumerate([1, 0, -1]):
        for j, dr in enumerate([-1, 0, 1]):
            row = frame[(frame.delta_L == dl) & (frame.delta_R == dr)]
            if len(row) != 1:
                raise RuntimeError(f'Missing/duplicate code {(dl, dr)}')
            out[i, j] = float(row.iloc[0][value_col])
    return out

def text_color(value, limit):
    return 'white' if abs(value) >= 0.58 * limit else '#222222'

def draw_matrix(matrix, output_pdf, output_png, limit, formatter,
                corner_words=False, reverse_colors=False, show_ylabels=True):
    colors = [FIG_ORANGE, FIG_LIGHT, FIG_BLUE] if reverse_colors else [FIG_BLUE, FIG_LIGHT, FIG_ORANGE]
    cmap = LinearSegmentedColormap.from_list('fig2_diverging', colors, N=256)
    norm = TwoSlopeNorm(vmin=-limit, vcenter=0.0, vmax=limit)
    fig, ax = plt.subplots(figsize=(2.28, 2.28))
    ax.imshow(matrix, cmap=cmap, norm=norm, interpolation='nearest', aspect='equal')
    ax.set_xticks([0, 1, 2], labels=[r'$-1$', r'$0$', r'$+1$'])
    ax.set_yticks([0, 1, 2], labels=[r'$+1$', r'$0$', r'$-1$'] if show_ylabels else ['', '', ''])
    ax.tick_params(axis='both', which='major', pad=3.0)
    ax.set_xticks(np.arange(-0.5, 3, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 3, 1), minor=True)
    ax.grid(which='minor', color='white', linewidth=1.0, alpha=0.90)
    ax.tick_params(which='minor', bottom=False, left=False)
    for i in range(3):
        for j in range(3):
            val = matrix[i, j]
            col = text_color(val, limit)
            number = formatter(val)
            if corner_words and (i, j) in {(0, 2), (2, 0)}:
                ax.text(j, i - 0.15, number, ha='center', va='center', fontsize=10.2, color=col)
                word = r'$S_m\,\mathrm{peak}$' if (i, j) == (0, 2) else r'$S_m\,\mathrm{dip}$'
                ax.text(j, i + 0.23, word, ha='center', va='center', fontsize=9.2, color=col)
            else:
                ax.text(j, i, number, ha='center', va='center', fontsize=10.2, color=col)
    for spine in ax.spines.values():
        spine.set_linewidth(0.75)
        spine.set_color('#333333')
    fig.subplots_adjust(left=0.19, right=0.985, bottom=0.15, top=0.985)
    save_formats(fig, output_pdf, output_png)
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', type=Path, required=True)
    ap.add_argument('--outdir', type=Path, required=True)
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.csv)
    def response_fmt(x):
        return r'$0$' if abs(x) < 5e-12 else rf'${x:+.1f}$'
    def probability_fmt(x):
        return r'$0.000$' if abs(x) < .0005 else rf'${x:+.3f}$'
    draw_matrix(matrix_from_rows(df, 'display_response'),
                args.outdir/'figure_02_response_matrix.pdf', args.outdir/'figure_02_response_matrix.png',
                .6, response_fmt, corner_words=True, reverse_colors=True, show_ylabels=True)
    draw_matrix(matrix_from_rows(df, 'display_probability_slope'),
                args.outdir/'figure_02_redistribution_matrix.pdf', args.outdir/'figure_02_redistribution_matrix.png',
                .025, probability_fmt, corner_words=False, reverse_colors=False, show_ylabels=False)

if __name__ == '__main__':
    main()
