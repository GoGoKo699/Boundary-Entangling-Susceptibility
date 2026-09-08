# Physical stabilizer scaling and paired location study

The source implements phase-free tableau evolution, exact cut entropies, conditional regression, size/time sensitivity, code redistribution, transition context, and paired projective measurements. Original state and intervention rows, archived resamples, group/maps, and supporting analysis outputs are in the root data bundle under `checkpoint_05/`.

```bash
python materialize_studies.py --output reproduced_studies
python scripts/analysis/reassess_evidence.py --output reproduced_evidence
```

For direct simulator validation, use the complete command in [the reproduction guide](../../docs/REPRODUCTION.md). `run_tableau_scaling.py --help` exposes the campaign parameters. The design subdirectory retains original locks and their checksums; default CLI settings alone do not identify a particular archived run.

Current interpretation preserves negative finite-size coefficients and the conditional paired location result. The historical exponential fit is not an endorsed law or physical length. No deterministic causal effect of the long-run monitoring probability is claimed. A disjoint seed is not external replication.
