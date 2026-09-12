# Evidence reassessment: distance profile, pairing, and finite-size inference

[Previous: methods](NUMERICAL_METHODS.md) · [Return to README](../README.md) · [Next: reproducibility limits](REPRODUCIBILITY_LIMITS.md)

**Figure status update:** The author has approved removal of the exponential curve and length annotation from the active Figure 4 distance panel. The original data and intervals are unchanged. See [the approved baseline and caption](FIGURE_BASELINE.md). The analysis below records the reassessment that motivated that decision.

**Analysis date:** 2026-09-05. **Basis:** the original Checkpoint 05 archive, SHA-256 `284a92bfac08af6194cd576ce07c4be90e1e760fcc7b0fc7951eaacd1fa975ce`.

This is a post-hoc sensitivity analysis and archived-row replay. It does not replace the locked primary estimands or their original intervals. The numerical circuit simulations were not rerun. New location intervals use 5,000 trajectory-cluster bootstrap draws and seed `2026090501`; size diagnostics reuse the 2,000 archived trajectory bootstraps per size/protocol/run. The subsequent approved artwork revision removes only the fitted curve and its annotation.

## Decisions

Keep the central-spectrum question, exact neighboring-purity mechanism, measured persistence through 256 qubits, independent-seed replication, and paired measurement-location result. Do not promote the fitted `xi=2.37` to an established physical localization length or describe a single exponential as an adequate law for the entire profile. Keep large-size extrapolations explicitly model-dependent. The historical curve remains in earlier source artifacts; the current Figure 4 omits it following author approval.

## 1. What was recovered from the stored observations

All 237,600 primary and replication state rows were read, and their relative response was recalculated from their central and neighboring entropies. The maximum discrepancy was `8.33e-17`. An independently written within-stratum estimator reproduced all 16 finite-size slopes, with maximum discrepancy below `8e-16`. The 75,600 intervention records reproduce the two original near-minus-far point estimates; the original distance means agree to better than `1e-15`.

These checks validate the path from stored observations to the stated point estimates. They do not establish that the original random-circuit generator was free of every possible error, nor do they constitute external replication.

## 2. The pairing rule, stated precisely

In the original conditional analysis, each potential location intervention is first retained only when it preserves the central stabilizer entropy. Eligible sides are averaged within each trajectory and distance. The distance-zero mean is paired with the mean over eligible far distances, `d >= n/4`, when both means exist. Thus the retained side sets can differ between near and far locations.

The new strict comparison fixes a **side** as well as a pre-state, pairs `d=0` with `d=n/4`, and requires both interventions to have `Delta S_m=0`. Eligible side-pair differences are then averaged within each pre-state, followed by equal weighting of the nine `(n,p)` cell means. The bootstrap resamples pre-states, not individual sides.

| Endpoint | Estimate | Fresh pointwise 95% interval | Pre-states |
|---|---:|---:|---:|
| Original unconditional | +0.0714074 | [+0.0655370,+0.0772593] | 5,400 |
| Original unchanged-spectrum | -0.0474290 | [-0.0493916,-0.0454882] | 4,790 |
| Strict same-side, both interventions unchanged | -0.0474737 | [-0.0493378,-0.0454700] | 4,786 |

The strict comparison retains 7,945 side pairs. Every one of its nine cell means has a negative pointwise interval. These new intervals are not replacements for the intervals in the frozen plots: they come from fresh resampling with a new seed.

The causal interpretation is restricted to the specified paired potential interventions and their joint unchanged-spectrum eligibility. It is not an unconditional population effect and is not the effect of assigning the long-run monitoring probability.

## 3. Does changing eligibility manufacture the distance profile?

A stricter post-hoc curve keeps a side/pre-state only when **all six** displayed interventions at `d=0,1,2,4,8,16` preserve the spectrum. Eligibility is fixed before averaging. It retains 6,008 side/pre-state combinations from 4,025 pre-states. The same trajectory is resampled jointly across all distances within each cell.

| Distance | Common-eligibility response | Fresh pointwise 95% interval |
|---:|---:|---:|
| 0 | -0.054862 | [-0.057248,-0.052457] |
| 1 | -0.048977 | [-0.052155,-0.045762] |
| 2 | -0.022101 | [-0.024490,-0.019751] |
| 4 | -0.006556 | [-0.007927,-0.005246] |
| 8 | -0.000904 | [-0.001385,-0.000486] |
| 16 | -0.000281 | [-0.000585,-0.000052] |

At four sites the mean magnitude is **11.95%** of its adjacent-cut value, with a percentile interval of **9.54%-14.52%**. At eight sites it is **1.65%**, interval **0.89%-2.51%**. These are ratios of pooled means, calculated jointly from the bootstrap curves, not averages of per-trajectory ratios.

This supports a rapidly attenuating, near-cut-concentrated response without assuming an exponential. It does not establish a hard finite range. The simultaneous six-distance bootstrap band crosses zero at `d=16` for the common-eligibility curve, although its pointwise interval is negative. Sparse far-distance nonzero events and the altered selected population limit tail interpretation.

## 4. Why the exponential is not the main conclusion

The archived source fits `-A exp(-d/xi)` by unweighted nonlinear least squares and bootstraps its fitted parameters. A narrow interval for a fitted parameter does not test the model's adequacy.

For the archived curve, all six predictions of the frozen fit fall outside the corresponding pointwise intervals. This is a diagnostic, not six independent hypothesis tests. A covariance-aware fit gives `xi=2.0455` and quadratic residual `Q=140.59`, with four nominal residual dimensions. On the common-eligibility curve the corresponding values are `xi=2.0657` and `Q=94.45`. No exact chi-square p-value is assigned: the covariance is estimated, the model is nonlinear, and the tail is sparse.

Changing eligibility therefore does not resolve the full-profile mismatch. The problem is also present in multiple individual cells at short distances, rather than appearing only after pooling different cells. Fits to different distance windows give different descriptive scales. These exploratory fits are all reported, not used to select a replacement headline model.

**Adopted Figure 4 revision:** retain the observed means and their original intervals; remove the exponential curve and `xi` annotation from the main artwork. Do not add another fitted function. A caption can state that the response is concentrated near the cut and decreases strongly with measurement distance. The historical fitted parameter and its diagnostics belong in this document, not in the physical claim. The replacement Python PDF is available; the external Overleaf project must use that replacement and the updated caption.

## 5. Finite sizes versus a limiting coefficient

The four original locked `1/n` extrapolations and their original intervals are reproduced from the archived size-level bootstrap arrays. Their diagonal quadratic residual diagnostics are:

| Run | Protocol | Q | Nominal residual dimension |
|---|---|---:|---:|
| Primary | Projective Z | 5.21 | 2 |
| Primary | Random Pauli | 16.78 | 2 |
| Replication | Projective Z | 0.74 | 2 |
| Replication | Random Pauli | 1.58 | 2 |

The primary random-Pauli series is not closely described by the locked line relative to its recorded errors. Resampling trajectory noise does not automatically include uncertainty about the finite-size model.

A transparent, post-hoc menu uses correction powers `0.5,1,1.5,2` over all sizes and four leave-one-size-out `1/n` fits. All 32 sensitivity intervals, and the four locked intervals, remain below zero. Across this finite menu the point intercepts range from about `-0.0665` to `-0.0445`. This range is **not** a confidence interval and the menu is not exhaustive. It supports stability of the negative extrapolated sign under the checked alternatives, not proof of a thermodynamic limit.

Furthermore, `beta_n` is an overlap-weighted within-spectrum regression coefficient. At `n=256`, no one central-entropy stratum spans the entire monitoring grid. Its support and weighting can change with size. The directly observed finite-size coefficients should carry the main conclusion; the limit remains conditional on the estimand and extrapolation assumptions.

## 6. Observable terminology

Write the existing observable explicitly:

$$
\chi_{\mathrm{rel}}=\frac{D}{D-1}\left(1-\frac{\mathbb E_U P'_m}{P_m}\right),\qquad D=2^{n/2}.
$$

It is a purity-normalized linear-entropy response. It is not generally the mean finite-gate change of `-log2(P_m)`. The symbol and numerical definition are unchanged; `D` in this note avoids confusing the half-chain dimension with measurement distance `d`.

## Reproduce this analysis

Install the repository dependencies, use the in-repository data bundle, and run from the repository root:

```bash
python scripts/analysis/reassess_evidence.py \
  --output reproduced_evidence --bootstrap 5000 --seed 2026090501
```

The script verifies the full ZIP hash before reading it and records hashes of every member used. It imports no original checkpoint estimator code. It writes the fresh paired intervals, cell profiles, common-eligibility curve, covariance and window diagnostics, independently reconstructed finite-size coefficients, and fixed-menu extrapolation checks. Full raw circuit generation and a fresh full finite-size bootstrap campaign are outside this pass.

The text results are in [`../results/evidence_reassessment/`](../results/evidence_reassessment/). The new bootstrap arrays are reproducible outputs, not frozen primary data. The original records are bundled as described in [`DATA_POLICY.md`](DATA_POLICY.md).

[Next: reproducibility limits](REPRODUCIBILITY_LIMITS.md) · [Return to README](../README.md)
