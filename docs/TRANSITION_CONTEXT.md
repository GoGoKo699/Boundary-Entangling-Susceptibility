# Relation to the monitored transition

Quarter-partition tripartite information places the high-size crossing near
$p\simeq0.27$ in the package convention, where $p$ is the measurement
probability per site per complete two-sublayer brickwork cycle. This convention
must be converted before numerical comparison with studies that measure after
each sublayer.

The fitted within-spectrum monitoring coefficient remains negative on both
sides of the crossing, with a smaller magnitude above it. This is a statement
about the coefficient of monitoring probability in the secondary hinge fit,
not a statement that every state's susceptibility is negative. The response
is **transition-sensitive but not an established order parameter**; the
observed coefficient change does not demonstrate distinct thermodynamic
limits or a singularity of the susceptibility.

The selected hinge-fit table is
`studies/checkpoint_05/results/transition_crossover_hinge_fits.csv`. The
transition-analysis source is
`studies/checkpoint_05/scripts/analyze_transition_crossover.py`. The
susceptibility was not used to choose the crossing location.

The crossing algorithm only considers grid intervals within `[0.235,0.295]`
and selects the candidate nearest `0.26`. Bootstrap proposals without a
crossing are omitted, so the reported intervals condition on crossing
existence under this rule. These are finite-size contextual estimates from
a different observable on the same trajectories, not a precise universal
critical point. See [Methods, Section 8](NUMERICAL_METHODS.md#8-independent-transition-estimate).
