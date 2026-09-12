# Beyond the Schmidt Spectrum

<a id="boundary-entangling-susceptibility-in-monitored-quantum-circuits"></a>

Boundary entangling susceptibility in monitored quantum circuits.

**Does the complete Schmidt spectrum across a cut determine the average response to a fresh gate crossing that cut?** For the response studied here, it does not. The central spectrum specifies the entanglement eigenvalues, but the response also depends on purities across the two neighboring cuts. This study asks how monitoring changes that remaining structure when the complete central spectrum is controlled.

The measured response is the expected change in normalized linear entropy from one independent two-qubit probe, divided by the input central purity. Haar-random and uniformly random two-qubit Clifford probes give the same average. This is a finite-gate quantity. It is neither a derivative with respect to monitoring probability nor an average finite logarithmic Rényi-2 entropy change.

In the tested monitored ensembles, stronger monitoring is associated with a lower response at fixed central spectrum. The physical stabilizer comparison remains negative through 256 qubits and repeats with disjoint seeds. A separate experiment applies alternative single measurements to copies of the same pre-state: its spectrum-preserving comparisons show a response change concentrated near the cut. These results have distinct comparison populations. They do not establish an unconditional causal effect of assigning a long-run monitoring rate, a thermodynamic theorem, a universal localization length, or a new transition order parameter.

<a id="reader-routes-and-scope"></a>

## Choose a route

| Route | Start and destination |
|---|---|
| **LEARN** | [Selected review passages and their project uses](docs/PROJECT_GUIDE.md#learn) → [local tutorial bridge](docs/TUTORIAL_BRIDGE.md) → [complete four-figure account](docs/DIALOGUE_REPORT.md) |
| **CHECK** | [Notation](docs/NOTATION.md) → [technical derivations](docs/THEORY.md) → [claim evidence](docs/CLAIM_EVIDENCE_MAP.md) → [estimators and comparison rules](docs/NUMERICAL_METHODS.md) → [limitations](docs/REPRODUCIBILITY_LIMITS.md) |
| **REPRODUCE** | [Environment and integrity checks](docs/REPRODUCTION.md#environment) → [figure redraw](docs/REPRODUCTION.md#redraw) → [record replay](docs/REPRODUCTION.md#record-replay) → [uncertainty regeneration](docs/REPRODUCTION.md#uncertainty) → [optional new-campaign instructions](docs/REPRODUCTION.md#new-campaign) |

The one external background tutorial is Matthew P. A. Fisher, Vedika Khemani, Adam Nahum and Sagar Vijay, *Random Quantum Circuits*, Annual Review of Condensed Matter Physics **14** (2023), read here as [arXiv:2207.14280v1](https://arxiv.org/abs/2207.14280v1). The [guide](docs/PROJECT_GUIDE.md) identifies the short findings route and the extra derivation reading. Other [primary references](docs/RELATED_WORK.md) supply attribution; they are not additional required tutorials. This reading route is an editorial choice for this repository, not an endorsed sequel to the review.

<a id="1-central-spectrum-insufficiency"></a>
<a id="2-an-exact-neighboring-cut-mechanism"></a>
<a id="3-physical-exact-spectrum-comparison-through-256-qubits"></a>
<a id="4-paired-measurement-location-intervention"></a>

## What each figure answers

| Figure | Question and evidence |
|---|---|
| [1: spectrum replacement](figures/README.md#figure-1) | Does a response difference remain after diagnostic spectrum equalization in finite-system states? All ten plotted contrasts are negative. The pointwise intervals condition on fixed archived references and observed support. |
| [2: boundary codes](figures/README.md#figure-2) | Which remaining state information carries the difference? Neighboring entropy increments specify exact stabilizer response values; their observed probability redistribution reconstructs the coefficient by an identity. |
| [3: physical matching](figures/README.md#figure-3) | Does the conditional difference persist without modifying states? Coefficients remain negative through the tested sizes and seeds. The limiting fit is model-dependent. |
| [4: measurement location](figures/README.md#figure-4) | How does one measurement's location change the later probe response on copies of the same pre-state? Eligible paired comparisons support near-cut concentration, without a fitted distance law. |

Open the [six-panel gallery](figures/README.md) for artwork, captions, tables and scripts, or the [41-question index](docs/DIALOGUE_QUESTION_MAP.md) for a particular objection. [Scientific story](docs/SCIENTIFIC_STORY.md) is a short recap; [results at a glance](docs/RESULTS_AT_A_GLANCE.md) is a numerical lookup.

<a id="reproduce-and-inspect"></a>

## Reproducibility and readiness

A complete checkout includes the required root `entanglement-data.zip`, checked against its [record manifest](data/record_bundle_manifest.json). The [reproduction guide](docs/REPRODUCTION.md) gives executable commands and distinguishes redraws, stored-record replay, bootstrap regeneration and new simulation. No old chat or separate checkpoint download is needed. Passing software checks is not independent scientific replication.

The manuscript remains the final step. The six accepted numerical panels and their source are present. **Actual editable external composite-schematic sources remain outstanding**; no unseen Overleaf material has been checked or reconstructed. Current Figure 1 uncertainty is reproducible, while its superseded historical resamples remain unrecovered. See [precise availability and limits](docs/REPRODUCIBILITY_LIMITS.md).

Development history is accessible through the [project guide](docs/PROJECT_GUIDE.md#history-and-readiness). The [older-baseline audit](audits/full-sanity-01/REVIEW.md) and [completed repair record](repairs/full-sanity-01/SUMMARY.md) retain their separate roles. The repaired entanglement-feature attribution and supporting exports are part of the current baseline.

Use the [citation record](CITATION.cff) and identify the commit or release used. Original code is licensed under [MIT](LICENSE); original documentation, data and figures under [CC BY 4.0](LICENSES/CC-BY-4.0.txt). See the [material scope and exceptions](LICENSE_STATUS.md) and [public-release preparation](docs/PUBLIC_RELEASE.md). [Contribution guidance](CONTRIBUTING.md) explains how to report corrections. The [implementation record](docs/reader-route-01/IMPLEMENTATION.md) describes the reader-route redesign and its checks.
