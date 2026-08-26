# Reproduction

## Core Python panels

Run

```bash
python reproduce.py --core-figures
```

The command reads the canonical files in `data/processed/core_figures/` and writes vector PDFs to `reproduced_figures/`.

The six accepted panels in `figures/core/` were frozen from the author-reviewed Overleaf baseline. PDF metadata can make regenerated hashes differ even when the numerical and visual content is unchanged, so `verify.py` checks inputs and load-bearing values rather than requiring byte-identical Matplotlib output.

## Full studies

Checkpoint-specific instructions are in `studies/checkpoint_04/README.md` and `studies/checkpoint_05/README.md`. The complete packages under `archives/` retain compressed raw arrays and tables.
