# Results at a glance

**Role: numerical lookup after the scientific account.** The canonical tables linked below own the numerical values. Read the [four-figure account](DIALOGUE_REPORT.md) for the comparisons and the [claim map](CLAIM_EVIDENCE_MAP.md) for their scope. [Return to README](../README.md).

The point estimates and Figures 2–4 retain their original numerical inputs. Figure 1 uses the [adopted support-conditioned uncertainty calculation](FIGURE1_UNCERTAINTY.md); its historical error bars are not the current ones. The [evidence reassessment](EVIDENCE_REASSESSMENT.md) adds post-hoc checks and revises the interpretation of the historical exponential curve, not the archived observations.

## Fixed-spectrum intervention

The endpoint is the relative-response contrast between monitoring probabilities 0.24 and 0.08 after imposing the same rank-4 reference spectrum.

| Family | Primary | Independent seed |
|---|---:|---:|
| Haar / projective Z | -0.2573 | -0.2074 |
| Clifford / projective Z | -0.4055 | -0.3192 |
| Floquet-Cartan / projective Z | -0.2081 | -0.1848 |
| Haar / random Pauli | -0.1882 | -0.1977 |
| Haar / weak Z | -0.1826 | -0.1781 |

All ten current nominal pointwise 95% support-conditioned intervals lie below zero. Source: [`../data/processed/core_figures/figure_01_panel_b.csv`](../data/processed/core_figures/figure_01_panel_b.csv).

## Exact mechanism

$$
\chi_{\mathrm{rel}}=\frac{D}{D-1}\left[1-\frac25\frac{P_{m-1}+P_{m+1}}{P_m}\right],\qquad D=2^{n/2}.
$$

The stabilizer boundary alphabet makes its ensemble mean a response-weighted boundary-code distribution. The representative n=256 reconstruction yields -0.0521300364. See [theory](THEORY.md).

## Physical large-size coefficients

All sixteen finite-size coefficients and their archived intervals are negative. The four locked inverse-size extrapolations are:

| Monitoring | Run | Intercept | Archived 95% interval |
|---|---|---:|---|
| Projective Z | Primary | -0.05176 | [-0.05453,-0.04890] |
| Projective Z | Independent | -0.04916 | [-0.05340,-0.04467] |
| Random Pauli | Primary | -0.05319 | [-0.05586,-0.05050] |
| Random Pauli | Independent | -0.05197 | [-0.05653,-0.04736] |

These are model-dependent extrapolations, not directly observed thermodynamic values. A post-hoc menu of 32 alternatives retains negative intervals, but model residuals and support changes limit precision. See [finite-size replay](../results/evidence_reassessment/finite_size_replay.csv) and [model sensitivity](../results/evidence_reassessment/finite_size_model_sensitivity.csv).

## Paired location intervention

The nonpositive change from each spectrum-preserving Pauli measurement is an exact stabilizer corollary for the averaged probe. It does not determine the sign of the near-minus-far difference below. The [theory](THEORY.md#5-one-measurement-corollary) states the assumptions and deduction.

The original near-minus-far estimates are +0.0714074 unconditionally and -0.0474290 on the unchanged-spectrum branch. The post-hoc strict same-side endpoint is -0.0474737 with a fresh 95% interval [-0.0493378,-0.0454700]. Every strict cell has a negative pointwise interval.

The common-eligibility curve uses 4,025 pre-states and keeps the selected sides fixed across six distances. Its magnitude at four sites is about 12% of the adjacent-cut magnitude; at eight sites it is about 1.6%. These are measured attenuation ratios, not a fitted correlation length.

The current Figure 4 has no exponential curve or length annotation. The historical value xi=2.372 [2.251,2.496] is preserved only as fit provenance in [the archived fit record](../results/historical_fit/figure_04_distance_fit.json), not as an endorsed physical localization length: residual checks reject its use as an adequate full-profile description. No replacement functional form is promoted. Read the [precise estimands and fit diagnostics](EVIDENCE_REASSESSMENT.md) before interpreting Figure 4.

[Next: claim-level evidence and limitations](CLAIM_EVIDENCE_MAP.md) · [Return to README](../README.md)
