# Core figure scripts

The supported entry point is `python reproduce.py --core-figures` from the repository root. It rebuilds all six panels in a fresh staging directory and validates 18 files: six PDFs, six PNGs, and six SVGs. The same Figure object is passed to each backend. PDF date metadata and SVG identifiers are stabilized; complete cross-platform binary equality is not promised.

| Figure | Supported script | Panels |
|---|---|---|
| 1 | `make_figure_01_frozen.py` | Fixed-spectrum response |
| 2 | `make_figure_02.py` | Response and redistribution matrices |
| 3 | `make_figure_03.py` | Size scaling |
| 4 | `make_figure_04.py` | Distance profile and conditioning contrast |

`export_formats.py` provides the common export function. Browser SVGs use text and may use fallback fonts; the PDF is the publication-font reference. The earlier `make_figure_01.py` is not called by the supported command.

The accepted numerical panels are preserved. The current Figure 4 distance panel contains neither an exponential curve nor a fitted-length annotation; the old fit is retained only as historical provenance. See [the current figure baseline](../../docs/FIGURE_BASELINE.md) and [evidence reassessment](../../docs/EVIDENCE_REASSESSMENT.md). Editable external composite schematics remain unavailable; numerical-panel reproduction does not verify an external manuscript layout.

[Next: figure-to-data gallery](../../figures/README.md) · [Return to README](../../README.md)
