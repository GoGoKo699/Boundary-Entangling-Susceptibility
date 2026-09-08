# Provenance and terminology repairs

Scope: audit F-04 and F-05c/d, plus the dialogue wording affected by F-05a.
No scientific data, archive member, historical design/notes, or audit record
was altered. No full physical or historical resampling campaign was run.

## Source evidence

- `studies/checkpoint_05/scripts/run_tableau_scaling.py:33–41,92–140`
  defines the task seed, run label, command arguments, sorted output rows and
  newly generated manifest. The initial simulator records use independent
  run labels `primary_scaling`, `independent_replication`, and
  `measurement_location_intervention`.
- The three preserved design locks state base seeds `2026082301`,
  `2026082401`, and `2026082501`. The audit's generation replay checks those
  choices on 27 archived trajectories and checks all 84,600 task seeds for
  collisions. That is bounded shared-simulator verification, not full
  independent regeneration.
- During this repair, all three included CP05 state tables were read directly
  from `entanglement-data.zip`. Their labels, protocols, full probability/size
  grids, trajectory counts, times, window columns and nonmissing TMI counts
  agree with the explicit commands in `docs/CAMPAIGN_RECIPES.md`.
- The complete bundle member list contains no CP05 simulation manifest,
  preflight log, or shell transcript. `provenance/SOURCE_MIGRATION.md:7`
  already states that the bundle retains selected records, not full ZIPs.
- `analyze_checkpoint05.py:191–228` exposes an analysis seed but omits it from
  its summary JSON. Its size/limit arrays contain 2,000 draws per endpoint;
  `pcboot` is computed but not saved. `analyze_measurement_location.py:127–153`
  similarly exposes a default seed without establishing the historical
  invocation. The current recipe does not claim to recover either seed.
- `analyze_measurement_location.py:14–37` defines the original side-dependent
  eligible means. The strict same-side comparison in the current reassessment
  is a different jointly preserving selected estimand.
- `analyze_transition_crossover.py:18–19,44–49` fits a monitoring coefficient,
  not the level of susceptibility. `analyze_checkpoint05.py:87–124` selects
  crossing candidates inside a fixed window and discards proposals without a
  crossing.

## Changes

1. `docs/RUN_HISTORY.md` keeps the chronology, three reported runtimes and
   failure narrative, but labels the missing manifests/log and historical
   status. It links the actual design directory and corrects the original
   versus strict intervention labels. Historical source notes remain intact.
2. `docs/CAMPAIGN_RECIPES.md` provides explicit three-run generation commands,
   source/member evidence, expected record counts, and fresh-analysis seeds
   deliberately distinguished from original execution history. It uses
   noncanonical output directories and flags full generation as optional.
3. `docs/NUMERICAL_METHODS.md` reserves the fixed-side principal-stratum
   interpretation for the strict comparison, states equal-cell weighting,
   adds the actual crossing-selection qualifications, and narrows the
   availability claim to records actually included.
4. `docs/DIALOGUE_REPORT.md` no longer endorses an obsolete derivative-style
   axis label or unavailable whole checkpoint/takeover archives. Its source
   index points to the included namespaces and explicit provenance limits.
5. `docs/TRANSITION_CONTEXT.md` identifies the negative quantity as the fitted
   monitoring coefficient, keeps the finite-size/contextual scope, and uses
   ordinary GitHub inline mathematics. No observation or plotted number changes.

The missing historical records remain missing after this repair. Accurate
documentation closes the false-availability claim, not the historical
provenance gap itself. The author's actual editable schematic sources remain
outside this subtask and are not fabricated.

## Checks executed in this repair

Using Python 3.12.13 in the existing pinned audit environment:

- Read all three compressed CP05 state tables directly from the root ZIP and
  checked unique run labels, protocol/size/rate/time grids, constant
  trajectories per cell, all window-width columns, total rows and nonmissing
  quarter-information counts. Primary: 172,800/57,600 state/trajectory rows;
  replication: 64,800/21,600; location: 5,400/5,400. Only primary and replication
  contain late-time quarter information.
- Searched the complete ZIP member list for original CP05 simulation
  manifests, `.log` files and `.sh` transcripts: none are included.
- Loaded both archived size-bootstrap NPZ members and checked every array
  has 2,000 elements.
- Parsed all seven Python commands in `CAMPAIGN_RECIPES.md` with each actual
  source script's argument parser. Intercepted the parser return before any
  simulation, analysis, materialization or output creation. All argument sets
  are accepted; the location command has `tmi=False`, `interventions=True`,
  and all eight intended distances. This validates command syntax and argument
  binding, not an unperformed full campaign's scientific output.
