# Code map

| Task | Source | Input |
|---|---|---|
| Exact three-cut response and stabilizer alphabet | `src/boundary_susceptibility/response.py`, `boundary_codes.py` | Purities or integer entropy increments |
| Integrity-checked original data access | `src/boundary_susceptibility/records.py` | Root `entanglement-data.zip` plus its manifest |
| Canonical graph redraws | `reproduce.py`, `scripts/figures/` | Frozen core CSV/JSON tables |
| Core record replay | `scripts/analysis/reproduce_core_records.py` | Original rows and resamples in the bundle |
| Earlier figure-design bootstrap reference | `studies/figure_design/bootstrap_reference.py` | Historical design calculation, not the accepted hybrid intervals |
| Independent September sensitivity replay | `scripts/analysis/reassess_evidence.py` | Checkpoint 05 data members in the bundle |
| Unpack study layouts safely | `materialize_studies.py` | Bundle and readable study source |
| State-vector intervention and rank/probe extensions | `studies/checkpoint_04/scripts/` | Discovery/confirmatory rows, spectra, and seeds |
| Stabilizer scaling and paired interventions | `studies/checkpoint_05/scripts/` | Clifford maps and fixed simulation parameters |
| Small simulator and theorem checks | Both study script directories | Group tables and explicit seeds |

The code keeps independent estimators and simulator validation paths separate. Cleanup does not merge them into one numerical implementation merely to remove duplication.

Use [the reproduction guide](REPRODUCTION.md) for commands. The [data manifest](../data/record_bundle_manifest.json) maps every raw member back to its original source identity. No later project is a software dependency.

See [precise reproducibility limits](REPRODUCIBILITY_LIMITS.md). Preserved original intervals and fully regenerated intervals are not interchangeable.
