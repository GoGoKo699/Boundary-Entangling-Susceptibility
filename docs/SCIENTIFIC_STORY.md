# Scientific story

## What is the question?

The Schmidt spectrum tells us how much bipartite entanglement is already present at one cut. The question here concerns a response: does that same spectrum determine the average change produced by an independent fresh gate crossing the cut?

For the purity-normalized linear-entropy response used in this project, the answer is no. The spectrum does not specify how the Schmidt vectors occupy the boundary sites and the interiors of the two halves.

A four-qubit example makes insufficiency concrete. Across `12|34`, the product state `|0000>` and the product of two Bell pairs, one inside `12` and one inside `34`, both have central spectrum `(1,0,0,0)`. The neighboring purities are `(1,1)` in the first case and `(1/2,1/2)` in the second. Substitution in the exact formula gives relative responses `4/15` and `4/5`. This is an explanatory example, not a novelty claim.

## What does the exact mechanism add?

A two-copy swap calculation expresses the average post-probe purity exactly. For a Haar or uniform two-qubit Clifford probe, the relative response is

$$
\chi_{\mathrm{rel}}=\frac{D}{D-1}\left[1-\frac25\frac{P_{m-1}+P_{m+1}}{P_m}\right],\qquad D=2^{n/2}.
$$

Thus the central spectrum fixes only one of the three required purities. The complete theory also treats locally dressed fixed two-qubit gates using four purity features. The [theory document](THEORY.md) separates these exact identities from empirical claims about monitored ensembles. Neighboring-cut purities are not synonymous with information contained in a small physical window.

The response is derived from normalized linear entropy, then divided by the input central purity. It must not be confused with the expectation of the finite change in logarithmic Renyi-2 entropy.

## What do the monitored-state data show?

Figure 1 applies a common central spectrum while preserving state-dependent Schmidt vectors. The held-out endpoint contrasts are negative across five tested state-generation families and a separate seed. This diagnostic controls eigenvalues, but it is not offered as an experimentally physical spectrum-replacement operation.

The physical stabilizer arm removes that objection. A stabilizer reduced state has a flat nonzero spectrum, so fixing the integer central entropy fixes the complete spectrum. Figures 2 and 3 compare naturally generated states within the same size, probe-time, and central-spectrum strata. The response depends on the two adjacent entropy increments, giving a finite nine-code description. Monitoring changes the conditional distribution of those codes.

An archived-row replay independently reconstructs all 16 finite-size monitoring coefficients from 237,600 stored state records. Their negativity persists through 256 qubits. The independent seed is a repeat of the simulation campaign, not an independently developed simulator or an external replication.

The fitted points at infinity in Figure 3 require an additional modeling step. Fixed-menu sensitivity fits retain negative intercepts, but the primary random-Pauli series shows a substantial residual under the locked inverse-size model. Sampling intervals do not account for every possible finite-size correction, and the exact-spectrum support can vary with size. The measured finite-size effect and the extrapolated limit must therefore remain distinct claims.

## What is controlled in the measurement-location intervention?

The same pre-state is copied and measured at different locations. On eligible interventions with unchanged central entropy, its complete central stabilizer spectrum is preserved. The original analysis averages eligible sides at each distance before pairing near and far means. Its negative pooled near-minus-far contrast is reproduced from the archived intervention records.

A stricter post-hoc analysis compares the same side and pre-state, requiring both near and far interventions to preserve the spectrum. Its pooled contrast is `-0.04747`, with a fresh 95% interval `[-0.04934,-0.04547]`. A separate common-eligibility profile holds the side/pre-state sample fixed across all six displayed distances. It retains strong near-cut concentration: the magnitude at four sites is about 12% of the adjacent-cut effect, and at eight sites about 1.6%.

Those observations do not establish the historical single-exponential law. Covariance-aware and cell-resolved residual checks still show substantial mismatch. The fitted `xi=2.37` is retained in the frozen artwork for provenance, not as a currently endorsed physical localization length. The [evidence reassessment](EVIDENCE_REASSESSMENT.md) gives the precise selection rules, new intervals, model diagnostics, and proposed figure revision.

## What is the contribution and its boundary?

The useful combination is complete-spectrum control, a fresh-gate response endpoint, an exact neighboring-purity mechanism, physical stabilizer comparisons at substantial size, and paired location interventions. The contribution should emphasize the monitored-state redistribution and controlled response mechanism, not treat elementary central-spectrum insufficiency as the entire discovery.

No new monitored-transition order parameter or critical exponent is asserted. Finite non-Clifford intervention checks do not establish a generic non-Clifford thermodynamic law. The location result is conditional on the defined eligible potential interventions and is not a randomized causal effect of the long-run monitoring probability. A rapidly attenuating measured profile is not a theorem of strict finite range.

The four-figure narrative remains the same. Its present evidential status is narrower than some archived checkpoint wording: direct finite-size persistence and paired near-cut concentration survive, whereas precise limiting and exponential-law interpretations require additional assumptions. The [research history](RESEARCH_HISTORY.md) explains the discarded flow-balance direction without making it part of the active result.
