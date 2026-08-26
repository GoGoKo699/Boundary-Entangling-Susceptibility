# Claim–evidence map

A compact machine-readable ledger is available at `results/core_claims.csv`. The canonical rows plotted in the six Python panels are under `data/processed/core_figures/`, while selected broader result tables remain next to the study that generated them.

## M1 — Central-spectrum insufficiency

**Claim.** States with the same complete central Schmidt spectrum can have systematically different fresh-gate susceptibilities.

**Evidence.** Held-out rank-4 spectrum intervention across five state-generation families, followed by an independent-seed replication. Rank and probe sensitivities are retained in the Checkpoint 04 study source.

**Status.** Supported numerically for the tested finite circuit and measurement families.

## M2 — Exact neighboring-cut mechanism

**Claim.** For a Haar-random or uniformly random two-qubit Clifford probe, the relative Rényi-2 response is fixed by \(P_{m-1},P_m,P_{m+1}\), not by \(P_m\) alone.

**Evidence.** Exact two-copy response-operator theorem and direct algebraic validation.

**Status.** Exact for all pure input states under the stated probe ensemble.

## M3 — Physical large-size persistence

**Claim.** Naturally generated stabilizer states matched at the complete central spectrum retain a negative monitoring-rate response through \(n=256\).

**Evidence.** Fixed-\((n,\tau,S_m)\) comparison under projective-\(Z\) and random-Pauli monitoring.

**Status.** Supported numerically through the tested size range. A nonzero thermodynamic limit is a supported extrapolation, not a theorem.

## M4 — Independent replication

**Claim.** The large-size conclusion survives a disjoint seed and different measurement basis.

**Evidence.** Separately locked replication using the same estimator and size grid.

**Status.** Supported numerically.

## M5 — Paired causal localization

**Claim.** On the unchanged-spectrum branch, moving one measurement toward the cut suppresses the subsequent fresh-gate response.

**Evidence.** Paired potential interventions on copies of the same premeasurement stabilizer state, with measurement location varied and \(\Delta S_m=0\) retained.

**Status.** Paired conditional causal effect of location. It is not a randomized causal effect of assigning the long-run monitoring probability.

## Explicitly excluded claims

- a new MIPT order parameter;
- a critical exponent or singular susceptibility;
- a universal non-Clifford thermodynamic scaling law;
- cumulative spectral-flow cancellation as a transition principle.
