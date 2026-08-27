# Figures

## Browser-visible core panels

`core_svg/` contains SVG exports of the six author-reviewed Python panels:

1. fixed-spectrum intervention response;
2. exact stabilizer response alphabet;
3. monitoring-induced boundary-code redistribution;
4. physical size scaling and independent replication;
5. paired distance decay;
6. conditional versus unconditional location contrast.

These SVGs are tracked so that a GitHub reader can inspect the complete result without a manuscript or a local Python environment.

## Reproducible source

The numerical source of truth is split into:

- canonical CSV/JSON inputs under `data/processed/core_figures/`;
- exact plotting scripts under `scripts/figures/`.

Running

```bash
python reproduce.py --core-figures
```

writes fresh vector PDFs and PNG previews to the untracked local directory `reproduced_figures/`.

## Author-reviewed manuscript baseline

The six final PDF panels were reviewed in the manuscript layout before migration. Their filenames, SHA-256 hashes, byte counts, corresponding browser SVGs, and reproduction scripts are recorded in `provenance/figure_sha256.csv`.

Those exact PDF binaries are **not tracked on the default branch**. This is deliberate: PDF metadata can vary between Matplotlib environments even when the numerical and visual content is unchanged. The repository verifies the canonical values, exact identities, and regenerated outputs rather than treating binary PDF identity as the scientific test. The frozen PDF set should accompany a future versioned release if an immutable copy is needed.
