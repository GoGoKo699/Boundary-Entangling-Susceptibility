# Figures

## `core_svg/`

Browser-visible SVG exports of the six author-reviewed Python panels:

1. fixed-spectrum intervention response;
2. exact stabilizer response alphabet;
3. monitoring-induced boundary-code redistribution;
4. physical size scaling and independent replication;
5. paired distance decay;
6. conditional versus unconditional location contrast.

The canonical numerical inputs and exact plotting scripts are tracked under
`data/processed/core_figures/` and `scripts/figures/`. Running

```bash
python reproduce.py --core-figures
```

writes fresh PDF and PNG outputs to `reproduced_figures/`.

## Author-reviewed PDF hashes

The exact manuscript-layout PDF and PNG hashes are preserved in
`provenance/figure_sha256.csv`. Binary PDF metadata is not used as a scientific
verification target; `verify.py` checks the underlying values and identities.
