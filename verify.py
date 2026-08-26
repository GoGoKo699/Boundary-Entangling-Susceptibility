#!/usr/bin/env python3
"""Fast repository-level scientific and structural verification."""
from __future__ import annotations

from pathlib import Path
import json

import pandas as pd

from boundary_susceptibility.boundary_codes import stabilizer_boundary_response
from boundary_susceptibility.response import haar_clifford_relative_response

ROOT = Path(__file__).resolve().parent

REQUIRED = [
    "README.md",
    "docs/SCIENTIFIC_STORY.md",
    "docs/THEORY.md",
    "docs/NUMERICAL_METHODS.md",
    "scripts/figures/make_figure_01.py",
    "scripts/figures/make_figure_02.py",
    "scripts/figures/make_figure_03.py",
    "scripts/figures/make_figure_04.py",
    "figures/core_svg/figure_01_panel_b.svg",
    "figures/core_svg/figure_02_response_matrix.svg",
    "figures/core_svg/figure_02_redistribution_matrix.svg",
    "figures/core_svg/figure_03_size_scaling.svg",
    "figures/core_svg/figure_04_distance_decay.svg",
    "figures/core_svg/figure_04_conditioning_contrast.svg",
]

missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
if missing:
    raise SystemExit(f"missing required repository files: {missing}")

# Exact nine-state stabilizer response alphabet.
expected = {
    (-1, -1): 0.6,
    (-1, 0): 0.4,
    (-1, 1): 0.0,
    (0, -1): 0.4,
    (0, 0): 0.2,
    (0, 1): -0.2,
    (1, -1): 0.0,
    (1, 0): -0.2,
    (1, 1): -0.6,
}
for code, value in expected.items():
    actual = stabilizer_boundary_response(*code)
    if abs(actual - value) > 1e-12:
        raise SystemExit(f"boundary-code identity failed for {code}: {actual}")

# Independent check of the neighboring-purity formula.
check = haar_clifford_relative_response(
    p_left=0.125,
    p_center=0.25,
    p_right=0.125,
    d=4,
)
if abs(check - 0.8) > 1e-12:
    raise SystemExit(f"neighboring-purity response identity failed: {check}")

# Figure 1: every held-out and independent interval remains below zero.
f1 = pd.read_csv(ROOT / "data/processed/core_figures/figure_01_panel_b.csv")
if len(f1) != 10 or not (f1["estimate"] < 0).all() or not (f1["ci_high"] < 0).all():
    raise SystemExit("Figure 1 sign/row-count verification failed")

# Figure 2: exact probability conservation and response reconstruction.
f2 = pd.read_csv(ROOT / "data/processed/core_figures/figure_02_boundary_codes.csv")
if len(f2) != 9:
    raise SystemExit("Figure 2 must contain all nine boundary codes")
if abs(float(f2["display_probability_slope"].sum())) > 5e-6:
    raise SystemExit("Figure 2 boundary-code probability slopes do not conserve probability")
reconstruction = float(f2["susceptibility_contribution"].sum())
direct = float(f2["direct_total_beta"].iloc[0])
if abs(reconstruction - direct) > 1e-12:
    raise SystemExit("Figure 2 susceptibility reconstruction failed")

# Figure 3: all finite-size and thermodynamic estimates are negative.
f3 = pd.read_csv(ROOT / "data/processed/core_figures/figure_03_size_scaling.csv")
if len(f3) != 20 or not (f3["beta"] < 0).all() or not (f3["ci_high"] < 0).all():
    raise SystemExit("Figure 3 persistence/replication verification failed")

# Figure 4: distance decay is negative and approaches zero; conditioning flips sign.
f4d = pd.read_csv(ROOT / "data/processed/core_figures/figure_04_distance_decay.csv")
if not (f4d["estimate"] < 0).all():
    raise SystemExit("Figure 4 distance effects must all be negative")
if not (f4d["estimate"].abs().diff().dropna() < 0).all():
    raise SystemExit("Figure 4 distance effect must decay monotonically in magnitude")
f4c = pd.read_csv(ROOT / "data/processed/core_figures/figure_04_conditioning_contrast.csv")
contrast = f4c.set_index("condition")["estimate"]
if not (
    contrast["unconditional"] > 0
    and contrast["central_spectrum_unchanged"] < 0
):
    raise SystemExit("Figure 4 conditional/unconditional sign reversal failed")

fit = json.loads(
    (ROOT / "data/processed/core_figures/figure_04_distance_fit.json").read_text(
        encoding="utf-8"
    )
)
if not (2.0 < float(fit["decay_length"]) < 3.0):
    raise SystemExit("Figure 4 decay length is outside the audited range")

# Repository policy: no manuscript or TikZ sources in the tracked project.
# Build the forbidden marker dynamically so this verifier does not match itself.
tikz_marker = "\\begin{" + "tikzpicture}"
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path.suffix.lower() == ".tex":
        raise SystemExit(f"TeX source is excluded from this repository: {path}")
    if path.suffix.lower() in {".md", ".py", ".yml", ".yaml"}:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        if tikz_marker in text:
            raise SystemExit(f"TikZ source is excluded from this repository: {path}")

print("verification passed")
