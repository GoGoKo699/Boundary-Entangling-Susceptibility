# Methods and definitions

## 1. Circuit ensemble

The large-size physical arm uses an open one-dimensional chain of even length
`n`. Each cycle contains:

1. one complete nearest-neighbor brickwork layer, consisting of both even and
   odd sublayers in a random order;
2. a fresh uniformly sampled two-qubit Clifford gate on every active bond;
3. independent single-site monitoring with probability `p` after the complete
   brickwork layer.

Two monitoring protocols are used:

- **projective Z:** every selected site is measured in the computational basis;
- **random Pauli:** every selected site is measured independently in X, Y, or Z
  with equal probability.

The probability `p` is therefore a probability per site per **complete two-
sublayer cycle**. It should not be compared numerically with papers that insert
measurements after each sublayer without converting conventions.

Initial states are independently sampled single-qubit stabilizer product
states. Probe times are expressed as `tau=cycles/n`.

## 2. Phase-free stabilizer simulation

The simulator stores the `n`-dimensional binary stabilizer row space as a
bit-packed `n x 2n` symplectic generator matrix. Stabilizer signs are omitted.
This is exact for every observable used here because:

- bipartite stabilizer entropies depend only on the support row space;
- Clifford gates transform that row space independently of signs;
- a random Pauli-measurement outcome changes only generator signs after the
  support-space update;
- deterministic measurement outcomes leave the support row space unchanged.

The 11,520 two-qubit Clifford matrices from Checkpoint 04 reduce to 720 unique
binary symplectic maps, each with multiplicity 16. Sampling the 720 maps
uniformly is therefore the correct phase-free support dynamics for a uniform
two-qubit Clifford.

The implementation was compared trajectory by trajectory with a direct
state-vector simulator for `n=4,6,8,10`, four measurement probabilities, both
monitoring protocols, four trajectories, and two probe times. Across 256
comparisons, all central entropies, neighboring entropies, response values, and
quarter-partition tripartite information values agreed exactly.

## 3. Stabilizer entropy and exact spectrum matching

For a region `A`, the stabilizer entropy is computed from the rank of the
restricted binary generator matrix. Pure stabilizer reduced states have a flat
nonzero spectrum. If the central entropy is `S_m`, then

$$
\lambda_1=\cdots=\lambda_{2^{S_m}}=2^{-S_m},
\qquad
\lambda_j=0\quad(j>2^{S_m}).
$$

Thus a fixed `(n,tau,S_m)` stratum is an exact complete-central-spectrum
stratum.

## 4. Entangling-susceptibility observables

Let `m=n/2`, `D=2^m`, and let `P_{m-1}`, `P_m`, and `P_{m+1}` be the purities
across the three adjacent cuts. The exact average normalized linear-entropy
response to a fresh Haar-random or uniformly random two-qubit Clifford gate on
the central bond is

$$
\chi_2
=
\frac{D}{D-1}
\left[
P_m-\frac25(P_{m-1}+P_{m+1})
\right].
$$

The primary large-size outcome is

$$
\chi_{\rm rel}=\frac{\chi_2}{P_m}.
$$

The relative response removes the trivial multiplicative central-purity scale,
which can become very small when the matched rank grows with system size. The
unnormalized `chi_2` remains a prespecified secondary outcome.

For stabilizer states,

$$
\chi_{\rm rel}
=
\frac{D}{D-1}
\left[
1-\frac25(2^{\delta_L}+2^{\delta_R})
\right],
$$

where `delta_L=S_m-S_{m-1}` and `delta_R=S_m-S_{m+1}`.

## 5. Primary simulation and independent replication

### Primary run

- sizes: `n=32,64,128,256`;
- probabilities: `p=0.20,0.22,0.24,0.25,0.26,0.27,0.28,0.30,0.34`;
- probe times: `tau=6,8,10`;
- 800 trajectories per `(protocol,n,p)` cell;
- 57,600 trajectories and 172,800 state records;
- base seed: `2026082301`.

### Independent replication

The same design was repeated with a disjoint base seed and 300 trajectories per
cell:

- 21,600 trajectories and 64,800 state records;
- base seed: `2026082401`.

The replication lock was timestamped before the primary analysis was complete.
Explicit run labels and generation commands are in [campaign recipes](CAMPAIGN_RECIPES.md).
These commands are reconstructed from the retained source, design locks, and
record fields, not claimed to be recovered historical shell transcripts.

## 6. Exact-spectrum fixed-effect estimator

For each protocol and size separately, rows from all three late probe times are
stratified by `(tau,S_m)`. A stratum is eligible when at least three probability
levels have at least ten trajectory records each. Within the eligible support,
fit

$$
y_i
=
\alpha_{\tau,S_m}
+
\beta_n\frac{p_i-0.26}{0.02}
+
\varepsilon_i.
$$

The primary outcome is `chi_rel`; the secondary outcome is `chi_2`. Hence
`beta_n` is the fixed-complete-spectrum change per `Delta p=0.02`.

Uncertainty is evaluated by:

- cluster-robust covariance with trajectory as the cluster;
- a trajectory bootstrap resampled separately within each `p` cell, with the
  observed common-support eligibility frozen.

At `n=256` there is no single entropy stratum spanning all nine probability
values. The estimand is therefore a connected local-overlap trend, not a direct
extreme-rate contrast. Every adjacent probability pair is also analyzed
separately to expose that support structure.

## 7. Predeclared finite-size model

The locked primary extrapolation is

$$
\beta_n=\beta_\infty+\frac{a}{n}.
$$

The exponent is not fitted. Weighted least squares uses the size-level
bootstrap intervals, and a second bootstrap propagates trajectory uncertainty
through the extrapolation. Alternative fixed powers and restricted-size fits
are reported only as sensitivity analyses.

## 8. Independent transition estimate

The monitored transition is located with the standard quarter-partition
tripartite information

$$
I_3(A:B:C)
=S_A+S_B+S_C-S_{AB}-S_{AC}-S_{BC}+S_{ABC}
$$

for four contiguous quarters of the open chain. Only `tau=10` is used. Pairwise
size crossings are linearly interpolated on the simulated probability grid and
bootstrapped over trajectories. The recorded algorithm considers adjacent
grid intervals wholly within `[0.235,0.295]`, selects the crossing nearest
`0.26` if there is more than one, and excludes bootstrap proposals with no
crossing. Its reported crossing intervals are therefore conditional on
crossing existence under this rule, not unconditional critical-point intervals.
This is a different observable on the same trajectories, not an independent
physical dataset.

The susceptibility is never used to choose the transition point. A hinge fit
at `p=0.27`, motivated by the independent high-size `I_3` crossing, is a
secondary analysis rather than the locked primary estimator.

## 9. Boundary-window entropy-summary test

Nested windows centered on the cut use half-widths
`h=1,2,4,8,16,32,64,128`, capped at `n/2`. For every window, the stored
features are:

- entropy of the whole window;
- entropy of its left and right halves;
- number of stabilizers fully supported in the window.

The first 400 trajectories per primary cell are training data and the last 400
are test data. Exact observed feature signatures predict the boundary code and
mean response. This is only a test of simple entropy summaries. It is not a
test of the complete local reduced stabilizer state.

## 10. Paired measurement-location intervention

A separate projective-Z run uses:

- `n=64,128,256`;
- `p=0.20,0.26,0.34`;
- 600 trajectories per cell;
- `tau=10`;
- one counterfactual measurement at distances
  `d=0,1,2,4,8,16,32,64` on both sides where the site exists;
- base seed `2026082501`.

Every location is evaluated on a copy of the same premeasurement stabilizer
state. The original conditional contrast keeps interventions with
`Delta S_m=0`, which exactly preserves the complete central stabilizer spectrum.
For every trajectory, the valid two-sided mean at `d=0` is compared with the
valid mean at distances at least `n/4`. The original endpoint can retain different sides at different distances; its eligibility is defined by the existence of the near and far means, not joint preservation for one fixed side. The stricter same-side check requires both $d=0$ and $d=n/4$ interventions to preserve the spectrum on the same side/pre-state. It is this fixed-side joint-preservation comparison that has the principal-stratum interpretation. The all-six-distance check imposes a common side/pre-state population. Each contrast averages eligible sides within pre-state, then pre-states within each $(n,p)$ cell, then gives the nine cells equal weight. These are distinct selected estimands, specified in [the evidence reassessment](EVIDENCE_REASSESSMENT.md), and do not identify an unconditional long-run monitoring-rate effect.

The unconditional contrast is secondary. It includes measurements that lower
`S_m` by one and therefore change the complete central spectrum.

For a single-site Pauli measurement on a pure stabilizer input, the nonpositive spectrum-preserving response change is an [exact corollary](THEORY.md#5-one-measurement-corollary). The sign of a near-minus-far difference and its distance dependence remain empirical. This interpretation changes no sampling, pairing, resampling, or eligibility rule.

## 11. Reproducibility

The state and intervention tables supporting the current figures, selected
analysis tables, archived size/location/hinge bootstrap arrays, design locks,
simulator source, symplectic maps, validation scripts, and figure scripts are
included and indexed in [the record manifest](../data/record_bundle_manifest.json).
This is a selected-record bundle, not every file from the historical campaigns.
Original simulation manifests, execution logs, and crossing resample arrays
are not included. Historical Figure 1 resampling seed recovery remains
incomplete; its current replacement is specified below. The original Figure 3
and Figure 4 analyzer invocation seeds have not been established from included
execution records. Their archived arrays can be replayed without claiming
fresh generation from those historical seeds. [Campaign recipes](CAMPAIGN_RECIPES.md)
distinguish these tasks. The verifier checks algebraic identities,
row counts, hashes, script compilation, figure readability, and the sign and
numerical ranges of every load-bearing result.

## Figure 1 uncertainty revision

The active Figure 1 bars use 50,000 valid support-conditioned trajectory-cluster percentile draws, primary pool `eligible_union`, seed 2026090801. Size/rate strata are resampled separately; time observations and eligibility masks remain clustered. A whole proposal is rejected if any required cell is empty. Fixed run-specific discovery spectra and common observed support are not re-estimated. These nominal pointwise post-hoc intervals are not simultaneous or exact finite-sample guarantees. The [adopted recipe](FIGURE1_UNCERTAINTY.md) and immutable plan define all details; other analyses are unchanged.
