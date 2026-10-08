<a id="approved-figure-baseline"></a>

# Figure specification

[Previous: figure gallery](../figures/README.md) · [Return to README](../README.md) · [Next: redraw the panels](REPRODUCTION.md#redraw)

<a id="figure-3-coefficient-label-revision-8-september-2026"></a>
<a id="figure-palette-revision-8-september-2026"></a>
<a id="figure-1-uncertainty-revision-8-september-2026"></a>
<a id="figure-4-revision-5-september-2026"></a>

## Numerical panels

| Figure | Plotted quantity | Method and caption |
|---|---|---|
| 1 | Equal-cell contrast after rank-4 spectrum replacement, with pointwise support-conditioned intervals | [Uncertainty procedure](FIGURE1_UNCERTAINTY.md), [caption](FIGURE1_CAPTION.md) |
| 2 | Exact boundary-code response and conditional code-probability coefficients | [Theory](THEORY.md#3-finite-alphabet-theorem), [caption](DIALOGUE_REPORT.md#figure-2-caption) |
| 3 | Within-spectrum $\beta_n$ per $\Delta p=0.02$, with model-dependent inverse-size fits | [Estimator](NUMERICAL_METHODS.md#6-exact-spectrum-fixed-effect-estimator), [caption](DIALOGUE_REPORT.md#figure-3-caption) |
| 4 | Measurement-induced response by distance and paired near-minus-far contrasts | [Pairing and eligibility](NUMERICAL_METHODS.md#10-paired-measurement-location-intervention), [caption below](#figure-4-caption) |

Figure 3's ordinate is a pooled finite-grid fixed-effect coefficient. Figure 4 displays observed means and trajectory-bootstrap intervals; its distance panel uses the original distance table without a fitted curve. The [evidence reassessment](EVIDENCE_REASSESSMENT.md) gives distance-fit and finite-size-model diagnostics.

## Reproducible assets

`python reproduce.py --core-figures` produces six PDF/PNG/SVG triples. PDFs and PNGs are in `figures/core/`; matching SVGs are in `figures/core_svg/`. The [gallery](../figures/README.md) links each panel to its canonical table and plotting script. The [current manifest](../provenance/current_baseline_sha256.json) protects their byte identities. The [palette](../figures/PALETTE.md) applies to figures only.

The [provenance index](../provenance/README.md) records source and revision identities. `provenance/figure_sha256.csv` identifies an external historical baseline, not current outputs.

<a id="replacement-figure-4-caption"></a>

## Figure 4 caption

**Paired measurement-location intervention at unchanged central spectrum.** (a) Copies of the same premeasurement stabilizer state receive one projective-Z measurement at distance d from the central cut. Retaining interventions with unchanged central entropy preserves the complete central Schmidt spectrum. Points show the measurement-induced change in the purity-normalized linear-entropy response to an independent fresh cross-cut probe, pooled with equal weight over nine (n,p) cells; bars are the original 95% trajectory-bootstrap intervals. The observed response is concentrated near the cut and decreases strongly in magnitude over the measured distances. No fitted distance law is imposed. (b) Paired near-minus-far effect, with far distances at least n/4. The pooled effect is +0.0714 [+0.0655,+0.0773] without spectrum conditioning and -0.0474 [-0.0494,-0.0455] under the original unchanged-spectrum eligibility rule. Eligible sides are averaged within each distance before pairing. The location comparison is controlled on copies of the same pre-state; its conditional interpretation does not concern assignment of the long-run monitoring rate. Stricter same-side and common-eligibility checks are documented separately and do not replace the plotted primary estimates.

[Next: redraw the panels](REPRODUCTION.md#redraw) · [Return to README](../README.md)
