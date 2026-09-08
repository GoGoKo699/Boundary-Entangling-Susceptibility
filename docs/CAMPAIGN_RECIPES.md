# Campaign recipes and execution provenance

These are explicit reproduction recipes for the three Checkpoint 05 physical
campaigns behind Figures 2–4. They are reconstructed from retained source,
design locks, and included observation fields, not recovered historical shell
transcripts. They do not change the accepted data or confidence intervals.
For the adopted Figure 1 resampling recipe, use
[Figure 1 uncertainty](FIGURE1_UNCERTAINTY.md); its unrecovered historical seed
is a separate issue.

## What is recorded and what is not

| Item | Evidence and status |
|---|---|
| Run labels, protocols, sizes, probability grid, trajectory indices and times | Present in the included state tables and independently checked against every row |
| Base simulation seeds | Stated in the retained design locks; combined with the recorded run labels and unchanged simulator, they reproduce 27 selected original trajectories in the [audit](../audits/full-sanity-01/SIMULATOR.md) |
| Window widths, late-time information and intervention geometry | Present as record columns and checked against the source; all three runs have requested half-widths `1,2,4,8,16,32,64,128`, capped at `n/2` |
| Original simulation manifests, preflight-failure log and shell invocations | Not included in the checkout or root bundle; unavailable historical provenance, not silently reconstructed |
| Figures 3–4 historical analysis seeds | Source defaults exist, but included execution records do not establish that those defaults were the actual invocation seeds |
| Archived uncertainty | Size/limit arrays have 2,000 draws per endpoint; intervention arrays have 5,000 draws. These arrays and their quantiles can be replayed without knowing the historical invocation seeds |
| Quarter-information crossing uncertainty | Original crossing interval tables are included; crossing resample arrays are not. The original analyzer computes but does not save those arrays |

The indexed [root bundle](../data/record_bundle_manifest.json) contains selected
members, not whole historical checkpoint archives. The
[source migration record](../provenance/SOURCE_MIGRATION.md) defines that scope.
The audit verified all 84,600 seed identities were distinct and replayed
27 trajectories, not all original trajectories. That replay shares the
production simulator; separate small-system kernel checks test its physics.

## 1. Prepare inputs

Run from the repository root, in the environment described in
[Reproduction](REPRODUCTION.md). Materialization checks the bundle and member
hashes and refuses to overwrite different existing files:

```bash
python materialize_studies.py --output reproduced_studies
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
```

All paths below write outside canonical figure, source-data and archive paths.
Use fresh output directories. The full campaigns are optional, expensive
generation tasks, not part of an ordinary redraw or CI run. The repair did
not rerun them. Together they generate 84,600 trajectories, 243,000 state rows,
and 75,600 intervention rows. Original reported runtimes have no included
execution manifests and are not portable resource estimates.

## 2. Physical generation

The source is
[`run_tableau_scaling.py`](../studies/checkpoint_05/scripts/run_tableau_scaling.py).
Each task uses the 64-bit little-endian BLAKE2b digest of
`repr(('checkpoint05', run_label, base_seed, protocol, n, p, trajectory_index))`.
The run label is part of the seed, not merely an output label. Preserve the
explicit labels and grids below to target the included trajectories. Worker
count and chunk size control scheduling, not that task seed. The commands use
one worker for a bounded concurrency setting, not as a claim about the
historical machine or worker count.

### Primary scaling

```bash
python studies/checkpoint_05/scripts/run_tableau_scaling.py \
  --outdir reproduced_campaigns/primary_scaling \
  --maps reproduced_studies/checkpoint_05/data/two_qubit_clifford_symplectic_maps.npz \
  --run-label primary_scaling \
  --protocols z_projective random_pauli \
  --sizes 32 64 128 256 \
  --p-values 0.20 0.22 0.24 0.25 0.26 0.27 0.28 0.30 0.34 \
  --trajectories 800 --probe-taus 6 8 10 --base-seed 2026082301 \
  --half-widths 1 2 4 8 16 32 64 128 --tmi \
  --workers 1 --chunksize 4
```

Expected output: 57,600 trajectories, 172,800 state rows, and quarter-information
fields on the 57,600 final-time rows. No location interventions are requested.
The [primary lock](../studies/checkpoint_05/design/PRIMARY_SCALING_DESIGN_LOCK_BEFORE_RUN.md)
specifies these physical parameters and the first-400/last-400 window split.

### Independent-seed replication

```bash
python studies/checkpoint_05/scripts/run_tableau_scaling.py \
  --outdir reproduced_campaigns/independent_replication \
  --maps reproduced_studies/checkpoint_05/data/two_qubit_clifford_symplectic_maps.npz \
  --run-label independent_replication \
  --protocols z_projective random_pauli \
  --sizes 32 64 128 256 \
  --p-values 0.20 0.22 0.24 0.25 0.26 0.27 0.28 0.30 0.34 \
  --trajectories 300 --probe-taus 6 8 10 --base-seed 2026082401 \
  --half-widths 1 2 4 8 16 32 64 128 --tmi \
  --workers 1 --chunksize 4
```

Expected output: 21,600 trajectories, 64,800 state rows, and quarter-information
fields on the 21,600 final-time rows. See the
[replication lock](../studies/checkpoint_05/design/INDEPENDENT_REPLICATION_LOCK_BEFORE_RUN.md).
The 300-trajectory replication does not have the primary arm's 400/400 split.

### Paired measurement-location arm

```bash
python studies/checkpoint_05/scripts/run_tableau_scaling.py \
  --outdir reproduced_campaigns/measurement_location_intervention \
  --maps reproduced_studies/checkpoint_05/data/two_qubit_clifford_symplectic_maps.npz \
  --run-label measurement_location_intervention --protocols z_projective \
  --sizes 64 128 256 --p-values 0.20 0.26 0.34 \
  --trajectories 600 --probe-taus 10 --base-seed 2026082501 \
  --half-widths 1 2 4 8 16 32 64 128 \
  --interventions --intervention-distances 0 1 2 4 8 16 32 64 \
  --workers 1 --chunksize 4
```

Expected output: 5,400 state rows and 75,600 geometrically valid interventions.
No quarter-information calculation is requested, matching the included records.
The source skips invalid sites. Each valid intervention acts on its own copy
of the final premeasurement state, not on the output of another intervention.
See the [paired-intervention lock](../studies/checkpoint_05/design/PAIRED_MEASUREMENT_INTERVENTION_LOCK_BEFORE_RUN.md).

The new generator writes a new `simulation_manifest.json` for each run. Its
new runtime and paths are not recovered historical provenance. Compare sorted
uncompressed record contents with declared floating-point tolerances, not
gzip bytes or wall-clock metadata: compression headers can differ even when
scientific rows agree.

## 3. Archived-data replay versus fresh analysis

The accepted intervals are reproduced by archived-array replay and the adopted
Figure 1 procedure in [Reproduction](REPRODUCTION.md). No extra physical
generation is needed for those commands.

For a separately declared fresh Checkpoint 05 bootstrap on the original
observations, the following two commands use new explicit recipe seeds
`202609080601` and `202609080602`. They are **not claimed to be the original
analysis seeds**, were not used to replace the accepted intervals, and were
not executed as full resampling campaigns during the repair.

```bash
python studies/checkpoint_05/scripts/analyze_checkpoint05.py \
  --states reproduced_studies/checkpoint_05/data/primary_scaling/stabilizer_scaling_states.csv.gz \
  --outdir reproduced_campaign_analysis/primary_fresh \
  --bootstrap 2000 --seed 202609080601 --train-cut 400

python studies/checkpoint_05/scripts/analyze_checkpoint05.py \
  --states reproduced_studies/checkpoint_05/data/independent_replication/stabilizer_scaling_states.csv.gz \
  --outdir reproduced_campaign_analysis/replication_fresh \
  --bootstrap 2000 --seed 202609080602 --skip-window
```

To analyze newly generated trajectories instead, substitute the corresponding
`reproduced_campaigns/` state file from Section 2 and a separate fresh output
directory. Point estimates should reproduce within numerical tolerance when
the physical records agree; fresh bootstrap arrays and their endpoints need
not equal the archived arrays. The analysis source defaults to seed
`2026082309`; its summary JSON omits the actual argument seed. Keep the command
and environment record alongside any fresh output rather than treating that
default as an execution record.

For fresh location intervals under the current original/strict/common
eligibility analyses, use the already specified September reassessment:

```bash
python scripts/analysis/reassess_evidence.py \
  --output reproduced_campaign_analysis/location_reassessment \
  --bootstrap 5000 --seed 2026090501
```

This command reads the indexed original bundle, generates new location
resamples, and reuses archived size resamples for size-model sensitivity.
It was executed in the audit with this seed. It does not regenerate the
historical Figure 4 arrays. The historical location analyzer defaults to seed
`2026082509`, but its actual historical invocation is not established. That
legacy analyzer also computes the rejected exponential fit; it is not the
recommended current location workflow, and its fitted length is not a
retained physical result.

The secondary hinge source deterministically derives its seed from
`(run, protocol, n)` and exposes a bootstrap-count option, not an independent
seed option. Its archived coefficient arrays replay. Neither that source rule
nor the printed default seeds fill the missing historical shell-log record.
