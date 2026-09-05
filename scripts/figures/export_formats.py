"""Export one Matplotlib Figure to three formats without changing its layout."""
from pathlib import Path
import matplotlib as mpl

def save_formats(figure, pdf: Path, png: Path) -> None:
    pdf, png = Path(pdf), Path(png)
    pdf.parent.mkdir(parents=True, exist_ok=True)
    png.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(pdf, metadata={'CreationDate': None, 'ModDate': None})
    figure.savefig(png, dpi=400)
    # SVG text keeps browser files small; the PDF embeds the publication fonts.
    # Browser fallback fonts need not rasterize identically to the embedded PDF.
    with mpl.rc_context({'svg.fonttype': 'none', 'svg.hashsalt': 'boundary-susceptibility'}):
        figure.savefig(pdf.with_suffix('.svg'), metadata={'Date': None})
