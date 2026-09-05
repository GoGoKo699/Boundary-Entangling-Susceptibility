# Code and evidence map

## Supported entry points

[`../reproduce.py`](../reproduce.py) rebuilds six frozen-layout panels from canonical inputs and checks all 18 PDF/PNG/SVG files. [`../scripts/figures/export_formats.py`](../scripts/figures/export_formats.py) exports the same Matplotlib figure to all three formats. Historical Figure 4 artwork is reproduced as recorded; its current interpretation is in [`EVIDENCE_REASSESSMENT.md`](EVIDENCE_REASSESSMENT.md).

[`../scripts/analysis/reassess_evidence.py`](../scripts/analysis/reassess_evidence.py) reads the hash-verified original Checkpoint 05 ZIP, recalculates the finite-size point estimates from stored entropy records, and performs the post-hoc pairing, distance-profile, and finite-size-model checks. It does not rerun random-circuit generation.

## Core plotting scripts

| Script in `scripts/figures/` | Panels |
|---|---|
| `make_figure_01_frozen.py` | Five-family fixed-spectrum response |
| `make_figure_02.py` | Boundary-response and probability-redistribution matrices |
| `make_figure_03.py` | Finite-size slopes and model-dependent extrapolations |
| `make_figure_04.py` | Recorded distance curve and conditioning contrast |

Canonical source tables are in [`../data/processed/core_figures/`](../data/processed/core_figures/). These small tables redraw figures; they are not a substitute for the archived trajectory data.

## Study sources

[`../studies/checkpoint_04/`](../studies/checkpoint_04/) contains the state-vector intervention, architecture/probe source, and theorem checks. [`../studies/checkpoint_05/`](../studies/checkpoint_05/) contains the stabilizer simulator, scaling and replication analysis, boundary codes, measurement-location analysis, design records, and validation source. Full data availability is documented in [`DATA_POLICY.md`](DATA_POLICY.md).

## Verification

[`../verify.py`](../verify.py) checks the existing frozen-result and repository-structure expectations. Those checks are regression checks, not a fresh independent simulation. [`../tests/test_identities.py`](../tests/test_identities.py) checks the reusable formulas. [`../tests/test_evidence_pipeline.py`](../tests/test_evidence_pipeline.py) tests estimator plumbing on synthetic data and validates the complete plotting output set.

The exact-identity package is [`../src/boundary_susceptibility/`](../src/boundary_susceptibility/). Its concise implementations cover the neighboring-purity formula and stabilizer response alphabet; the full locally dressed theorem is in [`THEORY.md`](THEORY.md) and the study validation scripts.

## Provenance

[`../provenance/figure_sha256.csv`](../provenance/figure_sha256.csv) identifies the original author-approved PDF bytes from the external Overleaf archive. Regenerated repository exports can have different PDF metadata. [`../results/evidence_reassessment/input_manifest.json`](../results/evidence_reassessment/input_manifest.json) records the archived members actually read by this reassessment. No nonexistent source-migration table or test module is assumed.
