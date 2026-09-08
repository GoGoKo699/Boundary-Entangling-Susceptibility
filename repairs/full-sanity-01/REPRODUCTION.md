# Repair verification record

This records checks actually executed for the authorized minimal repair on
`fix/full-sanity-01`, starting at audit commit
`897dba9926583d12bcaacb214d62a5652c1ba8e1`. The scientific audit baseline remains
`00009cf7cc02104e4c776863b3ea551bd38e00f4`. The entire 196-file audit package
is preserved as a historical result, not rewritten to pass the repaired code.
The [repair plan](PLAN.md), [follow-up review](REVIEW_FOLLOWUP.md), and
[summary](SUMMARY.md) state the scope and final disposition.

## Status of this verification record

The latest completed default test suite passes **63 tests**. Source verification,
all six-panel redraws, original-record replay, supporting-export reconstruction,
the 5,000-draw evidence reassessment, and small gate/tableau checks pass.
The accepted full Figure 1 run also passes generation, independent replay,
and adoption in one uninterrupted sequence: 1,009,814 proposals and one million
retained contrasts checked, maximum replay error `2.221e-16`, and all 26
expected output hashes verified. Two earlier directories contained shortened
NPZ artifacts and failed replay; they remain unaccepted diagnostic attempts.
Their failure cause remains unresolved and is recorded below, not erased by
the successful fresh sequence.

This document records local checks only. Remote CI and merge verification have
not yet been run at this report update; local success is not described as
remote success. The immutable audit's successful historical checks are not
substitutes for these repair-session checks.

## Environment and logging

The repair reused the clean virtual environment created for the audit:
`/workspace/scratch/0174ee249694/audit-venv`, Python **3.12.13**, on Linux
6.18.35, x86-64, glibc 2.39. It was not re-created during this repair.
The scientific dependency pins are NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0,
Matplotlib 3.10.8, Numba 0.65.1, llvmlite 0.47.0, and statsmodels 0.14.6;
pytest is 9.1.1. The complete measured package list is
[environment_freeze.log](logs/environment_freeze.log). Its editable-install
line names the starting audit commit because the repair was tested in an
uncommitted working tree; it does not mean the repaired source was absent.
The [audit environment record](../../audits/full-sanity-01/environment.json)
documents the original clean installation.

Every logged command runs from
`/workspace/scratch/0174ee249694/repo` through
[`code/run_logged.py`](code/run_logged.py). It puts the active Python
environment first on `PATH` and fixes
`OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`,
`PYTHONHASHSEED=0`, and `MPLBACKEND=Agg`.
Each `logs/NAME.json` contains the exact argument vector, working directory,
UTC timestamps, exit code, wall time, user/system CPU time, peak child RSS in
KiB, and environment overrides. Its corresponding `.log` records stdout and
stderr, including failures. Logs are never overwritten.

For example, with the documented environment activated, a repeat check uses
a new name:

```bash
python repairs/full-sanity-01/code/run_logged.py verify_repeat -- python verify.py
```

Some independent commands ran concurrently. The measured wall times below
are per command, not additive elapsed-session time; summed process RSS would
not estimate the actual concurrent memory peak. The largest recorded child
RSS in these completed commands is 489,476 KiB, about 478 MiB.

## Actual command ledger

Argument details and output paths are authoritative in the linked JSON logs.
Command abbreviations below preserve the scientific operation; every numeric
seed/count is shown in this record or its dedicated subsection.

| Log | Command/check | Exit | Wall seconds | Result |
|---|---|---:|---:|---|
| [validator_tests](logs/validator_tests.json) | `pytest -q tests/test_gate_validator_exit.py` | 0 | 1.943 | 2 tests pass, including controlled failure injection |
| [literature_translation](logs/literature_translation.json) | `python audits/full-sanity-01/code/check_literature_translation.py` | 0 | 0.048 | Exact rational coefficient translation passes |
| [preservation](logs/preservation.json) | `python repairs/full-sanity-01/code/check_preservation.py` | 0 | 0.164 | All 196 audit files and designated unchanged scientific inputs match |
| [supporting_records](logs/supporting_records.json) | `python scripts/analysis/reproduce_supporting_records.py --check` | 0 | 0.181 | 30 endpoints, 15 stencil rows reconstruct |
| [core_records](logs/core_records.json) | `python scripts/analysis/reproduce_core_records.py` | 0 | 5.142 | 156 checks pass; maximum difference `4.839e-13` |
| [reassess](logs/reassess.json) | `python scripts/analysis/reassess_evidence.py --bootstrap 5000 --seed 2026090501` | 0 | 12.111 | Original/strict/common location checks and size sensitivities pass |
| [figure1_full](logs/figure1_full.json) | `python scripts/analysis/complete_figure1_uncertainty.py` | 0 | 26.833 | Generator completes; later artifact verification fails, see below |
| [environment_freeze](logs/environment_freeze.json) | `python -m pip freeze` | 0 | 0.352 | Full package versions recorded |
| [pytest](logs/pytest.json) | `pytest -q` | 0 | 19.932 | Earlier suite: 61 tests pass |
| [verify](logs/verify.json) | `python verify.py` | 0 | 1.190 | 172 source members, current panels and inputs pass; no fresh resample array check |
| [figures](logs/figures.json) | `python reproduce.py --core-figures` | 0 | 6.333 | Six current PDF/PNG/SVG triples exported |
| [figure1_replay](logs/figure1_replay.json) | Independent verifier on first full-generation directory | 1 | 1.430 | `BadZipFile`; failed, not counted as replay |
| [figure1_adoption](logs/figure1_adoption.json) | Adoption check on first full-generation directory | 1 | 0.844 | Output hash mismatch; failed |
| [materialize](logs/materialize.json) | `python materialize_studies.py` | 0 | 0.235 | Bundle materialized in separate scratch workspace |
| [gate_invariants](logs/gate_invariants.json) | Gate validator, `--samples 100 --seed 123 --out ...` | 0 | 0.947 | Maximum coefficient error `1.166e-15` |
| [tableau_statevector](logs/tableau_statevector.json) | Documented tableau/state-vector validator | 0 | 2.512 | 256 cases; zero reported entropy/response differences |
| [figure1_replay_final](logs/figure1_replay_final.json) | Repeat verifier on first generation directory | 1 | 1.621 | Same unreadable NPZ; failed |
| [pytest_final](logs/pytest_final.json) | `pytest -q` after added final regression cases | 0 | 20.804 | **63 tests pass** |
| [figure1_full_retry](logs/figure1_full_retry.json) | Full generator in new `_retry` directory | 0 | 26.305 | Generator completes; subsequent replay still fails |
| [gate_invariants_final](logs/gate_invariants_final.json) | Gate validator accidentally invoked with `--output` | 2 | 1.463 | Invalid option; no successful numerical validation in this invocation |
| [gate_invariants_final_corrected_cli](logs/gate_invariants_final_corrected_cli.json) | Corrected command using `--out`, 100 samples, seed 123 | 0 | 0.841 | Gate validation passes |
| [figure1_replay_retry](logs/figure1_replay_retry.json) | Independent verifier on fresh `_retry` directory | 1 | 0.875 | `BadZipFile`; failed |
| [figure1_sequential](logs/figure1_sequential.json) | `python repairs/full-sanity-01/code/verify_figure1_sequence.py` | 0 | 29.315 | Fresh generation, complete independent replay and adoption all pass |
| [preservation_final](logs/preservation_final.json) | `python repairs/full-sanity-01/code/check_preservation.py` | 0 | 0.151 | Final immutable audit/input check passes |
| [verify_final](logs/verify_final.json) | `python verify.py` | 0 | 1.212 | Final source/member/panel verification passes |

The mistaken `--output` gate option was an invocation error, not a scientific
failure. Both command logs are retained, and only the successful corrected
`--out` invocation counts as the final gate check.

The staged whitespace check reports trailing spaces emitted by Matplotlib in
the six newly archived SVG reproductions. The same check excluding only
`repairs/full-sanity-01/reproduced_figures/*.svg` passes. These generated bytes
are preserved for exact reproduction instead of reformatted; source and
documentation changes have no reported whitespace errors.

## Inputs, estimators, seeds and tolerances

All recorded-data calculations use the unchanged root bundle SHA-256
`04e3e353a309b866634715b8b062b7531394fddbcdef1c61f8aec0ba3a4d0255`.
The member-level input hashes remain in the source manifest and generated
result manifests. The materialized workspace at
`/workspace/scratch/0174ee249694/repair-reproduced-studies` is a disposable input
copy, not a new canonical dataset or required external dependency.

- **Supporting export repair:** deterministic original-record reconstruction,
  no RNG. Source-member identities, support, four-purity coefficients and
  normalization are bound in the generated manifest. The tolerance is
  `2e-12`; observed maximum row/stencil error is `1.423e-16`, and maximum
  disagreement with matching verified archived point estimates is `5.552e-17`.
  Archived supporting intervals are source-verified, not newly bootstrapped.
- **Core replay:** 237,600 primary/replication state records and 75,600
  intervention records, ten Figure 1 points, and 156 numerical comparisons.
  Rounded exported values allow absolute tolerance `2e-11`; statewise response
  and code identities use `1e-12`. The maximum observed discrepancy is
  `4.838351941316432e-13`. Figures 3–4 interval checks reuse original archived
  arrays. Figure 1's historical interval source check does not reconstruct
  its missing historical resamples.
- **Evidence reassessment:** seed `2026090501`, 5,000 fresh trajectory-cluster
  location bootstrap draws. Size-model intervals reuse archived size-level
  resamples. Maximum response and slope differences are respectively below
  `1.2e-16` and `7.6e-16`. The strict support is 7,945 side pairs; common support
  is 6,008 side/pre-state combinations on 4,025 pre-states. These are declared
  post-hoc sensitivity estimands, not replacements for the primary data.
- **Figure 1 sampler:** adopted base seed `2026090801`, 50,000 valid draws for
  each of 20 run/family/pool combinations, one million retained contrasts per
  full successful generator execution. The primary `eligible_union` and
  `all_confirmatory` sensitivity retain references and observed support, and
  reject whole empty-cell proposals. They are bootstrap draws, not additional
  physical trajectories. The replay verifier reconstructs saved proposals
  without importing the sampler or drawing new RNG samples; its tolerance is
  `5e-14`, with `2e-12` for the historical comparison table. This independence
  is unavailable when a saved NPZ is unreadable. In the accepted sequential
  run, all 1,009,814 proposal vectors, one million retained contrasts and 1,280
  explicit row expansions pass; both maximum errors are
  `2.220446049250313e-16`. Adoption additionally verifies all 26 expected file
  hashes, ten primary intervals, and the current figure/source successor chain.
- **Gate validator:** 100 Haar-unitary samples with seed `123`; finite
  coefficient errors must all remain below `5e-13`, otherwise the repaired
  executable returns nonzero. Observed maximum error is
  `1.1657341758564144e-15`. Active tests inject known bad and nonfinite
  coefficients and verify both the result flag and nonzero exit.
- **Tableau/state-vector validator:** deterministic seeds
  `stable_seed_u64('cp05_tableau_validation', n, p, protocol, trajectory)`;
  256 cases, pass threshold `1e-10`, observed maximum zero. It shares
  production state-vector gate kernels and the response identity; it is not
  a wholly independent physical implementation or large-campaign replay.
- **Literature translation:** exact `Fraction` arithmetic, no seed and no
  floating tolerance. This compares the cited published EF equations in the
  project notation; it shares those published formulas, not repository
  numerical evolution code.

## Figure 1 artifact failures and unresolved cause

In the first and `_retry` directories the generator returned zero and printed
all 20 estimates/intervals. Independent loading subsequently found damaged NPZ
files. The first adoption check separately detected a resample hash mismatch.
Re-running the verifier on the first directory did not fix it; the fresh
second directory also failed independent replay.

The follow-up inspection identified damaged files as exact prefixes of the
valid frozen audit NPZs. Their immediate post-save hashes in
`ANALYSIS_STATUS.json` describe the full expected files, while the final
`OUTPUT_SHA256.json` describes shortened bytes. Self-consistency with that
later manifest therefore does not establish complete or canonical artifacts.
The source sampler and estimator have not changed. The cause of the file
shortening is not established, and the failure is not called transient or
resolved merely because the generator returned zero. See the
[artifact diagnostic](NPZ_DIAGNOSTIC.md).

A new uninterrupted generation/replay/adoption sequence then completed in
29.315 seconds using `reproduced_figure1_uncertainty_sequential`.
[`code/verify_figure1_sequence.py`](code/verify_figure1_sequence.py) runs the
unchanged generator, independent verifier and adoption checker as successive
subprocesses, propagating any nonzero exit. It alters no source estimator,
seed, tolerance or expected hash. The complete
[log](logs/figure1_sequential.log) and
[independent report](figure1_review_verification/independent_replay_sequential.json)
establish that this separate run passes. It is the accepted repair-session
Figure 1 reproduction, not a claim that the earlier damaged files were repaired
or their failure mechanism diagnosed.

## Output inventory and interpretation

All paths in this table are relative to `repairs/full-sanity-01/`.

| Output | Meaning |
|---|---|
| `logs/` | Exact command/status/environment records and complete stdout/stderr, including unsuccessful attempts |
| `supporting_exports/`, `reproduced_supporting_records/` | Independently checked replacement CP04 endpoints, stencils, support and source manifest |
| `reproduced_records/CORE_RECORD_REPLAY.json`, `core_values_replay.csv` | Actual core comparisons and per-check discrepancies/tolerances |
| `reproduced_records/tableau_statevector.json`, `gate_invariants_final.json` | Small simulator and final corrected gate-check results |
| `reproduced_evidence/` | Reassessed endpoints, support, intervals, size-model checks and fresh location bootstrap arrays |
| `reproduced_figures/` | Six current numerical panels in three formats, plus export status |
| `reproduced_figure1_uncertainty/`, `reproduced_figure1_uncertainty_retry/` | Unaccepted attempts; printed results do not validate damaged saved arrays |
| `reproduced_figure1_uncertainty_sequential/` | Accepted fresh generation, independent replay and exact-hash adoption |
| `figure1_review_verification/independent_replay_sequential.json` | Complete proposal/contrast/row-expansion replay report for the accepted run |

The [Figure 3 repair note](FIGURE3.md) additionally records focused 29-test
geometry/palette/adoption checks and visual inspection. Only its ordinate label
changes; all core numeric tables and other panels remain unchanged. The
[provenance note](PROVENANCE.md) records seven actual argument-parser checks
for campaign recipes and 45 resolved local paths. Those parser checks do not
execute full campaigns.

No original large physical campaign, historical Figure 3/4 RNG invocation,
external composite schematic, unseen Overleaf layout, thermodynamic limit or
physical exponential decay law was newly reproduced or established during
this repair. The missing original logs/manifests and editable external assets
remain explicitly missing. Remote CI and merge results must be verified
separately after the local repair record is complete.
