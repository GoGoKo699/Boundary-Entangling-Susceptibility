# Checkpoint 04 physical-stabilizer arm — design lock before full run

Created before launching the full physical-stabilizer simulation and before viewing its full-run results.

## Scientific purpose

Test the fixed-central-spectrum susceptibility effect using only dynamically reachable states, without replacing or truncating Schmidt coefficients.

Uniform two-qubit Clifford dynamics, a product of single-qubit stabilizer states, and projective Pauli measurements preserve the class of pure stabilizer states. Across any bipartition, the nonzero Schmidt coefficients of a pure stabilizer state are exactly flat. Consequently, within fixed `(measurement protocol, n, tau, Schmidt rank)`, the complete central Schmidt spectrum is identical. Comparisons across monitoring rates within these strata are therefore exact full-spectrum matches among physical trajectory states.

## Independent full-run grid

- dynamics: uniformly sampled two-qubit Clifford gates;
- initial states: independently sampled single-qubit stabilizer product states;
- measurement protocols: projective Z and independently sampled projective X/Y/Z;
- sizes: `n = 10, 12, 14`;
- monitoring rates: `p = 0.08, 0.12, 0.16, 0.20, 0.24`;
- probe times: `tau = 6, 8`;
- trajectories per `(protocol,n,p)`: 160;
- discovery trajectories: indices 0--79;
- confirmatory trajectories: indices 80--159;
- independent base seed: `2026082019`;
- finite Clifford probe bank: 12 gates per `(n,tau)`; exact unitary-2-design response is primary.

The earlier 30-trajectory pilot used a different seed and is not pooled with this run.

## Primary analysis

Use confirmatory trajectories only. Let

`stratum = (measurement_protocol, n, tau, log2_schmidt_rank)`.

A stratum is eligible when it contains at least two monitoring-rate levels and at least 8 confirmatory states in total. The primary endpoint is the exact expected normalized linear-entropy response to a fresh uniformly random two-qubit Clifford gate, which equals the Haar U(4) two-copy response.

For each measurement protocol separately, estimate the monitoring-rate coefficient in

`response ~ p_step + C(stratum)`,

where `p_step = (p-0.16)/0.04`. Use a cluster-robust covariance matrix with `trajectory_id` as the cluster. The fixed stratum effects ensure that the full central Schmidt spectrum is exactly identical within every comparison stratum.

The primary sign passes when the upper endpoint of the two-sided 95% confidence interval is below zero for both measurement protocols.

## Confirmatory nonparametric contrast

For each adjacent pair `(0.08,0.12)`, `(0.12,0.16)`, `(0.16,0.20)`, `(0.20,0.24)`, compute mean response differences within exact-spectrum strata supporting both rates, then average strata equally. Obtain trajectory-cluster bootstrap intervals by resampling trajectories within `(protocol,n,p)` cells. Report all adjacent contrasts; monotonicity is supportive but not required for the primary fixed-effect test.

## Mechanism and probe checks

1. Repeat the fixed-stratum regression for `Q_neighbor = P_left + P_right`. At fixed central spectrum, a positive coefficient in `Q_neighbor` is equivalent to a negative Haar/Clifford response coefficient.
2. Repeat for exact locally twirled XX probes at `theta=pi/8` and `theta=pi/4`.
3. Compare the exact Clifford response with the mean of the 12-gate finite Clifford bank and report half-bank reliability.
4. Require central-spectrum flatness error below `1e-10` and Schmidt-rank power-of-two error below `1e-10` for every state.

## Interpretation guardrails

- This is a matched physical-state comparison, not a randomized causal effect of assigned `p` after conditioning on a post-dynamics spectrum.
- It establishes physical reachability of the fixed-spectrum comparison in the tested stabilizer architecture; it does not establish universality over all circuit families.
- No critical point, scaling exponent, or order parameter will be inferred.
- The result is reported independently from the rank-truncated intervention arm.
