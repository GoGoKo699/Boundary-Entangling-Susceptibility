# Figure assets

`core/` contains regenerated PDF and PNG panels. `core_svg/` contains browser exports of the same six panels. The supported plotting command is `python reproduce.py --core-figures` from the repository root, producing six PDF/PNG/SVG triples.

The original external author-approved PDF bytes are identified by [`../provenance/figure_sha256.csv`](../provenance/figure_sha256.csv). Their identity is distinct from the regenerated repository files. The local rendering comparison is recorded in [`../provenance/EXPORT_COMPARISON_2026-09-05.json`](../provenance/EXPORT_COMPARISON_2026-09-05.json). No standalone font files, manuscript source, or TikZ code are included.

**Figure 4 remains historical artwork pending author review.** The observed points are supported, but the exponential curve and xi annotation should not be read as an adequate single-exponential law or a precisely determined physical length. See [`../docs/EVIDENCE_REASSESSMENT.md`](../docs/EVIDENCE_REASSESSMENT.md). No new functional form has been fitted into the main artwork.

Normal CI exports workflow artifacts and has read-only repository permissions. It does not push regenerated binaries onto `main`.
