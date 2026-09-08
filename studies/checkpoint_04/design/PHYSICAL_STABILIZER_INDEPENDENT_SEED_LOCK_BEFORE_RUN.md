# Physical stabilizer independent-seed replication lock

Written before inspecting any output from this replication run.

## Purpose

Replicate the physically reachable exact-central-spectrum result from the main monitored-Clifford arm using a disjoint stochastic seed.

## Locked design

- dynamics: uniformly sampled two-qubit Clifford gates from the same validated 11,520-element table;
- initial states: random single-qubit stabilizer product states;
- measurement protocols: projective Z and projective random Pauli;
- sizes: n = 10, 12, 14;
- monitoring rates: p = 0.08, 0.12, 0.16, 0.20, 0.24;
- probe times: tau = 6, 8;
- trajectories per cell: 80;
- split: 40 discovery, 40 confirmatory;
- finite Clifford probe bank: 12 gates per (protocol,n,tau) cell;
- base seed: 2026082107;
- primary outcome: exact Haar/Clifford-2-design normalized-linear-entropy response;
- exact matching stratum: fixed (measurement protocol, n, tau, log2 central Schmidt rank);
- primary analysis: confirmatory fixed-stratum regression of response on p in steps of 0.04, with trajectory-cluster robust uncertainty;
- success: both measurement protocols have negative point estimates and 95% confidence intervals below zero;
- mechanism check: neighboring-cut purity sum has positive estimates and 95% confidence intervals above zero;
- secondary probes: locally dressed XX(pi/8) and XX(pi/4) exact endpoints.

No result from this run was inspected before this lock was hashed.
