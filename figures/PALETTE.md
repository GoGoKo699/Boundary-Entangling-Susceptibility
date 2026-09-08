# Figure palette

The approved palette is inspired by the linked reproduction of Vincent van Gogh's [Irises](https://en.wikipedia.org/wiki/Irises_%28painting%29). The colors are design choices, not pigment measurements or exact pixel samples.

| Figure role | Color |
|---|---|
| Main series / iris blue | `#3F4D8C` |
| Second protocol / leaf green | `#477568` |
| Contrast / earth tone | `#A05A3C` |
| Matrix neutral midpoint | `#F7F5EC` |
| Dark matrix-label option | `#24313A` |

Figures retain white backgrounds. The warm and cool ends follow each panel's declared scale: the response and redistribution matrices have opposite color directions. Color alone does not indicate statistical significance, effect sign, or replication status. Filled circles, open squares, line styles, labels, and numbers retain their roles.

Only colors changed. Input tables, estimates, uncertainty intervals, normalization, panel size, axis range, text, and marker geometry did not. Matrix-label colors are selected for contrast against their cell backgrounds without moving or rewriting text.

`palette.json` is the single palette specification. The four numerical plotting programs are unchanged; their common exporter applies `scripts/figures/figure_palette.py` immediately before saving PDF, PNG, and SVG. Running the existing commands therefore produces the approved colors in every format. The palette tests compare the non-color artists before and after this step, test idempotence, and compare fresh files against the accepted outputs.

The adoption record is [here](../provenance/FIGURE_PALETTE_2026-09-08.json). The preceding figure and website previews remain in Git history. They are not a second active presentation.

## Repository presentation

The repository uses GitHub's default Markdown styling and navigation. There is no custom page background, typeface, CSS theme, JavaScript interface, or separate website build. This decision does not remove the scientific reading routes, proofs, methods, evidence, or reproducibility documentation.
