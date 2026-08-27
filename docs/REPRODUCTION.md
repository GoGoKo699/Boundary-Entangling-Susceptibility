# Reproduction

## Fast path

From a clean clone:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest -q
python verify.py
python reproduce.py --core-figures
```

The figure command reads only the canonical files in `data/processed/core_figures/` and writes fresh vector PDFs and PNG previews to the untracked local directory `reproduced_figures/`.

## What is tracked

The repository tracks three figure layers:

1. **Canonical numerical inputs** under `data/processed/core_figures/`.
2. **The exact Python plotting scripts** under `scripts/figures/`.
3. **Browser-visible SVG exports** of the author-reviewed panels under `figures/core_svg/`.

The SVG files let GitHub readers inspect the results without downloading a paper or running Python. The scripts and canonical tables are the reproducible source of truth.

## Author-reviewed PDF baseline

The final PDF panels were reviewed in the manuscript layout before migration. Their filenames, SHA-256 values, byte counts, corresponding browser copies, and plotting scripts are preserved in `provenance/figure_sha256.csv`.

The exact author-reviewed PDF binaries are not tracked on the default branch. Running the reproduction command creates new vector PDFs from the same canonical values. Matplotlib PDF metadata can differ across environments, so repository verification does not require byte-identical regenerated PDFs. An immutable copy of the frozen PDF set can be attached to a future versioned release.

## Full studies

The two study directories contain the load-bearing simulation and analysis source needed to understand and extend the final research stages:

- `studies/checkpoint_04/`: fixed-spectrum intervention, architecture/probe robustness, and response-operator validation;
- `studies/checkpoint_05/`: physical stabilizer matching, scaling, boundary-code decomposition, transition context, and paired location intervention.

Large compressed state tables and complete checkpoint archives are intentionally not committed to ordinary Git history. Their policy and planned release route are described in `docs/DATA_POLICY.md`.

## Verification philosophy

`verify.py` performs a fast clean-clone audit. It checks:

- required scientific documents and browser figures;
- validity of all tracked SVG files;
- local Markdown and HTML-image link integrity;
- the exact neighboring-purity and stabilizer boundary-code identities;
- row counts, signs, probability conservation, and exact response reconstruction for the four core results;
- the large-size and independent-replication sign tests;
- the paired-intervention sign reversal and localization range;
- the figure-provenance manifest format;
- the repository rule excluding manuscript TeX and TikZ sources.

This fast audit is not a replacement for rerunning every large simulation from raw trajectory archives. Those full archives remain a release/deposit task before public publication.
