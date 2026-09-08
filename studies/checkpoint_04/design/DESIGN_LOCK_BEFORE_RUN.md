# Checkpoint 04 design lock — cross-architecture and physical-reachability audit

Created before the Checkpoint 04 simulation and before viewing its results.

## Scientific questions

1. Does the fixed-central-spectrum reduction in entangling susceptibility survive structurally different monitored dynamics?
2. Does it survive different measurement protocols?
3. Is the conclusion specific to a Haar probe, or does it persist for other locally dressed entanglers?
4. Can a related effect be recovered by matching only physically generated states with nearby full central Schmidt spectra?

## Model families

All models are open one-dimensional qubit chains initialized in random product states. One circuit cycle contains both brickwork sublayers, followed by independent site monitoring with assigned rate `p`.

1. `haar_z`: fresh Haar U(4) gates; projective Z monitoring.
2. `clifford_z`: fresh uniformly sampled two-qubit Clifford gates; projective Z monitoring.
3. `floquet_cartan_z`: a fixed, generic, locally dressed Cartan brickwork layer repeated in time; projective Z monitoring.
4. `haar_random_pauli`: fresh Haar U(4) gates; projective measurements in independently sampled X, Y, or Z bases.
5. `haar_weak_z_eta06`: fresh Haar U(4) gates; selected sites undergo a two-outcome unsharp Z measurement of strength eta=0.6.

The two brickwork sublayer orders alternate deterministically between cycles to remove a fixed last-sublayer bias.

## Numerical grid

- sizes: n = 10, 12, 14;
- monitoring rates: p = 0.08, 0.16, 0.24;
- probe times: tau = 6, 8 circuit cycles per site;
- trajectories per `(family,n,p)`: 24;
- discovery trajectories: indices 0--11;
- confirmatory trajectories: indices 12--23;
- spectrum intervention: rank-4 central spectrum equalization;
- equalization target: discovery-pooled within each `(family,n,tau)` and never computed from confirmatory states.

## Probe ensembles

The primary endpoint is the exact expected normalized linear-entropy change under a fresh Haar U(4) gate at the central bond. A uniformly sampled two-qubit Clifford probe has the same endpoint because the Clifford group is a unitary 2-design.

Two non-Haar locally dressed fixed-entangler probes are also tested through their exact two-copy response operators:

- `cartan_xy_pi8`: exp[-i pi/8 (XX+YY)] with independent local Haar input dressing;
- `cartan_xx_pi4`: exp[-i pi/4 XX] with independent local Haar input dressing.

No finite gate bank is used for these linear-entropy endpoints.

## Primary intervention test

For each family and probe, use only confirmatory rank-4 equalized states. Compute the equal-cell contrast

`mean(response | p=0.24) - mean(response | p=0.08)`,

first within every `(n,tau)` cell and then average the six cell contrasts equally. Confidence intervals use a trajectory-cluster bootstrap resampled independently within `(family,n,p)` cells.

The sign is called architecture-robust only if it is negative in all three tested sizes for each of `haar_z`, `clifford_z`, and `floquet_cartan_z`. Measurement-protocol robustness requires a negative pooled contrast for `haar_z`, `haar_random_pauli`, and `haar_weak_z_eta06`; weak monitoring is reported separately if its effect is statistically unresolved.

## Physical-state matching arm

Within every `(family,n,tau)`, confirmatory physical states are matched without replacement between monitoring rates using the Hungarian algorithm and full-spectrum Hellinger distance. Both extreme (`0.08` versus `0.24`) and adjacent rate pairs are reported.

A strict-support subset is defined before analysis by

- Hellinger distance <= 0.12;
- absolute central-purity difference <= 0.03.

The physical arm is considered a clean replication only if the strict-support total-response contrast is negative with a confidence interval below zero. A negative neighboring-profile contribution without a negative total response is reported as partial mechanistic support, not replication.

## General response-operator theorem

For an arbitrary two-qubit probe ensemble E, define

Omega_E = E_U[ U^{dagger tensor 2} F_a U^{tensor 2} ].

The expected post-gate purity is the expectation of `F_L tensor Omega_E` in two copies of the pre-gate state. For locally input-dressed fixed entanglers, local twirling projects Omega onto the four-dimensional basis `{I, F_a, F_b, F_a F_b}`. The resulting four-stencil formula and coefficients are derived independently of the simulation and validated numerically.

## Interpretation guardrails

- No transition point or scaling exponent will be inferred from this grid.
- A negative fixed-spectrum trend is not called universal unless it survives every predeclared architecture arm.
- Physical matching is not treated as exact intervention.
- The old cumulative cancellation ratio remains rejected and is not recomputed.
