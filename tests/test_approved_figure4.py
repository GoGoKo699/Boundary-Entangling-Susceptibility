"""Protect the approved no-fit Figure 4 without asserting a fitted decay law."""
from pathlib import Path
import importlib.util
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/figures'))
spec = importlib.util.spec_from_file_location('approved_figure4', ROOT / 'scripts/figures/make_figure_04.py')
plot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plot)


def test_distance_panel_preserves_points_and_has_no_fit(monkeypatch, tmp_path):
    captured = []
    monkeypatch.setattr(plot, 'save_formats', lambda fig, pdf, png: captured.append(fig))
    path = ROOT / 'data/processed/core_figures/figure_04_distance_decay.csv'
    plot.configure()
    plot.distance_panel(path, tmp_path / 'distance.pdf', tmp_path / 'distance.png')
    ax = captured[0].axes[0]
    data = pd.read_csv(path)
    marker_line = next(line for line in ax.lines if line.get_marker() == 'o')
    np.testing.assert_allclose(marker_line.get_xdata(), data.distance)
    np.testing.assert_allclose(marker_line.get_ydata(), data.estimate)
    texts = [text.get_text() for text in ax.texts]
    assert texts == [r'$\Delta S_m=0$']
    # Error-bar cap lines and the horizontal zero reference are permitted.
    assert not any(len(line.get_xdata()) > len(data) for line in ax.lines)
    error_segments = ax.collections[0].get_segments()
    np.testing.assert_allclose([seg[0,1] for seg in error_segments], data.ci_low)
    np.testing.assert_allclose([seg[1,1] for seg in error_segments], data.ci_high)


def test_active_export_does_not_require_historical_fit_json():
    source = (ROOT / 'reproduce.py').read_text()
    assert '--fit-json' not in source
