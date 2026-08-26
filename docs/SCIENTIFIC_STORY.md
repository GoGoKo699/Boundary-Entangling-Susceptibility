# Project map after Checkpoint 05

## One-sentence result

At exactly fixed complete central Schmidt spectrum, stronger monitoring makes a
fresh cross-cut two-qubit gate generate less entanglement because it changes the
spatial embedding of the Schmidt vectors, encoded for stabilizer states by the
two neighboring entropy increments. The effect persists through 256 qubits,
replicates under a disjoint seed and a different measurement basis, and is
causally reproduced by moving one projective measurement toward the cut.

## Logic chain

1. **The historical flow-balance claim fails.** Cumulative unitary and
   measurement increments telescope toward cancellation in any stationary
   bounded coordinate. This branch is archived.
2. **A non-telescoping response survives.** States from more strongly monitored
   ensembles respond less to the next fresh cross-cut gate after central-state
   controls.
3. **The central spectrum is insufficient.** Counterfactual spectrum
   equalization reverses the unmatched trend while retaining the Schmidt
   vectors.
4. **An exact response theorem identifies the missing information.** For a Haar
   or uniformly random two-qubit Clifford probe,
   \[
   \chi_2=\frac{d}{d-1}\left[P_m-\frac25(P_{m-1}+P_{m+1})\right].
   \]
   The central spectrum fixes `P_m`, but not the neighboring-cut purities.
5. **Physical exact-spectrum states reproduce the result.** Stabilizer reduced
   states have flat nonzero spectra, so fixing the central entropy fixes the
   complete central spectrum without modifying the state.
6. **The effect persists at large size.** Exact-spectrum response slopes remain
   negative through `n=256` and extrapolate to a nonzero negative limit under
   the locked `1/n` model and every reported sensitivity model.
7. **The mechanism becomes finite and exact.** For stabilizer states the
   response is a nine-state function of
   `(S_m-S_{m-1},S_m-S_{m+1})`. Stronger monitoring shifts this boundary-code
   distribution toward local entanglement maxima.
8. **A paired intervention establishes locality.** On copies of the same
   premeasurement state, a measurement adjacent to the cut suppresses the next
   gate response more than a far measurement whenever the complete central
   spectrum remains unchanged. The effect decays over about 2.37 sites.
9. **The response is transition-sensitive but not an order parameter.** An
   independent tripartite-information crossing occurs near `p=0.27` in the
   package convention. The suppression weakens above the crossing but remains
   nonzero.

## Current central claim

> The complete central Schmidt spectrum does not determine boundary entangling
> susceptibility in monitored circuits. At fixed spectrum, monitoring reshapes
> the neighboring entanglement profile, and this spatial embedding controls the
> response to a fresh cross-cut gate.

## Main evidence

- Locked primary Clifford simulation: 57,600 trajectories, `n=32–256`.
- Independent-seed replication: 21,600 trajectories.
- Two monitoring protocols: projective Z and random Pauli.
- Exact stabilizer spectrum matching in `(tau,S_m)` strata.
- Exact local-twirl response theorem and stabilizer boundary-code reduction.
- Paired measurement-location intervention: 5,400 pre-states and 75,600 valid
  potential interventions.
- Direct state-vector validation at `n<=10` with zero discrepancies in all 256
  recorded comparisons.

## Paper structure now justified

1. Central-spectrum insufficiency and physical question.
2. Exact local response theorem.
3. Physical stabilizer exact-spectrum construction.
4. Large-size persistence and independent replication.
5. Boundary-code redistribution as the microscopic mechanism.
6. Paired cut-local measurement intervention.
7. Relation to, and distinction from, the monitored transition.
8. Scope and limitations.

## Keep

- The local-twirl four-purity response theorem.
- The Haar/Clifford three-cut specialization.
- Physical exact-spectrum stabilizer comparisons.
- Large-size and independent-seed results.
- Boundary-code theorem and probability decomposition.
- Paired measurement-location intervention.
- Tripartite-information crossing as contextual evidence.
- Cut-local decay and the conditional/unconditional sign reversal.

## Archive, but preserve for provenance

- Entanglement-trajectory fingerprints as a generic replacement for entropy.
- Cumulative spectral-flow cancellation ratio.
- “Flow-balance principle,” order-parameter, or critical-point-locator language.
- Six-coordinate multiplicity as if it supplied six independent tests.
- Aubry field-versus-transport competition as part of the central story.
- Artificial Schmidt-spectrum truncation as the final physical evidence; it is
  now historical motivation because physically reachable stabilizer states
  provide exact-spectrum controls.

## Unresolved before submission

- Independent specialist verification of both exact theorems.
- Final priority search for fixed-spectrum response and neighboring-cut purity
  antecedents.
- Whether a compact non-Clifford physical cross-check can be added without
  expanding the project into a new program.
- Whether a complete bounded-window reduced stabilizer state, rather than a few
  entropy summaries, reconstructs the boundary code.
- Exact journal framing and manuscript length.

## Publication status

The project is ready for manuscript construction and external theory audit. It
is not yet ready for submission. A balanced target is *Quantum* or *Physical
Review Research*. A PRL attempt is scientifically defensible if the paper is
kept narrow and the theorem/novelty audit is favorable.


## How to read the four core figures

The repository core follows the same causal and evidential order as the planned Letter: insufficiency, exact mechanism, physical persistence, then paired localization. The repository is broader only in its robustness and provenance material.
