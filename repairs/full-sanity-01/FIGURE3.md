# Figure 3 coefficient-label repair

Audit finding: F-05a / F23-2. The plotted ordinate is a finite-grid, within-spectrum fixed-effect coefficient, not a pointwise derivative. The replacement ylabel is **within-spectrum $\beta_n$ (per $\Delta p=0.02$)**.

## Changes and preserved material

Only the ylabel string changed in `scripts/figures/make_figure_03.py`. Its PDF, PNG and SVG were regenerated. The [new successor record](../../provenance/FIGURE3_LABEL_2026-09-08.json) records four exact before/after hashes and the unchanged predecessor-record hashes. The [current output manifest](../../provenance/current_baseline_sha256.json) changes only those three asset entries and explicitly identifies the successor.

The original Figure 1 adoption and palette adoption records are unchanged. The old Figure 3 exports remain byte-identical in the audit's `reproduced_figures` directory. No audit file was edited. Reversing the one specified label substitution recovers the original Figure 3 source SHA-256 exactly. No data, confidence interval, fit, color, marker, axis limit, panel size, or layout setting changed. The automatic centering of the new text necessarily has a different glyph bounding box; no other figure geometry changed.

The adoption checker retains the original Figure 1-to-palette hash chain, then checks the explicit Figure 3 successor against the palette's output and source hashes. Its successor allow-list is exactly the Figure 3 source and three exports, not a generic mechanism to override arbitrary protected files. Even changing the successor's source hash cannot authorize an extra numerical or layout edit, because the inverse substitution must recover the old locked source hash.

## Executed checks

Runtime: `/workspace/scratch/0174ee249694/audit-venv/bin/python`, the clean pinned environment retained from the audit (Python 3.12.13, Matplotlib 3.10.8, NumPy 2.3.5, pandas 2.2.3).

```bash
python scripts/figures/make_figure_03.py \
  --csv data/processed/core_figures/figure_03_size_scaling.csv \
  --pdf figures/core/figure_03_size_scaling.pdf \
  --png figures/core/figure_03_size_scaling.png
mv figures/core/figure_03_size_scaling.svg figures/core_svg/figure_03_size_scaling.svg
python -m pytest -q tests/test_figure3_label.py tests/test_figure1_adoption.py \
  tests/test_figure_palette.py tests/test_record_bundle.py
python scripts/analysis/check_figure1_adoption.py \
  --resamples audits/full-sanity-01/reproduced_figure1_uncertainty
```

All commands returned zero. The focused suite passed **29 tests in 6.14 seconds**. The adoption checker passed, including all 26 expected full-resampling outputs and ten current primary intervals. The regenerated PNG was opened and visually inspected: the new label fits, with no clipping or overlap, and the points, bars, lines and other labels retain their positions. `git diff --check` passed for the edited text files.

The new tests compare old/new artist geometry, removing only the specified ylabel text, and compare complete SVG trees after removing only that ylabel group. The SVG comparison preserves all other text, paths, numeric coordinates, uncertainty bars, transforms, dimensions and metadata. Existing palette tests regenerate all eighteen current exports and require exact byte agreement. Mutation tests reject changes to each of the five canonical numerical tables, a non-Figure-3 output, a Figure 3 output, the predecessor chain and either numerical or layout source edits even with an updated successor hash.

These are label-only and preservation checks. They share the plotting implementation and pinned rendering environment; they do not add new statistical evidence or replace the audit's independent record reconstruction.
