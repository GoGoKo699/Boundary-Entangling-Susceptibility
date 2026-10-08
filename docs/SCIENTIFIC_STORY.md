# Scientific story

For a first explanation, use the [review-to-project route](PROJECT_GUIDE.md#learn) and [bridge](TUTORIAL_BRIDGE.md). For direct checking, start at [notation](NOTATION.md). [Return to README](../README.md).

The complete question-and-answer treatment is the [four-figure dialogue report](DIALOGUE_REPORT.md). Its [question map](DIALOGUE_QUESTION_MAP.md) links individual topics.

## 1. Central spectrum and fresh response are different information

The central Schmidt spectrum determines eigenvalue-based entanglement quantities at one cut. It does not determine how the Schmidt vectors occupy the sites inside each half. For the purity-normalized linear-entropy response, a product state and a product of two internal Bell pairs provide a four-qubit illustration with the same central spectrum but responses 4/15 and 4/5. This illustrates the exact identity.

Figure 1 tests the monitored-state question by replacing eigenvalues with discovery-derived shared reference spectra while retaining the chosen leading Schmidt vectors. All plotted held-out contrasts and independent-seed contrasts are negative. The comparison is finite-system and diagnostic, not a physical prescription for spectrum replacement.

## 2. The exact mechanism is a neighboring-purity relation

For a Haar or uniform two-qubit Clifford probe,

```math
\chi_{\mathrm{rel}}=\frac{D}{D-1}\left[1-\frac25\frac{P_{m-1}+P_{m+1}}{P_m}\right],\qquad D=2^{n/2}.
```

The central spectrum fixes only one of the three required purities. For stabilizer states this becomes a nine-code function of the two adjacent entropy increments. Figure 2 compares the exact response alphabet with the observed redistribution of code probabilities. The [theory](THEORY.md) distinguishes the exact response functional from the empirical direction of that redistribution.

Neighboring-cut purities concern extended bipartitions. Their sufficiency is not a theorem that a small local density matrix reconstructs the response. The response is normalized linear-entropy change divided by input purity, not an average finite logarithmic Rényi-2 entropy increment.

## 3. Physical matching and finite-size persistence

Naturally generated stabilizer states have flat nonzero reduced-state spectra. Matching their central entropy at fixed size therefore fixes the complete central spectrum without modifying the states. Figure 3's monitoring coefficients remain negative through 256 qubits under two measurement protocols and disjoint simulation seeds.

An independently written stored-record estimator reconstructs all 16 finite-size coefficients from 237,600 state records. The simulation replication uses disjoint seeds with the same simulator.

Figure 3's lines and points at infinity depend on the locked inverse-size model. Checked alternative models retain negative intercepts, but model residuals and size-dependent spectrum support prevent a rigorous thermodynamic conclusion. Direct finite-size evidence and model-dependent extrapolation remain separate.

## 4. A controlled measurement-location contrast

On the spectrum-preserving branch, a single-site Pauli measurement on a pure stabilizer state cannot increase the specified Haar/uniform-Clifford averaged response. This follows from the existing neighboring-purity identity and nonincreasing stabilizer cut entropies. The ordering of two measurement locations remains an empirical question.

Figure 4 evaluates different measurement locations on copies of the same pre-state. Its conditional endpoint keeps spectrum-preserving interventions and compares eligible near and far means. Stricter post-hoc same-side joint-preservation and six-distance common-eligibility checks retain negative near-minus-far effects and near-cut concentration.

The distance panel shows the observations and intervals. A single exponential inadequately describes the full profile, so the spatial result is expressed through measured attenuation ratios. The [evidence reassessment](EVIDENCE_REASSESSMENT.md) gives the fit diagnostics and conditioning rules; the [figure baseline](FIGURE_BASELINE.md) contains the caption.

The three designs have distinct estimands: Figure 1 uses modified finite-system states, Figures 2–3 use conditional comparisons of unmodified stabilizer states, and Figure 4 uses paired measurement-location interventions. Their effect sizes need not coincide, and Figure 4 does not quantitatively derive Figure 3's long-run coefficient.

## Scope

The contribution is the monitored-state redistribution and controlled response mechanism at fixed complete central spectrum, connected to an exact identity and physical large-size evidence. The [claim map](CLAIM_EVIDENCE_MAP.md) states the assumptions and comparison population for each result.

[Next: complete four-figure account](DIALOGUE_REPORT.md) · [Return to README](../README.md)
