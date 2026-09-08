# Figures 2 and 3 independent audit

## Prospective calculation record

Written before this audit's new diagnostic calculations. The parent audit's
`PLAN.md` covers the frozen baseline and full scope. This component will read
the immutable original state tables directly through Python's ZIP reader,
without importing either original or current repository estimators.

Planned checks: reconstruct the 16 response coefficients using weighted
pairwise differences of rate-cell means within each `(tau,S_m)` stratum;
cross-check with an explicit dummy-variable weighted least-squares design;
reconstruct the nine Figure 2 indicator coefficients on identical support;
inspect nonnegative comparison weights, eligible trajectories, rate coverage,
and overlap connectedness; reproduce cluster standard errors directly from
trajectory score sums; inspect original bootstrap implementation and archived
arrays; replay the locked finite-size fits and fixed sensitivity menu from
fresh coefficients and archived bootstrap arrays; verify archived time and
adjacent-rate point estimates. Tiny synthetic tests will discriminate between
correct same-support regression and incorrect unweighted or pooled estimators.

No random-circuit campaign or full finite-size bootstrap campaign is planned.
The archive and stored entropies remain substantive shared dependencies; this
checks record-to-estimate arithmetic, not independent physical generation.
Expected resources: a few minutes, well below 1 GB RAM, one process. These
checks use no random seeds unless a deterministic synthetic example requires
one. Uncertainty reusing archived bootstrap arrays will be explicitly labeled.

Findings and executed commands will be appended after calculations.

### Coverage amendment before secondary calculations

At the parent auditor's request, extend the record checks to all 16 secondary
unnormalized coefficients and four locked secondary intercepts, eight archived
fixed-0.27 hinge point fits/interval arrays, and quarter-partition tripartite
information means and crossing point estimates. This closes the retained
appendix E5/G claims; it does not fit a new hinge, choose a new breakpoint, or
launch a new simulation/bootstrap campaign. The crossing interval tables will
be inspected as archived output, not labeled independently regenerated.

## Verdict for this component

The central Figure 2 arithmetic and Figure 3 finite-size conclusions survive.
No defect in their record-to-estimate calculation was found. Figure 2 is an
exact linear decomposition of Figure 3's representative coefficient, not an
independent sample or experiment. The claimed finite-size sign replication is
supported under the declared selection rule. A thermodynamic limit is still
conditional on an extrapolation model and on a sequence of changing selected
populations. Two small, concrete presentation corrections are warranted below.

### F23-1: one current page confuses response with monitoring coefficient

**Minor scientific documentation defect; diagnosis certain.**
`docs/TRANSITION_CONTEXT.md:9–12` says the fixed-spectrum response remains
negative on both sides of the crossing. The checked negative quantities are
monitoring coefficients, not the response itself. The current dialogue states
the distinction correctly at `docs/DIALOGUE_REPORT.md:452–458`.

A counterexample exists in the actual primary selected support:
projective Z, `n=256`, `tau=10`, `S_m=0`. The rate-0.26 cell has 11 rows with
mean response `+0.2909091`; rate 0.28 has 50 rows with mean `+0.328`. This
stratum has five rate cells meeting the ten-row threshold. Both cells are
eligible in the primary regression. Their individual responses are all
positive. See `results/figures23_positive_response_example.csv`.
For any pure stabilizer state with `S_m=0`, both entropy increments belong to
`{-1,0}`, so the response alphabet is strictly positive. No noise fluctuation
is needed for this counterexample.

**Smallest repair:** replace “fixed-spectrum response remains negative” with
“the fitted within-spectrum monitoring coefficients remain negative” and
retain the secondary/model-dependent description of the hinge analysis.
No data or figure point needs changing.

### F23-2: Figure 3 labels a finite-grid projection as a derivative

**Minor notation defect; diagnosis certain.**
`scripts/figures/make_figure_03.py:63` labels the ordinate
`beta_n = partial chi_rel / partial(p/0.02)`. The estimator at
`studies/checkpoint_05/scripts/analyze_checkpoint05.py:15–51` is one pooled
linear fixed-effect coefficient on observed support. It is neither a
pointwise derivative nor a separately identified constant effect at every
rate. `docs/DIALOGUE_REPORT.md:191` already acknowledges this mismatch.

**Smallest repair:** use “within-spectrum coefficient per Delta p=0.02” (or
just `beta_n`, with that definition in the caption). The finite-size points,
uncertainty, model lines, and layout can remain.

### F23-3: important inferential limits are real and largely disclosed

**Known limitations, not newly discovered blocking defects.**
The actual sampling unit is a physical trajectory, with three time records
at `tau=6,8,10`. The 50,000 Figure 1 resamples have no bearing on the Figure 3
physical sample count. Figure 3 has 57,600 primary and 21,600 replication
trajectories overall. No calibration trajectories enter these fits.

At fixed protocol and size, the population is the conditional monitored
Clifford ensemble represented by retained `(tau,S_m,p)` cells. Counts of at
least ten are imposed per cell, then at least three retained rates per
`(tau,S_m)` stratum. Rows in a below-threshold rate cell are excluded even if
its entropy stratum otherwise qualifies. The fit uses equal record weights,
not equal stratum weights or equal cell means. Its extrapolation therefore
does not follow one common fixed-spectrum population through size.

The pairwise implementation makes the identification explicit. If `s` denotes
`(tau,S_m)`, `N_sp` is a retained cell count, `N_s=sum_p N_sp`,
`x_p=(p-.26)/.02`, and `ybar_sp` is its response mean, then

$$
\widehat\beta_n=
\sum_{s,p<q}\omega_{spq}
\frac{\bar y_{sq}-\bar y_{sp}}{x_q-x_p},\qquad
\omega_{spq}\propto
\frac{N_{sp}N_{sq}}{N_s}(x_q-x_p)^2.
$$

All these comparison weights are nonnegative and sum to one. Thus the
negative coefficient is an actual weighted within-spectrum difference, not
an artifact of negative regression weights. A nonzero coefficient establishes
that not every retained within-spectrum conditional mean is rate-invariant.
It does not establish individual monotonicity, a universal derivative, or an
unconditional causal effect of assigning long-run monitoring probability.

The rate-overlap graphs are connected on the rates that enter each fit. But
no stratum spans all nine rates already at `n=128`, and at `n=256` the largest
strata cover seven rates in primary and six in replication. The replication
primary estimator excludes `p=.20` entirely at `n=256`. The primary fit retains
only 84 projective-Z and 51 random-Pauli trajectories there, from 800 sampled
per cell; pairs touching that rate carry about 0.568% and 0.401% of total
comparison weight. These are concrete examples of the limitation disclosed
at `docs/NUMERICAL_METHODS.md:151–154`,
`docs/EVIDENCE_REASSESSMENT.md:75–77`, and
`docs/CLAIM_EVIDENCE_MAP.md:9–10,20`.

As a planned support diagnostic, restricting both runs to their shared
eligible rate/spectrum cells retains negative `n=256` point coefficients:
primary/replication projective Z `-0.0510554/-0.0455090` and random Pauli
`-0.0502437/-0.0521451`. This is not a fresh inferential endpoint: record-count
weights still differ and no new interval was calculated. See
`results/figures23_shared_run_support.csv`.

All 16 finite-size coefficients and their plotted pointwise percentile
intervals are below zero; coefficients range from `-0.0522284` to
`-0.0274694` per `Delta p=.02`. All 48 archived time-specific coefficients
and intervals are negative, after independently replaying their distinct
five-row cell threshold (`analyze_time_sensitivity.py:16–18`). This supports
the late-time finite-size claim under the tested design, not all times or
ensembles. Of 128 adjacent-rate coefficients, two point estimates are
positive and 23 intervals cross zero. At `n=256` all 32 point estimates are
negative, but the replication Z `.24→.25` interval crosses zero. The main
retained claim does not incorrectly require every adjacent contrast to be
significant. See `results/figures23_adjacent.csv` and
`results/figures23_time_sensitivity.csv`.

### F23-4: original uncertainty and finite-size models

**Supported within scope; broadening the claim would require revision.**
The source clusters all eligible time rows from one trajectory, resamples
trajectory IDs separately within each rate, and recomputes weighted stratum
means for each draw (`analyze_checkpoint05.py:45–74`). The bootstrap pool
contains only trajectories with at least one retained row. The observed
eligibility mask is fixed, and selected sample sizes by rate are conditioned
upon. Unlike the current Figure 1 sampler, this source does not reject an
entire proposal merely because a particular rate/stratum cell becomes empty;
zero-weight strata drop out of its weighted normal equations. Only a
nonfinite whole-fit draw would be omitted. The archived primary arrays have
2,000 valid draws per endpoint. These are bootstrap draws, not new
trajectories. The intervals do not cover the uncertainty of discovering the
observed support or selecting the threshold rule. They are pointwise, not
simultaneous across every size, rate comparison, code, and analysis.

The cluster score calculation independently reproduces every reported
secondary cluster standard error. The source's small-sample multiplier is
that of the one-column absorbed fit; charging degrees of freedom for all
absorbed intercepts increases these standard errors by at most 0.2542% in
the 16 datasets. This is a convention-level sensitivity and does not alter
the primary percentile intervals. It is not a load-bearing defect.

The locked size fit uses `CI_width/3.92` as its diagonal standard-error
estimate, four sizes, fixed exponent 1, and fixed weights when propagating
the archived size bootstraps (`analyze_checkpoint05.py:127–140`). Independent
replay gives:

| Run | Protocol | Intercept | Original pointwise interval | Residual Q (2 dimensions) |
|---|---|---:|---|---:|
| Primary | Projective Z | -0.0517583 | [-0.0545343,-0.0488976] | 5.2134 |
| Primary | Random Pauli | -0.0531901 | [-0.0558561,-0.0505010] | 16.7832 |
| Replication | Projective Z | -0.0491629 | [-0.0533977,-0.0446687] | 0.7439 |
| Replication | Random Pauli | -0.0519658 | [-0.0565252,-0.0473612] | 1.5773 |

The 32 post-hoc alternatives were also independently replayed, including
their different weight convention, the standard deviations of archived
bootstrap arrays (`scripts/analysis/reassess_evidence.py:254–272`). Their
intercepts range from `-0.0664751` to `-0.0444571` and all intervals stay below
zero. Model noise, choice, and changing support are not propagated by simply
resampling finite-size estimates. The primary Pauli residual is substantial;
none of these finite menus proves a thermodynamic limit. The current
README, dialogue, and reassessment correctly retain that boundary.

An initial audit implementation applied the locked CI-width weights to the
entire alternative menu. It gave a slightly different range
`[-0.0663685,-0.0444590]`; no source defect was inferred. Reading the source's
explicit weight switch resolved the discrepancy, and the final audit code
now compares all 36 models with the actual reassessment table. The initial
audit-only results are retained in
`results/figures23_initial_ci_weight_models.csv` for transparency and are not
the current sensitivity replay.

### F23-5: Figure 2 ordering, values, and independence

**Pass.** `make_figure_02.py:20–28,39–42` implements rows
`delta_L=+1,0,-1`, columns `delta_R=-1,0,+1`. Its exact response values with
`D/(D-1)` removed are

| delta_L \\ delta_R | -1 | 0 | +1 |
|---|---:|---:|---:|
| +1 | 0 | -0.2 | -0.6 |
| 0 | +0.4 | +0.2 | -0.2 |
| -1 | +0.6 | +0.4 | 0 |

The central peak/dip corner annotations have the correct signs. Finite-size
normalization is retained in response coefficients; at `n=256` it is
indistinguishable from one in binary64. All nine displayed primary-Z
probability slopes at `n=256` match the independently fitted indicators.
Their sum is zero, and the response-weighted sum is `-0.0521300363926` on
17,630 eligible rows from 6,360 trajectories. The reconstruction is true for
all 16 groups and 144 indicator fits. The six nonzero high-/low-response
outer codes exhibit the displayed redistribution with archived pointwise
cluster intervals excluding zero. Several other code intervals cross zero;
the matrix is not nine independent observations.

The empirical result is the fitted change in code frequencies. The weighted
response reconstruction follows exactly by linearity on identical support
and weights (`analyze_boundary_code_decomposition.py:24–38`). It must not
be counted as a second statistical replication. The active caption and
dialogue say this correctly (`DIALOGUE_REPORT.md:165–169,353–363`). Rounding
the matrix labels to three digits cannot preserve machine-precision sums.

### F23-6: secondary observable and transition context

**Pass for retained bounded claims; contextual caveats apply.**
All 16 unnormalized `chi_2` slopes, their archived percentile intervals,
and four locked secondary intercepts were independently reconstructed from
raw neighboring purities. They are negative. The primary-Z intercept is
`-0.0095798352`, interval `[-0.0104444562,-0.0087047856]`, agreeing with
`DIALOGUE_REPORT.md:402–404`. Within one spectrum stratum, dividing by its
fixed purity preserves the sign. Across heterogeneous strata the pooled
linear and relative coefficients have different effective purity factors;
one cannot convert them using a single overall average purity.

The eight archived hinge fits use at least four eligible rates per stratum,
cell threshold ten, and regress both a linear rate term and a positive-part
term at `.27` (`analyze_transition_crossover.py:9–20,33–50`). An independent
full dummy-variable fit reproduces all eight pairs of coefficients, selected
row counts, and original interval-array quantiles. All changes in slope have
positive pointwise intervals while slopes on both sides remain negative.
Primary Z at `n=256` gives `-0.11227216` below and `-0.03851005` above,
consistent with the reported rounded values. This is a secondary descriptive
piecewise-linear fit, not evidence for a singularity or universal exponent.

All 79,200 late-time quarter-information rows were reconstructed by the
seven-entropy inclusion-exclusion expression, then every rate-cell mean and
all 12 size-pair crossing points were replayed. The four `128/256` crossings
range from `.2674286` to `.273125`, supporting the contextual “near .27.”
These are an independent observable on the same physical trajectories, not
an independent dataset. Source `analyze_checkpoint05.py:87–124` restricts
candidate crossings to the interval `[.235,.295]` and selects the candidate
nearest `.26`; this is not an unconstrained search for a thermodynamic
critical point. Replication Z at `64/128` has two candidates,
`.2675` and `.2757143`. Its archived bootstrap keeps only 84.4% of proposals
that yield a crossing, so its percentile interval is conditioned on crossing
existence in the chosen window. This does not undermine the narrowly stated
high-size context, but these intervals must not be promoted into precise,
unconditional critical-point inference.

## Executed checks, independence, and remaining coverage

Commands used the root audit's clean pinned environment, Python 3.12.13,
NumPy 2.3.5 and pandas 2.2.3:

```bash
/workspace/scratch/0174ee249694/audit-venv/bin/python audits/full-sanity-01/code/figures23_audit.py --root . --output audits/full-sanity-01/results
/workspace/scratch/0174ee249694/audit-venv/bin/python audits/full-sanity-01/code/figures23_secondary.py --root . --output audits/full-sanity-01/results
/workspace/scratch/0174ee249694/audit-venv/bin/python -m pytest -q audits/full-sanity-01/code/test_figures23_audit.py
```

The final primary script passed 416 numerical comparisons in 9.92 seconds,
peak RSS 540,924 KiB. The secondary script passed 76 comparisons in 3.04
seconds, peak RSS 481,176 KiB. Two synthetic estimator tests passed in 0.47
seconds. Logs are `results/figures23_run.log`,
`results/figures23_secondary.log`, and `results/figures23_tests.log`.
No warnings or failed execution occurred. No RNG draws, physical simulations,
or new uncertainty intervals were generated in this component. Source CSV
rounding is allowed up to `1e-11`; original record identities use tighter
`1e-12`/`1e-15` tolerances; exact count and integer identities use zero tolerance.
Maximum discrepancy across the final primary comparisons was
`5.50e-12` (a residual diagnostic, not a coefficient error). The summary JSONs
record per-check tolerances and input-member hashes.

The two audit programs import no repository analysis or simulator code. The
primary estimator uses pairwise rate-cell contrasts, cross-checked against
an explicit dummy-variable regression. Secondary code imports the
audit-owned selection/pairwise implementation only. ZIP bytes and hashes
are checked using Python standard-library code against the manifest. All
237,600 original state response records are reconstructed from stored
entropies. This is independence of the estimator implementation, not of the
archived circuit outcomes or the theoretical neighboring-purity identity.

Original finite-size and hinge bootstrap arrays were replayed; they were
not regenerated from resampling seeds. Original crossing resample arrays
are not included in the root bundle (the generator does not save `pcboot`
at `analyze_checkpoint05.py:214,223–228`); crossing interval tables were
inspected and copied with explicit labels, not claimed independently
regenerated. The actual historical seed used for each Figure 3 resampling
campaign has not been established by this component. A default analyzer
seed is present at line 193, but a code default alone is not provenance of
an actual run. The parent audit handles whole-repository provenance and
small simulator/gate verification. No large physical generation campaign
was repeated here, and no thermodynamic limit or continuous monitoring-rate
derivative was tested.

## Source coverage ledger for this component

The following current sources were read for the Figures 2/3 assessment:

- `README.md` (current Figure 2/3 and scope sections);
  `docs/NUMERICAL_METHODS.md`; `docs/EVIDENCE_REASSESSMENT.md`;
  `docs/SCIENTIFIC_STORY.md`; `docs/FIGURE_BASELINE.md`;
  `docs/REPRODUCTION.md`; `docs/TRANSITION_CONTEXT.md`;
  `docs/CLAIM_EVIDENCE_MAP.md`; `results/core_claims.csv`;
  `docs/DIALOGUE_REPORT.md` (M4–M7, D, E, G, H and source list);
  `docs/DIALOGUE_QUESTION_MAP.md`; `figures/README.md`.
- `scripts/figures/make_figure_02.py` and `make_figure_03.py`;
  `scripts/analysis/reproduce_core_records.py` (Figures 2/3 workflow);
  `scripts/analysis/reassess_evidence.py` (source adapter, FE, size workflow).
- `studies/checkpoint_05/scripts/analyze_checkpoint05.py`;
  `analyze_boundary_code_decomposition.py`; `analyze_finite_size_sensitivity.py`;
  `analyze_time_sensitivity.py`; `analyze_transition_crossover.py`;
  `run_tableau_scaling.py` (trajectory identifiers, record and seed plumbing).
- `studies/checkpoint_05/design/PRIMARY_SCALING_DESIGN_LOCK_BEFORE_RUN.md`;
  `INDEPENDENT_REPLICATION_LOCK_BEFORE_RUN.md`;
  `studies/checkpoint_05/notes/RUN_HISTORY_AND_PROTOCOL_DEVIATIONS.md`;
  `requirements-reproducible.txt`;
  `src/boundary_susceptibility/records.py`; `data/record_bundle_manifest.json`;
  both canonical Figure 2/3 CSVs; the current finite-size reassessment CSV.

Original archive members actually read are enumerated with SHA-256 hashes in
`results/figures23_summary.json` and `results/figures23_secondary_summary.json`.
These include both complete scaling state tables, original size and adjacent
analysis tables, original size and hinge resample arrays, time tables,
secondary limit tables, and crossing tables. Historical source fit language
is not adopted as a current scientific claim.
