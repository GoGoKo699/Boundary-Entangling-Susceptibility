# Run history and protocol deviations

## Chronology

| Stage | Lock time (UTC) | Purpose | Data used in primary inference? |
|---|---|---|---|
| Calibration plan | 2026-08-18 20:51:54 | Validate simulator, benchmark runtime, choose probability window and late probe times | No |
| Primary design lock | 2026-08-18 21:01:52 | Freeze ensemble, sizes, probability grid, outcomes, exact-spectrum estimator, and `1/n` extrapolation | Yes |
| Independent replication lock | 2026-08-18 21:11:20 | Repeat the complete primary grid with a disjoint seed and fewer trajectories | Replication only |
| Paired intervention lock | 2026-08-18 21:18:58 | Freeze the measurement-location potential-outcome design | Separate causal arm |

The SHA-256 records stored in `design/` verify the text of all four locks.
These are internal timestamped locks, not a public preregistration.

## Simulation runs

### Calibration

- Coarse calibration: 1,440 trajectories and 4,320 state rows.
- Dense calibration: 7,200 trajectories and 14,400 state rows.
- Projective-Z monitoring only.
- Used to choose the primary probability grid and verify approximate late-time
  stationarity.
- Excluded from primary and replication confidence intervals.

### Locked primary scaling run

- Base seed: `2026082301`.
- Projective Z and random Pauli monitoring.
- `n=32,64,128,256`.
- Nine measurement probabilities from 0.20 to 0.34.
- 800 trajectories per `(protocol,n,p)` cell.
- Probe times `tau=6,8,10`.
- 57,600 trajectories; 172,800 state records.
- Runtime recorded in the manifest: 596.89 seconds.

### Independent-seed replication

- Base seed: `2026082401`.
- Same grid and estimator as the primary run.
- 300 trajectories per cell.
- 21,600 trajectories; 64,800 state records.
- Runtime: 228.01 seconds.

### Paired measurement-location intervention

- Base seed: `2026082501`.
- `n=64,128,256`; `p=0.20,0.26,0.34`; 600 trajectories per cell.
- 5,400 premeasurement trajectories.
- 75,600 valid location interventions.
- Runtime: 70.60 seconds.

## Deviations and failures

### Intervention preflight failure

The first intervention preflight attempted to cast a missing distance for an
out-of-range site to an integer. It stopped before producing an analyzable
result. The failure log is preserved at
`data/measurement_location_intervention/preflight_failure_invalid_distance_nan.log`.

The simulator was corrected to skip geometrically invalid locations. The
locked distances, valid-location rule, seed, trajectory count, outcomes, and
analysis were unchanged. The complete intervention was then rerun from the
start. No partial output from the failed preflight entered the analysis.

### Post-lock secondary analyses

The following were not the locked primary endpoint and are labeled secondary
or sensitivity analyses:

- alternative finite-size corrections;
- time-resolved slopes;
- the hinge fit at `p=0.27`;
- boundary-code probability decomposition;
- nested-window entropy-summary reconstruction;
- conditional distance-decay fit;
- unconditional measurement-location effect.

They refine interpretation but do not replace the primary thermodynamic test.

### Common-support restriction

No single exact-rank stratum at `n=256` spans the entire probability grid. The
primary coefficient is therefore a connected trend over overlapping exact-rank
strata. Adjacent-probability contrasts were added to expose the supported
comparisons. This is a scope limitation, not a deviation from the locked
eligibility rule.

## Reporting language

Use:

- “locked primary analysis followed by independent-seed replication”;
- “physical exact-spectrum conditional comparison” for the long-run `p`
  analysis;
- “paired causal effect of measurement location within a principal stratum”
  for the intervention.

Do not use:

- “preregistered study”;
- “causal effect of assigning monitoring probability”;
- “order parameter”;
- “universal critical exponent.”
