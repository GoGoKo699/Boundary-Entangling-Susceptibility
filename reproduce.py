#!/usr/bin/env python3
"""Regenerate the six core Python panels from canonical tables."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def run(command: list[object]) -> None:
    command_text = [str(item) for item in command]
    print("+", " ".join(command_text))
    subprocess.run(command_text, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-figures", action="store_true")
    args = parser.parse_args()
    if not args.core_figures:
        parser.error("select --core-figures")

    output = ROOT / "reproduced_figures"
    output.mkdir(exist_ok=True)

    run(
        [
            sys.executable,
            ROOT / "scripts/figures/make_figure_01_frozen.py",
            "--csv",
            ROOT / "data/processed/core_figures/figure_01_panel_b.csv",
            "--pdf",
            output / "figure_01_panel_b.pdf",
            "--png",
            output / "figure_01_panel_b.png",
        ]
    )
    run(
        [
            sys.executable,
            ROOT / "scripts/figures/make_figure_02.py",
            "--csv",
            ROOT / "data/processed/core_figures/figure_02_boundary_codes.csv",
            "--outdir",
            output,
        ]
    )
    run(
        [
            sys.executable,
            ROOT / "scripts/figures/make_figure_03.py",
            "--csv",
            ROOT / "data/processed/core_figures/figure_03_size_scaling.csv",
            "--pdf",
            output / "figure_03_size_scaling.pdf",
            "--png",
            output / "figure_03_size_scaling.png",
        ]
    )
    run(
        [
            sys.executable,
            ROOT / "scripts/figures/make_figure_04.py",
            "--distance-csv",
            ROOT / "data/processed/core_figures/figure_04_distance_decay.csv",
            "--contrast-csv",
            ROOT / "data/processed/core_figures/figure_04_conditioning_contrast.csv",
            "--fit-json",
            ROOT / "data/processed/core_figures/figure_04_distance_fit.json",
            "--distance-pdf",
            output / "figure_04_distance_decay.pdf",
            "--distance-png",
            output / "figure_04_distance_decay.png",
            "--contrast-pdf",
            output / "figure_04_conditioning_contrast.pdf",
            "--contrast-png",
            output / "figure_04_conditioning_contrast.png",
        ]
    )

    print(f"Core figures written to {output}")


if __name__ == "__main__":
    main()
