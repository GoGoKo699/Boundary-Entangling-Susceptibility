# Validation and audit trail

The repository separates exact identities, numerical observations, extrapolations, and causal statements. The checks below are intended to make those boundaries auditable.

## Exact algebraic checks

- The neighboring-purity response is evaluated independently through the reusable implementation in `src/boundary_susceptibility/response.py`.
- The full stabilizer boundary alphabet is checked for all nine pairs \((\delta_L,\delta_R)\in\{-1,0,1\}^2\).
- The Figure 2 probability slopes sum to zero and their response-weighted sum reconstructs the measured \(n=256\) coefficient to floating-point precision.
- Checkpoint 04 includes direct response-operator and gate-invariant validation scripts.

## Simulation cross-checks

- The phase-free tableau simulator was compared directly with a state-vector implementation for \(n=4,6,8,10\), both monitoring protocols, four probabilities, four trajectories, and two probe times.
- All 256 recorded comparisons agreed in central and neighboring entropies, response values, and tripartite-information values.
- The primary large-size run and independent-seed replication use disjoint base seeds and separately locked designs.

## Core numerical checks

`verify.py` checks that:

- all ten Figure 1 contrasts and confidence intervals are negative;
- all nine Figure 2 boundary codes are present and exactly reconstruct the response;
- every finite-size and extrapolated Figure 3 estimate has a confidence interval below zero;
- every Figure 4 distance effect is negative and decreases monotonically in magnitude;
- the unconditional and unchanged-spectrum paired contrasts have opposite signs;
- the fitted localization length remains in the audited range.

## Repository-structure checks

The verifier also requires the reader-facing documents, plotting scripts, canonical data, and browser figures. It rejects any tracked `.tex` file or manuscript TikZ source.

GitHub Actions runs the unit tests and repository verifier on every push and pull request.

## Limits of the fast verifier

The fast verifier does not rerun tens of thousands of trajectories or reconstruct all bootstrap arrays. Full trajectory-level reruns require the complete checkpoint data assets described in `docs/DATA_POLICY.md`.
