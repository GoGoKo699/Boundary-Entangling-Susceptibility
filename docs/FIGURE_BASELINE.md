# Approved figure baseline

## Current figure palette

The six panels use the approved [Irises palette](../figures/PALETTE.md). All data, intervals, labels, axes, marker shapes, panel sizes, and fitted/no-fit choices are unchanged. This palette applies only to figures. The repository uses standard GitHub Markdown. The earlier revision descriptions below record what changed at their respective dates, not a claim that the old colors are still active.

## Figure 1 uncertainty revision: 8 September 2026

The active Figure 1 panel now uses the reviewed primary support-conditioned bootstrap intervals. Point positions, fonts, colors, dimensions, axes, family order, and plotting source are unchanged. The former CSV/PDF/PNG/SVG are preserved under `results/historical_figure1/`. See [the current method](FIGURE1_UNCERTAINTY.md) and [replacement caption](FIGURE1_CAPTION.md). Figures 2–4 remain unchanged.

## Figure 4 revision: 5 September 2026

The author approved the minimal Figure 4 distance-panel revision on 5 September 2026. The active version removes the historical exponential curve and its length annotation. Observed means, original intervals, dimensions, axes, label positions, and the conditioning-contrast panel are unchanged. At that Figure 4 revision, Figures 1–3 were unchanged; the later Figure 1 uncertainty revision is described above.

The four-figure [dialogue report](DIALOGUE_REPORT.md) uses this baseline. Its question identifiers follow [DIALOGUE_QUESTION_MAP.md](DIALOGUE_QUESTION_MAP.md).

## Reproducible assets

`python reproduce.py --core-figures` produces six PDF/PNG/SVG triples. The current Figure 4 generator takes the original distance and contrast CSVs only. It neither reads nor refits `results/historical_fit/figure_04_distance_fit.json`.

Current publication PDFs/PNGs are in `figures/core/`; browser SVGs are in `figures/core_svg/`. `scripts/figures/make_figure_04.py` is the current plotting source. For Overleaf, replace only `Graph/figure_04_distance_decay.pdf`. No geometry or figure insertion change is necessary. The old sentence asserting an exponential law must also be removed from the caption; a complete replacement is below.

The earlier `provenance/figure_sha256.csv` identifies the historical external Overleaf baseline. It is not a current-output checksum list. Its original entries and the fit JSON are retained for provenance, not as evidence for an accepted exponential law. The [evidence reassessment](EVIDENCE_REASSESSMENT.md) explains why the model was not retained.

## Replacement Figure 4 caption

**Paired measurement-location intervention at unchanged central spectrum.** (a) Copies of the same premeasurement stabilizer state receive one projective-Z measurement at distance d from the central cut. Retaining interventions with unchanged central entropy preserves the complete central Schmidt spectrum. Points show the measurement-induced change in the purity-normalized linear-entropy response to an independent fresh cross-cut probe, pooled with equal weight over nine (n,p) cells; bars are the original 95% trajectory-bootstrap intervals. The observed response is concentrated near the cut and decreases strongly in magnitude over the measured distances. No fitted distance law is imposed. (b) Paired near-minus-far effect, with far distances at least n/4. The pooled effect is +0.0714 [+0.0655,+0.0773] without spectrum conditioning and -0.0474 [-0.0494,-0.0455] under the original unchanged-spectrum eligibility rule. Eligible sides are averaged within each distance before pairing. The location comparison is controlled on copies of the same pre-state; its conditional interpretation does not concern assignment of the long-run monitoring rate. Stricter same-side and common-eligibility checks are documented separately and do not replace the plotted primary estimates.
