> Historical source document, preserved for the recorded run conventions. Current claim strength and reproducibility status are in the root `docs/` guides; historical fit language is not an active claim.

# Checkpoint 04 run history and protocol deviations

## Locked primary design

`DESIGN_LOCK_BEFORE_RUN.md` was written and hashed before the full simulation was viewed. It fixed the five circuit/measurement families, three sizes, three monitoring rates, two probe times, 24 trajectories per cell, rank-4 intervention, three probe ensembles, primary contrast, bootstrap unit, and physical-matching calipers.

## Primary run

- base seed: `2026081804`;
- 24 trajectories per `(family,n,p)`;
- 12 discovery and 12 confirmatory trajectories;
- 2,160 saved physical states;
- 4,149 physical/intervention response rows;
- exact response-operator endpoints, not finite gate-bank estimates.

The primary result was analyzed with deterministic stable seeds and 4,000 trajectory-cluster bootstrap replicates.

## Independent-seed replication

After the primary result, the complete five-family rank-4 matrix was rerun with:

- base seed: `2026081805`;
- 16 trajectories per cell;
- 8 discovery and 8 confirmatory trajectories;
- 1,440 physical states;
- 2,769 response rows.

This is an independent-seed replication, not a blinded preregistration.

## Rank-2 robustness run

The primary Clifford arm revealed that many stronger-monitoring stabilizer states had central Schmidt rank below four. A rank-2 intervention was therefore run after inspecting the primary support table. It uses the primary base seed and grid but newly constructs discovery-pooled rank-2 targets.

This result is explicitly **post hoc**. Its role is to test whether the Clifford sign was an artifact of rank-4 eligibility. It is not substituted for the locked primary analysis.

## Physical matching reporting correction

The physical matching calipers were fixed before analysis. However, the design lock did not impose a minimum number of strict-support pairs. Several model/rate comparisons produced one-pair subsets, for which bootstrap intervals collapse to a point. These are retained in the raw output but are not interpreted as evidence.

During reporting, a conservative evidence-quality rule was added:

- at least 12 strict-support pairs;
- pairs drawn from at least three `(n,tau)` cells.

This guardrail changes interpretation only. It does not alter matching, estimates, calipers, or stored data.

## Exploratory and abandoned work

Work directories contain pilot and cellwise execution files used to benchmark and recover interrupted simulations. They are not included in the clean scientific package unless needed for provenance. The clean package contains the finalized simulator, primary data, rank-2 robustness data, independent-seed data, deterministic analysis, and validation outputs.

## Claims not introduced

Checkpoint 04 does not estimate a transition point, critical exponent, thermodynamic scaling law, or universal order parameter. It also does not claim that the rank-truncated equalized states are dynamically reachable.
