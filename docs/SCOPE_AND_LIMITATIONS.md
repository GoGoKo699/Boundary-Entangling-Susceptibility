# Scope and limitations

[Previous: claim evidence](CLAIM_EVIDENCE_MAP.md) · [Return to README](../README.md) · [Next: reproducibility limits](REPRODUCIBILITY_LIMITS.md)

## Supported core

The project studies a fresh-gate, purity-normalized linear-entropy response. The complete central Schmidt spectrum is insufficient; neighboring-cut purity features determine the Haar/uniform-Clifford response exactly. Monitored stabilizer ensembles exhibit negative within-spectrum monitoring coefficients through 256 qubits and in an independent-seed campaign. Paired location contrasts and a stricter common-eligibility profile support concentration of the measurement-induced suppression near the cut.

The nonpositive single-measurement sign is an exact corollary for pure stabilizer inputs, projective Pauli measurements preserving the central spectrum, and the stated averaged fresh probe. The empirical content in Figure 4 is spatial concentration and the paired near-minus-far difference. Neither the sign corollary nor that intervention quantitatively derives the long-run monitoring coefficient.

## Distinctions that matter

- Finite-size coefficients are directly measured through 256 qubits. Limiting coefficients depend on the extrapolation model, and exact-spectrum support changes with size.
- The distance result is summarized by measured attenuation ratios. Residual checks show that a single exponential inadequately describes the full profile.
- Far-distance events are sparse, and a simultaneous band includes zero at the farthest displayed point in the common-eligibility analysis.
- The simulation replication uses disjoint seeds with the same implementation.
- The paired causal claim concerns measurement-location interventions on copies of the same pre-state within the specified eligible population. The long-run monitoring-rate comparisons condition on a post-dynamics spectrum and remain associational.
- The exact response formula uses purities of extended bipartitions, even though the probe acts on two boundary qubits.

The [evidence reassessment](EVIDENCE_REASSESSMENT.md) provides the supporting model, support and pairing diagnostics for Figures 3 and 4.

Figure 1 intervals use a fully specified, pointwise, support-conditioned bootstrap recipe. Fixed reference spectra, selected support and small Clifford samples limit inference; discovery-reference uncertainty is excluded. See [reproducibility limits](REPRODUCIBILITY_LIMITS.md) for record and replay coverage, and [license scope](../LICENSE_STATUS.md) for the terms applying to the included materials.

[Next: reproducibility limits](REPRODUCIBILITY_LIMITS.md) · [Return to README](../README.md)
