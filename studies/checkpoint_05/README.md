# Checkpoint 05 — physical scaling and causal locality

This study supplies the physical large-system evidence used by the main project:

- phase-free bit-packed stabilizer simulation through 256 qubits;
- exact complete-spectrum matching within `(n,tau,S_m)` strata;
- projective-Z and random-Pauli monitoring;
- locked primary analysis and independent-seed replication;
- finite boundary-code decomposition;
- paired measurement-location intervention on copies of the same pre-state.

## Main scripts

- `scripts/stabilizer_tableau.py`: simulation engine and exact observables.
- `scripts/run_tableau_scaling.py`: primary, replication, and intervention runner.
- `scripts/analyze_checkpoint05.py`: fixed-spectrum slopes and finite-size extrapolation.
- `scripts/analyze_measurement_location.py`: paired near/far and distance-decay analyses.
- `scripts/analyze_boundary_code_decomposition.py`: exact code redistribution.
- `scripts/validate_tableau_against_statevector.py`: independent small-system validation.

The canonical values used by the four core figures are mirrored under `data/processed/core_figures/`. Large compressed trajectory tables are reserved for release assets.
