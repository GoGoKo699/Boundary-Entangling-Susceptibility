# Extended results

The repository is slightly broader than the planned Letter. The four core figures remain the primary narrative, while the study directories preserve the most useful robustness and generalization results.

## Checkpoint 04 extensions

Under `studies/checkpoint_04/results/`:

- `intervention_cross_architecture.csv`: five state-generation families, the primary fresh probe, and independent-seed comparisons;
- `probe_response_coefficients.csv`: exact four-purity coefficients for the tested locally dressed probes;
- `response_stencil_decomposition.csv`: state-side purity shifts entering each response stencil.

The included source also supports rank-2, rank-4, and rank-8 interventions, three fresh-probe ensembles, and direct validation of the local-twirl coefficient formula.

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
