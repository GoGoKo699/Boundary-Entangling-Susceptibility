# Reproduction record for the independent audit

Baseline: `00009cf7cc02104e4c776863b3ea551bd38e00f4`. All commands were inspected before execution and ran against unchanged scientific source. Output destinations alone were redirected under this audit directory or disposable scratch. This document records completed executions, not an instruction to repeat the original large campaigns.

## Environment and inputs

A new virtual environment was created at `/workspace/scratch/0174ee249694/audit-venv`. Python **3.12.13**, Linux x86_64, and all six versions in `requirements-reproducible.txt` were used: NumPy 2.3.5, pandas 2.2.3, Matplotlib 3.10.8, SciPy 1.17.0, Numba 0.65.1 and statsmodels 0.14.6. Pytest was 9.1.1. The source allows Python >=3.11; CI selects 3.11. This audit did **not** also run a separate Python 3.11 environment. The full dependency closure is in [environment.freeze.txt](environment.freeze.txt); platform and BLAS details are in [environment.json](environment.json) and [numpy_config.txt](numpy_config.txt). `pip check` passed. Transitive dependencies are recorded here but were not all pinned by the original repository.

Installation used `python -m venv`, then the environment's `python -m pip install -r requirements-reproducible.txt` and `python -m pip install -e .`. See [install.log](install.log). For another checkout, use those local installation commands; the editable line in the freeze file records the audited source identity rather than requiring a second network clone.

The working directory was `/workspace/scratch/0174ee249694/repo`. Logged runs set `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`, `PYTHONHASHSEED=0`, and `MPLBACKEND=Agg`. [run_logged.py](code/run_logged.py) saved explicit argv, UTC start/end, exit code, wall/CPU time, peak child RSS, and the thread environment for each command. RSS is the command's child-process high-water mark, not a sum of memory across concurrent jobs.

All 207 baseline blobs match their Git hashes and the tree matches `1f20614c0e72a632953f8a53c5b234af2b9c74e7`. The 17,227,222-byte input archive has SHA-256 `04e3e353a309b866634715b8b062b7531394fddbcdef1c61f8aec0ba3a4d0255`. Every one of its 172 members passed the supplied manifest checks and materialization. Diagnostic summaries additionally record hashes of the original members they actually used. Materialization output was `/workspace/scratch/0174ee249694/reproduced_studies`; it is reproducible from the tracked ZIP and is not duplicated in this package.

## Documented commands actually executed

The following argv are copied from execution logs. `python` and `pytest` resolved to the clean environment because the runner prepended that environment to PATH. All scientific outputs are retained in the indicated audit subdirectories. The first pytest invocation selected the original `tests/` directory; the later invocation used the user-requested literal `pytest -q`.

| Run | Exit | Wall seconds | Peak RSS MiB | Log |
|---|---:|---:|---:|---|
| verify | 0 | 2.16 | 85.8 | [output](logs/verify.log), [resources](logs/verify.json) |
| pytest_baseline | 0 | 19.83 | 200.0 | [output](logs/pytest_baseline.log), [resources](logs/pytest_baseline.json) |
| core_figures | 0 | 10.76 | 140.1 | [output](logs/core_figures.log), [resources](logs/core_figures.json) |
| core_records | 0 | 6.61 | 477.0 | [output](logs/core_records.log), [resources](logs/core_records.json) |
| reassess | 0 | 12.66 | 471.5 | [output](logs/reassess.log), [resources](logs/reassess.json) |
| figure1_full | 0 | 29.06 | 91.5 | [output](logs/figure1_full.log), [resources](logs/figure1_full.json) |
| figure1_replay | 0 | 4.43 | 113.0 | [output](logs/figure1_replay.log), [resources](logs/figure1_replay.json) |
| figure1_adoption | 0 | 0.71 | 85.9 | [output](logs/figure1_adoption.log), [resources](logs/figure1_adoption.json) |
| materialize | 0 | 0.40 | 26.7 | [output](logs/materialize.log), [resources](logs/materialize.json) |
| tableau_statevector | 0 | 15.22 | 263.7 | [output](logs/tableau_statevector.log), [resources](logs/tableau_statevector.json) |
| gate_invariants | 0 | 0.85 | 94.8 | [output](logs/gate_invariants.log), [resources](logs/gate_invariants.json) |
| pytest_final | 0 | 14.95 | 200.4 | [output](logs/pytest_final.log), [resources](logs/pytest_final.json) |
| pytest_independent | 0 | 0.80 | 85.7 | [output](logs/pytest_independent.log), [resources](logs/pytest_independent.json) |
| confirmed_defects_unmasked | 1 | 0.38 | 27.5 | [output](logs/confirmed_defects_unmasked.log), [resources](logs/confirmed_defects_unmasked.json) |

**verify**

```bash
python verify.py
```

**pytest_baseline**

```bash
pytest -q tests
```

**core_figures**

```bash
python reproduce.py --core-figures --output audits/full-sanity-01/reproduced_figures
```

**core_records**

```bash
python scripts/analysis/reproduce_core_records.py --output audits/full-sanity-01/reproduced_records
```

**reassess**

```bash
python scripts/analysis/reassess_evidence.py --output audits/full-sanity-01/reproduced_evidence --bootstrap 5000 --seed 2026090501
```

**figure1_full**

```bash
python scripts/analysis/complete_figure1_uncertainty.py --output audits/full-sanity-01/reproduced_figure1_uncertainty
```

**figure1_replay**

```bash
python scripts/analysis/verify_figure1_uncertainty.py --output audits/full-sanity-01/reproduced_figure1_uncertainty --report audits/full-sanity-01/figure1_review_verification/independent_replay.json
```

**figure1_adoption**

```bash
python scripts/analysis/check_figure1_adoption.py --resamples audits/full-sanity-01/reproduced_figure1_uncertainty
```

**materialize**

```bash
python materialize_studies.py --output /workspace/scratch/0174ee249694/reproduced_studies
```

**tableau_statevector**

```bash
python studies/checkpoint_05/scripts/validate_tableau_against_statevector.py --clifford-table /workspace/scratch/0174ee249694/reproduced_studies/checkpoint_05/data/two_qubit_clifford_group.npz --maps /workspace/scratch/0174ee249694/reproduced_studies/checkpoint_05/data/two_qubit_clifford_symplectic_maps.npz --report audits/full-sanity-01/reproduced_records/tableau_statevector.json
```

**gate_invariants**

```bash
python studies/checkpoint_04/scripts/validate_gate_invariant_formula.py --out audits/full-sanity-01/reproduced_records/gate_invariants.json --samples 100 --seed 123
```

**pytest_final**

```bash
pytest -q
```

**pytest_independent**

```bash
pytest -q -rx audits/full-sanity-01/code/math_independent.py audits/full-sanity-01/code/figure1_diagnostic_tests.py audits/full-sanity-01/code/figure1_confirmed_defects.py audits/full-sanity-01/code/test_figures23_audit.py
```

**confirmed_defects_unmasked**

```bash
pytest -q --runxfail audits/full-sanity-01/code/figure1_confirmed_defects.py
```

## Outcomes and tolerances

- **Verification and tests:** original suite 33 passed. Final default discovery 35 passed, including two audit estimator tests. The explicitly invoked independent suite passed eight checks with two strict expected failures for compact supporting-table defects. Unmasking those two assertions returned exit 1 with two failures, as intended. This does not repair or endorse the defective source tables. A separate controlled validator-exit regression produced one strict xfail (exit 0) and one unmasked failure (exit 1), each in about one second. Its injected coefficient error was 0.12500000000000083; the validator wrote passes=false but returned 0. The code and exact commands are in MATHEMATICS.md; logs are results/validator_confirmed_defect_xfail.log and results/validator_confirmed_defect_runxfail.log. This tests failure detection, not a new physical dataset.
- **Figures:** all six panels exported in PDF, PNG and SVG, 18 files total. Existing tests compare exports to the approved baseline. All six regenerated PNGs were actually viewed; see [FIGURE_RENDERING.md](FIGURE_RENDERING.md). No external composite or unseen Overleaf layout was inspected.
- **Original records:** 156 checks passed over 237,600 scaling state rows and 75,600 location-intervention rows. Maximum reported numerical discrepancy was `4.84e-13` (the detailed replay reports per-check tolerances). Hashes and counts require exact agreement; rounded archival numerical outputs use declared tolerances.
- **Reassessment:** the specified fresh 5,000-draw run, seed `2026090501`, completed. It reconstructs finite-size fits and fresh paired/common-location inference; it does not regenerate all historical bootstrap campaigns. Original, strict and common paired estimates and the rejection of a single physical exponential are retained in the result tables.
- **Figure 1:** default base seed `2026090801`; PCG64 with `SeedSequence([base,pool_index,run_index,family_index])`. Twenty run/family/pool outputs each retained 50,000 valid draws, one million retained contrasts total. The independent RNG-free verifier checked all 1,009,814 proposals and 1,280 explicit row expansions; maximum discrepancy `2.22e-16`. Adoption and every expected output hash agree. Empty-cell proposals are rejected as whole contrasts. Linear-interpolated 2.5/97.5 percentiles are conditional on observed support and fixed references. Neither the historical seed nor unconditional interval coverage is recovered by this success.
- **Supplied physical checks:** tableau/statevector comparison passed 256 cases with zero reported entropy error; the 100-gate invariant test, seed 123, gave maximum coefficient error `1.17e-15`, below its `5e-13` threshold. The audit separately found that this latter script does not exit nonzero on its false flag; actual fresh values pass despite that enforcement flaw.

The complete resample arrays, multiplicities, eligibility masks and status/seed manifests are preserved in `reproduced_figure1_uncertainty/`; they are computational bootstrap output, not additional trajectories. `reproduced_evidence/new_location_bootstraps.npz` is fresh reassessment uncertainty. Original Figures 3/4 arrays remain in the root archive. Crossing uncertainty arrays were never included: crossing point estimates were independently reconstructed, while their historical intervals were source-inspected only.

## Independent audit calculations

The component reports give exact commands, input members, assumptions and per-check tolerances. All paths below are inside this audit directory unless stated otherwise.

| Check | Actual scope and result | Resources / seed | Substantive shared dependencies |
|---|---|---|---|
| `code/math_independent.py` | Haar/local twirls, gate limits, independent Clifford representatives, stabilizer spectra and measurement sign; explicit excluded-scope counterexamples | 6.56 s; seed 202609080101; absolute diagnostic tolerance 2e-10 | NumPy and mathematical definitions; no repository scientific imports |
| `code/figure1_independent.py` | All 60 references, 3,600 physical spectra, rank support and ten canonical contrasts; max point error 1.11e-16 | 0.34 s; deterministic | Original records and response identity; no repository analysis imports |
| `code/figure1_trajectory_replay.py` | Two n=10 trajectories at two probe times; original/equalized outputs; max error 1.93e-14 | 1.85 s; base seed 2026081804; tolerance 2e-10 | Source evolution and SVD; independent purity contraction |
| `code/figure1_extensions.py` | All 45 original extension endpoints pass four-purity reconstruction; all 30 compact endpoints disagree; ten compact stencil equalities fail | 0.20 s final run; deterministic; tolerance 2e-11 for exports | Original records, supplied probe coefficients; independent estimator implementation |
| `code/figures23_audit.py` | 416 numerical comparisons, including 16 coefficients, 144 code slopes, 128 adjacent and 48 time endpoints, cluster errors and model menu | 9.92 s; peak 528.2 MiB; deterministic | Original records, archived resamples; pairwise and explicit-dummy estimators are independently written |
| `code/figures23_secondary.py` | 76 comparisons: 16 unnormalized coefficients, four intercepts, eight hinge fits, 12 crossing points | 3.04 s; peak 469.9 MiB; deterministic | Original records, archived hinge/size arrays and audit estimator helpers |
| `code/figure4_independent.py` | Exact rational reconstruction of all 75,600 interventions; original/strict/common eligibility, equal-cell means and sparse support | See logs/figure4_independent.log; deterministic | Original recorded entropies; Python Fraction implementation, no source analysis imports |
| `code/simulator_independent.py` | 11,520 gates, 720 maps, all map/Pauli combinations, multiword ranks, alternate measurement pivot, 432 dense measurement cases | 11.84 s; seed 2026090819; 2e-12 general tolerance, 1e-10 Pauli identification | Production kernels are tested against separately constructed dense/integer oracles; archive gate inputs remain shared |
| `code/simulator_archive_replay.py` | 27 selected archived trajectories; 75 snapshots, 42 interventions; all recorded features; 84,600 seeds have no collisions | 8.61 s; exact run labels/base seeds in JSON and SIMULATOR_REPLAY_PLAN.md | Production simulator and maps; independently derived task seeds |
| `code/check_literature_translation.py` | Exact rational equivalence of literature transfer row and four-purity invariants; Haar dimensions 2–8 and special probes | Deterministic; exact Fraction equality | Explicit published equations and notation dictionary; no repository imports |
| `code/navigation_inventory.py` | 221 local links across 64 Markdown files, all resolve; 50 Python AST/import inventories | Deterministic | Pinned Git tree; AST scan is not counted as scientific source review |

The Python entry points above are reproducible from repository root. Figures 2/3 scripts take `--root . --output audits/full-sanity-01/results`; other defaults are rooted relative to their audit source paths. Detailed executable commands and retained logs are in [MATHEMATICS.md](MATHEMATICS.md), [FIGURE1.md](FIGURE1.md), [FIGURES23.md](FIGURES23.md), [FIGURE4.md](FIGURE4.md), [SIMULATOR.md](SIMULATOR.md), and [LITERATURE.md](LITERATURE.md). The audit code is intended to assess this frozen baseline; it may deliberately fail if the source later changes.

## Warnings, failed attempts and independence limits

The optional NumPy configuration dump warned that PyYAML was unavailable; this did not affect numerical execution. No scientific command warning was suppressed from the logs. The first independent simulator harness attempt failed during Numba cache import resolution because the harness renamed a dynamic module. The unchanged source imported under its original module name then passed. Both attempt and successful logs are retained. An initial audit sensitivity calculation used the locked CI-width weights for all model alternatives; source inspection showed that the documented sensitivity menu uses bootstrap standard deviations instead. The initial audit-only values are preserved and distinguished from the corrected independent replay in FIGURES23.md. Neither harness issue was misclassified as a baseline defect.

Ordinary terminal Git lacked HTTPS credentials. The authenticated GitHub connection supplied all verified objects and was used for the audit branch; no source or access control was changed to work around authentication. Final commit/remote verification is reported with the delivered package. No remote CI success is asserted unless explicitly verified; local tests are the evidence described here.

No full original large simulation campaign, original Figure 3/4 bootstrap campaign, discovery-reference resampling study, exhaustive stabilizer enumeration, or independent external implementation campaign was performed. These are explicit scope limits. The canonical estimators, current full Figure 1 sampler and required reproduction commands were executed. Archived-row checks test computation on supplied physical records; only targeted dense and original-generation checks provide additional physical evidence. No new broad empirical or thermodynamic conclusion is inferred.

## Output map

Start at [REVIEW.md](REVIEW.md) and [CLAIM_AUDIT.csv](CLAIM_AUDIT.csv). `logs/` records executions; `results/` contains independent evidence; `reproduced_records/`, `reproduced_evidence/`, `reproduced_figure1_uncertainty/`, and `reproduced_figures/` hold requested replays. [FIX_PLAN.md](FIX_PLAN.md) proposes repairs separately. [COVERAGE.md](COVERAGE.md) lists completed coverage and explicit exclusions. The original data archive remains at repository root. All new tracked objects belong to `audits/full-sanity-01/`; the scientific baseline is untouched.


## Final package verification

After all reports and claim paths were present, `python verify.py` passed again in 2.01 seconds (logs/verify_final.log and .json). The independent `code/verify_audit_package.py` confirmed all 207 original blobs unchanged, all 22 claim rows resolvable, and the audit-only change boundary; the first run took 0.12 seconds (logs/package_boundary.log and .json). A final invocation also verifies every listed SHA-256 in file_manifest.csv after packaging. The manifest excludes itself and disposable Python caches. It authenticates delivered bytes, not their scientific truth. Audit tests and diagnostic results are separate from the original scientific tree.
