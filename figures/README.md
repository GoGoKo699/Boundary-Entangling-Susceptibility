# Figures

These six Python panels form the four-figure scientific account. The [full dialogue](../docs/DIALOGUE_REPORT.md) explains their relationship; the [figure baseline](../docs/FIGURE_BASELINE.md) records the current versions and captions.

| Figure | PDF panels | Numerical input |
|---|---|---|
| 1: fixed-spectrum comparison | [Response comparison](core/figure_01_panel_b.pdf) | [Table](../data/processed/core_figures/figure_01_panel_b.csv) |
| 2: boundary-code mechanism | [Exact response](core/figure_02_response_matrix.pdf), [redistribution](core/figure_02_redistribution_matrix.pdf) | [Table](../data/processed/core_figures/figure_02_boundary_codes.csv) |
| 3: physical size comparison | [Size dependence](core/figure_03_size_scaling.pdf) | [Table](../data/processed/core_figures/figure_03_size_scaling.csv) |
| 4: paired location intervention | [Distance profile](core/figure_04_distance_decay.pdf), [conditioning contrast](core/figure_04_conditioning_contrast.pdf) | [Distance](../data/processed/core_figures/figure_04_distance_decay.csv), [contrast](../data/processed/core_figures/figure_04_conditioning_contrast.csv) |

The approved [Irises palette](PALETTE.md) applies only to the figures. `core/` holds publication PDF/PNG outputs; `core_svg/` holds the matching browser SVGs. The numerical inputs and figure geometry are unchanged.

## Preview

### Figure 1

![Fixed-spectrum response comparison](core_svg/figure_01_panel_b.svg)

### Figure 2

![Exact boundary-code response](core_svg/figure_02_response_matrix.svg)

![Boundary-code probability redistribution](core_svg/figure_02_redistribution_matrix.svg)

### Figure 3

![Conditional monitoring coefficients and model-dependent extrapolations](core_svg/figure_03_size_scaling.svg)

### Figure 4

![Spectrum-preserving distance profile without a fitted decay law](core_svg/figure_04_distance_decay.svg)

![Paired unconditional and spectrum-preserving location contrasts](core_svg/figure_04_conditioning_contrast.svg)

## Reproduce

Run `python reproduce.py --core-figures` to rebuild all six PDF/PNG/SVG triples. The [reproduction guide](../docs/REPRODUCTION.md) gives the separate commands for recalculating the statistics and uncertainty. A figure redraw is not a new analysis or simulation.

The Figure 1 intervals use the adopted 50,000-draw support-conditioned procedure. The Figure 4 distance plot retains its observations and intervals without the rejected exponential fit. Historical output identities remain in the provenance records; the [active manifest](../provenance/current_baseline_sha256.json) identifies current output files.
