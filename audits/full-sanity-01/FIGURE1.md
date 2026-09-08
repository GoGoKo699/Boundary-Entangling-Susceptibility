# Figure 1 and retained finite-intervention extensions: independent audit

Baseline: `00009cf7cc02104e4c776863b3ea551bd38e00f4`.

**Verdict:** The current Figure 1 point estimates and adopted uncertainty calculation survive. A major, separately located defect affects the active compact Checkpoint 04 supporting tables: they disagree with the included original records, and their purported exact decomposition is internally inconsistent. The core Figure 1 panel does not read those defective compact tables.

## Pre-result follow-up resource note

2026-09-08: Independently reconstructing all archived reference spectra, rank masks and point estimates succeeded. The original full physical generator remains a substantive dependency of those records. Before additional physical calculations, specify a bounded replay of two primary trajectories, Haar/Z and Clifford/Z, each at n=10, p=0.08, trajectory index 12, probe times 6 and 8, base seed 2026081804. Purpose: check whether the included simulator reaches original records and spectrum-replaced responses under the documented pinned environment, especially the disclosed numerical SVD basis choice. Budget: two length-80-cycle, 1024-amplitude trajectories, well below one CPU minute and 100 MB beyond imports. The generator is intentionally reused; independent audit code will contract purities from the returned vectors and compare the archive. This is a source-generation replay, not independently developed simulation or new ensemble evidence. Any observed SVD ambiguity will be assessed against the explicit disclosure at docs/DIALOGUE_REPORT.md:282–284, not automatically classified as a defective observable.

The retained gate-space extension was subsequently traced into its original rows and compact exports, following the original plan's coverage of supporting calculations. No additional simulation or extension bootstrap was run. Inspection of the compact decomposition revealed its mismatch before the independent extension reconstruction; that follow-up is exploratory error diagnosis, not a prespecified new endpoint.

## 1. Major confirmed finding: active supporting tables disagree with their source

**F1-E1, high certainty, major reproducibility/completeness defect.** `studies/checkpoint_04/results/README.md:3–6` describes the compact endpoint and decomposition tables as load-bearing results and exact accounting. `docs/EXTENDED_RESULTS.md:7–11` points readers to them as the retained extension. They are not marked superseded. Nevertheless:

* All 30 endpoint rows in `studies/checkpoint_04/results/intervention_cross_architecture.csv:2–31` differ from the original-record reconstruction at tolerance 2e-11. Some primary Haar discrepancies are small (order 1e-6), but other discrepancies are large: up to 0.0369902866.
* All 15 `reconstruction` values in `studies/checkpoint_04/results/response_stencil_decomposition.csv:2–16` disagree with the independently reconstructed current record values.
* Ten of those 15 rows also fail the identity `reconstruction = observed_response_contrast` **within the compact table itself**. Thus uncertain historical provenance cannot explain away the exact-accounting claim.

Concrete examples:

| Endpoint | Compact stated endpoint | Compact reconstructed endpoint | Original-row/direct/exact-stencil result |
|---|---:|---:|---:|
| Primary Floquet-Cartan, XY pi/8 | -0.0985805295422 | -0.0800936164752 | -0.0770481378164718 |
| Independent Haar/Z, XY pi/8 | -0.0932413149314 | Not tabulated | -0.0562510283752865 |

The first row is compact endpoint line 6 and decomposition line 6; the second is compact endpoint line 30. The first correct point is even outside its compact interval [-0.104089593763,-0.0930477535354]. This is not an export-rounding issue, nor a choice between relative and unnormalized entropy response: all three numbers in the first row purport to be the same unnormalized, normalized-linear-entropy change, chi2.

The authoritative internally consistent source chain checked here is the root `entanglement-data.zip` members:

1. `checkpoint_04/data/intervention/{primary_rank4,independent_seed_rank4,posthoc_rank2}/state_response_rows.csv.gz`;
2. `checkpoint_04/analysis/consolidated/intervention_cross_architecture.csv` (SHA-256 `9342e61c83d155e1c3be62861e6029a68870da854813efc79213b3ee66529995`);
3. the exact four-purity coefficients in `docs/THEORY.md` and the checked source `response_from_stencil` definition.

The independent audit groups confirmatory rank-supported states into each available (n,tau,p) cell, contrasts rates 0.24 and 0.08, and weights common rate-supported cells equally. It independently contracts each purity shift with the exact gate coefficients **and its own cell's D/(D-1)**. All 45 original-archive endpoints (three runs, five families, three probes) agree with both the independently reconstructed stencil and the archived consolidated analysis, to <1e-12. All remain negative. The archived consolidated source has 45 rows, including rank two; the defective compact endpoint export has 30 rank-four rows. These distinct schemas are another reason not to assume byte identity.

`results/figure1_compact_table_discrepancies.csv` gives every affected endpoint, its exact compact file line, stored value, reconstructed value and discrepancy. `results/figure1_extension_points.csv` includes all 45 independent reconstructions and the 15 decomposition comparisons. `code/figure1_confirmed_defects.py` contains two strict expected-failure tests, one entirely internal to the compact table and one against the independently verified archive value. They produced **2 xfailed**, as intended; these are confirmed defects, not passes of the compact tables.

**Consequence and smallest adequate repair:** Preserve the inconsistent exports as identified historical provenance, reconcile their source version, and regenerate or replace the active compact exports from the included record chain in a separately authorized repair. Bind those exports to direct response and contribution identities in a regression test. Until then, do not quote their magnitudes or confidence intervals as current results. Their old provenance has not been diagnosed, so the audit does not guess how the discrepancy arose. No core Figure 1 file or original scientific input was altered here.

## 2. Estimand, intervention and sampling population

For run r and family f, let C_f be the observed support shared by both runs. The current estimate is

$$
\widehat\Delta_{rf}=\frac1{|C_f|}\sum_{(n,\tau)\in C_f}
\left[\overline y_{rf,n,\tau,.24}-\overline y_{rf,n,\tau,.08}\right],\quad
y=\frac{D}{D-1}\left[1-\frac{.4(P_L+P_R)}{P_m}\right].
$$

P_m is the **input** purity after the diagnostic spectrum replacement. This is an average normalized linear-entropy change divided by input purity, not an average finite change of logarithmic Renyi-2 entropy. The source implements the former at `cross_architecture_simulation.py:343–348` and sampler `complete_figure1_uncertainty.py:169–182`. The independent record audit derives y from P_L, P_R and P_m rather than reusing the recorded response column. The algebraic two-outcome example in the audit diagnostic tests independently distinguishes the two observables.

`cross_architecture_simulation.py:223–240,469–510,680–714` implements SVD, rank eligibility and reference replacement. Eligible states have at least four squared singular values above 1e-12. The first four Schmidt-vector pairs are retained, all higher components discarded, and their squared amplitudes set to a target mu. Discovery spectra of eligible states are first normalized within the leading four, then pooled across the monitoring grid within (family,n,tau), averaged, and renormalized. It is not a rate-by-rate target or a pooled cross-run target.

The primary run has trajectories 0–11 for discovery and 12–23 for confirmation; the independent run has 0–7 and 8–15. Independent extraction checked all 3,600 physical spectra and metadata, all 1,800 discovery-spectrum records, and all 3,318 available equalized states. Discovery and re-evolved physical-spectrum copies agree exactly. All 60 references reconstruct with maximum error 1.11e-16. Every recorded equalization mask matches rank from the complete stored spectrum; every target purity agrees with sum(mu^2) to 1.11e-16. No confirmatory trajectory contributes to reference estimation. All 1,800 actual trajectory seeds from the two base seeds are distinct after the source's 32-bit hashing. This verifies the finite grid, not a mathematical collision guarantee for arbitrary future runs.

`independent_seed_replication.py` is an auxiliary driver taking supplied references; the plotted independent campaign is the documented 16-trajectory, 8/8 run with its **own** archived discovery references. It must not be silently interpreted as a repeat at the primary reference. Source evolution uses random pure-product factors for all five families (`cross_architecture_simulation.py:147–156`); Clifford dynamics therefore does not imply that every Figure 1 input is a stabilizer state. The later exact-flat-spectrum arm is separate.

The common support is n=10,12,14 and tau=6,8 for four families. Clifford uses (10,6),(10,8),(12,8),(14,6). The support depends on both runs' observed rank eligibility; it was not a blind six-cell confirmatory design. This is disclosed in the adopted post-hoc procedure. Equal cell weighting is distinct from pooling all states, and trajectory indices at the two times remain dependent. Nothing pairs individual states across monitoring rates.

## 3. Independent primary results and sparse-support consequences

| Family | Primary estimate | Independent estimate | Cells per run |
|---|---:|---:|---:|
| Haar/Z | -0.257266454 | -0.207432357 | 6 |
| Clifford/Z | -0.405537421 | -0.319248097 | 4 |
| Floquet-Cartan/Z | -0.208080604 | -0.184777801 | 6 |
| Haar/random Pauli | -0.188156077 | -0.197691810 | 6 |
| Haar/weak Z | -0.182587695 | -0.178141025 | 6 |

All ten estimates agree with the active canonical panel to 1.11e-16. Every retained cell contrast is negative; this is a finite-sample directional observation, not a simultaneous inferential statement. The strongest family cannot be ranked as a common-population physical effect solely by these pooled magnitudes, since reference spectra and support vary by family/run/cell.

The accepted support contains 1,062 eligible state/time rows in 568 eligible clusters. The all-confirmatory sensitivity starts with 600 original clusters. In high-rate Clifford cells, eligible counts are primary 3,3,3,7 and independent 3,4,4,3. These small physical populations determine information content. Fifty thousand resamples do not improve underlying physical sample size.

## 4. Adopted 50,000-draw recipe and its actual coverage

The locked machine plan and `docs/FIGURE1_UNCERTAINTY_PLAN.md` agree with `complete_figure1_uncertainty.py:88–160,163–228,247–295`:

* Strata are separate (run,family,n,p); primary pools are the union of trajectories having a rank-eligible retained time. All-confirmatory pools additionally include trajectories with no eligible retained row.
* N whole trajectories are drawn with replacement from each N-member stratum. A trajectory's multiplicity applies jointly to all its retained time values and eligibility mask. Missingness is structural rank ineligibility, never a numerical zero.
* The entire proposed family/run contrast is rejected if any required time/rate/size cell is empty. The first 50,000 valid proposals are kept; support and cell weights never change.
* The base seed is 2026090801, with PCG64 SeedSequence [base,pool_index,run_index,family_index], ordered strata/IDs/times, batches of 1,000 and a 1,000,000-proposal cap. Linear-interpolated .025 and .975 percentiles are used.
* The all-confirmatory sensitivity retains the same target, support and rejection rule. Its pool selection was recorded before new resampling, though historical effects and support were already known. This is an internal prospective calculation plan for a post-hoc revision, not a public preregistration.

The root audit executed the complete sampler, separate verifier and adoption binding in the clean pinned environment. The saved outputs are `reproduced_figure1_uncertainty/` and `figure1_review_verification/independent_replay.json`. All 20 analyses (2 pools x 2 runs x 5 families) completed: 1,009,814 proposed vectors, 1,000,000 retained contrasts and 1,280 explicit duplicated-row expansions were checked. Maximum independent-replay disagreement is 2.22e-16, and all expected adoption hashes passed. The verifier uses a separate contraction and expands selected duplicated rows, but still shares the original record definitions and formula. Hash agreement binds an output to the adoption; it is not by itself a physical or statistical proof.

The new independent raw-record audit also computes support survival from sets of eligible trajectory IDs using rational inclusion-exclusion. Clifford primary-pool rejection probabilities are exactly 0.02048 and 0.0169968007040, agreeing with the sampler. Full-confirmatory counterparts are 0.0915439311985 and 0.0535361044115. Realized rates need not equal these probabilities: the independent sensitivity realized 5.448%, for example. The current primary and all-confirmatory intervals all remain below zero; the reported Monte Carlo batch diagnostics concern numerical stability of the resampling distribution, not additional experiments.

These are nominal **pointwise support-conditioned percentile intervals**. They omit reference estimation, support discovery and (for Floquet) uncertainty in the fixed gate realization. The Floquet gates are shared within a run/size by `cross_architecture_simulation.py:351–358`; the conditional interpretation is therefore essential. Rejection also conditions on complete support. Neither small-sample exact coverage nor an unconditional repeated-study coverage rate is established. The baseline clearly states these limitations at `docs/FIGURE1_UNCERTAINTY.md:9–13` and in the active caption. They do not nullify the conditional calculation, and they do not justify a broader unqualified population or universal-sign claim.

The historical bootstrap seed and full recipe remain unavailable. The adopted recipe reproduces a declared replacement and preserves the history; it does not reconstruct the old RNG or explain interval changes solely by a changed seed. Current and historical paths are correctly separated. No failing primary Figure 1 test or estimation defect was found.

## 5. SVD degeneracy: a real disclosed limit, not a manufactured defect

The numerical operation is gauge dependent in degenerate Schmidt eigenspaces. Among all rank-eligible extreme-rate confirmatory rows **before the common-support restriction**, primary Clifford has 93/96 rows with a leading selected gap below 1e-10 and 25/96 with a degenerate rank-four boundary; independent Clifford has 60/61 and 16/61 respectively. Nonflat spectra occur in 62/96 and 38/61 of those rows. No such gaps occur in the other four families in these stored records. The threshold is a diagnostic, not an exact algebraic classification.

`code/figure1_diagnostic_tests.py` constructs the same four-qubit maximally entangled input matrix I/2 in two valid SVD gauges, then assigns the same complete spectrum (0.4,0.3,0.2,0.1). The resulting relative responses are -28/45 and -12/25. This demonstrates that the spectrum replacement cannot be described as a unique basis-independent physical operation. `docs/DIALOGUE_REPORT.md:282–284` already discloses precisely this issue. It does not refute the recorded chosen-basis diagnostic or the independent physically generated exact-spectrum arm.

The specified two n=10 trajectories replayed the original and equalized responses at both times, eight records total. Maximum error was 1.93e-14 (tolerance 2e-10); actual runtime 1.85 s. State evolution, SVD and reconstruction are shared original code, while the audit explicitly indexes subsystem amplitudes and contracts purities independently. These examples provide local source-to-record evidence; the full original state-vector campaign and cross-platform SVD-gauge stability were not rerun.

## 6. Retained gate-space criterion: what was and was not checked

The archival extreme-rate A=Delta(P_L+P_R), B=Delta(P_Lb), M=4A-5B values were independently recomputed for all 15 (run,family) combinations from the primary rank-four, independent rank-four and post-hoc rank-two rows. All agree within 2.8e-16, and all point inequalities are positive. The **archived** lower-margin intervals are positive in primary Haar/Z, Floquet-Cartan and weak Z (3/5), and all five rank-two families, as stated at `docs/THEORY.md:281–285`. Extension intervals were inspected as saved analysis outputs; their bootstrap was not freshly regenerated here and no saved bootstrap vectors for this particular extension are claimed to have been replayed.

Keep two distinctions when reporting this extension:

1. The exact criterion at `docs/THEORY.md:248–278` is at fixed dimension. Its extension script `analyze_gate_space_universality.py:29–37` pools raw shifts equally over sizes. For the equally weighted chi2 endpoint across different n, the correct pooled sufficient quantities include the cell factor D/(D-1). The audit computed those weighted quantities independently and all 15 point inequalities remain positive. The saved unweighted intervals are not intervals for these weighted quantities. Minimal clarification: state explicitly the archived pooled raw-purity estimand, or supply the matching weighted diagnostic before assigning its intervals to the normalized pooled response criterion.
2. The older extension bootstrap at that script's lines 43–48 uses nanmean and therefore drops undefined cells within a draw; it does not follow the adopted current Figure 1 rejection rule. Its two marginal lower-interval checks at lines 51–55 do not provide a calibrated simultaneous confidence statement for every gate/family. This is a disclosed post-hoc supporting direction test, not a universal empirical theorem. No new gate-space campaign is needed merely to preserve that qualified scope.

## 7. Audit executions and reproducibility limits

All commands below were run from the repository root using `/workspace/scratch/0174ee249694/audit-venv/bin/python`, Python 3.12.13, NumPy 2.3.5, SciPy 1.17.0. Source files were read before execution. Numerical comparisons use 2e-11 for record/export comparisons, 1e-12 for exact extension contractions, and 2e-10 for the bounded trajectory replay. Source-member SHA-256 values and observed errors are in the accompanying JSON results.

| Audit command (after the Python executable) | Actual result |
|---|---|
| `audits/full-sanity-01/code/figure1_independent.py` | Passed; 0.34 s; all 60 references, 3,600 physical spectra, ten points and support checks |
| `audits/full-sanity-01/code/figure1_trajectory_replay.py` | Passed; 1.85 s; 2 trajectories / 8 variant records; BLAS/OMP threads set to 1 |
| `-m pytest -q audits/full-sanity-01/code/figure1_diagnostic_tests.py` | 3 passed in 0.14 s |
| `audits/full-sanity-01/code/figure1_extensions.py` | Archive identities passed; compact discrepancies recorded; 0.20 s on final output run |
| `-m pytest -q -rx audits/full-sanity-01/code/figure1_confirmed_defects.py` | 2 strict xfailed in 0.03 s, documenting confirmed compact-table defects |

The first record audit and extension code import no repository scientific Python. They share immutable original data and explicitly stated equations, so they test analysis independently of the existing implementation, not data-generation independence. The bounded trajectory replay explicitly shares the generator. Full sampler commands and logs are recorded in the root audit reproduction report and are not counted as a second physical dataset.

Unperformed: complete original state-vector campaign; fresh uncertainty from new discovery references or newly selected support; fresh Floquet-disorder ensemble; exact calibration of sparse-sample bootstrap coverage; full extension bootstrap regeneration; provenance recovery for the inconsistent compact exports. These are either explicit limits or the stated supporting-table repair target, not concealed passes.

## 8. Source coverage for this audit component

Read and traced current Figure 1 material: `README.md` Figure 1 section; `docs/SCIENTIFIC_STORY.md`; `docs/NUMERICAL_METHODS.md`; `docs/NOTATION.md`; `docs/DIALOGUE_REPORT.md` M3 and B1–B4; `docs/FIGURE1_UNCERTAINTY.md`; `docs/FIGURE1_UNCERTAINTY_PLAN.md`; `docs/FIGURE1_UNCERTAINTY_REVIEW.md`; `docs/FIGURE1_CAPTION.md`; `docs/FIGURE_BASELINE.md`; `docs/REPRODUCTION.md`; `docs/REPRODUCIBILITY_LIMITS.md`; `docs/RESULTS_AT_A_GLANCE.md`; `docs/EXTENDED_RESULTS.md`; `docs/THEORY.md` local-dressing and gate-space sections; `docs/CODE_MAP.md`; relevant claim and scope references.

Read active analysis code: `scripts/analysis/complete_figure1_uncertainty.py`, `verify_figure1_uncertainty.py`, `check_figure1_adoption.py`, Figure 1 portion of `reproduce_core_records.py`; `analysis_plans/figure1_uncertainty_2026-09-08.json`; `tests/test_figure1_uncertainty.py`; adoption assertions; permanent support/interval/pattern/Monte-Carlo tables and generated full replay status.

Read study sources: `studies/checkpoint_04/README.md`, `results/README.md`, its three compact result CSVs, `design/DESIGN_LOCK_BEFORE_RUN.md`, `notes/RUN_HISTORY_AND_PROTOCOL_DEVIATIONS.md`, `scripts/cross_architecture_simulation.py`, the rank/seed/SVD/reference paths in `cross_architecture_rankflex.py`, `independent_seed_replication.py`, `build_consolidated_checkpoint04_analysis.py`, `analyze_gate_space_universality.py`; `studies/figure_design/FIGURE_01_SPEC.md` and `bootstrap_reference.py` as explicitly historical material. Read original archive discovery/full spectra and metadata, state rows, reference spectra, validation records and the relevant consolidated extension tables. Exact members and hashes are recorded in `figure1_independent_summary.json` and `figure1_extension_summary.json`.
