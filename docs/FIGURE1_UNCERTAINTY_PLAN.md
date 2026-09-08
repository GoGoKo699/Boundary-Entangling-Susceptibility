# Figure 1 uncertainty review: calculation plan

> Historical review/design record. The author subsequently adopted the primary recipe on 8 September 2026. See [the current procedure](FIGURE1_UNCERTAINTY.md); statements below about pending adoption describe the earlier review stage.

Baseline: `c54dca28464832ecebeb6602c4c490d3d68d3015`. This is a new post-hoc uncertainty calculation on existing data, not recovery of the missing historical bootstrap and not an independent simulation. Historical results and eligibility counts have been inspected; no new bootstrap results were computed before this lock. It is an internal prospective calculation record, not public preregistration.

The complete machine-readable plan was frozen locally at `2026-09-08T05:36:35.356216+00:00`, SHA-256 `5514e46d1ed2bbba54237fb98d5bf7ab7f0da312d6c0f8a22ef1a18c26413d93`, and will be included with the implementation. The statistical procedure is specified below.

## Estimand and data

Use `state_response_rows.csv.gz` from `checkpoint_04/data/intervention/primary_rank4/` and `independent_seed_rank4/` in the repository record bundle. Keep `split=confirmatory`, `variant=equalized_rank4`, and monitoring probabilities 0.08 and 0.24. Reconstruct the response as `probe_haar_or_clifford_2design_delta_linear_norm/pre_purity`.

In each run and family separately, average the high-minus-low cell means equally over the fixed common support. The family order is Haar/Z, Clifford/Z, Floquet-Cartan/Z, Haar/random Pauli, Haar/weak Z. Support is n=10,12,14 and tau=6,8, except Clifford uses exactly (10,6), (10,8), (12,8), (14,6), shared between the runs. Never estimate a new support set from a bootstrap sample. Verify all ten point estimates against the accepted table before comparing intervals.

The archived target spectra remain fixed, including their differences between runs. These intervals condition on those references, observed support, and any fixed circuit realization; they do not include uncertainty from rebuilding discovery references or selecting a new support. Do not pool the two runs.

## Primary bootstrap

Resample whole trajectory clusters within each (run,family,n,p) stratum. The primary pool is the union of trajectories with at least one eligible row on the retained support. This follows the pool construction in the historical figure-design bootstrap. Retain time rows and eligibility masks together. A missing equalized row is structural rank ineligibility, not a numerical zero.

Draw exactly the original pool size with replacement within each stratum. If ANY required cell mean is undefined in a proposed joint run/family replicate, reject that entire replicate and propose another. Never drop cells, change their weights, or fill missing responses. Record the rejection count and its exact support-survival probability. This is explicitly a support-conditioned cluster bootstrap; it is not an unconditional repeated-study confidence procedure.

Retain 50,000 valid replicates for every run/family. Use NumPy Generator(PCG64(SeedSequence([2026090801,pool_index,run_index,family_index]))). Orders: pools [eligible_union,all_confirmatory], runs [primary,independent], and the family order above. Within each replicate, strata are ordered by increasing n and then p; trajectories are sorted by trajectory_index; times are increasing. Generate blocks of 1,000 proposals, taking the first 50,000 valid proposals, with a hard cap of 1,000,000 proposals. Save all used multiplicity matrices and validity masks, as well as the retained bootstrap contrasts.

Report percentile endpoints 0.025 and 0.975 using NumPy quantile method `linear`. These are nominal pointwise intervals, not simultaneous intervals or exact finite-sample coverage guarantees. No p-values are inferred from the fraction of negative bootstrap draws.

## One prespecified sensitivity

Repeat the same estimator, fixed support, rejection rule, and 50,000-draw calculation using ALL confirmatory trajectories in each (run,family,n,p) pool, including those with no eligible retained row. Use pool_index=1. This tests the effect of conditioning the primary pool on observed eligibility; it still conditions on survival of every required cell and on fixed references/support. Do not choose the preferred method by its sign or closeness to the old intervals.

## Reporting and checks

Report all ten historical/new comparisons, widths, per-cell sample counts, trajectory counts, eligibility patterns, and rejection rates. Use five consecutive 10,000-draw subsets only as Monte Carlo stability diagnostics, not additional experiments. Save enough source data and multiplicities to replay the new intervals without regenerating random numbers. Independently check weighted and explicit duplicated-row calculations.

The success criterion is a reproducible and honest calculation, not that every interval must stay negative. Report any sign change. Small Clifford samples and uncertainty not captured by the conditional procedure remain limitations even after increasing the bootstrap count.

The accepted figures, five canonical CSVs, all other results, and main remain unchanged until review. Do not tune a seed to reproduce the historical error bars, relabel different resamples as original, start a simulation campaign, or include the separate channel project.
