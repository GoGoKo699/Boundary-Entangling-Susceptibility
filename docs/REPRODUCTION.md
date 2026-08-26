# Reproduction

## Core Python panels

Run

```bash
python reproduce.py --core-figures
```

The command reads the canonical files in `data/processed/core_figures/` and writes vector PDFs to `reproduced_figures/`.

The six accepted panels were frozen from the author-reviewed Overleaf baseline. PDF metadata can make regenerated hashes differ even when the numerical and visual content is unchanged, so `verify.py` checks inputs and load-bearing values rather than requiring byte-identical Matplotlib output.

## Full studies

Checkpoint-specific instructions are retained under `studies/checkpoint_04/` and `studies/checkpoint_05/`. Large compressed raw-state archives are handled according to `docs/DATA_POLICY.md`.