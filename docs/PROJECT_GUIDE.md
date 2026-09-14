# Project guide

[Return to the project entrance](../README.md)

The project asks whether a complete central Schmidt spectrum determines a state's response to a designated fresh boundary gate, and how monitoring changes the response-relevant information that remains. Choose a route below. Basic quantum mechanics and linear algebra are assumed; project notation is introduced locally.

<a id="understand-the-result"></a>

## LEARN

Use **one background tutorial**: Matthew P. A. Fisher, Vedika Khemani, Adam Nahum and Sagar Vijay, *Random Quantum Circuits*, Annual Review of Condensed Matter Physics **14** (2023). All references below use [arXiv:2207.14280v1](https://arxiv.org/abs/2207.14280v1), [versioned PDF](https://arxiv.org/pdf/2207.14280v1), dated 28 July 2022. Its 56 PDF pages coincide with the printed preprint folios. These are **v1 PDF pages, not journal pagination**.

For the findings, read **§§2.1–2.4 (pp.5–11), the Clifford/stabilizer portion of §3.3.4 (pp.27–28), the opening conceptual paragraphs of §4.1 (p.30), and §4.1.1 (pp.31–32)**. Skip passages already familiar. Then read the [tutorial bridge](TUTORIAL_BRIDGE.md) and the [four-figure account](DIALOGUE_REPORT.md). The remaining free-fermion/automaton discussion in §3.3.4, the percolation argument later on p.30, and most of Sections 3 and 4 are not prerequisites.

For the derivation, add only the **purity/Haar-averaging portion of §3.1.3 (pp.16–18)**, then follow the bridge's short two-copy calculation into [THEORY](THEORY.md). The membrane and replica developments are not needed to obtain the single-probe response.

### Review-to-project map

The source roles are different:

- **(a) Review background:** concepts actually taught by the selected tutorial.
- **(b) Established machinery explained locally:** primary-attributed identities and their specializations. Local explanations supply the steps needed here; the original papers are attribution, not a second reading assignment.
- **(c) Project content:** the response definitions, boundary-code label, comparison designs, analysis choices and empirical findings. A project label or deduction does not imply a novelty claim.

| Review section / v1 PDF page | Concept learned there (a) | Project use | Local explanation still needed | Destination |
|---|---|---|---|---|
| §2.1, pp.5–6 | Reduced-state eigenvalues, entropies, Schmidt decomposition | Ask what complete-spectrum control leaves free | (c) Spectrum versus response; cut and normalization conventions | [Bridge: question](TUTORIAL_BRIDGE.md#what-changes-after-the-review), [notation](NOTATION.md) |
| §2.2, pp.6–8 | Local gates, Born probabilities, conditional states | Separate preparation from the later probe | (c) Designated independent probe; the four-qubit illustration | [Experiment](TUTORIAL_BRIDGE.md#what-is-the-experiment-and-what-is-random), [worked example](TUTORIAL_BRIDGE.md#same-central-spectrum-different-response) |
| §2.3, pp.8–10; §2.4, pp.10–11 | Brickwork circuits, Haar gates, monitored trajectories | Define the input ensemble and time | (c) Complete two-sublayer cycle, preparation-arm differences, three distinct averages | [Experiment](TUTORIAL_BRIDGE.md#what-is-the-experiment-and-what-is-random), [methods](NUMERICAL_METHODS.md#1-circuit-ensemble) |
| §3.3.4, Clifford portion pp.27–28 | Stabilizer representation, Rényi-order independence, limited Haar-moment agreement | Physical complete-spectrum matching at large size | (b) Flat projector spectrum and two-design specialization; (c) entropy-increment codes and conditional sampling | [Physical matching](TUTORIAL_BRIDGE.md#why-stabilizers-permit-physical-spectrum-matching), [theory](THEORY.md#2-flat-spectrum-lemma) |
| §4.1 opening, p.30; §4.1.1, pp.31–32 | Monitored entanglement and pure trajectories versus their mixture | Identify which states the response probes | (c) Response at fixed spectrum, rather than primarily locating a transition; trajectory-level statistics | [Question and averages](TUTORIAL_BRIDGE.md#what-changes-after-the-review), [dialogue M6](DIALOGUE_REPORT.md#m6) |
| **Derivation addition:** §3.1.3, pp.16–18 | Purity replicas, Haar averaging, averaging purity versus entropy | Evaluate the fresh probe analytically | (b) Exact two-qubit trace calculation and entanglement-feature dictionary; (c) input-purity-normalized response | [Response calculation](TUTORIAL_BRIDGE.md#what-response-is-measured), [full dictionary](THEORY.md#entanglement-feature-dictionary) |

The review's Eq.13 (p.16) relates purity to Rényi-2 entropy using natural logarithms. Eq.14 (p.17) is a schematic single-site Haar-pairing explanation. It does **not** explicitly derive our exact two-site coefficient $2/5$ or our susceptibility formula. The local calculation credits the established transfer machinery in [RELATED_WORK](RELATED_WORK.md). Its replica-pairing labels are not the project's entropy-increment boundary codes.

One optional passage serves a specific question: the paragraph on p.31 immediately before §4.1.1 explains why a measurement deep inside a monitored volume-law state can have a small entropy effect. Read it if interested in why location matters. Figure 4 measures a different endpoint, the change in a subsequent fresh-gate response; that paragraph predicts neither its paired ordering nor a localization length.

This map was checked against the actual v1 PDF, including the relevant equations and surrounding prose. Direct PDF retrieval succeeded after the web-reader fetch failed. No review text, figures or pages are distributed here. The route is this repository's educational choice and implies no endorsement by the review's authors.

**Next:** [TUTORIAL_BRIDGE](TUTORIAL_BRIDGE.md), then [DIALOGUE_REPORT](DIALOGUE_REPORT.md). Use the [question index](DIALOGUE_QUESTION_MAP.md) to skip to a particular issue.

<a id="check-the-argument"></a>

## CHECK

[Notation](NOTATION.md) → [theory](THEORY.md) → [claim evidence](CLAIM_EVIDENCE_MAP.md) → [methods](NUMERICAL_METHODS.md) → [evidence reassessment](EVIDENCE_REASSESSMENT.md) and [reproducibility limits](REPRODUCIBILITY_LIMITS.md).

The theory is the home for complete derivations, including the general and locally dressed probes. Methods define the estimators and eligible populations. The claim map separates exact statements from conditional observations and model-dependent interpretations. [RELATED_WORK](RELATED_WORK.md) owns primary attribution and the repaired entanglement-feature correspondence. Specialists can use this route directly.

<a id="reproduce-the-evidence"></a>

## REPRODUCE

[Environment](REPRODUCTION.md#environment) → [integrity/tests](REPRODUCTION.md#integrity) → [redraw](REPRODUCTION.md#redraw) → [stored-record replay](REPRODUCTION.md#record-replay) → [current uncertainty regeneration](REPRODUCTION.md#uncertainty) → [optional new-campaign instructions](REPRODUCTION.md#new-campaign).

[REPRODUCTION](REPRODUCTION.md) owns the executable route and explains each operation's meaning. The [figure gallery](../figures/README.md) maps questions to canonical data, caption and plotting script; [CODE_MAP](CODE_MAP.md) maps the underlying implementations. The [record manifest](../data/record_bundle_manifest.json) identifies the included raw members. A reader can reproduce the current numerical workflows without another tutorial, old chats, a missing checkpoint archive or My-tone.

<a id="before-writing-the-manuscript"></a>
<a id="research-history"></a>

## History and readiness

The manuscript remains the final step. Current proofs, estimators, evidence, attribution and numerical panels are traceable here. The actual editable external composite schematics remain unavailable; the accepted six numerical panels do not recover those assets or verify an unseen Overleaf layout. This is an asset-completion gap, separate from understanding and reproducing the current study.

The [full audit](../audits/full-sanity-01/REVIEW.md) assesses its older frozen baseline. The [repair summary](../repairs/full-sanity-01/SUMMARY.md) records the integrated equation-level attribution, corrected supporting exports, figure label and validation changes. Those completed repairs are not pending work. [Reproducibility limits](REPRODUCIBILITY_LIMITS.md) distinguishes current calculations from unrecovered historical invocations and resamples.

[Research history](RESEARCH_HISTORY.md), [run history](RUN_HISTORY.md), and [provenance](../provenance/README.md) are optional source tracing. [Citation status](../CITATION.cff), [license scope](../LICENSE_STATUS.md), and [current public-release preparation](PUBLIC_RELEASE.md) have separate roles. No new hosting, release or permission grant is implied.

[Return to README](../README.md) · [Continue with the bridge](TUTORIAL_BRIDGE.md)
