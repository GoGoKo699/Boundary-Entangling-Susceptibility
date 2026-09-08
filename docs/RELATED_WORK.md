# Novelty and literature audit

## Scope of this audit

This audit asks whether the Checkpoint 05 combination is already established:

1. compare monitored states at exactly the same complete central Schmidt
   spectrum;
2. measure their response to a fresh cross-cut two-qubit gate;
3. identify the missing information as neighboring-cut purity or a stabilizer
   boundary code;
4. demonstrate large-size persistence and a paired cut-local measurement
   intervention.

A targeted search through 2026-08-19 did not identify a paper containing this
complete combination. This is not proof of absolute priority. The novelty claim
should be phrased as a new synthesis and application of several established
ingredients.

**Current framing.** This is the retained targeted-search record, not a new priority audit. The [claim map](CLAIM_EVIDENCE_MAP.md) distinguishes exact ingredients from empirical evidence. In particular, the single-measurement suppression sign is a corollary; the paired spatial dependence is empirical. The revised contribution wording below does not claim that different comparison designs estimate the same numerical effect.

## Established background that must be credited

### Monitored-circuit entanglement transitions

Hybrid unitary-measurement circuits exhibit volume-law and area-law phases and
can be simulated at large sizes in Clifford ensembles. Li, Chen, and Fisher
studied one-dimensional monitored Clifford circuits up to 512 qubits and
reported a measurement-driven entanglement transition (arXiv:1901.08092).
Lunt, Szyniszewski, and Pal analyzed measurement-induced criticality and
entanglement clusters in Clifford circuits (arXiv:2012.03857).

**Not novel here:** the existence of the transition, stabilizer simulation of
large monitored systems, or tripartite information as a transition diagnostic.

### Stabilizer entanglement structure

Efficient entanglement calculations and the flat nonzero reduced-state spectra
of pure stabilizer states are standard stabilizer-formalism facts; see Fattal,
Cubitt, Yamamoto, Bravyi, and Chuang (arXiv:quant-ph/0406168).

**Not novel here:** that fixing a stabilizer entropy fixes its complete flat
Schmidt spectrum.

### Clifford designs

The uniform multiqubit Clifford group is a unitary 3-design and therefore a
2-design; see Webb (arXiv:1510.02769) and Zhu (arXiv:1510.02619).

**Not novel here:** replacing a two-copy Haar average by a uniform Clifford
average.

### Swap/purity and entanglement-feature methods

Two-copy swap operators and purity features are established tools for random
unitary dynamics. You and Gu formulated second-Renyi entanglement features for
random Hamiltonian dynamics (arXiv:1803.10425).

**Not novel here:** using two-copy operators to express averaged linear-entropy
response.

### Entangling power and gate typicality

Entangling power and gate typicality are established local invariants of
bipartite gates; see Jonnadula, Mandayam, Zyczkowski, and Lakshminarayan
(arXiv:1909.08139). Their relation to measurement-induced transitions has been
studied by Manna, Madhok, and Lakshminarayan (arXiv:2407.17776).

**Not novel here:** the invariant language or the broad statement that gate
structure affects monitored-circuit entanglement.

### Spatial entanglement and coding structure in monitored circuits

Yoshida connected monitored-Clifford entanglement structure to decoding and
spacetime error-correction data (arXiv:2109.08691). More recent work develops a
graph-theoretic picture of typical monitored-Clifford output states
(arXiv:2608.03102).

**Not novel here:** that monitored trajectories contain spatial information
beyond one bipartite entropy.

### Other proposed transition observables

Recent work proposes localizable entanglement as an operational MIPT order
parameter with finite-size scaling (arXiv:2601.14185).

**Consequence for framing:** the present susceptibility should not be marketed
as a competing order parameter. It remains nonzero on both sides of the
transition and instead resolves a microscopic response mechanism.

## Closest conceptual antecedents

The closest bodies of work are:

- entanglement-feature and swap-operator formulas for local random dynamics;
- entangling-power descriptions of two-qubit gates;
- monitored-circuit coding and graph-state structure;
- stabilizer entropy profiles and cluster descriptions;
- interventions or diagnostics based on localizable entanglement.

None of the sources found in the targeted search directly asks whether two
states with the **same complete central Schmidt spectrum** have different
fresh-gate susceptibilities because of their neighboring spatial entanglement
profile.

## Conservative contribution statement

The strongest defensible novelty statement is:

> We formulate and test a fixed-spectrum response question for monitored
> quantum states. The exact local-twirl identity specifies the neighboring-cut
> information omitted by the central spectrum. In monitored stabilizer
> circuits this becomes a finite boundary-code description. Physical
> within-spectrum monitoring coefficients remain negative through 256 qubits
> and repeat with disjoint seeds. A separate paired measurement-location
> intervention establishes spatial dependence of the spectrum-preserving
> response change in its specified selected populations; it does not derive
> the long-run monitoring coefficient.

The novelty lies in the combination of:

1. complete-spectrum control;
2. response rather than static entropy as the endpoint;
3. an exact neighboring-cut mechanism;
4. physical large-size stabilizer realization;
5. paired causal localization.

## Claims to avoid

Do not state that the work:

- invents stabilizer spectrum matching;
- invents Clifford/Haar two-copy equivalence;
- invents entanglement features, entangling power, or gate typicality;
- provides a new MIPT order parameter;
- proves a new universality class;
- establishes absolute priority for the general local-twirl coefficient formula;
- applies to arbitrary non-Clifford monitored systems in the thermodynamic
  limit.

## Priority risks for external review

1. A mathematically equivalent four-purity response formula may exist under
   different terminology in operator-entanglement or entanglement-feature
   literature.
2. A stabilizer entropy-gradient or local-rank identity may be known in graph-
   state language.
3. The empirical result may be viewed as a specific consequence of Clifford
   flat spectra unless its physical question and paired intervention are made
   central.
4. The transition crossover is secondary and should not be oversold.

These risks justify an independent specialist search and theorem audit before
submission.

## Reference set

- D. Fattal et al., *Entanglement in the stabilizer formalism*,
  arXiv:quant-ph/0406168.
- Z. Webb, *The Clifford group forms a unitary 3-design*, arXiv:1510.02769.
- H. Zhu, *Multiqubit Clifford groups are unitary 3-designs*,
  arXiv:1510.02619.
- Y.-Z. You and Y. Gu, *Entanglement Features of Random Hamiltonian Dynamics*,
  arXiv:1803.10425.
- Y. Li, X. Chen, and M. P. A. Fisher, *Measurement-driven entanglement
  transition in hybrid quantum circuits*, arXiv:1901.08092.
- B. Jonnadula et al., *Entanglement measures of bipartite quantum gates and
  their thermalization under arbitrary interaction strength*,
  arXiv:1909.08139.
- O. Lunt, M. Szyniszewski, and A. Pal, *Measurement-induced criticality and
  entanglement clusters*, arXiv:2012.03857.
- B. Yoshida, *Decoding the Entanglement Structure of Monitored Quantum
  Circuits*, arXiv:2109.08691.
- S. Manna, V. Madhok, and A. Lakshminarayan, *Entangling power, gate
  typicality, and measurement-induced phase transitions*, arXiv:2407.17776.
- S. Manna, A. Lakshminarayan, and V. Madhok, *Localizable Entanglement as an
  Order Parameter for Measurement-Induced Phase Transitions*,
  arXiv:2601.14185.
- Y.-X. Zhang and Y.-X. Zhang, *Typical Output States of Monitored Random
  Clifford Circuits: A Graph-Theoretic Approach*, arXiv:2608.03102.
