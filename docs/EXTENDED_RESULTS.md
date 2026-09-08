# Extended results

The repository is slightly broader than the planned Letter. The four core figures remain the primary narrative, while the study directories preserve the most useful robustness and generalization results.

## Checkpoint 04 extensions

Under [studies/checkpoint_04/results/](../studies/checkpoint_04/results/README.md):

- `intervention_cross_architecture.csv`: five state-generation families, three fresh probes, and primary/independent rank-four comparisons;
- `probe_response_coefficients.csv`: exact four-purity coefficients for the tested locally dressed probes;
- `response_stencil_decomposition.csv`: state-side purity shifts entering each response stencil.

These repaired compact exports are bound to original state records, with exact
per-cell normalization, support counts and a deterministic replay command in
the linked results guide. They report the normalized linear-entropy change chi2
without division by input purity, rather than Figure 1's chi_rel, and each run
uses its own two-rate comparison support.
The explicitly named `archived_ci_*` columns are older 4,000-draw, variable-support
pointwise bootstrap diagnostics, not freshly generated intervals or the
current Figure 1 uncertainty. The inconsistent previous compact tables remain
clearly marked historical; none of the canonical four-figure inputs is replaced
by this repair.

The included source also supports recorded rank-2 and rank-4 interventions (the rank-flexible code supports other ranks, but that alone is not a recorded result), three fresh-probe ensembles, and direct validation of the local-twirl coefficient formula.

The gate-space sufficient criterion in [THEORY](THEORY.md#6-fixed-spectrum-gate-space-criterion)
is exact at a fixed dimension. The archived gate-space analysis pools raw purity
shifts equally over size/time cells, whereas a pooled chi2 criterion needs the
cell-specific D/(D-1) factors. The independent audit found positive margins for
both point constructions, but the archived raw-shift intervals are not
dimension-weighted intervals. The older gate-space bootstrap also omits empty
cells within a draw and checks marginal lower endpoints. It is therefore a
post-hoc supporting direction diagnostic, not a simultaneous confidence
guarantee over every probe, family or size. No new extension bootstrap is claimed
by the deterministic compact-table repair.

## Checkpoint 05 extensions

Under `studies/checkpoint_05/`:

- timestamped primary, replication, calibration, and paired-intervention design locks;
- finite-size, time-window, transition, boundary-code, and paired-location analysis source;
- direct tableau-versus-state-vector validation source;
- `results/transition_crossover_hinge_fits.csv` for the transition-context sensitivity analysis.

The canonical large-size, boundary-code, and paired-intervention estimates plotted in the main figures are kept once, without duplication, under `data/processed/core_figures/`.

## Results intentionally kept secondary

- alternative fixed finite-size correction powers;
- time-resolved response slopes;
- the hinge fit around the independently located transition;
- the general locally dressed four-purity response family;
- gate-space sufficient conditions;
- conditional/unconditional response decomposition;
- simple bounded-window entropy-summary reconstruction.

These results test scope and mechanism. They are not separate headline claims and should not be interpreted as a new order parameter, critical exponent, or generic non-Clifford thermodynamic theorem.
