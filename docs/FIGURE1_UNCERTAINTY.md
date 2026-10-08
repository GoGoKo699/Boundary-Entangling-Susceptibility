<a id="figure-1-adopted-uncertainty-calculation"></a>

# Figure 1: uncertainty calculation

## Definition

The endpoint is the equal-cell average of the response at p=0.24 minus the response at p=0.08. Analysis is separate by run and family. The primary pool is `eligible_union`: within each size/rate stratum, retain trajectories with at least one eligible row on the fixed comparison support. Resample whole trajectories, keeping their two probe times and rank-eligibility masks together. Reject an entire proposed contrast if any required cell is empty. Do not drop cells or impute responses.

Keep the first 50,000 valid draws. The seed is 2026090801 with PCG64 and the per-pool/run/family SeedSequence specified in the [machine-readable plan](../analysis_plans/figure1_uncertainty_2026-09-08.json). Endpoints are the 0.025 and 0.975 quantiles using linear interpolation. The primary pool was chosen before calculation, not selected by its interval width or sign. The all-confirmatory-pool sensitivity is retained but does not define the plotted bars.

The original reference spectra and observed cross-run support are fixed. These are nominal pointwise, support-conditioned percentile intervals. They do not provide simultaneous or exact finite-sample coverage, nor do they include uncertainty in estimating discovery references or selecting support. High-rate Clifford cells contain only 3–7 eligible trajectories. More bootstrap draws do not create additional physical data. This is a post-hoc statistical revision, not recovery of the historical seed or an independent simulation.

## Reproduce from the included original records

Use an empty output directory:

```bash
python scripts/analysis/complete_figure1_uncertainty.py --output reproduced_figure1_uncertainty
python scripts/analysis/verify_figure1_uncertainty.py --output reproduced_figure1_uncertainty --report figure1_review_verification/independent_replay.json
python scripts/analysis/check_figure1_adoption.py --resamples reproduced_figure1_uncertainty
```

The sampler saves every used proposal's multiplicities, validity flag, and retained contrast. The separately written verifier reconstructs the estimates from the source rows without importing the sampler or using its RNG. The adoption check binds those verified outputs to the current plotting table and expected hashes. CI performs all three steps and uploads the complete resample output. All inputs needed to regenerate the resamples are included in the checkout.

The small permanent tables and expected resample hashes are in [results/figure1_uncertainty](../results/figure1_uncertainty/). The sampler's `ANALYSIS_STATUS.json` retains its historical `new_intervals_adopted: false` field because the sampler never changes the repository. Current adoption status is recorded separately in [provenance/FIGURE1_ADOPTION_2026-09-08.json](../provenance/FIGURE1_ADOPTION_2026-09-08.json).

<a id="historical-record-and-presentation"></a>

## Source records

All ten plotted intervals remain below zero. The [historical comparison report](FIGURE1_UNCERTAINTY_REVIEW.md) records the differences from superseded intervals; [reproducibility limits](REPRODUCIBILITY_LIMITS.md#historical-figure-1) explains their separate provenance. Use the [Figure 1 caption](FIGURE1_CAPTION.md) with the current panel.
