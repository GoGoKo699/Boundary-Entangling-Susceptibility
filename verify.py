#!/usr/bin/env python3
"""Fast repository-level scientific, rendering, and structural verification."""
from __future__ import annotations

import csv
import html
import json
from pathlib import Path
import re
from urllib.parse import unquote
import xml.etree.ElementTree as ET

import pandas as pd

from boundary_susceptibility.boundary_codes import stabilizer_boundary_response
from boundary_susceptibility.response import haar_clifford_relative_response

ROOT = Path(__file__).resolve().parent

REQUIRED = [
    "README.md",
    "docs/SCIENTIFIC_STORY.md",
    "docs/THEORY.md",
    "docs/NUMERICAL_METHODS.md",
    "docs/VALIDATION.md",
    "docs/REPRODUCTION.md",
    "provenance/figure_sha256.csv",
    "scripts/figures/make_figure_01_frozen.py",
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

# Every browser figure must be well-formed SVG rather than a broken placeholder.
for svg_path in sorted((ROOT / "figures/core_svg").glob("*.svg")):
    if svg_path.stat().st_size < 1000:
        raise SystemExit(f"SVG is unexpectedly small: {svg_path.relative_to(ROOT)}")
    try:
        root_element = ET.parse(svg_path).getroot()
    except ET.ParseError as exc:
        raise SystemExit(f"invalid SVG {svg_path.relative_to(ROOT)}: {exc}") from exc
    if not root_element.tag.lower().endswith("svg"):
        raise SystemExit(f"unexpected SVG root element: {svg_path.relative_to(ROOT)}")

# Verify that local Markdown links and HTML image sources resolve in a clean clone.
markdown_link = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
html_source = re.compile(r"<(?:img|source)\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
external_prefixes = ("http://", "https://", "mailto:", "data:", "#")
broken_links: list[str] = []

for markdown_path in sorted(ROOT.rglob("*.md")):
    if ".git" in markdown_path.parts:
        continue
    text = markdown_path.read_text(encoding="utf-8", errors="strict")
    raw_targets = markdown_link.findall(text) + html_source.findall(text)
    for raw_target in raw_targets:
        target = html.unescape(raw_target.strip())
        if not target or target.startswith(external_prefixes):
            continue
        if target.startswith("<") and ">" in target:
            target = target[1 : target.index(">")]
        elif re.search(r"\s+[\"']", target):
            target = re.split(r"\s+[\"']", target, maxsplit=1)[0]
        target = unquote(target.split("#", 1)[0].split("?", 1)[0]).strip()
        if not target:
            continue
        candidate = ROOT / target.lstrip("/") if target.startswith("/") else markdown_path.parent / target
        if not candidate.resolve().exists():
            broken_links.append(
                f"{markdown_path.relative_to(ROOT)} -> {raw_target}"
            )

if broken_links:
    details = "\n".join(f"  - {item}" for item in broken_links)
    raise SystemExit(f"broken local documentation links:\n{details}")

# The frozen-PDF manifest identifies external author-reviewed binaries honestly.
manifest_path = ROOT / "provenance/figure_sha256.csv"
with manifest_path.open(newline="", encoding="utf-8") as handle:
    manifest_rows = list(csv.DictReader(handle))
required_manifest_columns = {
    "accepted_filename",
    "source_archive",
    "sha256",
    "bytes",
    "browser_copy",
    "reproduction_script",
    "tracked_binary",
}
if len(manifest_rows) != 6:
    raise SystemExit("figure provenance manifest must contain exactly six PDF panels")
if not required_manifest_columns.issubset(manifest_rows[0]):
    raise SystemExit("figure provenance manifest has missing columns")
seen_filenames: set[str] = set()
for row in manifest_rows:
    filename = row["accepted_filename"]
    digest = row["sha256"]
    if filename in seen_filenames or not filename.endswith(".pdf"):
        raise SystemExit(f"invalid or duplicate accepted figure filename: {filename}")
    seen_filenames.add(filename)
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise SystemExit(f"invalid SHA-256 for {filename}")
    if int(row["bytes"]) <= 0:
        raise SystemExit(f"invalid byte count for {filename}")
    if row["source_archive"] != "Overleaf.zip" or row["tracked_binary"].lower() != "false":
        raise SystemExit(f"incorrect tracking status for {filename}")
    for field in ("browser_copy", "reproduction_script"):
        if not (ROOT / row[field]).is_file():
            raise SystemExit(f"missing {field} for {filename}: {row[field]}")

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
