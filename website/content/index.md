# The same spectrum. A different boundary response.

A Schmidt spectrum specifies the eigenvalue-based entanglement across one cut. It does not specify how the Schmidt vectors occupy the sites within either half. What does that distinction change when a fresh gate acts only on the two boundary sites?

This project studies the **purity-normalized linear-entropy response** to an independent Haar-random or uniformly random two-qubit Clifford gate. An exact identity identifies the neighboring-cut purities that the central spectrum omits. The numerical study asks how monitored dynamics reorganizes that information at fixed central spectrum.

<div class="route-grid">
<a class="route" href="../../docs/SCIENTIFIC_STORY.md"><strong>Understand the result</strong><span>Start with the physical question and the four comparisons.</span></a>
<a class="route" href="../../docs/THEORY.md"><strong>Check the argument</strong><span>Definitions, exact identities, assumptions, and proof steps.</span></a>
<a class="route" href="../../docs/REPRODUCTION.md"><strong>Reproduce the evidence</strong><span>Separate figure redraws, record reanalysis, and simulation checks.</span></a>
</div>

## What was compared?

The study uses three distinct designs. **Figure 1** modifies eligible finite-system states to share reference eigenvalues. **Figures 2–3** compare unmodified stabilizer states within exact-spectrum strata. **Figure 4** applies alternative measurements to copies of the same premeasurement state.

These comparisons answer different questions. Their effect sizes are not interchangeable, and the paired location experiment does not quantitatively derive the long-run monitoring coefficient.

## The response in one equation

For an even chain, let $m=n/2$, $D=2^m$, and $P_j$ be the purity of sites $1,\ldots,j$. The designated fresh-gate ensemble gives

$$
\chi_{\mathrm{rel}}
=\frac{D}{D-1}\left[1-\frac25\frac{P_{m-1}+P_{m+1}}{P_m}\right].
$$

The central spectrum fixes $P_m$, but not the two neighboring purities. These are purities of extended bipartitions, not merely of a small local reduced density matrix. The response is not an average finite increment of logarithmic Rényi-2 entropy.

The [complete derivation](../../docs/THEORY.md) and [notation guide](../../docs/NOTATION.md) specify the conventions. The [related-work account](../../docs/RELATED_WORK.md) separates the established ingredients from the monitored-state question studied here.

## What does the evidence support?

In the tested ensembles, response differences remain within the declared fixed-spectrum comparisons. Physical conditional coefficients remain negative through 256 qubits and repeat with disjoint seeds. The paired intervention reveals a spectrum-preserving response change concentrated near the cut.

The study does not establish a new transition order parameter, a rigorous thermodynamic limit, generic non-Clifford large-size universality, or a precise exponential localization length. Independent seeds are not independent software or external replication. The [claim-and-evidence map](../../docs/CLAIM_EVIDENCE_MAP.md) keeps these distinctions attached to each result.

## Read the project, not its development history

The [dialogue](../../docs/DIALOGUE_REPORT.md) follows nine main questions and 32 appendix questions. It is the complete scientific account. The website provides shorter routes into that same source, together with the figures, proofs, methods, records, and executable checks. A manuscript is not needed to follow the argument.
