# Migration checkpoint — 2026-08-26

This checkpoint records the first complete reader-facing migration of the surviving project to the default branch.

## Reader-facing layer

- Root README explains the four-step scientific chain without requiring a manuscript.
- `docs/` contains the full story, numerical results, exact theory, methods, validation, FAQ, limitations, related work, research history, and reproduction instructions.
- `results/core_claims.csv` separates exact, numerical, extrapolated, causal, and excluded statements.

## Reproducibility layer

- Canonical human-readable inputs for all six Python panels are under `data/processed/core_figures/`.
- Supported plotting entry points are under `scripts/figures/`.
- `reproduce.py --core-figures` regenerates PDFs and PNGs locally.
- Browser-visible SVG exports are under `figures/core_svg/`.
- `verify.py`, unit tests, and GitHub Actions provide a fast audit.

## Research layer

- Checkpoint 04 retains the fixed-spectrum intervention, cross-architecture/probe source, response-operator validation, and selected result tables.
- Checkpoint 05 retains the physical stabilizer simulator, scaling and replication source, boundary-code and transition analyses, paired intervention, design locks, and validation source.

## Deliberate exclusions

- no manuscript TeX or TikZ;
- no obsolete trajectory-fingerprint or cumulative flow-balance workflow;
- no Aubry–André branch in the active project;
- no opaque complete checkpoint archives in ordinary Git history.

## Remaining before public release

Licensing, raw-archive release/deposit, immutable data URLs, specialist theorem audit, and temporary-branch cleanup remain pending.
