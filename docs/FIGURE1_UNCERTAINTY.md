# Figure 1: adopted uncertainty calculation

The author approved the primary uncertainty recipe and revised intervals on 8 September 2026 after reviewing their comparison with the historical intervals. Only Figure 1 error bars change. All point estimates, metadata, common comparison support, plotting code and visual design are unchanged. Figures 2–4 are unchanged.

## Definition

The endpoint is the equal-cell average of the response at p=0.24 minus the response at p=0.08. Analysis is separate by run and family. The primary pool is `eligible_union`: within each size/rate stratum, retain trajectories with at least one eligible row on the fixed comparison support. Resample whole trajectories, keeping their two probe times and rank-eligibility masks together. Reject an entire proposed contrast if any required cell is empty. Do not drop cells or impute responses.

Keep the first 50,000 valid draws. The seed is 2026090801 with PCG64 and the per-pool/run/family SeedSequence specified in the unchanged [machine-readable plan](../analysis_plans/figure1_uncertainty_2026-09-08.json). Endpoints are the 0.025 and 0.975 quantiles using linear interpolation. The primary pool was chosen before calculation, not selected by its interval width or sign. The all-confirmatory-pool sensitivity is retained but does not define the plotted bars.

The original reference spectra and observed cross-run support are fixed. These are nominal pointwise, support-conditioned percentile intervals. They do not provide simultaneous or exact finite-sample coverage, nor do they include uncertainty in estimating discovery references or selecting support. High-rate Clifford cells contain only 3–7 eligible trajectories. More bootstrap draws do not create additional physical data. This is a post-hoc statistical revision, not recovery of the historical seed or an independent simulation.

## Reproduce from the included original records

Use an empty output directory:

```bash
python scripts/analysis/complete_figure1_uncertainty.py --output reproduced_figure1_uncertainty
python scripts/analysis/verify_figure1_uncertainty.py --output reproduced_figure1_uncertainty --report figure1_review_verification/independent_replay.json
python scripts/analysis/check_figure1_adoption.py --resamples reproduced_figure1_uncertainty
```

The unchanged sampler saves every used proposal's multiplicities, validity flag, and retained contrast. The separately written verifier reconstructs the estimates from the source rows without importing the sampler or using its RNG. The adoption check binds those verified outputs to the current plotting table and expected hashes. CI performs all three steps and uploads the complete resample output. The resamples remain regenerable after temporary CI artifacts expire; no old chat, external research repository, or historical checkpoint ZIP is required.

The small permanent tables and expected resample hashes are in [results/figure1_uncertainty](../results/figure1_uncertainty/). The sampler's `ANALYSIS_STATUS.json` retains its historical `new_intervals_adopted: false` field because the sampler never changes the repository. Current adoption status is recorded separately in [provenance/FIGURE1_ADOPTION_2026-09-08.json](../provenance/FIGURE1_ADOPTION_2026-09-08.json).

## Historical record and presentation

The superseded table and all three former panel formats are preserved byte-for-byte in [results/historical_figure1](../results/historical_figure1/). Its missing original bootstrap seed is not retroactively recovered. The original record bundle and the locked analysis plan remain untouched. The pre-adoption [comparison report](FIGURE1_UNCERTAINTY_REVIEW.md) is retained with its historical review status clearly labeled.

All ten revised intervals remain below zero. The primary Clifford interval is about 10.6% wider and the independent weak-Z interval about 22.9% wider than their historical counterparts; differences are not attributed solely to random-seed changes because the full historical recipe was unavailable. No interval was tuned to reproduce the old values.

For Overleaf, replace only `Graph/figure_01_panel_b.pdf` and update the uncertainty description using [the Figure 1 caption](FIGURE1_CAPTION.md). This repository does not edit the external Overleaf project. No figure insertion or layout change is needed.
