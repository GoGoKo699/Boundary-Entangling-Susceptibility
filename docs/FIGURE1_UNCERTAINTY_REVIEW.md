# Figure 1 uncertainty calculation: review candidate

**Date:** 8 September 2026. **Baseline:** `c54dca28464832ecebeb6602c4c490d3d68d3015`.

All ten newly calculated nominal 95% intervals remain below zero. All ten intervals in the prespecified full-confirmatory-pool sensitivity remain below zero as well. The existing figure, canonical plotting table, and main branch have not been replaced. The [candidate table](../results/figure1_uncertainty_review/figure_01_candidate_intervals.csv) is separate from the accepted data.

This is a post-hoc statistical revision, not recovery of the historical RNG seed or an independent circuit campaign. It supplies a fully specified replacement recipe; the missing original bootstrap does not become retrospectively replayable.

## Preserved definition

Keep confirmatory equalized-rank-4 rows, compute `probe_haar_or_clifford_2design_delta_linear_norm/pre_purity`, and compare p=0.24 minus p=0.08. Average the cell contrasts equally within each run and family. Four families use n=10,12,14 and tau=6,8. Clifford uses exactly (10,6), (10,8), (12,8), (14,6), shared between the two runs. The maximum point-estimate discrepancy from the accepted table is 1.11e-16.

The archived run-specific reference spectra are fixed. No discovery/reference resampling, new common-support selection, cross-run pooling, or new Floquet circuit realization is introduced. The accepted point-estimate strings and other non-interval fields are preserved in the candidate CSV.

## Plan and resampling

The [calculation plan](FIGURE1_UNCERTAINTY_PLAN.md) was committed at `fc1f3c56693ebf52e207e5b251758fe3dbd35ca3` before new resampling. Its [machine-readable form](../analysis_plans/figure1_uncertainty_2026-09-08.json) has SHA-256 `5514e46d1ed2bbba54237fb98d5bf7ab7f0da312d6c0f8a22ef1a18c26413d93`. Historical results and support were already known, so this is not public preregistration.

The primary pool is the union of trajectories with at least one eligible retained-time record, following the earlier figure-design cluster construction. Draw N whole trajectories with replacement within each (run,family,n,p) stratum, keeping their time rows and rank-eligibility masks together. Reject an entire joint run/family proposal if any required cell mean is undefined. Never drop a cell, reweight the support, or impute a missing response.

Retain 50,000 valid draws per contrast. The base seed is 2026090801, with explicitly indexed PCG64/SeedSequence streams and batches of 1,000. Endpoints are the 0.025 and 0.975 quantiles using the `linear` convention. Every used trajectory multiplicity, validity flag, selected index and contrast is stored. These are nominal pointwise support-conditioned cluster-percentile intervals, not simultaneous or exact finite-sample coverage guarantees.

## Comparison

| Family | Run | Estimate | Historical 95% interval | New 95% interval |
|---|---|---:|---|---|
| Haar / Z | Primary | -0.257266 | [-0.290035,-0.224650] | [-0.288915,-0.226144] |
| Haar / Z | Independent | -0.207432 | [-0.247495,-0.168210] | [-0.246306,-0.169002] |
| Clifford / Z | Primary | -0.405537 | [-0.554810,-0.254009] | [-0.563577,-0.230949] |
| Clifford / Z | Independent | -0.319248 | [-0.465917,-0.169028] | [-0.457240,-0.187935] |
| Floquet-Cartan / Z | Primary | -0.208081 | [-0.235598,-0.181222] | [-0.235821,-0.181719] |
| Floquet-Cartan / Z | Independent | -0.184778 | [-0.225251,-0.145508] | [-0.219996,-0.150064] |
| Haar / random Pauli | Primary | -0.188156 | [-0.222552,-0.154161] | [-0.217862,-0.158194] |
| Haar / random Pauli | Independent | -0.197692 | [-0.235858,-0.159070] | [-0.235344,-0.160746] |
| Haar / weak Z | Primary | -0.182588 | [-0.203706,-0.161596] | [-0.204179,-0.160761] |
| Haar / weak Z | Independent | -0.178141 | [-0.206932,-0.148811] | [-0.213363,-0.141912] |

The primary Clifford width increases by 10.6%; the independent weak-Z width increases by 22.9%. Other widths change in both directions. These differences must not all be attributed to the seed: the original hybrid interval routine is missing, and the new recipe explicitly fixes the support and undefined-resample rule.

## Sparse support and sensitivity

The accepted analysis uses 1,062 eligible state/time records in 568 eligible trajectory clusters. The high-rate Clifford cells contain only 3,3,3,7 eligible trajectories in the primary run and 3,4,4,3 in the independent run. Repeated times are correlated.

Primary Clifford rejects 1,035/51,035 proposed draws (2.028%); independent Clifford rejects 862/50,862 (1.695%). Their exact support-loss probabilities are 2.048% and 1.700%. No other family had an undefined proposal in the realized calculation. Rejecting incomplete draws is an explicit conditioning step, not a claim that support uncertainty is absent.

The predeclared sensitivity starts from all 600 original confirmatory trajectory clusters, including clusters with no eligible retained row. It uses the same point estimator and complete-support rule. Its Clifford intervals are [-0.571135,-0.222326] and [-0.460978,-0.181013], respectively; rejected fractions are 9.150% and 5.448%. All ten sensitivity intervals remain negative. The five fixed 10,000-draw subsets also retain negative upper endpoints throughout. This is resampling stability, not new physical evidence.

## Verification and archived outputs

The [independent verifier](../scripts/analysis/verify_figure1_uncertainty.py) reconstructs the source matrices itself and imports neither the [sampler](../scripts/analysis/complete_figure1_uncertainty.py) nor its estimator. It checks 1,009,814 proposed vectors and all 1,000,000 accepted contrasts, plus 1,280 explicit duplicated-row expansions. Maximum local disagreement is 2.22e-16.

All 23 tests pass, including ten new method tests. A complete separate local rerun reproduces all 28 numerical output files byte-for-byte. The original 174 baseline files remain unchanged locally.

GitHub Actions run **34192000938**, executing code commit `1c704f4ab98a8626fa72b815d28bf45eb8ac95e7`, passed the complete 50,000-draw primary and sensitivity analyses, the separate replay verifier, all tests, and protected-baseline checks. Its downloaded artifact **10042543425** has SHA-256 `3cc41daaf70e3c920b246f5fedd905af6268b837ba41b8b162642fa1fcc70250`. All 20 resample archives and all five CSVs are byte-identical to the local run; all 560 saved arrays agree exactly. Metadata records the different Python version.

Actions artifacts have finite retention. The author-facing delivery includes the complete saved resamples and six unchanged source members for long-term local archiving. The executable repository recipe always regenerates them from the committed original data; it does not require an expiring artifact as an input.

## Reproduction and adoption boundary

```bash
python scripts/analysis/complete_figure1_uncertainty.py --output reproduced_figure1_uncertainty
python scripts/analysis/verify_figure1_uncertainty.py --output reproduced_figure1_uncertainty --report figure1_review_verification/replay.json
```

Use an empty output directory. All multiplicities, intervals, support counts, rejection diagnostics, and Monte Carlo sub-batches are written there. Neither command replaces an accepted figure or plotting CSV.

The recommendation is to adopt the reproducible primary recipe and new intervals in an explicitly approved Figure 1 revision, preserving the historical table separately and updating the caption's uncertainty definition. This pass does not make that adoption. No new simulation, whole-discovery uncertainty, external replication, universal suppression law, or exact small-sample coverage has been established.
