> Historical figure-design record. The current accepted artwork is defined in `docs/FIGURE_BASELINE.md` at repository root; the original Figure 4 fit is not endorsed. The earlier Figure 1 statistics differ from the accepted hybrid-panel table.

# Figure 3 Specification — Physical Persistence and Replication

## Main-text questions

1. **Could the result be an artifact of replacing Schmidt coefficients?**
2. **Does the physical fixed-spectrum effect survive increasing system size and an independent replication?**

## Claims

- Physically generated stabilizer states with the same central stabilizer entropy have exactly the same complete central Schmidt spectrum; no spectrum replacement is required.
- The negative fixed-spectrum response slope persists through `n = 256`, is consistent with a nonzero thermodynamic limit, and independently replicates under a new seed and a different measurement basis.

## Final geometry

- Two-column figure, target size approximately **7.08 in × 3.05 in**.
- Panel (a): approximately 28–30% of the width.
- Panel (b): approximately 70–72% of the width.

## Panel (a): physical exact-spectrum matching

Display the stabilizer flat-spectrum identity:

`lambda_1 = ... = lambda_(2^S_m) = 2^(-S_m)`, with all remaining eigenvalues zero.

Then display:

`same S_m  =>  same complete central Schmidt spectrum`.

Show states generated at different monitoring probabilities entering the same `(n, tau, S_m)` stratum and then being compared without modification.

Required annotation:

> No spectrum replacement; no state modification.

## Panel (b): size dependence and independent replication

Plot

`beta_n = partial chi_rel / partial(p/0.02) |_(n, tau, S_m)`

against `1/n`, with labeled points for `n = 32, 64, 128, 256` and an extrapolated point at `1/n = 0`.

Series:

- projective Z, primary: filled navy circle, solid fit;
- projective Z, independent: open navy square, dashed fit;
- random Pauli, primary: filled teal circle, solid fit;
- random Pauli, independent: open teal square, dashed fit.

Sources:

- `analysis/primary/fixed_spectrum_size_slopes.csv`;
- `analysis/replication/fixed_spectrum_size_slopes.csv`;
- `analysis/primary/thermodynamic_limit_fits.csv`;
- `analysis/replication/thermodynamic_limit_fits.csv`.

Filters:

- `outcome == chi_relative`.

The main panel uses the locked `beta_n = beta_infinity + a/n` fits. Alternative correction models remain an appendix table, not an inset.

## Caption draft

**FIG. 3. The fixed-spectrum suppression is physical, large-system, and reproducible.** (a) Pure stabilizer states have a flat nonzero Schmidt spectrum; therefore matching the central stabilizer entropy `S_m` within a fixed `(n, tau)` stratum fixes the complete central spectrum without altering the states. (b) The conditional monitoring slope of `chi_rel` is negative at every simulated size through `n = 256` for projective-Z and random-Pauli monitoring. Open symbols show an independent-seed replication. The lines are the locked `1/n` fits; every extrapolated intercept remains below zero. The data support persistence but do not determine a universal finite-size correction exponent.

## Material excluded from Figure 3

- tripartite-information crossing;
- below/above-transition hinge fits;
- complete rank-support histograms;
- every entropy stratum;
- alternative correction curves;
- unnormalized-response analysis;
- separate-time results.

## Acceptance criteria

- Every raw size-resolved point is visibly below zero.
- Primary and independent results remain distinguishable in grayscale.
- The reader sees replication before reading the extrapolated intercept.
- The schematic makes exact-spectrum matching physical and modification-free.
- The caption says “consistent with” a nonzero limit, not “proves.”
