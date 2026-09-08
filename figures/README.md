# Figures

The [approved baseline](../docs/FIGURE_BASELINE.md) contains six Python data panels forming four narrative figures. `core/` holds PDF/PNG outputs and `core_svg/` holds browser SVGs. The [dialogue report](../docs/DIALOGUE_REPORT.md) uses the same panels and adds no fifth narrative figure.

The active Figure 4 distance panel omits the historical exponential curve and its length annotation. The original data points, confidence intervals, labels, and page dimensions are unchanged. Its contrast panel and all panels of Figures 1–3 are unchanged.

Run `python reproduce.py --core-figures` to rebuild six PDF/PNG/SVG triples in `reproduced_figures/`. All three formats come from the same Python source. The current Figure 4 generator has no decay-fit input.

The earlier external Overleaf PDF hashes in `provenance/figure_sha256.csv` are historical identities, not current-output checksums. The historical fit is discussed in the evidence reassessment but is not an active graphical or physical claim.

## Figure 1 intervals adopted on 8 September 2026

The active Figure 1 panel has revised error bars from the reviewed 50,000-draw support-conditioned recipe, without any layout or point-estimate change. Earlier statements above about Figures 1–3 remaining unchanged refer to the Figure 4 revision. The old Figure 1 outputs remain under `results/historical_figure1/`. See [the current caption](../docs/FIGURE1_CAPTION.md).
