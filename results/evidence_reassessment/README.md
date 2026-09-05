# Archived-row replay and post-hoc evidence checks

Read [`../../docs/EVIDENCE_REASSESSMENT.md`](../../docs/EVIDENCE_REASSESSMENT.md) for definitions and conclusions. These are new sensitivity analyses, not a relabeling of the original primary endpoint or its confidence intervals.

| File | Meaning |
|---|---|
| `summary.json` | Actual replay counts, discrepancies, seed, and computation environment |
| `input_manifest.json` | SHA-256 identities of the eleven original archive members read |
| `paired_endpoint_bootstraps.csv` | Fresh trajectory-cluster intervals for original and strict same-side paired endpoints |
| `common_profile.csv` | Common-eligibility distance means, pointwise intervals, and simultaneous bands |
| `common_relative_magnitude.csv` | Jointly bootstrapped ratios of pooled means relative to d=0 |
| `frozen_distance_fit_residuals.csv` | Historical fit predictions compared with original means and intervals |
| `distance_fit_sensitivity.csv` | All reported windows and weighting schemes; not a best-model search |
| `common_cell_fit_diagnostics.csv` | Covariance-aware short-distance diagnostics for each common-eligibility cell |
| `finite_size_replay.csv` | Recalculated finite-size coefficients compared with the original values |
| `finite_size_model_sensitivity.csv` | Four locked fits plus 32 fixed-menu model/size sensitivities |

The archive-based script regenerates these and additional per-cell/profile tables, along with `new_location_bootstraps.npz`. New location intervals use 5,000 resamples with seed 2026090501. Size intervals in this reassessment reuse archived trajectory bootstraps. A model residual statistic is a descriptive diagnostic here, not an exact calibrated p-value.

Canonical inputs in `data/processed/core_figures/` and the accepted manuscript panels are unchanged. Permanent access to the full original raw archive is still pending; this directory is not a replacement for that data deposit.
