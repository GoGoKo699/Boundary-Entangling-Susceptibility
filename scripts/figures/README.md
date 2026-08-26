# Core figure scripts

`reproduce.py --core-figures` is the supported entry point.

| Composite figure | Script | Outputs |
|---|---|---|
| Figure 1 | `make_figure_01_frozen.py` | response forest PDF and PNG |
| Figure 2 | `make_figure_02.py` | response-alphabet and redistribution PDFs |
| Figure 3 | `make_figure_03.py` | size-scaling PDF and PNG |
| Figure 4 | `make_figure_04.py` | distance-decay and conditioning-contrast PDFs and PNGs |

`make_figure_01_frozen.py` contains the final author-reviewed typography and spacing. The earlier `make_figure_01.py` is retained only as a pre-freeze plotting variant and is not called by the supported reproduction command.

All scripts read human-readable canonical tables from `data/processed/core_figures/`. They do not read manuscript TeX or TikZ.
