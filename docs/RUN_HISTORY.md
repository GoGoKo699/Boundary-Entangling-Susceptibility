# Run history and protocol deviations

## Chronology

| Stage | Lock time (UTC) | Purpose | Data used in primary inference? |
|---|---|---|---|
| Calibration plan | 2026-08-18 20:51:54 | Validate simulator, benchmark runtime, choose probability window and late probe times | No |
| Primary design lock | 2026-08-18 21:01:52 | Freeze ensemble, sizes, probability grid, outcomes, exact-spectrum estimator, and `1/n` extrapolation | Yes |
| Independent replication lock | 2026-08-18 21:11:20 | Repeat the complete primary grid with a disjoint seed and fewer trajectories | Replication only |
| Paired intervention lock | 2026-08-18 21:18:58 | Freeze the measurement-location potential-outcome design | Separate causal arm |

The SHA-256 records stored in [the Checkpoint 05 design directory](../studies/checkpoint_05/design/) verify the text of all four locks.
These are internal timestamped locks, not a public preregistration.

This chronology and the runtimes below retain the [historical run account](../studies/checkpoint_05/notes/RUN_HISTORY_AND_PROTOCOL_DEVIATIONS.md).
The original simulation manifests and preflight-failure log are not included
in the current checkout or indexed data bundle, so their timing and failure
details cannot be independently checked here. The included observations do
establish the run labels, grids, record counts, and measurement geometry.
The recorded base seeds and retained simulator also reproduce the audit's
27 selected original trajectories; that bounded check is not a replay of
every trajectory. See [campaign recipes and provenance limits](CAMPAIGN_RECIPES.md).

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
- Historical reported runtime: 596.89 seconds; original manifest unavailable.

### Independent-seed replication

- Base seed: `2026082401`.
- Same grid and estimator as the primary run.
- 300 trajectories per cell.
- 21,600 trajectories; 64,800 state records.
- Historical reported runtime: 228.01 seconds; original manifest unavailable.

### Paired measurement-location intervention

- Base seed: `2026082501`.
- `n=64,128,256`; `p=0.20,0.26,0.34`; 600 trajectories per cell.
- 5,400 premeasurement trajectories.
- 75,600 valid location interventions.
- Historical reported runtime: 70.60 seconds; original manifest unavailable.

## Deviations and failures

### Intervention preflight failure

The historical account reports that the first intervention preflight attempted
to cast a missing distance for an out-of-range site to an integer and stopped
before producing an analyzable result. Its named log,
`data/measurement_location_intervention/preflight_failure_invalid_distance_nan.log`,
is not an included bundle member or tracked file. It has not been recovered.

The account further reports a correction to skip geometrically invalid
locations, followed by a complete rerun with the locked distances, valid-location
rule, seed, trajectory count, outcomes, and analysis unchanged, and no partial
preflight output used. The current simulator contains that skip and the
included intervention records obey the valid-location rule. These source and
record checks corroborate the current implementation, not the unavailable
failure transcript or the precise sequence of historical execution.

### Post-lock secondary analyses

The following were not the locked primary endpoint and are labeled secondary
or sensitivity analyses:

- alternative finite-size corrections;
- time-resolved slopes;
- the hinge fit at `p=0.27`;
- boundary-code probability decomposition;
- nested-window entropy-summary reconstruction;
- conditional distance-decay fit, now rejected as a physical decay law and
  retained only as a historical analysis;
- unconditional measurement-location effect.

They refine interpretation but do not replace the locked finite-size analysis.
Neither the locked extrapolation nor the checked alternatives demonstrate a
thermodynamic limit.

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
- “paired measurement-location contrast under the stated eligibility rule”
  for the original intervention, whose retained near and far sides can differ;
- “fixed-side joint-preservation principal-stratum effect” only for the strict
  same-side check, which evaluates both interventions on each eligible
  side/pre-state. The selected populations and equal-cell weighting are
  defined in [Methods, Section 10](NUMERICAL_METHODS.md#10-paired-measurement-location-intervention)
  and [the evidence reassessment](EVIDENCE_REASSESSMENT.md).

Do not use:

- “preregistered study”;
- “causal effect of assigning monitoring probability”;
- “order parameter”;
- “universal critical exponent.”
