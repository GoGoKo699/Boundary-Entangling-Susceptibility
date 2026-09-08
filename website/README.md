# Project website: source-derived preview

The website is a reader interface to the consolidated Boundary-Entangling-Susceptibility study. It is not a manuscript, a new scientific analysis, or a public deployment.

## Preview on GitHub

Open the [repository preview](preview/README.md) or [six-panel palette comparison](preview/FIGURES.md) directly. The root README links both. Those Markdown pages and their inline images work inside the existing private repository. The screenshots show the separate static-site layout, not an interactive website embedded in a README.

The read-only `website-preview` workflow builds and checks the full site and retains it as an artifact. It does not deploy GitHub Pages or publish private source. Public hosting remains a separate decision.

## Build

The tested converter is Pandoc 3.1.11.1. Use Python 3.11+ and install `website/requirements.txt`. The plotting preview additionally uses the existing `requirements-reproducible.txt` environment.

```bash
python scripts/site/preview_figures.py --output ../bes-irises-figures
python scripts/site/build.py --output ../bes-site-preview --figures ../bes-irises-figures
python scripts/site/check.py --site ../bes-site-preview
python -m http.server 8000 --directory ../bes-site-preview --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/` after starting the local server. The output is static and self-contained. JavaScript is optional for reading; it supplies local search and theme controls. No font files, analytics, third-party embeds, or network-dependent mathematical renderer are distributed.

The build requires an empty output path outside the scientific repository. It does not overwrite accepted figures, modify source files, or rerun circuit simulations or statistical analysis. It refuses a changed scientific source until `website/scientific_baseline.json` is deliberately reviewed and updated. The 199 scientific baseline files remain in place; the old root README is preserved byte-for-byte in `website/source_snapshots/original_README.md.txt`. That explicit presentation exception lets the current README serve as an editable entrance without rewriting the frozen source downloads.

## One scientific source

All baseline Markdown is rendered directly. The nine main questions and eight appendix groups are extracted verbatim from `docs/DIALOGUE_REPORT.md`, with links to their complete source and source register. The original 32 appendix question IDs remain. Generated pages are not separately edited. `website/figures.json` maps each figure to its code, input table, methodological scope, and source question.

The new landing and resource prose is presentation text based on `docs/SCIENTIFIC_STORY.md` and `docs/CLAIM_EVIDENCE_MAP.md`. `website/palette.json` specifies the Irises-inspired proposal. `scripts/site/preview_figures.py` evaluates the original plotting scripts with color-literal substitutions and the default cycle changed only in memory. The accepted scripts and assets remain unchanged. Original and preview outputs are both accessible and distinctly labeled.

## Reader routes

Home → scientific question → nine existing reader questions → four figure guides → theory/methods → reproduction → resources. The reference library preserves all baseline Markdown, with history labeled separately. Every figure has direct data, code, caption-context, and accepted-asset links. Proofs and statistical qualifications remain in the route rather than being replaced by verification badges.

## Release boundary

Do not enable public deployment as part of this preview. Repository and Pages visibility are separate decisions, and no reuse license has been selected. The preview is maintained in the repository with source/asset preservation and site checks. No live hosting or reuse license is implied by the preview.

## Stages before manuscript

1. Review this reader architecture and color semantics, not merely its homepage.
2. Refine the in-repository presentation; apply the selected palette to canonical figures only after approval, keeping data and geometry fixed.
3. Complete the source-to-page prose review and the pending related-work attribution integration. Do not treat style editing as scientific review.
4. Validate all reader routes, math, downloads, mobile layouts, and the scientific pipeline from a clean checkout. Decide hosting and reuse permissions.
5. Freeze the repository/site scientific account. The manuscript is assembled last.

## Mathematical rendering

Pandoc converts source mathematics to native MathML. A rendering-only AST normalization expands brace-delimited legacy `\rm` into `\mathrm{...}` because the MathML converter does not accept the legacy declaration. Each conversion is recorded in `BUILD.json`. Source Markdown is never edited. Wide equations can be scrolled with a keyboard or touch; they are not reduced to unreadable text.

## Editorial source

The presentation follows the repository mode of My-tone v0.6.1, read at commit `005873301782c06f21b1c6e73a5ce3b08c630cc4`. Its private corpus and tools are not bundled or required to build the site. See `EDITORIAL_POLICY.md` for the separation between presentation checks and scientific review.

## Refresh screenshots and figure candidates

After building and checking the site above, use `scripts/site/capture_preview.py` to refresh the three tracked screenshots. Install `website/requirements-preview.txt` and Playwright Chromium first. The renderer loads the generated page and its local assets in memory and blocks network requests. It does not host or publish anything.

```bash
python scripts/site/capture_preview.py --site ../bes-site-preview --output website/preview/images
```

Copy only the verified proposal outputs from `../bes-irises-figures/` into `website/preview/irises/` when intentionally refreshing that proposal. Do not copy them into `figures/core` or `figures/core_svg`. Screenshots are review aids, not numerical evidence; the canonical data and accepted assets remain unchanged.
