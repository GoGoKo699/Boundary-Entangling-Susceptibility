# Selected Checkpoint 04 results

These supporting tables are deterministic exports of the included original
records, separate from the canonical Figure 1 panel. The inconsistent earlier
compact exports are preserved, not endorsed, in
[historical/pre_full_sanity_01/](historical/pre_full_sanity_01/README.md).

- [intervention_cross_architecture.csv](intervention_cross_architecture.csv): 30 primary and independent rank-4 endpoint contrasts across five state-generation families and three probes.
- [response_stencil_decomposition.csv](response_stencil_decomposition.csv): all four exact contributions for the 15 primary rank-4 endpoints, using precisely the same estimator and support as the endpoint table.
- [intervention_comparison_support.csv](intervention_comparison_support.csv): every retained run/family/size/time/rate cell, its eligible rows and trajectory counts, equal-cell weight and dimension factor.
- [supporting_records_manifest.json](supporting_records_manifest.json): original compressed-member SHA-256 identities, filtering, estimator, exact coefficients, checks and export hashes.
- [probe_response_coefficients.csv](probe_response_coefficients.csv): gate-ensemble coefficients used by the exact response theorem.

## Endpoint definition and scope

The response is chi2, the normalized linear-entropy change, **without division by
input central purity**. It is not chi_rel from current Figure 1 and not a finite
logarithmic Renyi-2 entropy change. Select `split=confirmatory`,
`variant=equalized_rank4`, and monitoring rates .08 and .24. For each run and
family, retain its own (n,tau) cells with observations at both rates. The point
is the equal-cell average of the high-rate minus low-rate mean response.
Eligibility and reference spectra are fixed at their observed values.

The primary and independent runs therefore need not share the same comparison
support. Figure 1 instead uses a cross-run support intersection and divides by
input purity. The archived directory label `independent_seed_rank4` corresponds
to the consolidated archive's run label `independent_rank4`; the manifest makes
that translation explicit. The 30-row export intentionally excludes the
separate post-hoc rank-two arm; it is not a copy of the 45-row archive table.

The factor D/(D-1), D=2^(n/2), is applied **within each size cell** before pooling.
The decomposition's `delta_P_*` fields are raw equal-cell purity shifts;
`D_weighted_delta_P_*` fields include this factor. Only the latter enter the
pooled normalized-response contributions. The observed and reconstructed totals
agree to 2e-12; small central contributions are floating-point residuals of a
fixed central reference, not central-spectrum changes.

## Archived uncertainty, not newly generated uncertainty

`archived_ci_low`, `archived_ci_high` and `archived_bootstrap_reps` are copied from
the explicitly hashed consolidated archive **only after verifying its matching
point estimate against original rows**. They are retained for historical
supporting context, not presented as the adopted current Figure 1 uncertainty.
No bootstrap has been run by this exporter and no original extension draw
vectors or historical invocation are claimed to have been recovered.

The included older `balanced_bootstrap` source resamples whole trajectories
within size/rate strata, preserving dependence across times. Its 4,000-draw
calculation omits undefined cells within each draw. It does not reject entire
empty-cell proposals as the current Figure 1 procedure does. Thus these are
older post-hoc, nominal pointwise, variable-support percentile diagnostics,
with references and observed eligibility held fixed, not calibrated
simultaneous or unconditional intervals. Bootstrap draws are not new physical
trajectories.

## Reproduction

From the repository root:

```bash
python scripts/analysis/reproduce_supporting_records.py --output reproduced_supporting_records --check
pytest -q tests/test_supporting_exports.py
```

The generator verifies original member hashes, reconstructs every response from
its four purities, checks all 30 points against the consistent archived table,
and binds the four generated exports byte-for-byte. Tests also contract the
original decimal records with exact rational gate-invariant coefficients in a
separate implementation and compare every endpoint with the frozen independent
audit. These checks share original observations and the stated mathematical
identity, not the source simulator or its analysis implementation. They do not
reproduce an additional physical campaign or uncertainty calculation.
