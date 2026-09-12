# Related work and primary attribution

<a id="novelty-and-literature-audit"></a>

[Return to README](../README.md) · [Background reading map](PROJECT_GUIDE.md#learn) · [Next: exact theory](THEORY.md)

The one pedagogical starting point is Fisher, Khemani, Nahum and Vijay, *Random Quantum Circuits*, Annual Review of Condensed Matter Physics **14** (2023), using [arXiv:2207.14280v1](https://arxiv.org/abs/2207.14280v1), [PDF](https://arxiv.org/pdf/2207.14280v1). The selected passages and PDF pagination are verified in the [project guide](PROJECT_GUIDE.md). The papers below supply primary attribution and comparisons; readers need not study them to follow the local bridge or four-figure account. Their essential ingredients are explained in [THEORY](THEORY.md). The retained bounded literature assessment follows.

## Scope of this audit

This audit asks whether the Checkpoint 05 combination is already established:

1. compare monitored states at exactly the same complete central Schmidt
   spectrum;
2. measure their response to a fresh cross-cut two-qubit gate;
3. identify the missing information as neighboring-cut purity or a stabilizer
   boundary code;
4. demonstrate large-size persistence and a paired cut-local measurement
   intervention.

A targeted search through 2026-08-19, with equation-level checks added on
2026-09-08, did not identify a paper establishing this complete empirical
combination. This bounded search is not proof of priority. In particular,
the local purity-transfer identities are established, and fixed-Schmidt-orbit
response also has prior formulations.

**Current framing.** The [claim map](CLAIM_EVIDENCE_MAP.md) distinguishes exact
ingredients, their direct deductions, and empirical evidence. The
single-measurement suppression sign is a corollary; the paired spatial
dependence is empirical. Different comparison designs need not estimate the
same numerical effect. This page integrates the focused attribution repair,
not an exhaustive priority certification.

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

The direct antecedent of the four-purity stencil is Kuo et al.,
[arXiv:1910.11351v2](https://arxiv.org/abs/1910.11351v2), Eqs. (19) and (60).
Akhtar and You, [arXiv:2006.08797v2](https://arxiv.org/abs/2006.08797v2),
Eq. (20), give its Haar cut-transfer specialization. The
[theory dictionary](THEORY.md#entanglement-feature-dictionary) supplies the
subsystem, invariant and normalization translation, including the
noncontiguous purity.

**Not novel here:** the transfer rule, its Haar neighboring-purity identity,
or writing an averaged linear-entropy response with two-copy operators.
The stabilizer alphabet and single-measurement sign corollary are direct
deductions, not independent empirical discoveries.

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

Fan, Vijay, Vishwanath, and You,
[arXiv:2002.12385v1](https://arxiv.org/abs/2002.12385v1), Eq. (13), Figure 4,
and Appendix E relate a weak-measurement entropy drop to distance-dependent
qudit-environment information. Their normalized entanglement-feature
treatment uses a ratio-of-averages approximation. Here Figure 4 instead
conditions on an unchanged central spectrum and measures the change in the
**subsequent fresh-gate response**. Its paired spatial endpoint is not their
entropy drop, and their reported decay behavior is not a decay law for this
repository.

Rudziński, Tartaglione, and Życzkowski,
[arXiv:2605.26867v2](https://arxiv.org/abs/2605.26867v2), Section VI,
Eqs. (86)-(97), study response averaged over fixed Schmidt orbits, including
linear entropy. They average local-unitary orbits for bipartite channels,
with two-qubit entanglement diagnostics. The present comparisons retain the
spatial structure of monitored many-body states and apply a designated
two-site cross-cut probe. Fixed-spectrum response itself is therefore not
claimed as unprecedented; the monitored conditional coefficients and paired
location contrasts are the distinct empirical targets here.

These comparisons supplement entangling-power, monitored-code, graph-state,
stabilizer-profile and localizable-entanglement antecedents above. None of
these equations establishes the signs or effect sizes of the repository's
specified monitored-population endpoints.

## Conservative contribution statement

The strongest defensible novelty statement is:

> We formulate and test a fixed-spectrum response question for monitored
> quantum states. The established local-twirl identity specifies the neighboring-cut
> information omitted by the central spectrum. In monitored stabilizer
> circuits this becomes a finite boundary-code description. Physical
> within-spectrum monitoring coefficients remain negative through 256 qubits
> and repeat with disjoint seeds. A separate paired measurement-location
> intervention establishes spatial dependence of the spectrum-preserving
> response change in its specified selected populations; it does not derive
> the long-run monitoring coefficient.

The empirical contribution lies in the tested combination of:

1. complete-spectrum control;
2. response rather than static entropy as the endpoint;
3. an exact neighboring-cut mechanism;
4. physical large-size stabilizer realization;
5. paired measurement-location contrasts in specified selected populations.

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

1. The four-purity transfer formula is already present in the
   entanglement-feature literature. Its translation and attribution must be
   retained wherever the local-twirl mechanism is used.
2. A stabilizer entropy-gradient or local-rank identity may be known in graph-
   state language.
3. The empirical result may be viewed as a specific consequence of Clifford
   flat spectra unless its physical question and paired intervention are made
   central.
4. The transition crossover is secondary and should not be oversold.

The independent repository audit checked the stated equations and scope.
Its bounded literature search neither certifies priority nor supplies evidence
for a stronger population, localization or thermodynamic claim.

## Reference set

- M. P. A. Fisher, V. Khemani, A. Nahum and S. Vijay, *Random Quantum Circuits*, Annual Review of Condensed Matter Physics **14** (2023). Single background tutorial; section/page references use [arXiv:2207.14280v1](https://arxiv.org/abs/2207.14280v1), dated 28 July 2022.

- D. Fattal et al., *Entanglement in the stabilizer formalism*,
  arXiv:quant-ph/0406168.
- Z. Webb, *The Clifford group forms a unitary 3-design*, arXiv:1510.02769.
- H. Zhu, *Multiqubit Clifford groups are unitary 3-designs*,
  arXiv:1510.02619.
- Y.-Z. You and Y. Gu, *Entanglement Features of Random Hamiltonian Dynamics*,
  arXiv:1803.10425.
- W.-T. Kuo, A. A. Akhtar, D. P. Arovas, and Y.-Z. You, *Markovian
  Entanglement Dynamics under Locally Scrambled Quantum Evolution*,
  [arXiv:1910.11351v2](https://arxiv.org/abs/1910.11351v2),
  [Phys. Rev. B **101**, 224202 (2020)](https://doi.org/10.1103/PhysRevB.101.224202).
- A. A. Akhtar and Y.-Z. You, *Multi-Region Entanglement in Locally Scrambled
  Quantum Dynamics*, [arXiv:2006.08797v2](https://arxiv.org/abs/2006.08797v2),
  [Phys. Rev. B **102**, 134203 (2020)](https://doi.org/10.1103/PhysRevB.102.134203).
- R. Fan, S. Vijay, A. Vishwanath, and Y.-Z. You, *Self-Organized Error
  Correction in Random Unitary Circuits with Measurement*,
  [arXiv:2002.12385v1](https://arxiv.org/abs/2002.12385v1),
  [Phys. Rev. B **103**, 174309 (2021)](https://doi.org/10.1103/PhysRevB.103.174309).
- Y. Li, X. Chen, and M. P. A. Fisher, *Measurement-driven entanglement
  transition in hybrid quantum circuits*, arXiv:1901.08092.
- B. Jonnadula et al., *Entanglement measures of bipartite quantum gates and
  their thermalization under arbitrary interaction strength*,
  arXiv:1909.08139.
- O. Lunt, M. Szyniszewski, and A. Pal, *Measurement-induced criticality and
  entanglement clusters: a study of 1D and 2D Clifford circuits*,
  [arXiv:2012.03857](https://arxiv.org/abs/2012.03857).
- B. Yoshida, *Decoding the Entanglement Structure of Monitored Quantum
  Circuits*, arXiv:2109.08691.
- S. Manna, V. Madhok, and A. Lakshminarayan, *Entangling power, gate
  typicality, and measurement-induced phase transitions*, arXiv:2407.17776.
- S. Manna, A. Lakshminarayan, and V. Madhok, *Localizable Entanglement as an
  Order Parameter for Measurement-Induced Phase Transitions*,
  arXiv:2601.14185.
- Y.-X. Zhang and Y.-X. Zhang, *Typical Output States of Monitored Random
  Clifford Circuits: A Graph-Theoretic Approach*, arXiv:2608.03102.
- M. Rudziński, G. Tartaglione, and K. Życzkowski, *Entangling power and
  fidelity diagnostic for bipartite quantum channels*,
  [arXiv:2605.26867v2](https://arxiv.org/abs/2605.26867v2).

[Next: technical derivations and the entanglement-feature dictionary](THEORY.md) · [Return to README](../README.md)
