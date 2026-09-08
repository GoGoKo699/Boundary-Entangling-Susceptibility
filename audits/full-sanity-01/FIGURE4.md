# Independent Figure 4 audit

Audit target: `00009cf7cc02104e4c776863b3ea551bd38e00f4`. All calculations here were covered by the initial audit plan. No scientific baseline file was changed. The independent record calculation ran on Python 3.12.13, using only the standard library, in about two seconds. The scientific independence and unperformed checks are stated below.

## Verdict

**M5 survives as the stated empirical, selected-population result.** The original before/after response, near-minus-far estimates, equal-cell pooling, stricter same-side result, common-population profile, and support counts reconstruct independently. No mathematical, computational, or inferential defect that overturns Figure 4 was found. The active interpretation correctly distinguishes the nonpositive individual-measurement response from the empirical spatial ordering, and rejects a localization length or exponential law.

There is one minor terminology inconsistency: the unqualified instruction to call the original intervention a “principal-stratum” effect is less precise than the current detailed eligibility definitions. It should distinguish the original eligibility-dependent side averages from the fixed-side joint-preservation contrast. This is a small documentation repair; the current detailed report and replacement caption already provide the qualifications needed for the retained conclusion.

## Independent calculation and results

`code/figure4_independent.py` reads the two compressed CSV members directly with `zipfile`, `gzip`, and `csv`. It imports no repository scientific code, Pandas estimator, NumPy estimator, or prior replayer. Responses and all averaging steps use exact rational arithmetic. It verifies the entire bundle hash and records both input-member hashes. It reconstructs each response from the three cut entropies, using

$$
P_j=2^{-S_j},\quad \overline P'_m=\tfrac25(P_{m-1}+P_{m+1}),\quad
\chi_2=\frac{2^{n/2}}{2^{n/2}-1}(P_m-\overline P'_m),\quad
\chi_{\mathrm{rel}}=\chi_2/P_m.
$$

The postmeasurement response divides by the postmeasurement state's input purity; the premeasurement response divides by the premeasurement state's input purity. Their difference is the plotted measurement-induced response change. On the conditional branch these purities are equal. This is neither a sampled response to one particular fresh gate nor an average logarithmic entropy change.

| Check | Fresh result |
|---|---:|
| Pre-states, unique identifiers | 5,400 |
| Valid location records, unique state/distance/side keys | 75,600 |
| Records at n=64 / 128 / 256 | 21,600 / 25,200 / 28,800 |
| Maximum pre-state response discrepancy | 1.943e-16 |
| Maximum post-minus-pre discrepancy | 2.220e-16 |
| Deterministic interventions, all entropy/response changes zero | 23,157 |
| Original unconditional mean | +0.07140740741318075 |
| Original conditional mean | -0.047429022532922346 |
| Strict same-side mean | -0.04747371958652684 |
| Strict eligible side pairs / pre-states | 7,945 / 4,786 |
| Common eligible side/pre-state combinations / pre-states | 6,008 / 4,025 |

The exact record calculation also checks all three entropy changes are in `{0,-1}` and every spectrum-preserving row has nonpositive response change, with equality exactly when both neighboring entropies are unchanged. This is a complete check of the archived records, **not** an independent universal proof or a new physical trajectory campaign. The mathematical proof is assessed separately in the mathematical audit.

The archived entropy records and Haar transfer identity remain substantive shared inputs. Reimplementing their analysis does not independently validate the original 5,400 large tableaus or their sampled circuit histories. The simulator review and small-system checks address those separately.

## Estimands, sampling, selection, and weighting

The input population is a separate projective-Z monitored Clifford campaign: n=64,128,256; p=0.20,0.26,0.34; 600 independent trajectories in each of nine cells; one snapshot at tau=10; base seed 2026082501. Current methods specify this at `docs/NUMERICAL_METHODS.md:202–223`. The source task seed includes run label, base seed, protocol, n, p, and trajectory index (`studies/checkpoint_05/scripts/run_tableau_scaling.py:33–41`). Unlike Figures 1 and 3, Figure 4 contributes one pre-state time per trajectory, so there are no repeated probe-time observations in this endpoint.

Each requested distance is evaluated on both copies where geometrically valid, with left site `m-1-d` and right site `m+d`. The source explicitly copies the tableau before each measurement (`studies/checkpoint_05/scripts/stabilizer_tableau.py:333–374`). No location intervention changes the input of another location intervention. Every raw record was checked against that geometry and against the full expected site set for its size. Invalid distances are absent rather than treated as zero effects.

All records use the Z axis. The phase-free update returns whether the measurement is deterministic or random; it does not store sampled signs (`stabilizer_tableau.py:110–142`). For these pure stabilizer inputs, a nondeterministic single-site Pauli measurement has two equiprobable outcomes with the same phase-free support and hence the same three entropies. The purity endpoints and eligibility are therefore outcome independent, while deterministic measurements leave the support unchanged. No Born weights are missing from this particular endpoint. This statement does not extend to non-Pauli measurements, nonstabilizer states, or sign-sensitive observables; the active explanation has that restriction (`docs/DIALOGUE_REPORT.md:414–426`).

The original conditional endpoint is reconstructed as follows:

1. Retain each state/location/side record only if its central entropy change is zero.
2. At each distance, average over the remaining sides within that pre-state.
3. Within that pre-state, subtract its eligible far-distance mean from its eligible d=0 mean; retain the pre-state only if both means exist.
4. Average these paired contrasts within each `(n,p)` cell, then average the nine cell means with weight 1/9 each.

This is exactly the original source implementation (`studies/checkpoint_05/scripts/analyze_measurement_location.py:14–37,48–66`), the current methods, and `docs/EVIDENCE_REASSESSMENT.md:19–33`. For this actual distance grid the far set contains **one distance per size**, namely d=16,32,64 for n=64,128,256 respectively. Thus “average eligible far interventions” versus “average sides and then distances” cannot introduce a weighting difference in this archive. A hypothetical multi-distance far grid would require more care, but is not a defect of these results.

The original endpoint retains 4,790 pre-states, 519–553 per cell. Eligible near/far side sets differ for 1,619 of those pre-states and are disjoint for four. The active account explicitly discloses that different sides can survive. The original conditional estimator is not an average over all trajectories or a fixed-side paired treatment contrast. Its inferential population is selected by the existence of both eligible averages. Equal-cell pooling estimates an equally weighted mixture of the nine cell-specific selected means, not a pooled selected-individual mean with sample-count weights.

The strict comparison fixes a side and requires both its d=0 and d=n/4 measurements to preserve the central spectrum. It averages eligible side differences within pre-state before averaging within cell and across cells. This identifies a well-defined joint-preservation principal-stratum effect because both potential interventions are actually computed on the same pre-state. The complete potential-outcome information in simulation avoids the usual unobserved-stratum identification problem; it does not identify a broader population effect. The strict checks are post-hoc and concern a different selected estimand, as documented (`docs/EVIDENCE_REASSESSMENT.md:23–33`; `docs/DIALOGUE_REPORT.md:438`).

Every cell-specific conditional and strict mean is negative. Independent values, sample sizes, and numbers of positive/zero/negative pre-state contrasts appear in `results/figure4/figure4_endpoints_by_cell.csv`.

## Distance profile and uncertainty

The left panel is post-minus-pre at each distance, **not** near-minus-far. Its original eligible population changes with distance. Both facts are correct in the active dialogue (`docs/DIALOGUE_REPORT.md:225–244`) and approved caption (`docs/FIGURE_BASELINE.md:25–27`). The historical figure specification still calls the curve relative to a far measurement and promotes an exponential; that file begins with an explicit historical/superseded notice and is not authoritative (`studies/figure_design/FIGURE_04_SPEC.md:1`). The active generator reads only the data CSVs and never reads or fits the historical decay parameter (`scripts/figures/make_figure_04.py:14–25,40–42`).

The independent common-eligibility calculation requires all six displayed interventions at a fixed side/pre-state to preserve central entropy **before** averaging. It yields:

| d | Original mean | Original pre-states / nonzero | Common mean | Common pre-states / nonzero |
|---:|---:|---:|---:|---:|
| 0 | -0.0475146573 | 4,790 / 1,724 | -0.0548615080 | 4,025 / 1,488 |
| 1 | -0.0437093851 | 5,230 / 1,186 | -0.0489772508 | 4,025 / 923 |
| 2 | -0.0184610996 | 5,340 / 555 | -0.0221013849 | 4,025 / 388 |
| 4 | -0.0053992612 | 5,390 / 176 | -0.0065560623 | 4,025 / 119 |
| 8 | -0.0011111111 | 5,400 / 39 | -0.0009036075 | 4,025 / 20 |
| 16 | -0.0002777778 | 5,400 / 8 | -0.0002814912 | 4,025 / 5 |

The common-population magnitude ratios are 11.9502% at d=4 and 1.64707% at d=8, agreeing with the current reported 11.95% and 1.65%. These are ratios of equal-cell pooled means, not average individual ratios. The complete common population removes distance-dependent eligibility as an explanation for this particular pooled attenuation pattern. It does not remove initial state selection or establish a law at unmeasured distances.

The original analysis resamples whole pre-states within each cell. Original endpoints resample already retained paired pre-state values; the original curve jointly samples all its distance values and masks from a trajectory pivot (`analyze_measurement_location.py:40–66,87–107`). This preserves location dependence and avoids treating the 75,600 records as independent trajectories. Its percentile intervals have 5,000 draws. There are 600 pre-states per original curve cell and hundreds eligible at d=0; although the source permits `nanmean` to drop an empty cell in a bootstrap replicate, the probability of resampling no eligible d=0 records at the worst observed cell is `(81/600)^600`, approximately 10^-522. This implementation policy is therefore immaterial at the actual support and 5,000-draw budget, not a Figure 1-style sparse-cell concern.

The current reassessment separately clusters retained pre-states for original, strict, and common selected populations, preserves all distances jointly, and pools cells equally (`scripts/analysis/reassess_evidence.py:107–158,165–239`). It gives pointwise percentile intervals and explicitly separate simultaneous six-mean bands. Its root audit replay supplies the fresh 5,000-draw run with seed 2026090501; this independent exact-record script intentionally does not duplicate that resampling or claim to regenerate the historical arrays.

Tail limitations are real: just five common-population pre-states have a nonzero d=16 effect. A percentile interval below zero there is not strong evidence for a general tail law or simultaneous significance. The current document reports that the simultaneous band crosses zero and refuses both strict finite support and a localization length (`docs/EVIDENCE_REASSESSMENT.md:37–60`). No correction to that restrained interpretation is needed.

## Individual ordering versus population effect

The records include two positive strict **individual** same-side near-minus-far contrasts. Both occur at n=64, p=0.20, side -1, trajectories 326 and 455: the d=0 change is zero and the d=16 change is `-0.40000000009313225`, so near-minus-far is positive. Their exact record keys and values are saved in `results/figure4/figure4_positive_individual_pairs.csv`.

These are useful checks against accidentally strengthening the claim. They do not contradict the nonpositive sign of either individual measurement response, nor the strongly negative selected-population mean. The active report already says two nonpositive responses need not have negative difference (`docs/DIALOGUE_REPORT.md:221`) and does not assert pointwise spatial ordering. Therefore this is a confirmed scope boundary, **not a baseline scientific defect**. Since these examples come from archived entropy records, their physical provenance shares the original simulator until independently regenerated.

Neither original nor strict Figure 4 estimates the effect of assigning the long-run monitoring rate. It does not quantitatively derive the Figure 3 conditional rate coefficient. These restrictions are explicit in `docs/SCIENTIFIC_STORY.md:35–43`, `docs/CLAIM_EVIDENCE_MAP.md:11,16`, and `results/core_claims.csv`, M5 and T1. The effects from different selected populations need not match numerically. The positive unconditioned and negative conditioned bars must not be read as a causal mediation decomposition; the active caption does not make that claim.

## Finding and minimum repair

**F4-DOC-01, minor documentation, high certainty.** `docs/RUN_HISTORY.md:90–98` recommends “paired causal effect of measurement location within a principal stratum” without distinguishing the original side-selection rule from the strict same-side rule. `docs/NUMERICAL_METHODS.md:215` similarly calls the original endpoint a primary principal-stratum contrast before specifying the more nuanced selection at lines 217–218. The independent calculation confirms different near/far eligible side sets on 1,619 pre-states, including four disjoint sets. The original result can be interpreted through state-dependent eligible-side interventions, but is not itself a fixed-side jointly preserving pair. The current long-form discussion and strict result already resolve the substantive inferential issue.

**Smallest repair:** change those short labels to “paired measurement-location contrast under the stated eligibility rule,” reserving the fixed-side principal-stratum label for the strict same-side check; link the existing precise methods. Preserve data, estimates, figures, and the distinction between original and post-hoc checks. No new simulation or redesign is needed.

## Coverage and remaining limits

Covered here: current methods/claim/caption chain; original intervention and analysis source; design scope; raw geometry; all input/output response records; sampling unit, outcomes, normalization, eligibility, weights, original and strict endpoints, common-distance profile, effect sizes and sparse support; seed construction; original and fresh bootstrap algorithms by inspection; explicit exclusions of pointwise ordering and spatial laws. Supporting files contain exact numeric outputs and the reproducible command below.

Not performed in this subtask: fresh large-system trajectory generation; reproduction of stored preflight-failure logs or original wall-clock timing; rerunning the original 5,000-draw bootstrap campaign from its RNG seed; checking an unseen external composite schematic or Overleaf layout. The repository-wide audit separately runs documented fresh reassessment and archived interval replay, reviews small-system simulator equivalence, and assesses source completeness. This report must not be read as passing any of those checks merely by association.

```bash
/workspace/scratch/0174ee249694/audit-venv/bin/python \
  audits/full-sanity-01/code/figure4_independent.py \
  --output audits/full-sanity-01/results/figure4
```

The full stdout is in `logs/figure4_independent.log`. An initial exploratory attempt to locate `checkpoint_05/data/measurement_location_intervention/simulation_manifest.json` in the consolidated bundle raised a `KeyError`; that optional historical manifest is not a member. The audit then used the actual archived records plus retained methods and source. This did not affect the calculations or get reported as a passed manifest check.
