<a id="figures"></a>

# Four figures, four jobs

[Previous: four-figure account](../docs/DIALOGUE_REPORT.md) · [Learning route](../docs/PROJECT_GUIDE.md) · [Return to README](../README.md)

The six accepted Python panels form one argument: a diagnostic comparison at a replaced spectrum, an exact interpretation of physical stabilizer states, a physical size and seed comparison, and a paired measurement-location intervention. The [complete account](../docs/DIALOGUE_REPORT.md) explains the evidence in that order. Start with the [bridge](../docs/TUTORIAL_BRIDGE.md) if the response, boundary code, or distinction between the three comparison designs is unfamiliar.

This gallery connects the question to the canonical artwork, numerical table, plotting script, caption, claim, and method. The caption links identify their authoritative homes; the short explanations here are reading advice. Claim IDs are the M1–M5 entries in the [claim ledger](../results/core_claims.csv), distinct from the dialogue's nine main-question IDs.

<a id="preview"></a>
<a id="figure-1"></a>

## Figure 1: does a difference survive diagnostic spectrum replacement?

Within each family, size, and time cell, eligible states receive shared rank-4 eigenvalues while retaining their own leading Schmidt vectors. Monitoring rate varies. The plotted quantity is the equal-cell mean response at $p=0.24$ minus that at $p=0.08$, separately for the primary and independent-seed runs. All ten plotted estimates and intervals lie below zero in the tested finite families.

The operation modifies the states and is diagnostic. Its current nominal pointwise intervals are support-conditioned and hold archived run-specific references fixed. They are not simultaneous intervals and do not include reference-selection uncertainty. Historical resamples were not recovered.

![Figure 1. Fixed-spectrum response comparison.](core_svg/figure_01_panel_b.svg)

[PDF](core/figure_01_panel_b.pdf) · [canonical table](../data/processed/core_figures/figure_01_panel_b.csv) · [plot script](../scripts/figures/make_figure_01_frozen.py) · [adopted caption](../docs/FIGURE1_CAPTION.md)

Read [M3](../docs/DIALOGUE_REPORT.md#m3) and [reference construction](../docs/DIALOGUE_REPORT.md#b1); check [claim M1](../docs/CLAIM_EVIDENCE_MAP.md) and the [uncertainty method](../docs/FIGURE1_UNCERTAINTY.md).

**Next question:** which unfixed state information sets this response?

<a id="figure-2"></a>

## Figure 2: what do the neighboring cuts explain?

The first panel is exact: the two neighboring entropy increments label nine boundary codes and six response values after removing $D/(D-1)$. The second panel is empirical: at fixed $n=256$ and projective-Z monitoring, it estimates how code probabilities change with monitoring rate after controlling time and central stabilizer spectrum. These states have not undergone spectrum replacement.

The observed redistribution favors lower-response codes in this displayed comparison. Its response-weighted reconstruction of the direct coefficient is an identity, so it is not independent statistical evidence. The exact response rule alone does not predict the redistribution.

![Figure 2, first panel. Exact boundary-code response.](core_svg/figure_02_response_matrix.svg)

![Figure 2, second panel. Conditional boundary-code probability coefficients.](core_svg/figure_02_redistribution_matrix.svg)

[Response PDF](core/figure_02_response_matrix.pdf) · [redistribution PDF](core/figure_02_redistribution_matrix.pdf) · [canonical table](../data/processed/core_figures/figure_02_boundary_codes.csv) · [plot script](../scripts/figures/make_figure_02.py) · [adopted caption](../docs/DIALOGUE_REPORT.md#figure-2-caption)

Read [M4–M5](../docs/DIALOGUE_REPORT.md#m4); check [claim M2](../docs/CLAIM_EVIDENCE_MAP.md), [exact alphabet and reconstruction](../docs/THEORY.md#3-finite-alphabet-theorem), and the [conditional estimator](../docs/NUMERICAL_METHODS.md#6-exact-spectrum-fixed-effect-estimator).

**Next question:** does the physical conditional comparison persist across sizes and new seeds?

<a id="figure-3"></a>

## Figure 3: how far does the physical evidence extend?

At each size and protocol, a fixed-effect regression controls time and complete central stabilizer spectrum while monitoring rate varies over supported observations. The ordinate is the within-spectrum coefficient $\beta_n$ per $\Delta p=0.02$. The figure compares four sizes through $n=256$, two protocols, and disjoint primary and replication seeds. All 16 finite-size estimates and their plotted intervals are negative.

Conditioning on a post-dynamics spectrum does not identify the unconditional causal effect of assigning a monitoring rate. The lines and points at infinity use a locked inverse-size model; their sign is model-dependent evidence, not a thermodynamic theorem. The seed repeat uses the same large-system simulator.

![Figure 3. Conditional monitoring coefficients and model-dependent extrapolations.](core_svg/figure_03_size_scaling.svg)

[PDF](core/figure_03_size_scaling.pdf) · [canonical table](../data/processed/core_figures/figure_03_size_scaling.csv) · [plot script](../scripts/figures/make_figure_03.py) · [adopted caption](../docs/DIALOGUE_REPORT.md#figure-3-caption)

Read [M6–M7](../docs/DIALOGUE_REPORT.md#m6); check [claims M3–M4 and limitation L1](../docs/CLAIM_EVIDENCE_MAP.md), the [fixed-effect estimator](../docs/NUMERICAL_METHODS.md#6-exact-spectrum-fixed-effect-estimator), and [finite-size fit](../docs/NUMERICAL_METHODS.md#7-predeclared-finite-size-model).

**Next question:** what does changing one measurement location do on copies of the same state?

<a id="figure-4"></a>

## Figure 4: where does one spectrum-preserving measurement matter?

Copies of the same premeasurement stabilizer state receive alternative single projective-Z measurements. The earlier circuit history is fixed; the measurement location varies. The first panel shows the measurement-induced change in the averaged fresh-probe response at each distance under the original spectrum-preserving eligibility. The second shows paired near-minus-far contrasts, both without and with that eligibility.

The conditional near-minus-far contrast is negative, and stricter selected-population checks retain near-cut concentration. A single allowed measurement's nonpositive change is an exact corollary; it does not order two locations. The data supply that comparison within the stated populations. No exponential localization length, asymptotic distance law, or strict finite range is established.

![Figure 4, first panel. Spectrum-preserving distance profile without a fitted decay law.](core_svg/figure_04_distance_decay.svg)

![Figure 4, second panel. Paired unconditional and spectrum-preserving location contrasts.](core_svg/figure_04_conditioning_contrast.svg)

[Distance PDF](core/figure_04_distance_decay.pdf) · [contrast PDF](core/figure_04_conditioning_contrast.pdf) · [distance table](../data/processed/core_figures/figure_04_distance_decay.csv) · [contrast table](../data/processed/core_figures/figure_04_conditioning_contrast.csv) · [plot script](../scripts/figures/make_figure_04.py) · [adopted caption](../docs/FIGURE_BASELINE.md#replacement-figure-4-caption)

Read [M8](../docs/DIALOGUE_REPORT.md#m8) and [Appendix F](../docs/DIALOGUE_REPORT.md#f1); check [claim M5, corollary T1, and limitation L2](../docs/CLAIM_EVIDENCE_MAP.md), [pairing and eligibility](../docs/NUMERICAL_METHODS.md#10-paired-measurement-location-intervention), and the [stricter checks](../docs/EVIDENCE_REASSESSMENT.md).

<a id="reproduce"></a>

## Reproduce or inspect an asset

Follow the [reproduction guide](../docs/REPRODUCTION.md) for environment setup, checks, figure redraw, stored-record replay, and uncertainty regeneration. Redrawing canonical tables does not regenerate the underlying statistics or simulations. The [code map](../docs/CODE_MAP.md) identifies the corresponding analysis paths.

The [approved figure baseline](../docs/FIGURE_BASELINE.md) owns version and caption decisions. `core/` contains PDF/PNG outputs; `core_svg/` contains matching SVGs. The [active manifest](../provenance/current_baseline_sha256.json) identifies current output files. The [approved palette](PALETTE.md) stays inside the figures. Editable external composite-schematic sources remain an asset-completion gap, recorded in the [project guide](../docs/PROJECT_GUIDE.md#history-and-readiness); the six accepted panels are available here.

**Next:** [four-figure conclusion](../docs/DIALOGUE_REPORT.md#m9), [claim evidence](../docs/CLAIM_EVIDENCE_MAP.md), or [reproduction](../docs/REPRODUCTION.md). **Return:** [learning route](../docs/PROJECT_GUIDE.md) · [README](../README.md).
