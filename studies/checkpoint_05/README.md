# Checkpoint 05 — physical scaling, boundary codes, and causal locality

This study converts the Checkpoint 04 intervention result into a physical large-system statement using monitored stabilizer states.

## Scientific role

For a pure stabilizer state, fixing the central entropy \(S_m\) fixes the complete flat Schmidt spectrum. States generated at different monitoring rates can therefore be compared within the same \((n,\tau,S_m)\) stratum without replacing coefficients or modifying the state.

Checkpoint 05 establishes four linked results:

1. the fixed-spectrum response remains negative through \(n=256\);
2. the conclusion independently replicates under a disjoint seed and random-Pauli monitoring;
3. the response is exactly determined by the finite boundary code
   \((S_m-S_{m-1},S_m-S_{m+1})\);
4. moving one projective measurement toward the cut suppresses the subsequent response on the branch with \(\Delta S_m=0\), with a range of about \(2.37\) sites.

## Frozen design records

`design/` contains timestamped internal locks for:

- calibration;
- the primary large-size scaling analysis;
- the independent-seed replication;
- the paired measurement-location intervention.

These are internal analysis locks, not a public preregistration.

## Included source

| File | Purpose |
|---|---|
| `scripts/stabilizer_tableau.py` | Phase-free binary stabilizer simulation and entropy routines |
| `scripts/run_tableau_scaling.py` | Primary and replication circuit grids |
| `scripts/analyze_checkpoint05.py` | Exact-spectrum fixed-effect estimates and thermodynamic fits |
| `scripts/analyze_boundary_code_decomposition.py` | Nine-state response reconstruction |
| `scripts/analyze_finite_size_sensitivity.py` | Fixed-form extrapolation checks |
| `scripts/analyze_time_sensitivity.py` | Probe-time sensitivities |
| `scripts/analyze_transition_crossover.py` | Independent tripartite-information context and hinge analysis |
| `scripts/analyze_measurement_location.py` | Paired location intervention and decay fit |
| `scripts/build_symplectic_maps.py` | Unique phase-free two-qubit Clifford maps |
| `scripts/validate_tableau_against_statevector.py` | Direct small-system cross-validation |

## Included results

The canonical rows plotted in Figures 2–4 live in `data/processed/core_figures/`. The study result directory retains selected transition and sensitivity tables. The complete methods, numerical grids, seeds, sample counts, and estimator definitions are in `docs/NUMERICAL_METHODS.md` and `docs/RUN_HISTORY.md`.

## Interpretive boundary

The large-size monitoring-rate comparison is an exact-spectrum conditional comparison, not a randomized causal effect of assigning \(p\). Causality applies to the paired measurement-location arm, where the same premeasurement state is copied and only the measurement location is changed. The response remains nonzero on both sides of the independently located monitored transition and is not presented as an order parameter.

## Raw-data policy

The complete trajectory/state tables, intervention rows, and bootstrap arrays are preserved in the handover checkpoint archive but are not committed as opaque binary data. They are planned as a release/data-deposit asset; see `docs/DATA_POLICY.md`.
