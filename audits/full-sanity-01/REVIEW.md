# Independent full scientific and reproducibility audit

**Repository:** GoGoKo699/Boundary-Entangling-Susceptibility  
**Frozen baseline:** `00009cf7cc02104e4c776863b3ea551bd38e00f4`  
**Tree:** `1f20614c0e72a632953f8a53c5b234af2b9c74e7`  
**Audit branch:** `audit/full-sanity-01`  
**Audit date:** 8 September 2026

## Executive verdict

**The four-figure study survives within its current stated scope. The repository is not yet complete for manuscript preparation.** No result-overturning defect was found in the core mathematical identities, canonical figure estimates, adopted Figure 1 resampling, or tested physical simulator behavior. However, two retained Checkpoint 04 supporting tables contain confirmed numerical inconsistencies. Equation-level attribution to directly equivalent entanglement-feature formulas is missing, and the acknowledged editable external schematics remain absent. These must be resolved before treating the repository as a trustworthy, complete source for all eventual paper content.

This is a fresh audit of the pinned source, not an endorsement inherited from previous reports or CI. The original scientific files, data, figures, plans and provenance were not repaired. Every new tracked file is under this audit directory. The final delivery identifies the audit commit and independently verified remote branch state; no merge is requested or performed.

| Dimension | Conclusion |
|---|---|
| Mathematical validity | Core two-copy, four-purity, Haar/Clifford, stabilizer-spectrum and restricted measurement-sign statements are correct. Independent derivations and dense checks agree. |
| Statistical support | Negative finite-system conditional contrasts, finite-size coefficients and selected paired location means are supported. Their stated conditioning and population boundaries are essential. Bootstrap draws are not new trajectories. |
| Computational reproducibility | All requested documented reproduction commands pass in a clean pinned environment. Independent calculations recover the primary numbers. Green checks do not detect the inconsistent compact supporting tables. Full historical campaigns and original Figures 3/4 bootstrap generation were not rerun. |
| Attribution | Major completion needed: the exact transfer machinery is already present in the specified primary literature. The distinctive empirical combination is not invalidated, but generic fixed-spectrum response and spatial measurement sensitivity also have relevant antecedents. Priority is not certified. |
| Repository completeness | Current figures, records and documented workflows are available. Inconsistent supporting tables, missing editable external schematics, and inaccurate historical availability statements prevent an unqualified completeness verdict. |

## 1. Scope, authority and evidence levels

The authenticated GitHub connection confirmed repository ID 1347195921 and read/write access. At acquisition, `main` equalled the pinned baseline and the requested audit branch did not exist. It was created at that exact commit. All 207 baseline blobs, including the 17,227,222-byte archive, and the complete Git tree were independently hash-verified. The signed commit was reconstructed exactly from the API payload; the initial working tree was clean. There is no repository instruction file in the complete baseline tree. Direct HTTPS cloning lacked terminal credentials, so the authenticated connection supplied the exact snapshot. This is an exact shallow checkout, not a synthetic replacement baseline. See [baseline](BASELINE.md) and [inventory](baseline_inventory.csv).

The [plan](PLAN.md), inventory and [coverage ledger](COVERAGE.md) were saved before scientific calculations. Component notes identify prospective targeted checks and subsequent exploratory follow-ups. Six bounded review streams covered mathematics, Figure 1, Figures 2–3, Figure 4, literature, and simulator/completeness; the principal reviewer ran the documented reproduction, inspected all regenerated panels, verified material diagnoses and synthesized this report. No manuscript, unrelated channel-capacity project, external correspondence or new research campaign was used.

Evidence is distinguished throughout:

- **Analytical deduction:** re-derived from definitions, with assumptions explicit.
- **Fresh independent computation:** new code, with shared archive/formula/library dependencies stated.
- **Source replay:** existing scripts rerun; useful reproducibility evidence, not independent implementation.
- **Archived uncertainty:** quantiles and fits reconstructed from original arrays, not fresh historical bootstrap generation.
- **External literature:** primary equations inspected and translated; no absence-of-search-result priority proof.

The coverage is calculation-based: all primary Figure 1 points/references, all 16 Figure 3 coefficients, all Figure 4 intervention records, code redistribution, selected supporting analyses, full current Figure 1 resampling, dense physical identities, gate maps and targeted original-generation replay. The [claim audit](CLAIM_AUDIT.csv) maps exact sources to outcomes. The component reports contain source lines, equations, commands and detailed support tables.

## 2. Findings ordered by severity

### F-01. Major: retained compact Checkpoint 04 numerical tables are inconsistent

**Evidence:** `studies/checkpoint_04/results/intervention_cross_architecture.csv:2–31`; `studies/checkpoint_04/results/response_stencil_decomposition.csv:2–16`; current endorsement at `studies/checkpoint_04/results/README.md:3–6` and `docs/EXTENDED_RESULTS.md:7–13`.

All 30 compact endpoint estimates disagree with corresponding original-row/consolidated-archive estimates. Ten of 15 compact stencil rows, the two non-Haar probes in all five families, also fail their own stated equality between reconstruction and observed contrast. All 15 compact reconstructions differ from independently reconstructed original-row values. These differences are much larger than rounding tolerances.

For the primary Floquet-Cartan/Z, locally dressed XY probe (`response_stencil_decomposition.csv:6`):

| Quantity | Value |
|---|---:|
| Compact table's component sum/reconstruction | -0.0800936164752 |
| Same row's claimed observed response contrast | -0.0985805295422 |
| Independent original-row result and archived consolidated result | -0.0770481378164718 |

The independent four-purity calculation agrees with the original-row direct response for all 45 checked run/family/probe endpoints. Thus this is a **supporting export/provenance defect, not a false response theorem**. Both an independent record reconstruction and a separate standard-library cross-check confirmed it. The exact cause of the compact export corruption has not been established; no unsupported explanation about its history is asserted.

The four canonical figures and their replayers do not consume these compact tables, so their passing results are unaffected. The qualitative alternate-probe signs also remain negative in the verified original records. But readers cannot trust the advertised quantitative compact extension or its purported exact accounting. See [Figure 1 and extensions](FIGURE1.md), [all discrepancies](results/figure1_compact_table_discrepancies.csv), [independent extension code](code/figure1_extensions.py), and [confirmed-defect tests](code/figure1_confirmed_defects.py).

**Certainty:** high, directly demonstrated. **Minimum repair:** either regenerate and provenance-bind these compact tables under explicit run, support, weighting and normalization, or retire their quantitative authority and route readers to verified archived results. Preserve the bad originals as clearly historical evidence if needed. Add record-to-export and stencil-equality regression coverage. No repair was implemented here.

### F-02. Major: direct equation-level antecedents are omitted

**Evidence:** `docs/RELATED_WORK.md:53–60,143–145`; `docs/THEORY.md:79–197,235–244,326–347`; acknowledged at `docs/PROJECT_GUIDE.md:23`.

Kuo, Akhtar, Arovas and You, [arXiv:1910.11351v2](https://arxiv.org/abs/1910.11351v2), Eqs. (19), (60), give the exact entanglement-feature transfer and general two-site operator. Akhtar and You, [arXiv:2006.08797v2](https://arxiv.org/abs/2006.08797v2), Eq. (20), gives the Haar transfer with coefficient `q/(q²+1)`, hence `2/5` for qubits. Their transfer row gives the same four input purities and, after translating operator-entanglement invariants, all four coefficients in this repository. Our rational translation verifies the equivalence without numerical tolerance. The current statement that an equivalent formula “may exist” must be replaced by the actual relationship.

The machinery and elementary stabilizer/sign consequences should be credited as established ingredients or direct deductions. The monitored fixed-spectrum redistribution and selected location comparisons remain distinct empirical evidence. A focused comparison should also discuss Fan et al. [2002.12385](https://arxiv.org/abs/2002.12385) on spatial measurement response and Rudziński et al. [2605.26867](https://arxiv.org/abs/2605.26867) on fixed-Schmidt-orbit response, with their different endpoints and assumptions. This does not license importing either paper's spatial law or channel results into the study.

**Certainty:** high about equation equivalence and missing attribution; no absolute priority conclusion. **Minimum repair:** add the equation-level dictionary and relevant endpoint distinctions at their use. See [literature audit](LITERATURE.md) and [exact translation](results/literature_translation.json).

### F-03. Completion requirement: editable external composite schematics are absent

**Evidence:** `docs/PROJECT_GUIDE.md:21–23`, historical design specifications under `studies/figure_design/`, and the complete tracked tree. The six numerical Python panels are present and reproduce. The separate schematic/composite elements described in the designs have no tracked editable source. No unseen Overleaf layout was examined.

**Consequence:** this blocks the stated goal of having all eventual figure components in the repository; it does not invalidate the numerical panels. **Certainty:** high for the audited tree. **Minimum repair:** obtain the author's actual editable assets and their source/provenance mapping, or explicitly decide which schematic components the eventual study retains. Do not fabricate replacements or infer approval from historical hashes.

### F-04. Moderate provenance/documentation gap: some historical availability statements are inaccurate

**Evidence:** `docs/DIALOGUE_REPORT.md:508` calls a full Checkpoint 04 archive preserved; `provenance/SOURCE_MIGRATION.md:7` describes selected members. `docs/RUN_HISTORY.md:43,57–60` refers to an original manifest and a preserved preflight-failure log absent from the baseline tree and 172-member root bundle. Actual original Figures 3/4 bootstrap invocation/seed manifests are not fully recorded in the retained execution provenance; defaults alone do not prove which invocation produced archived arrays.

All documented core commands nevertheless run from included data, and 27 bounded original-generation trajectories replayed successfully using recovered run labels and documented base seeds. This is not evidence of a missing input to the core workflows or a failed simulator. It is evidence that “all historical records are preserved” is too broad. Historical timestamps are internal assertions bound to text, not externally certified preregistration.

**Certainty:** high about absent files and inconsistent availability wording; original discarded execution details remain unknown. **Minimum repair:** replace references to unavailable full archives/logs with precise included-member paths and availability status; add explicit campaign command/seed recipes for future regeneration, marking unrecovered historical bootstrap invocations honestly. See [completeness](COMPLETENESS.md) and [simulator audit](SIMULATOR.md).

### F-05. Minor precision and reader issues

The Figure 3 derivative-style axis (`scripts/figures/make_figure_03.py:63`) is not the literal pooled fixed-effect estimator; the dialogue already acknowledges this at line 191. `src/boundary_susceptibility/response.py:4` calls the observable “Relative Renyi-2 response” although the correct numerical function is a purity-normalized linear-entropy response. `docs/THEORY.md:152–177` uses realignment without defining its indices; lines 195–197 can imply that two response invariants completely classify two-qubit gates, which they do not. `docs/RUN_HISTORY.md:90–98` and `docs/NUMERICAL_METHODS.md:215` use a short principal-stratum label less precise than their detailed explanation of the original variable-side endpoint. `docs/TRANSITION_CONTEXT.md` should consistently distinguish a negative monitoring coefficient from a negative response. One bibliography title is truncated.

**Certainty:** high for the observed text/numerical distinction; invariant classification is a wording ambiguity. **Minimum repair:** align the labels with existing precise definitions, define realignment, and reserve fixed-side joint-preservation terminology for the strict comparison. These are small corrections, not reasons for new campaigns or a redesign. See component reports for exact subfindings.

### F-06. Minor: one CI validator does not enforce its numerical failure flag

`studies/checkpoint_04/scripts/validate_gate_invariant_formula.py:27–32` computes `passes` but only prints/saves the result. `.github/workflows/tests.yml:41` runs that script without asserting the JSON flag. Thus a numerical discrepancy can leave this CI step green. The actual audit run returned `passes=true` with maximum error `1.17e-15`; this is a validation-enforcement defect, not a current wrong formula. Static control flow and an audit-only controlled fault-injection regression establish the diagnosis. **Certainty:** high. **Minimum repair:** return a nonzero exit status when the check fails and test that behavior. See [mathematical coverage closure](MATHEMATICS.md) and [regression](code/validator_confirmed_defect.py).

## 3. Why the central claims survive

### Mathematics

From the swap identity and input-purity normalization,

$$
\chi_{\rm rel}=\frac{D}{D-1}\left(1-\frac{\mathbb E P'_m}{P_m}\right),\qquad
\mathbb E P'_m=\frac25(P_{m-1}+P_{m+1}).
$$

The general two-copy operator is exact; the four-purity local-dressing stencil includes the noncontiguous `L union b` region and requires global purity only when replacing `P_Lab` with `P_R`. Identity, SWAP, product/Bell configurations and the stated Cartan probes agree. Newly generated Clifford representatives reproduce the Haar response operator independently of the archived gate bank. At fixed central stabilizer entropy the whole spectrum is flat and fixed; adjacent increments give the six response values from nine codes. The exact code regression decomposition is not additional independent statistical evidence.

For a central-spectrum-preserving single-site projective Pauli measurement on a pure stabilizer state, neither neighboring-cut entropy increases; subtracting the response identity proves nonpositive response change for each outcome of nonzero Born probability. Equality requires both neighboring purities unchanged. This is valid for the Haar/uniform-Clifford ensemble-averaged probe, not each gate. Independent dense tests covered 300 states, 9,820 nonzero-probability outcomes and 4,602 eligible outcomes without a violation. Explicit physical counterexamples demonstrate failure of overbroad generic-input, individual-gate and universal near/far-ordering versions. The baseline excludes those versions. See [mathematics](MATHEMATICS.md).

### Statistical designs and populations

| Figure | Estimand and sampling unit | Independent result and principal limit |
|---|---|---|
| 1 | Equal-cell high-minus-low response after rank-4 replacement; whole trajectory clusters across two times; run-specific discovery references and observed cross-run support fixed | All 60 reference spectra and ten points reconstructed; all ten current intervals below zero. Clifford uses four common cells and only 3–7 eligible high-rate trajectories per cell. No reference-selection/support uncertainty or simultaneous guarantee is supplied. |
| 2 | Same eligible rows and linear estimator applied to nine code indicators; representative n=256 projective Z | Response-weighted slopes reconstruct `-0.0521300363926`. Probability redistribution is empirical; reconstruction is algebraic and not independent replication. |
| 3 | Within `(tau,S_m)` fixed-effect coefficient per Δp=.02; eligible rate cells have ≥10 rows and strata ≥3 rates; trajectories cluster across times | All 16 coefficients recovered; all are negative with archived intervals below zero. Weights and rate support change with size/run. At n=256 in the replication campaign, p=.20 does not enter the primary estimator’s support. This is conditional finite-size evidence, not an unconditional causal effect or a demonstrated thermodynamic limit. |
| 4 | Post-minus-pre response and near-minus-far; alternative location interventions on one pre-state; eligible sides first, then pre-state and equal-cell means | Original conditional `-0.0474290225`; strict same-side `-0.0474737196`, fresh interval `[-0.0493378474,-0.0454699506]`. Strict selection retains 4,786 pre-states; common six-distance selection retains 4,025. Outcome signs do not affect these phase-free stabilizer endpoints. |

Figure 1's adopted 50,000-valid-draw procedure matches its recorded plan, including `eligible_union`, the all-confirmatory sensitivity, fixed references/support, whole-proposal empty-cell rejection, PCG64/SeedSequence and linear quantiles. Its new reproducible seed does not recover the missing historical bootstrap. An independent replay checked all 1,009,814 proposals, one million retained contrasts and 1,280 explicit row expansions, with maximum discrepancy `2.22e-16`. Repeated computational resamples do not increase physical sample support.

The Figure 3 overlap graph supports a local-overlap pooled coefficient, not every extreme-rate or adjacent-rate claim. An independent pairwise-cell estimator and explicit dummy-variable fit recover all coefficients; time and adjacent comparisons were also inspected. Some individual adjacent uncertainty can include zero. The 32 checked alternative size fits retain negative intercept intervals, but the primary random-Pauli locked-fit residual remains substantial (`Q≈16.78` on two nominal residual dimensions), and the finite-size estimand itself changes its support. No thermodynamic proof follows.

Figure 4's selected side sets differ between near/far on 1,619 of 4,790 original eligible pre-states; four have disjoint side sets. The strict same-side comparison addresses this concern and remains negative. The common-population magnitude of the response change at d=4 is 11.95% of the adjacent value, at d=8 it is 1.65%; at d=16 only five common-population trajectories have nonzero effects. This supports measured near-cut concentration, not a hard finite range or fitted physical localization length. Individual strict pairs can have positive near-minus-far difference, consistent with the baseline's distinction between a population effect and a sign theorem.

The current captions and long-form discussion already make most of these inferential restrictions explicit. Disclosure would not rescue an overbroad claim, but the retained core claims here actually respect the restrictions. Larger studies or stronger uncertainty guarantees are optional extensions unless stronger claims are sought.

## 4. Reproduction, independence and test adequacy

The clean environment uses Python 3.12.13 and the exact six numerical/plotting versions in `requirements-reproducible.txt`; all installed transitive versions are recorded. The documented commands, redirected only to audit or scratch outputs, passed: verification, baseline pytest, 18 figure exports, core-record replay, reassessment, full Figure 1 sampling/replay/adoption, study materialization, tableau/statevector and gate-invariant checks. [REPRODUCTION.md](REPRODUCTION.md) records actual commands, seeds, tolerances, timings, warnings and outputs.

The existing test suite passed **33 tests**; final default discovery passed **35 tests**, including two audit estimator tests. The separately invoked audit suite passed eight checks and recorded two strict expected failures, both confirmed as actual assertion failures when unmasked. The record replayer performed 156 checks over 237,600 scaling rows and 75,600 intervention rows. The supplied simulator comparison passed 256 cases exactly. Additional independent simulator checks covered all 11,520 gate matrices, all 720 support maps with multiplicity 16, bit boundaries through n=256, and 432 Born-rule/Kraus cases. Twenty-seven bounded archived trajectories reproduced 75 probe records and 42 intervention rows; this checks a portion of original generation, not all historical campaigns. All six regenerated PNGs were visually inspected, and current tests compare all 18 exports byte-for-byte to the baseline.

Hashes establish identity, not scientific truth. Several baseline tests check hard-coded signs, formula values or matching exports. The preserved original intervals are not fresh bootstrap simulations. The original source validators share some simulator helpers/gate data. Audit-only dense physics, alternative row estimators, exact rational computations and explicit counterexamples provide additional independence. Conversely, all archived-row reanalyses still share the original generated records. The missed F-01 tables illustrate why successful CI cannot stand in for the scientific audit. Confirmed-defect diagnostics intentionally expose failures of those table assertions; they must not be described as passing science tests.

## 5. What remains missing or unchecked, and stopping decision

Missing or requiring correction: F-01 compact supporting values/provenance; F-02 equation-level attribution and focused neighboring-work comparison; F-03 actual editable schematic sources; F-04 accurate historical availability/campaign recipes; F-05 small definition/label corrections; F-06 validator failure enforcement. [FIX_PLAN.md](FIX_PLAN.md) proposes the smallest adequate repairs in separate categories. None was applied to the baseline.

Not performed: complete rerun of every original large simulation or original Figures 3/4 bootstrap campaign; reconstruction of the unrecovered historical Figure 1 seed; exhaustive stabilizer enumeration; independent external replication; external certification of internal locks; unseen Overleaf/composite layout review; exhaustive literature priority proof. These are explicit limits, not checks reported as passed. The code, archived inputs and targeted generation checks establish the documented reproducibility scope without requiring a new full campaign in this audit.

**Claims surviving:** M1–M5 and T1 under their declared finite-system, input, probe, conditioning and population restrictions; L1 only as model-dependent checked-menu evidence. **Claims remaining rejected or unclaimed:** L2 physical single-exponential localization length, L3 new order parameter, unconditional monitoring-rate causality, universal individual spatial ordering, and generic non-Clifford thermodynamic conclusions. **Claims needing revision:** the quantitative authority of the retained compact Checkpoint 04 exports and the incomplete attribution/completeness statements. The audit stops with this report and repair plan.
