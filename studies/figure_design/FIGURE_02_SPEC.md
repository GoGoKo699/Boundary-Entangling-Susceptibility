> Historical figure-design record. The current accepted artwork is defined in `docs/FIGURE_BASELINE.md` at repository root; the original Figure 4 fit is not endorsed. The earlier Figure 1 statistics differ from the accepted hybrid-panel table.

# Figure 2 Specification — Exact Neighboring-Cut Mechanism

## Main-text questions

1. **What information, absent from the central spectrum, determines the fresh-gate response?**
2. **How does monitoring reorganize that information?**

## Claim

For a Haar-random or uniformly random two-qubit Clifford probe, the relative response is fixed exactly by the central purity and its two neighboring-cut purities. In monitored stabilizer states, stronger monitoring shifts the corresponding boundary-code distribution toward local entanglement peaks, which have lower response.

## Final geometry

- Two-column figure, target size approximately **7.08 in × 3.05 in**.
- Two panels only.
- Panel (a): approximately 42% of the width.
- Panel (b): approximately 58% of the width.

## Panel (a): exact neighboring-cut identity

Show the local partition

`L  a | b  R`

and mark cuts `m-1`, `m`, and `m+1`.

Display prominently:

`chi_rel = [d/(d-1)] [1 - (2/5)(P_(m-1) + P_(m+1))/P_m]`.

Visually label:

- `P_m`: fixed by the complete central Schmidt spectrum;
- `P_(m-1), P_(m+1)`: not fixed by that spectrum.

The visual inference must be immediate:

`same P_m` does not imply `same neighboring purity profile`, and therefore does not imply `same response`.

The general four-purity locally dressed theorem is excluded from this panel and placed in the appendix.

## Panel (b): exact boundary alphabet and measured redistribution

Use two aligned 3×3 matrices.

### Left matrix: exact response alphabet

Coordinates:

`delta_L = S_m - S_(m-1)`, `delta_R = S_m - S_(m+1)`,

with each coordinate in `{-1, 0, +1}`.

Print the exact values of

`chi_rel / [d/(d-1)] = 1 - (2/5)(2^delta_L + 2^delta_R)`:

| `delta_L \ delta_R` | -1 | 0 | +1 |
|---|---:|---:|---:|
| -1 | +0.6 | +0.4 | 0 |
| 0 | +0.4 | +0.2 | -0.2 |
| +1 | 0 | -0.2 | -0.6 |

Add small profile labels for a central local minimum, a locally flat profile, and a central local maximum.

### Right matrix: probability redistribution

Use the primary projective-Z data at `n = 256` from:

- `analysis/synthesis/boundary_code_decomposition.csv`

Filter:

- `run == primary`;
- `protocol == z_projective`;
- `n == 256`.

Plot `probability_slope_per_dp02` in each code cell. Print every signed number. Use a diverging palette centered at zero, but ensure the signs remain legible in grayscale.

The caption states that weighting the measured probability shifts by the exact alphabet reconstructs the directly measured susceptibility slope to machine precision. The reconstruction is not given a third inset.

## Caption draft

**FIG. 2. Neighboring-cut purities provide the exact missing information.** (a) For a Haar-random or uniformly random two-qubit Clifford probe across the central cut, the relative response depends on the central purity and the purities across the immediately neighboring cuts. Fixing the complete central Schmidt spectrum fixes `P_m` but not `P_(m-1)` or `P_(m+1)`. (b) For stabilizer states this dependence reduces to a nine-state boundary alphabet. Stronger projective-Z monitoring shifts probability toward codes in which the central cut is a local entanglement maximum, thereby lowering the response. At `n = 256`, the weighted code redistribution reconstructs the measured slope to machine precision.

## Material excluded from Figure 2

- swap-operator derivation;
- general locally dressed four-purity coefficients;
- entangling power and gate typicality;
- random-Pauli heat map;
- separate-time matrices;
- transition context.

## Acceptance criteria

- The main identity is readable before any matrix detail.
- The reader can distinguish information fixed by the central spectrum from information left free.
- Every matrix cell contains a printed value.
- The measured redistribution visually points from high-response codes toward low-response codes.
- The exact and numerical parts are visually distinguished.
