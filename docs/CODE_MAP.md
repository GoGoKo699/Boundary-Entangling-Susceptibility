# Code map

## Reader-facing package

`src/boundary_susceptibility/response.py`
: Exact neighboring-purity and locally dressed response formulas.

`src/boundary_susceptibility/boundary_codes.py`
: Stabilizer boundary codes, exact response alphabet, and weighted reconstruction.

`reproduce.py`
: Rebuilds the six accepted Python-generated core panels from their canonical tables.

`verify.py`
: Runs deterministic consistency, hash, and exact-identity checks.

## Core figure scripts

| Script | Output |
|---|---|
| `scripts/figures/make_figure_01.py` | Fixed-spectrum cross-family response panel |
| `scripts/figures/make_figure_02.py` | Exact response and boundary-code redistribution matrices |
| `scripts/figures/make_figure_03.py` | Large-size scaling and replication panel |
| `scripts/figures/make_figure_04.py` | Paired distance-decay and conditioning-contrast panels |

The plotting scripts contain no manuscript or TikZ code. Conceptual diagrams used in the paper are intentionally not part of this repository.

## Canonical core data

| Path | Contents |
|---|---|
| `data/processed/core_figures/figure_01_panel_b.csv` | Primary and independent fixed-spectrum endpoint contrasts |
| `data/processed/core_figures/figure_02_boundary_codes.csv` | Nine exact responses and representative probability shifts |
| `data/processed/core_figures/figure_03_size_scaling.csv` | Finite-size slopes and thermodynamic intercepts |
| `data/processed/core_figures/figure_04_distance_decay.csv` | Distance-resolved paired response |
| `data/processed/core_figures/figure_04_conditioning_contrast.csv` | Unconditional and unchanged-spectrum near-minus-far effects |
| `data/processed/core_figures/figure_04_distance_fit.json` | Locked exponential-fit parameters |

## Full research studies

`studies/counterfactual_intervention_and_universality/`
: State-vector intervention, probe and architecture robustness, theorem checks, and physical stabilizer reachability.

`studies/physical_scaling_and_causal_locality/`
: Large stabilizer simulations, boundary-code analysis, finite-size scaling, transition context, and paired location intervention.

The study directories preserve their final internal organization where doing so protects imports and provenance. Their top-level README files explain entry points and runtime requirements.

## Tests

`tests/test_response.py`
: Exact neighboring-purity and boundary-code values.

`tests/test_figure_data.py`
: Canonical table schemas and load-bearing sign checks.

`tests/test_reproduction.py`
: Smoke reproduction of all six core panels.

## Provenance

`provenance/figure_sha256.csv`
: Author-approved frozen panel hashes.

`data/manifests/source_migration.csv`
: Mapping from final checkpoint sources to repository destinations.

`provenance/VERIFICATION_REPORT.json`
: Machine-readable clean-repository verification result.
