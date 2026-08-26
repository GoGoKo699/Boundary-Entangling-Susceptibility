# Provenance

## Figure baseline

`figure_sha256.csv` records the exact PDF and PNG assets reviewed in the frozen manuscript layout before repository migration. Its `path` column preserves the intended asset names; those binary files are not required to be tracked at those paths on the default branch.

The repository instead tracks:

- browser-visible SVG exports under `figures/core_svg/`;
- canonical numerical inputs under `data/processed/core_figures/`;
- exact Python plotting scripts under `scripts/figures/`.

Running `python reproduce.py --core-figures` regenerates fresh vector PDFs and PNG previews locally. Scientific verification is based on canonical values, exact identities, and stated estimands rather than PDF metadata hashes.

## Source migration

- `SOURCE_MIGRATION.md` explains which final checkpoints supplied each scientific layer.
- `MIGRATION_STATUS.md` separates completed repository work from tasks intentionally deferred until public release.
