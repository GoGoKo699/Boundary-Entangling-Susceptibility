# Checkpoint 05 primary scaling design lock

This file was frozen after the explicitly labeled calibration runs and before
any primary-run trajectory was generated.

## Calibration-only information used

The coarse and dense calibration runs used disjoint seeds and only the
projective-Z architecture. The standard quarter-partition tripartite mutual
information gave the cleanest 64-versus-128 crossing between p=0.26 and 0.27,
with linear interpolation near p=0.263. The late-time half-chain entropy showed
no systematic drift between tau=6 and tau=8 at the resolution of the
calibration.

Calibration data will not enter primary confidence intervals or finite-size
fits.

## Primary physical question

At exactly fixed complete central Schmidt spectrum, does the monitoring-rate
change of the *relative* boundary entangling susceptibility remain nonzero as
system size increases?

For stabilizer states, fixing the central entropy S_m fixes the full flat
Schmidt spectrum. Define

    chi_rel = chi_2 / P_m
            = [d/(d-1)] [1 - (2/5)(2^(S_m-S_{m-1}) + 2^(S_m-S_{m+1}))].

The relative response is primary because it removes the trivial multiplicative
purity scale P_m that can vanish when the matched central rank grows with n.
The unnormalized chi_2 remains a prespecified secondary outcome.

## Primary simulation

- open chain;
- random single-qubit stabilizer product initial states;
- fresh uniformly sampled two-qubit Clifford gates in both brickwork
  sublayers of every cycle;
- monitoring after each complete two-sublayer cycle;
- protocols: projective Z (primary) and independently random Pauli
  (prespecified ensemble replication);
- sizes n = 32, 64, 128, 256;
- p grid = 0.20, 0.22, 0.24, 0.25, 0.26, 0.27, 0.28, 0.30, 0.34;
- 800 trajectories per (protocol,n,p) cell;
- post-measurement probe times tau = 6, 8, 10, where cycle = tau*n;
- primary base seed 2026082301.

## Exact-spectrum fixed-effect estimand

For each protocol and size separately, use rows from all three probe times and
strata (tau,S_m). A stratum is eligible when at least three p levels each have
at least ten trajectory rows. Fit

    y_i = alpha_(tau,S_m) + beta_n * ((p_i-0.26)/0.02) + error_i.

The primary outcome y is chi_rel. The secondary outcome is chi_2. The
coefficient beta_n is the response change per Delta p=0.02 after exact full-
spectrum stratification. Uncertainty is clustered by trajectory and checked by
a trajectory bootstrap within each (n,p) cell.

## Predeclared thermodynamic model

The only primary finite-size model is

    beta_n = beta_infinity + a/n.

The exponent is not fitted. beta_infinity and its interval are obtained by
weighted least squares and a bootstrap that propagates the trajectory-level
uncertainty of every beta_n. Exponential and free-exponent fits may be shown
only as sensitivity analyses and cannot replace the primary model.

Primary success requires the projective-Z beta_infinity interval to exclude
zero. Random-Pauli results are replication, not a second opportunity to rescue
a failed primary result.

## Independent transition estimate

The transition is estimated only from the standard quarter-partition
tripartite mutual information I3 at tau=10. Pairwise size crossings and their
bootstrap intervals are reported. The new susceptibility is not used to locate
p_c.

The susceptibility may be called transition-sensitive only if its fixed-
spectrum adjacent-p contrasts show a reproducible feature near the independently
estimated p_c. It will not be called an order parameter without distinct
thermodynamic limits in the two phases.

## Boundary-window analysis

Nested window entropy features use half-widths h=1,2,4,8,16,32,64,128, capped
at n/2. This is explicitly a test of entropy summaries of bounded windows, not
of the complete reduced density matrix. The first 400 trajectories per cell
are training data and the last 400 are test data. Prediction of the two-integer
boundary code (S_m-S_{m-1}, S_m-S_{m+1}) is evaluated out of sample. No claim
of full boundary locality will be made from these summaries alone.

## Paired measurement-location intervention

A separate, independently seeded run will use n=64,128,256 and p=0.20,0.26,0.34.
At tau=10, one projective Z measurement is applied counterfactually at equal
measurement count and paired pre-state, at distances d=0,1,2,4,8,16,32,64 on
both sides where available. The primary causal endpoint is the change in
chi_rel among interventions that leave S_m unchanged. Near-cut versus far
(distance at least n/4) effects are compared by trajectory bootstrap.

## Stopping and reporting rules

- If beta_infinity includes zero, report a finite-size or vanishing effect.
- If exact-rank common support collapses, report the supported estimand and do
  not extrapolate unsupported p ranges.
- If the effect persists but is smooth through p_c, frame it as a generic
  monitored-dynamics mechanism, not a transition diagnostic.
- Do not revive cumulative flow balance.
