"""Apply the approved figure-only palette without altering plotted quantities.

The numerical plotting programs remain unchanged. All three output formats use
this one color pass in export_formats.save_formats; no website styling is used.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, to_hex, to_rgba
from matplotlib.lines import Line2D
from matplotlib.collections import Collection
from matplotlib.patches import Patch
from matplotlib.text import Text

ROOT = Path(__file__).resolve().parents[2]


def load_palette():
    return json.loads((ROOT / 'figures/palette.json').read_text())


def contrast(foreground, background):
    def luminance(color):
        rgb = to_rgba(color)[:3]
        return sum(w * (v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4)
                   for w, v in zip((.2126, .7152, .0722), rgb))
    lo, hi = sorted((luminance(foreground), luminance(background)))
    return (hi + .05) / (lo + .05)


def apply_palette(figure):
    """Recolor existing artists; preserve data, alpha, layout, and scale direction.

    This is idempotent. Only the declared source colors and the original C0
    blue are mapped. Grays, white backgrounds, and non-color properties remain.
    """
    palette = load_palette()
    mapping = palette['figure_mapping']
    mapping = {key.lower(): value for key, value in mapping.items()}

    def recolor(color):
        rgba = to_rgba(color)
        replacement = mapping.get(to_hex(rgba[:3]).lower())
        if replacement is None:
            return color
        return (*to_rgba(replacement)[:3], rgba[3])

    for artist in figure.findobj():
        if isinstance(artist, Line2D):
            artist.set_color(recolor(artist.get_color()))
            artist.set_markerfacecolor(recolor(artist.get_markerfacecolor()))
            artist.set_markeredgecolor(recolor(artist.get_markeredgecolor()))
        elif isinstance(artist, Collection):
            for getter, setter in ((artist.get_facecolor, artist.set_facecolor),
                                   (artist.get_edgecolor, artist.set_edgecolor)):
                colors = getter()
                if len(colors):
                    setter([recolor(color) for color in colors])
        elif isinstance(artist, Patch):
            artist.set_facecolor(recolor(artist.get_facecolor()))
            artist.set_edgecolor(recolor(artist.get_edgecolor()))
        elif isinstance(artist, Text):
            artist.set_color(recolor(artist.get_color()))

    checks = []
    for ax in figure.axes:
        for image in ax.images:
            cmap = image.get_cmap()
            # Both matrices use this three-stop map, in opposite directions.
            # Read the actual stops, not sampled values near the midpoint.
            if cmap.name == 'fig2_diverging':
                segments = cmap._segmentdata
                stops = [tuple(segments[channel][i][1] for channel in ('red', 'green', 'blue'))
                         for i in range(3)]
                colors = [recolor(color) for color in stops]
                image.set_cmap(LinearSegmentedColormap.from_list(cmap.name, colors, N=cmap.N))
            data = np.asarray(image.get_array())
            if data.ndim != 2:
                continue
            for label in ax.texts:
                x, y = label.get_position()
                j, i = int(np.floor(x + .5)), int(np.floor(y + .5))
                if not (0 <= i < data.shape[0] and 0 <= j < data.shape[1]):
                    continue
                background = to_hex(image.cmap(image.norm(data[i, j])))
                chosen = max((palette['colors']['ink'], '#FFFFFF'),
                             key=lambda fg: contrast(fg, background))
                if contrast(chosen, background) < 4.5:
                    chosen = '#000000'
                label.set_color(chosen)
                ratio = contrast(chosen, background)
                if ratio < 4.5:
                    raise ValueError('Insufficient matrix-label contrast')
                checks.append({'text': label.get_text(), 'contrast': ratio})
    return checks
