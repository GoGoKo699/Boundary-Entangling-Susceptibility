# Finite fixed-spectrum and probe study

This directory retains the original state-vector simulator, rank-flexible version, independent-seed driver, physical-stabilizer driver, deterministic analyses, and gate-theorem validation source. Raw discovery/confirmatory rows, reference spectra, group tables, and supporting analysis outputs are in the root data bundle under `checkpoint_04/`.

```bash
python materialize_studies.py --output reproduced_studies
python studies/checkpoint_04/scripts/cross_architecture_simulation.py \
  --outdir reproduced_studies/intervention_smoke --families haar_z clifford_z \
  --sizes 8 --p-values 0.08 0.24 --trajectories 4 \
  --discovery-trajectories 2 --probe-taus 1 --workers 1
python studies/checkpoint_04/scripts/build_consolidated_checkpoint04_analysis.py \
  --primary reproduced_studies/checkpoint_04/data/intervention/primary_rank4 \
  --independent reproduced_studies/checkpoint_04/data/intervention/independent_seed_rank4 \
  --rank2 reproduced_studies/checkpoint_04/data/intervention/posthoc_rank2 \
  --outdir reproduced_studies/intervention_analysis --bootstrap-reps 4000
```

The consolidated original analyses include unnormalized outcomes. The current Figure 1 point-estimate replay uses `scripts/analysis/reproduce_core_records.py`. The older design bootstrap in `studies/figure_design/bootstrap_reference.py` does not reproduce the accepted hybrid intervals; see `docs/REPRODUCIBILITY_LIMITS.md`. Do not interchange relative and unnormalized response magnitudes.

The preserved runs use rank four and a post-hoc rank-two control. The rank-flexible simulator accepts other ranks, but software support is not evidence that a rank-eight campaign was completed. No new physical experiment or later channel calculation belongs to this study.
