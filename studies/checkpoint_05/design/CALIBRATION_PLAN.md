# Checkpoint 05 calibration plan

The calibration stage is limited to simulator validation, runtime benchmarking,
and a coarse independently seeded estimate of the transition window. It is not
used for the primary thermodynamic fit.

Planned calibration:

- validate the binary stabilizer simulator against exact state vectors for
  n <= 10 under identical Clifford gates and projective Pauli measurements;
- benchmark n = 32, 64, 128, 256;
- use a coarse Z-measurement grid p = 0.08, 0.12, 0.16, 0.20, 0.24, 0.28 at
  n = 32 and 64 to locate the finite-size transition window from standard
  entanglement observables;
- freeze the primary p grid, trajectory allocation, stationary probe times,
  fixed-spectrum estimand, and finite-size model after calibration and before
  the primary run.

The calibration seed family is disjoint from the primary and replication seed
families.
