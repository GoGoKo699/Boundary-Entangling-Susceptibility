# Reproduction

## Fast path

From a clean clone:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
python verify.py
python reproduce.py --core-figures
```

The figure command reads only the canonical files in
`data/processed/core_figures/` and writes fresh vector PDFs and PNG previews to
`reproduced_figures/`.

## What is tracked

The repository tracks three layers:

1. **Canonical numerical inputs** under `data/processed/core_figures/`.
2. **The exact Python plotting scripts** under `scripts/figures/`.
3. **Browser-visible SVG exports** of the author-reviewed panels under
   `figures/core_svg/`.

The SVG files let GitHub readers inspect the results without downloading a
paper or running Python. The scripts and canonical tables are the reproducible
source of truth.

## Author-reviewed PDF baseline

The final PDF panels were reviewed in the manuscript layout before migration.
Their SHA-256 values and byte counts are preserved in
`provenance/figure_sha256.csv`. Those exact PDF/PNG binaries are not required by
the Git workflow because Matplotlib PDF metadata can vary across environments;
regeneration is checked through data values, identities, and visual outputs
rather than byte equality.

## Full studies

The two study directories contain the load-bearing simulation and analysis
source needed to understand and extend the final research stages:

- `studies/checkpoint_04/`: fixed-spectrum intervention, architecture/probe
  robustness, and response-operator validation;
- `studies/checkpoint_05/`: physical stabilizer matching, scaling,
  boundary-code decomposition, transition context, and paired location
  intervention.

Large compressed state tables and complete checkpoint archives are intentionally
not committed to ordinary Git history. Their policy and planned release route
are described in `docs/DATA_POLICY.md`.

## Verification philosophy

`verify.py` checks:

- required scientific documents and browser figures;
- the exact neighboring-purity and stabilizer boundary-code identities;
- row counts, signs, probability conservation, and exact response
  reconstruction for the four core results;
- the large-size and independent-replication sign tests;
- the paired-intervention sign reversal and localization range;
- the repository rule excluding manuscript TeX and TikZ sources.

This is a fast repository audit, not a replacement for rerunning every large
simulation from raw trajectories.
