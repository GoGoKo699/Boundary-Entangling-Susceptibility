# Notation

- `n`: even number of qubits; `m=n/2` is the central cut.
- `P_j`: purity of the reduced state on sites 1 through j.
- `S_j`: stabilizer entropy in bits across cut j.
- `D=2^(n/2)`: half-chain Hilbert-space dimension. Older theory/methods documents and source functions use `d` for this same dimension; it is not a local on-site dimension.
- `d` in Figure 4 and location-analysis tables: measurement distance from the central cut in sites. The current overview uses uppercase `D` for dimension to avoid this collision; frozen artwork and original source field names are unchanged.
- `chi_2`: expected normalized linear-entropy change under a fresh gate.
- `chi_rel=chi_2/P_m`: purity-normalized response. It is not generally the expected finite-gate increment of logarithmic Renyi-2 entropy.
- `delta_L=S_m-S_(m-1)` and `delta_R=S_m-S_(m+1)`: stabilizer boundary code.
- `beta_n`: within-spectrum monitoring-rate regression coefficient per probability increase 0.02, at fixed size and within `(tau,S_m)` strata.
- `xi`: historical single-exponential fit parameter. Its previous physical localization-length interpretation is not supported by the current full-profile diagnostics.

The [evidence reassessment](EVIDENCE_REASSESSMENT.md) distinguishes original primary results from post-hoc sensitivity checks.
