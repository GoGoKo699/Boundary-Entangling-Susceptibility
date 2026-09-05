# Core figure scripts

The supported entry point is `python reproduce.py --core-figures` from the repository root. It rebuilds all six panels in a fresh staging directory and validates 18 files: six PDFs, six PNGs, and six SVGs. The same Figure object is passed to each backend. PDF date metadata and SVG identifiers are stabilized; complete cross-platform binary equality is not promised.

| Figure | Supported script | Panels |
|---|---|---|
| 1 | `make_figure_01_frozen.py` | Fixed-spectrum response |
| 2 | `make_figure_02.py` | Response and redistribution matrices |
| 3 | `make_figure_03.py` | Size scaling |
| 4 | `make_figure_04.py` | Distance profile and conditioning contrast |

`export_formats.py` provides the common export function. Browser SVGs use text and may use fallback fonts; the PDF is the publication-font reference. The earlier `make_figure_01.py` is not called by the supported command.

The plot values and accepted manuscript layout are preserved. Figure 4 still contains the historical exponential for reproducibility; that fit is not endorsed as a physical law. See [`../../docs/EVIDENCE_REASSESSMENT.md`](../../docs/EVIDENCE_REASSESSMENT.md) before interpreting the curve or its xi annotation.
