# Checkpoint 04 — spectrum intervention and response universality

This study established three ingredients:

1. exact central-spectrum equalization while retaining state-dependent Schmidt vectors;
2. cross-family and cross-probe suppression of the fresh-gate response;
3. an exact two-copy response operator reducing locally dressed probes to a four-purity stencil.

The root documents `docs/THEORY.md` and `docs/SCIENTIFIC_STORY.md` provide the clean exposition. This directory retains the simulation and validation code used for the intervention study and selected derived tables beyond the planned Letter.

## Main scripts

- `scripts/cross_architecture_simulation.py`: state-vector circuit families and spectrum intervention.
- `scripts/analyze_checkpoint04.py`: held-out contrasts, support, and rank checks.
- `scripts/validate_response_operator.py`: direct response-operator validation.
- `scripts/validate_gate_invariant_formula.py`: invariant-coefficient check.

Large raw state-row archives are not stored in ordinary Git history; see `docs/DATA_POLICY.md`.
