# Frequently asked questions

## What is fixed by same-spectrum matching?

The complete central Schmidt eigenvalue list, including zeros and rank. In the diagnostic intervention the list is replaced while state-dependent Schmidt vectors are retained. In the physical stabilizer arm, matching `(n,tau,S_m)` fixes the complete flat spectrum without altering the state.

## Is the response an entropy increment?

It is the expected normalized linear-entropy change divided by the input central purity. It is not generally the mean finite-gate increment of `-log2(P_m)`. The explicit definition is in the root README and [numerical methods](NUMERICAL_METHODS.md).

## Why does the central spectrum not suffice?

It does not fix the neighboring-cut purities that enter the exact fresh-gate formula. A small exact example is in the [scientific story](SCIENTIFIC_STORY.md). The empirical contribution concerns the monitored distribution of this missing spatial information.

## Does the exact formula imply a local reduced state is sufficient?

No. The probe acts on the boundary qubits, but the purity features concern extended bipartitions. The nine-code stabilizer description is not a theorem of reconstruction from a small physical window.

## Does the project prove a nonzero thermodynamic limit?

No. The within-spectrum coefficients are directly observed to be negative through 256 qubits. The original inverse-size extrapolations and a finite menu of post-hoc alternatives have negative intercepts, but model residuals and changing support limit the precision of a thermodynamic interpretation. See [evidence reassessment](EVIDENCE_REASSESSMENT.md).

## Is the localization length exactly 2.37 sites?

No. That value is the historical unweighted exponential-fit parameter. A narrow bootstrap parameter interval did not establish the adequacy of the exponential. The revised interpretation is a response concentrated near the cut and rapidly decreasing at the sampled distances. The original curve remains visible only because the accepted artwork has not yet been revised.

## Could changing selected trajectories produce the distance profile?

A post-hoc common-eligibility check keeps only side/pre-state combinations whose central spectrum is preserved under every displayed location intervention. The profile remains near-cut concentrated. This check uses a different selected population and does not establish a strict finite range; its simultaneous uncertainty band includes zero at the farthest displayed distance.

## What is causal?

The specified paired location interventions on copies of the same pre-state. A strict same-side sensitivity comparison requires unchanged central spectrum under both potential interventions before calculating the contrast. This is not an unconditional population effect and not the causal effect of assigning the long-run monitoring rate.

## What does independent replication mean here?

The primary design was repeated with a disjoint base seed. This is independent-seed replication, not an independent implementation or external laboratory replication. Separate direct state-vector/tableau tests address some implementation risks.

## Is this a new transition order parameter?

No. Transition context is secondary. Neither an order parameter nor a critical exponent is claimed.

## What non-Clifford evidence is included?

The finite state-vector intervention study includes Haar and fixed non-Clifford Floquet-Cartan dynamics, along with weak and random-Pauli measurement variants. The large-system physical exact-spectrum evidence is stabilizer/Clifford based.

## What does green CI establish?

That the included software, frozen-result regression checks, structural checks, and figure-generation tests pass in the recorded environment. It does not independently prove the scientific interpretation or rerun the original circuit campaign. The separate archive-based reassessment command recomputes selected estimates from stored observations.

## Where are the raw data?

The original Checkpoint 04 and Checkpoint 05 ZIP identities are in [data policy](DATA_POLICY.md). A permanent raw-data deposit remains pending. Small canonical figure tables and selected source are tracked; they must not be mistaken for the full trajectory-level data.
