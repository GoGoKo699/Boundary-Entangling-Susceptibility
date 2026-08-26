# Checkpoint 04 — fixed-spectrum intervention and response universality

This study asks whether the complete central Schmidt spectrum determines the response to a fresh gate crossing the cut.

## Scientific role

Checkpoint 04 supplies the discovery intervention and the general response theorem:

1. generate monitored states under several circuit and measurement families;
2. replace the central Schmidt eigenvalues by a common reference spectrum while retaining the state-dependent Schmidt vectors;
3. apply the same fresh probe ensemble;
4. compare the resulting relative Rényi-2 response across monitoring histories;
5. derive and validate the exact four-purity response operator for locally dressed two-qubit probes.

The fixed-spectrum contrasts remain negative across five state-generation families, three probe ensembles, and an independent seed. This establishes central-spectrum insufficiency in the tested finite systems. Checkpoint 05 supplies the later physical large-size construction without spectrum replacement.

## Included source

| File | Purpose |
|---|---|
| `scripts/cross_architecture_simulation.py` | State-vector simulator for the intervention and architecture/probe grid |
| `scripts/cp04_common.py` | Shared gates, measurements, Schmidt operations, and response utilities |
| `scripts/analyze_checkpoint04.py` | Held-out contrasts, bootstrap intervals, rank/probe sensitivities, and summaries |
| `scripts/validate_response_operator.py` | Direct two-copy response-operator checks |
| `scripts/validate_gate_invariant_formula.py` | Checks coefficients against entangling power and gate typicality |

## Included results

- `results/intervention_cross_architecture.csv`: architecture/probe endpoint contrasts;
- `results/probe_response_coefficients.csv`: exact response coefficients for the tested probes;
- `results/response_stencil_decomposition.csv`: decomposition into the four required purity features.

The concise theorem is presented in `docs/THEORY.md`; the headline Figure 1 and Figure 2 inputs are in `data/processed/core_figures/`.

## Scope

This study does not establish a thermodynamic universality class or an MIPT order parameter. The spectrum replacement is a diagnostic intervention. Its physical relevance is tested independently with naturally generated exact-spectrum stabilizer states in `studies/checkpoint_05/`.

## Raw-data policy

The full compressed state-response rows, bootstrap arrays, and duplicate generated artifacts remain outside ordinary Git history. They are planned as a versioned release/data-deposit asset; see `docs/DATA_POLICY.md`.
