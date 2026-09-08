# Primary-literature and equation-level attribution audit

Baseline: `00009cf7cc02104e4c776863b3ea551bd38e00f4`. Reviewed on 2026-09-08. This report assesses the frozen source; it does not edit the scientific baseline. Equation numbers below refer to the linked arXiv versions; page numbers are the printed PDF pages, starting at one. HTML conversion dates are not publication dates.

## Verdict and findings

**Established identities are mathematically consistent with the prior literature, but their equation-level attribution is incomplete.** The principal empirical claims are not refuted by finding the known identities. The specific combination of monitored ensembles, controlled complete central spectra, a designated fresh local probe, and paired measurement-location comparisons remains distinguishable from the antecedents examined. This bounded search does not establish priority.

**LIT-01, major attribution/completeness issue, high confidence.** `docs/RELATED_WORK.md:53-60` names the 2018 introduction of entanglement features but omits the two directly relevant 2020 transfer-rule papers. Its `143-145` describes an equivalent formula as something that may exist. Equivalence is confirmed below, including the full locally dressed four-purity operator, not merely the Haar special case. `docs/THEORY.md:79-197,235-244,326-347` should cite these results at their use. `docs/PROJECT_GUIDE.md:23` correctly records this as unfinished. Smallest repair: add the two references and a short convention/translation table; replace the hypothetical-equivalence sentence with the actual equation-level relationship. No recalculation is required solely for this repair.

**LIT-02, important positioning omission, high confidence about overlap; no priority conclusion.** `docs/RELATED_WORK.md:91-126` does not compare with Fan et al.'s measurement-distance response or the 2026 fixed-Schmidt-orbit response work. Those are closer than generic MIPT background to the words "response", "complete-spectrum control", and "localization". Add concise comparisons of endpoints and conditioning, as below. They do not establish this repository's empirical conditional rate coefficient or near-minus-far endpoint, and their decay assumptions must not be imported as a law for Figure 4.

**LIT-03, minor bibliography issue, high confidence.** `docs/RELATED_WORK.md:170-171` truncates the Lunt et al. title: the full title includes “a study of 1D and 2D Clifford circuits”. All eleven cited arXiv IDs resolve to the intended authors/topics. The two Zhang authors have different full names, Yu-Xuan and Yu-Xiang; the repeated `Y.-X.` initials in `179-180` are legitimate but less clear. Adding journals, DOIs and versioned links improves traceability; missing journals alone do not invalidate an otherwise correct arXiv reference.

## Exact dictionary and independent algebra

Use `q` here for one-site Hilbert dimension to avoid both the repository's half-chain dimension `D` and distance `d`. The EF papers use `d=q`. Their Ising down-spin means inclusion in a subsystem, and `X_i` toggles inclusion; it is not a physical gate on the state. Thus the four terms for output region `La` map as follows:

| EF row operation | Input region | Repository purity |
|---|---|---|
| identity | `La` | `P_m` |
| `X_a` | `L` | `P_{m-1}` |
| `X_b` | `Lab` | `P_{m+1}` |
| `X_a X_b` | `Lb` | noncontiguous `P_{L union b}` |

For pure global inputs `P_Lab=P_R`; without global purity that last substitution is unavailable. The swap expectation defining each subsystem purity itself holds for mixed density matrices too. For a fresh probe, local input scrambling suffices because output local rotations leave the subsystem purity invariant. Nothing requires the monitored preparation dynamics to be locally scrambled, in equilibrium, or described by an EF mean-field model.

### Published inputs

Kuo, Akhtar, Arovas and You, *Markovian Entanglement Dynamics under Locally Scrambled Quantum Evolution*, [arXiv:1910.11351v2](https://arxiv.org/abs/1910.11351v2), Phys. Rev. B **101**, 224202 (2020), DOI `10.1103/PhysRevB.101.224202`: Eqs. (4)-(5) define state/operator features; (17), (19) give the inverse identity metric and exact averaged transfer; (59)-(60), p.12, give the general two-site operator through two invariants. Equation (19), p.4, is the directly relevant antecedent. The later logarithm-of-average entropy approximation is unnecessary for this repository's purity endpoint. [HTML](https://arxiv.org/html/1910.11351v2), [PDF](https://arxiv.org/pdf/1910.11351v2).

Akhtar and You, *Multi-Region Entanglement in Locally Scrambled Quantum Dynamics*, [arXiv:2006.08797v2](https://arxiv.org/abs/2006.08797v2), Phys. Rev. B **102**, 134203 (2020), DOI `10.1103/PhysRevB.102.134203`: Eq. (20), p.7, gives the exact Haar transfer matrix; Eqs. (21)-(22) give fractional-SWAP/SWAP examples. Its disconnected-region dependence is directly relevant to `P_Lb`. Eqs. (30)-(33), pp.9-10, discuss continuous-time entropy growth including multiregion information. Those velocity formulas and MPS approximations should not be substituted for a finite fresh-gate increment. [HTML](https://arxiv.org/html/2006.08797v2), [PDF](https://arxiv.org/pdf/2006.08797v2).

Jonnadula et al., [arXiv:1909.08139v2](https://arxiv.org/abs/1909.08139v2), use exactly the rescaled `e_p,g_t` conventions in `THEORY.md`: Eqs. (16), (18), p.4. Their Eq. (25) converts operator entanglements to these invariants; Eq. (31), p.6, matches the repository's Cartan formulas under `c_1=2 alpha`, `c_2=2 beta`, `c_3=2 gamma` (the sign is immaterial in the squared sines). These are not the original unrescaled entangling-power convention. [HTML](https://arxiv.org/html/1909.08139v2), [PDF](https://arxiv.org/pdf/1909.08139v2).

### Audit expansion

The following is our algebraic translation, not a claim that these symbols appear in the papers. Let `E=E_op(V)`, `E_s=E_op(V SWAP)` and `e_s=1-q^{-2}`. With normalized vectorized `V`, its `AC` and `AD` purities are `1-E` and `1-E_s`. Consequently the coefficients denoted `A_ij,B_ij` by Kuo et al. become

$$A=q^4 E,\qquad B=q^4(e_s-E_s).$$

Multiplying their operator by the inverse identity metric gives

$$T=I-Q\,[u-v(X_a+X_b)+wX_aX_b],\qquad Q=(I-Z_aZ_b)/2,$$

$$u=\frac{A-B/q^2}{(q^2-1)^2},\quad v=\frac{A-B}{q(q^2-1)^2},\quad w=\frac{A/q^2-B}{(q^2-1)^2}.$$

Taking the row corresponding to the cut yields

$$\mathbb E P'_{La}=v P_L+(1-u)P_{La}-wP_{Lb}+vP_{Lab}.$$

For qubits, `E=3(e_p+2g_t)/8` and `E_s=3(e_p-2g_t+2)/8`, so

$$u=g_t+5e_p/6,\quad v=2e_p/3,\quad w=5e_p/6-g_t.$$

This exactly reproduces `THEORY.md:183-192`. Coefficients can be negative; they are transfer coefficients on constrained purity features, not probabilities of four physical trajectories.

The Haar operator is

$$T_{\rm Haar}=I-Q\left[I-\frac{q}{q^2+1}(X_a+X_b)\right].$$

Its cut row is `q/(q^2+1)` times the two neighboring purities. At `q=2`, with `m=n/2` and `D=2^m`, the definitions alone then give

$$\chi_2=\frac{D}{D-1}(P_m-\mathbb E P'_m),\qquad
\chi_{\rm rel}=\frac{D}{D-1}\left[1-\frac25\frac{P_{m-1}+P_{m+1}}{P_m}\right].$$

The denominator is input purity. Neither this expression nor the EF transfer licenses replacing `E[-log(P'_m/P_m)]` by `1-E[P'_m]/P_m`. Uniform two-qubit Clifford averaging gives the same degree-(2,2) moment by the unitary-design result; a generic random sequence of Clifford generators need not be uniform merely because all generated gates are Clifford.

The audit-only [exact rational check](code/check_literature_translation.py) verifies the affine coefficient conversion, all three listed repository probes, identity/SWAP limits, and Haar local dimensions 2 through 8. [Output](results/literature_translation.json). It imports no source implementation and uses no seed or numerical tolerance. It shares the published transfer identities and invariant definitions, so it is an independent translation check, not independent physical validation of those premises.

## Other retained ingredients and current neighboring work

Fattal et al., [quant-ph/0406168v1](https://arxiv.org/abs/quant-ph/0406168v1), Eqs. (4)-(6), p.2, give the reduced stabilizer projector and entropy/rank relation. Its equal nonzero eigenvalues justify `P_j=2^{-S_j}`. Substitution into the transfer rule and integer adjacent increments produces the repository's boundary alphabet. The code-probability decomposition is linear algebra. Those facts, and subtraction on the branch preserving `P_m` to obtain T1, are deductions rather than statistically independent discoveries. The outcome-specific sign theorem additionally needs the stabilizer Pauli-measurement entropy argument in `THEORY.md:448-482`; local operations' average entanglement monotonicity by itself would not prove an outcome-specific statement for arbitrary pure states.

Webb, [1510.02769v3](https://arxiv.org/abs/1510.02769v3), Theorem 2, and Zhu, [1510.02619v2](https://arxiv.org/abs/1510.02619v2), Theorem 1, establish the stronger 3-design result. A 2-design is all that the purity calculation requires. This justifies the retained scope, not equality of whole monitored Haar and Clifford trajectory distributions.

Fan, Vijay, Vishwanath and You, [2002.12385v1](https://arxiv.org/abs/2002.12385v1), Phys. Rev. B **103**, 174309 (2021), is an additional close antecedent. Eq. (8) gives Haar transfer; Eq. (13), p.4, and Appendix E relate a weak-measurement entropy drop to qudit-environment information. Figure 4 studies distance from the boundary. Appendix D.2 discusses stabilizer entropy-drop events. Its normalized monitored-EF treatment uses a ratio-of-averages approximation (Eqs. (6)-(7)); its reported power law cannot certify this repository's conditional profile. Here the central entropy is held unchanged and the endpoint is the *subsequent gate response change*. That is an important difference. [Full text](https://arxiv.org/html/2002.12385v1).

Li and Fisher, [2007.03822v4](https://arxiv.org/abs/2007.03822v4), Phys. Rev. B **103**, 104306 (2021), Theorem 1, Eqs. (13)-(14), connect logical operators supported in a region of a stabilizer code to mutual information with a purifying reference. This is relevant spatial/coding background, not the fresh two-qubit gate endpoint. No result from the separate noisy-record project is used here.

Rudziński, Tartaglione and Życzkowski, [2605.26867v1](https://arxiv.org/abs/2605.26867v1), *Entangling power and fidelity diagnostic for bipartite quantum channels*, is directly relevant to the generic idea of fixed-spectrum response. Section VI, Eqs. (86)-(95), defines entanglement variation averaged over fixed Schmidt orbits, including linear entropy. It averages a full two-qubit local-unitary orbit and treats noisy bipartite channels; it does not supply this monitored many-body comparison or retained spatial geometry. A short distinction is appropriate; claiming that fixed-Schmidt response itself is unprecedented would not be justified. The HTML title uses “diagnostics”; the arXiv landing metadata uses “diagnostic”. [Full text](https://arxiv.org/html/2605.26867v1).

## Verification of the repository reference set

All IDs below were opened on arXiv. Full-text depth is explicitly distinguished from metadata verification; this is not a review of every theorem in every cited paper.

| ID in baseline | Verified bibliographic detail | Relevant inspection |
|---|---|---|
| [quant-ph/0406168](https://arxiv.org/abs/quant-ph/0406168) | Fattal, Cubitt, Yamamoto, Bravyi, Chuang; *Entanglement in the stabilizer formalism*; 2004 | Full short paper, especially Eqs. (4)-(8) |
| [1510.02769](https://arxiv.org/abs/1510.02769) | Zak Webb; *The Clifford group forms a unitary 3-design*; Quantum Inf. Comput. 16, 1379-1400 (2016) | Theorem 2 and twirl definitions |
| [1510.02619](https://arxiv.org/abs/1510.02619) | Huangjun Zhu; *Multiqubit Clifford groups are unitary 3-designs*; Phys. Rev. A 96, 062336 (2017) | Theorem 1 and frame-potential criterion |
| [1803.10425](https://arxiv.org/abs/1803.10425) | Yi-Zhuang You, Yingfei Gu; *Entanglement Features of Random Hamiltonian Dynamics*; Phys. Rev. B 98, 014309 (2018) | Definitions, Sec. V.3 Eqs. (49)-(50), Appendix A |
| [1901.08092](https://arxiv.org/abs/1901.08092) | Yaodong Li, Xiao Chen, Matthew P. A. Fisher; title matches; Phys. Rev. B 100, 134306 (2019) | Sec. III.3 stabilizer profiles; Fig. 2 verifies 512-qubit statement |
| [1909.08139](https://arxiv.org/abs/1909.08139) | Bhargavi Jonnadula, Prabha Mandayam, Karol Życzkowski, Arul Lakshminarayan; title matches; Phys. Rev. Research 2, 043126 (2020) | Eqs. (16),(18),(25),(31), Table I; exact normalization checked |
| [2012.03857](https://arxiv.org/abs/2012.03857) | Oliver Lunt, Marcin Szyniszewski, Arijeet Pal; full title ends *a study of 1D and 2D Clifford circuits*; Phys. Rev. B 104, 155111 (2021) | Model, criticality and cluster definitions; no fresh-gate identity claimed there |
| [2109.08691](https://arxiv.org/abs/2109.08691) | Beni Yoshida; title matches; arXiv submission 2021 | Secs. 8-9 spatial/state-dependent structure; no journal reference on landing page |
| [2407.17776](https://arxiv.org/abs/2407.17776) | Sourav Manna, Vaibhav Madhok, Arul Lakshminarayan; title matches; Phys. Rev. A 110, 062422 (2024) | Gate-family definitions and phase-transition target; does not compare selected input spectra |
| [2601.14185](https://arxiv.org/abs/2601.14185) | Sourav Manna, Arul Lakshminarayan, Vaibhav Madhok; title matches | Eq. (2): maximal separation with nonzero localizable entanglement; distinct observable |
| [2608.03102](https://arxiv.org/abs/2608.03102) | Yu-Xuan Zhang, Yu-Xiang Zhang; title matches; v2 dated 2026-08-14 | Graph-state Eq. (8), graph counting Eq. (13), monitored output-state structure |

## Search coverage and remaining limits

This pass opened both mandatory papers in HTML and PDF and visually checked the PDF pages containing Eqs. (19), (60) and the Haar transfer Eq. (20). It inspected the listed reference set at the depths above and followed directly relevant citations/search matches to the three additional works. Searches on 2026-09-08 included `entanglement feature fixed Schmidt spectrum gate entangling susceptibility monitored states`, `monitored entangling spectrum response`, `entanglement feature measurement purity`, `susceptibility Clifford entanglement`, and `fixed Schmidt entangling power`, followed by current-search verification. Search engines returned irrelevant material and sometimes relaxed queries; only the primary papers actually opened support this report.

The search found no paper reproducing the entire declared design and empirical result. That is not exhaustive coverage of every unpublished, differently named, or unindexed result. No external specialist correspondence, full citation-network census, or priority certification was performed. The recommended repair is focused attribution and comparison, not another simulation campaign, a new decay fit, or a manuscript draft.
