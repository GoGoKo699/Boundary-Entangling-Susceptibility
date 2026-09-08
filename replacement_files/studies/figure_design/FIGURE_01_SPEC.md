> Historical figure-design record. The current accepted artwork is defined in `docs/FIGURE_BASELINE.md` at repository root; the original Figure 4 fit is not endorsed. The earlier Figure 1 statistics differ from the accepted hybrid-panel table.

# Figure 1 Specification — Central-Spectrum Insufficiency

## Main-text question

**At the same complete central Schmidt spectrum, do states produced by different monitoring histories still respond differently to the same fresh gate?**

## Claim

States with identical complete central Schmidt spectra retain a systematic monitoring-dependent difference in fresh-gate entangling susceptibility. The central spectrum is therefore insufficient to determine the response.

## Final geometry

- Two-column figure.
- Final page size: **7.08 in × 3.05 in**.
- Two panels only.
- Panel widths: 3.05 in and 3.97 in, separated by 0.06 in.

## Panel (a): diagnostic fixed-spectrum intervention

Display, from left to right:

1. Two monitored states, labeled `p = 0.08` and `p = 0.24`, with visibly different initial central spectra.
2. The intervention `lambda_alpha -> tilde(lambda)_alpha`.
3. A common rank-4 central spectrum.
4. Explicit retention of the state-dependent left and right Schmidt vectors.
5. The same fresh cross-cut gate `U_ab` applied to both states.
6. A shorter response bar for the stronger-monitoring state.

Required footer:

> central spectrum fixed; spatial embedding retained

The schematic is a diagnostic intervention, not a proposed physical protocol. The caption must state this.

## Panel (b): endpoint contrast across state-generation families

### Plotted quantity

`Delta chi_rel = chi_rel(p = 0.24) - chi_rel(p = 0.08)`.

### Rows

1. Haar dynamics + projective Z measurements.
2. Clifford dynamics + projective Z measurements.
3. Floquet–Cartan dynamics + projective Z measurements.
4. Haar dynamics + random-Pauli measurements.
5. Haar dynamics + weak Z measurements, eta = 0.6.

### Encodings

- Filled navy circle: held-out primary run.
- Open light-blue square: independent-seed run.
- Horizontal bars: 95% trajectory-cluster bootstrap interval.
- Dashed vertical line: zero.
- Leftward annotation: suppression.

### Axis

- Range: `[-0.62, 0.025]`.
- Label: `Delta chi_rel = chi_rel(0.24) - chi_rel(0.08)`.
- No panel title.

## Canonical data and estimand

Sources:

- `checkpoint_04/data/intervention/primary_rank4/state_response_rows.csv.gz`
- `checkpoint_04/data/intervention/independent_seed_rank4/state_response_rows.csv.gz`

Filters:

- `split == confirmatory`;
- `variant == equalized_rank4`;
- Haar/Clifford two-design fresh probe;
- `p_low = 0.08`, `p_high = 0.24`.

Response reconstruction:

`chi_rel = probe_haar_or_clifford_2design_delta_linear_norm / pre_purity`.

The point estimate is the equal-weight mean of the high-minus-low contrast over the available `(n, tau)` cells, with `n = 10, 12, 14` and `tau = 6, 8`. Trajectory indices are resampled within each `(n, p)` cell while their time records are retained jointly. Candidate v1 uses 10,000 bootstrap replicates.

Canonical table:

- `figure_data/fig01b_fixed_spectrum_relative_response.csv`

## Caption draft

**FIG. 1. The complete central Schmidt spectrum does not determine fresh-gate entangling susceptibility.** (a) For states generated at monitoring probability `p`, the central Schmidt eigenvalues are replaced by the same rank-4 spectrum, while the left and right Schmidt vectors are retained; all states then receive the same independent Haar/Clifford two-design probe across the cut. (b) Endpoint contrast `Delta chi_rel = chi_rel(0.24) - chi_rel(0.08)`, balanced over `n = 10, 12, 14` and `tau = 6, 8`. Filled circles denote the held-out primary run, open squares the independent-seed run, and bars 95% trajectory-cluster bootstrap intervals. All ten intervals lie below zero.

## Material excluded from Figure 1

- unmatched physical-state trend;
- rank-2 or rank-8 interventions;
- non-Haar probe families;
- size-resolved intervention estimates;
- transition data;
- the response theorem.

## Acceptance criteria

- All ten point estimates and confidence intervals lie below zero.
- Primary and independent estimates are visible without relying on color.
- The intervention clearly distinguishes eigenvalues changed from vectors retained.
- Every label is readable on the PRL scale proof at 100%.
- The grayscale rendering preserves the conclusions.
- The figure contains no appendix-only claim.
