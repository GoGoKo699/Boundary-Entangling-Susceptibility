"""Ensure the GitHub browser panel is the same adopted export as the PDF."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_browser_svg_matches_current_plot(tmp_path):
    subprocess.run([
        sys.executable, str(ROOT / "scripts/figures/make_figure_01_frozen.py"),
        "--csv", str(ROOT / "data/processed/core_figures/figure_01_panel_b.csv"),
        "--pdf", str(tmp_path / "figure_01_panel_b.pdf"),
        "--png", str(tmp_path / "figure_01_panel_b.png"),
    ], check=True)
    expected = (tmp_path / "figure_01_panel_b.svg").read_bytes()
    assert (ROOT / "figures/core_svg/figure_01_panel_b.svg").read_bytes() == expected
    assert not (ROOT / "figures/core/figure_01_panel_b.svg").exists()
