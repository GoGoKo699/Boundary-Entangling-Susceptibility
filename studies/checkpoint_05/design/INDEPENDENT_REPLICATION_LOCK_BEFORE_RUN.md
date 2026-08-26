# Checkpoint 05 independent replication lock

This replication was specified while the primary scaling process was still
running and before its output tables existed.

- same simulator, architecture, p grid, protocols, sizes, and observables as
  the primary scaling run;
- 300 trajectories per (protocol,n,p) cell;
- probe times tau = 6, 8, 10;
- independent base seed 2026082401;
- the same exact-rank eligibility rule and fixed-effect estimand;
- the same predeclared beta_n = beta_infinity + a/n thermodynamic model;
- primary replication criterion: the projective-Z beta_infinity estimate for
  chi_relative has the same sign as the primary estimate and its 95% interval
  excludes zero;
- if the primary result fails its own criterion, the replication cannot be used
  to replace or rescue it.
