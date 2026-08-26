# Results at a glance

This page collects the load-bearing numerical values behind the four-step repository story. Exact identities are separated from finite-sample estimates and extrapolations.

## 1. Fixed-spectrum intervention

After replacing the central Schmidt eigenvalues by a common rank-4 spectrum while retaining the original Schmidt vectors, the endpoint contrast

\[
\Delta\chi_{\mathrm{rel}}
=\chi_{\mathrm{rel}}(p=0.24)-\chi_{\mathrm{rel}}(p=0.08)
\]

is negative in all five tested state-generation families, in both the held-out primary analysis and the independent-seed run.

| Family | Primary | Independent seed |
|---|---:|---:|
| Haar / projective Z | -0.2573 | -0.2074 |
| Clifford / projective Z | -0.4055 | -0.3192 |
| Floquet-Cartan / projective Z | -0.2081 | -0.1848 |
| Haar / random Pauli | -0.1882 | -0.1977 |
| Haar / weak Z | -0.1826 | -0.1781 |

All ten 95% trajectory-cluster bootstrap intervals lie below zero. The exact plotted rows are in `data/processed/core_figures/figure_01_panel_b.csv`.

## 2. Exact boundary response

For a Haar-random or uniformly random two-qubit Clifford probe,

\[
\chi_{\mathrm{rel}}
=\frac{d}{d-1}
\left[
1-\frac{2}{5}\frac{P_{m-1}+P_{m+1}}{P_m}
\right].
\]

For stabilizer states this becomes

\[
\frac{\chi_{\mathrm{rel}}}{d/(d-1)}
=1-\frac{2}{5}\left(2^{\delta_L}+2^{\delta_R}\right),
\qquad
\delta_{L,R}\in\{-1,0,1\}.
\]

At `n=256`, the measured redistribution of the nine boundary codes reconstructs the direct fixed-spectrum monitoring coefficient

\[
\beta_{256}=-0.0521300364
\]

to floating-point precision. The complete nine-row decomposition is in `data/processed/core_figures/figure_02_boundary_codes.csv`.

## 3. Physical large-size persistence

For naturally generated monitored stabilizer states, matching within fixed `(n, tau, S_m)` strata fixes the complete central Schmidt spectrum without modifying the states.

The projective-Z primary estimates per monitoring increase `Delta p=0.02` are

| n | beta_n |
|---:|---:|
| 32 | -0.02924 |
| 64 | -0.03872 |
| 128 | -0.04482 |
| 256 | -0.05213 |

The locked `1/n` extrapolations are:

| Monitoring | Run | beta_infinity | 95% interval |
|---|---|---:|---:|
| Projective Z | Primary | -0.05176 | [-0.05453, -0.04890] |
| Projective Z | Independent | -0.04916 | [-0.05340, -0.04467] |
| Random Pauli | Primary | -0.05319 | [-0.05586, -0.05050] |
| Random Pauli | Independent | -0.05197 | [-0.05653, -0.04736] |

These values support, but do not prove, a nonzero thermodynamic response. No universal finite-size correction exponent is claimed.

## 4. Paired measurement-location intervention

Copies of the same premeasurement stabilizer state receive one projective-Z measurement at different distances from the central cut. On the branch with `Delta S_m=0`, the complete central spectrum is unchanged.

The conditional response change is

| Distance d | Delta chi_rel(d) |
|---:|---:|
| 0 | -0.04751 |
| 1 | -0.04371 |
| 2 | -0.01846 |
| 4 | -0.00540 |
| 8 | -0.00111 |
| 16 | -0.00028 |

A zero-asymptote exponential fit gives

\[
\xi=2.372\quad[2.251,2.496]
\]

sites. The paired near-minus-far contrast is

\[
+0.0714\quad\text{unconditionally},
\qquad
-0.0474\quad\text{when the central spectrum is unchanged}.
\]

The sign reversal separates central-rank headroom from the spatial-embedding effect.

## Evidential status

- The response identities and stabilizer boundary alphabet are exact.
- The intervention, boundary-code redistribution, size dependence, and localization are numerical.
- The thermodynamic value is an extrapolation.
- Causality applies to the paired assignment of measurement location on the same pre-state, conditional on the unchanged-spectrum branch.
- The susceptibility is not claimed to be an order parameter.
