#!/usr/bin/env python3
"""Export retained CP04 chi2 endpoints and exact stencils from original records.

This record-only calculation does not generate physical samples or bootstrap
draws. Archived intervals are copied only after the matching point is verified.
They are not the current Figure 1 intervals, whose estimand and support differ.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import csv
from fractions import Fraction
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "studies/checkpoint_04/results"
TOLERANCE = 2e-12
P_LOW, P_HIGH = 0.08, 0.24
RUNS = ("primary_rank4", "independent_seed_rank4")
ARCHIVE_RUN = {"primary_rank4": "primary_rank4", "independent_seed_rank4": "independent_rank4"}
ARCHIVED_ENDPOINTS = "checkpoint_04/analysis/consolidated/intervention_cross_architecture.csv"
SOURCE_SHA256 = {
    "checkpoint_04/data/intervention/primary_rank4/state_response_rows.csv.gz":
        "1f3139866d13838a659e4c6e9e127170f11a7050ead1885810796f67bd89068c",
    "checkpoint_04/data/intervention/independent_seed_rank4/state_response_rows.csv.gz":
        "153710199f198a1440f56e610255c61628eba4f9ee4745737ed03e9fc6693026",
    ARCHIVED_ENDPOINTS: "9342e61c83d155e1c3be62861e6029a68870da854813efc79213b3ee66529995",
}
# Output-purity coefficients in the order (P_L, P_A, P_Lb, P_R).
# Exact rational values of probe_response_coefficients.csv; no gate simulation.
COEFFICIENTS = {
    "haar_or_clifford_2design": (Fraction(2, 5), 0, 0, Fraction(2, 5)),
    "cartan_xy_pi8": (Fraction(1, 3), Fraction(1, 4), Fraction(-1, 12), Fraction(1, 3)),
    "cartan_xx_pi4": (Fraction(4, 9), Fraction(1, 9), Fraction(-2, 9), Fraction(4, 9)),
}
FILES = ("intervention_cross_architecture.csv", "response_stencil_decomposition.csv",
         "intervention_comparison_support.csv", "supporting_records_manifest.json")


def mean(values):
    values = list(values)
    if not values:
        raise ValueError("An empty cell cannot enter the estimator")
    return math.fsum(values) / len(values)


def require_close(actual, expected, label):
    if not math.isfinite(actual) or not math.isfinite(expected) or abs(actual - expected) > TOLERANCE:
        raise ValueError(f"{label}: {actual!r} versus {expected!r}")


def read_sources(archive):
    tables = {}
    with zipfile.ZipFile(archive) as bundle:
        for member, expected in SOURCE_SHA256.items():
            content = bundle.read(member)
            actual = hashlib.sha256(content).hexdigest()
            if actual != expected:
                raise ValueError(f"Source-member identity mismatch: {member}")
            if member.endswith(".gz"):
                content = gzip.decompress(content)
            tables[member] = list(csv.DictReader(io.StringIO(content.decode("utf-8"))))
    return tables


def reconstruct(archive):
    sources = read_sources(archive)
    archived = {(r["run"], r["family"], r["probe"]): r for r in sources[ARCHIVED_ENDPOINTS]}
    endpoints, decompositions, support = [], [], []
    maximum_row_error = maximum_archived_error = 0.0
    for run in RUNS:
        member = f"checkpoint_04/data/intervention/{run}/state_response_rows.csv.gz"
        grouped = defaultdict(list)
        for row in sources[member]:
            p = float(row["p_measure"])
            if row["split"] == "confirmatory" and row["variant"] == "equalized_rank4" and p in (P_LOW, P_HIGH):
                key = (row["family"], int(row["n"]), float(row["tau"]), p)
                grouped[key].append(row)
        for family in sorted({key[0] for key in grouped}):
            cells = sorted({(n, tau) for f, n, tau, _ in grouped if f == family
                            and (f, n, tau, P_LOW) in grouped and (f, n, tau, P_HIGH) in grouped})
            if not cells:
                raise ValueError(f"No two-rate support: {run}/{family}")
            shifts = []
            for n, tau in cells:
                d = 2 ** (n // 2)
                factor = d / (d - 1)
                pools = {p: grouped[(family, n, tau, p)] for p in (P_LOW, P_HIGH)}
                for p, rows in pools.items():
                    ids = [r["trajectory_id"] for r in rows]
                    if len(set(ids)) != len(ids):
                        raise ValueError(f"Duplicate trajectory in {run}/{family}/{n}/{tau}/{p}")
                    support.append({"run": run, "family": family, "n": n, "tau": tau,
                                    "p_measure": p, "eligible_rows": len(rows),
                                    "eligible_trajectories": len(set(ids)),
                                    "cell_weight": 1 / len(cells), "D_over_D_minus_1": factor})
                delta = {key: mean(float(r[key]) for r in pools[P_HIGH]) -
                         mean(float(r[key]) for r in pools[P_LOW]) for key in ("P_A", "P_L", "P_Lb", "P_R")}
                require_close(delta["P_A"], 0.0, f"Fixed reference purity: {run}/{family}/{n}/{tau}")
                shifts.append((factor, delta))
            for probe, rational in COEFFICIENTS.items():
                coeff = tuple(float(x) for x in rational)
                field = f"probe_{probe}_delta_linear_norm"
                direct_cells = []
                for n, tau in cells:
                    factor = 2 ** (n // 2) / (2 ** (n // 2) - 1)
                    for p in (P_LOW, P_HIGH):
                        for r in grouped[(family, n, tau, p)]:
                            predicted = factor * ((1 - coeff[1]) * float(r["P_A"]) - coeff[0] * float(r["P_L"])
                                                  - coeff[2] * float(r["P_Lb"]) - coeff[3] * float(r["P_R"]))
                            direct = float(r[field])
                            require_close(predicted, direct, f"Rowwise stencil: {run}/{r['state_id']}/{probe}")
                            maximum_row_error = max(maximum_row_error, abs(predicted - direct))
                    direct_cells.append(mean(float(r[field]) for r in grouped[(family, n, tau, P_HIGH)]) -
                                        mean(float(r[field]) for r in grouped[(family, n, tau, P_LOW)]))
                estimate = mean(direct_cells)
                weights = (1 - coeff[1], -coeff[0], -coeff[2], -coeff[3])
                terms = [mean(factor * weight * delta[key] for factor, delta in shifts)
                         for key, weight in zip(("P_A", "P_L", "P_Lb", "P_R"), weights)]
                reconstructed = math.fsum(terms)
                require_close(reconstructed, estimate, f"Pooled stencil: {run}/{family}/{probe}")
                old = archived[(ARCHIVE_RUN[run], family, probe)]
                require_close(estimate, float(old["estimate"]), f"Archived point: {run}/{family}/{probe}")
                maximum_archived_error = max(maximum_archived_error, abs(estimate - float(old["estimate"])))
                endpoints.append({"run": run, "intervention_rank": 4, "family": family, "probe": probe,
                                  "estimate": estimate, "archived_ci_low": float(old["ci_low"]),
                                  "archived_ci_high": float(old["ci_high"]),
                                  "archived_bootstrap_reps": int(old["bootstrap_reps"]),
                                  "p_low": P_LOW, "p_high": P_HIGH, "common_cells_within_run": len(cells),
                                  "interval_status": "archived_variable_support_not_regenerated"})
                if run == "primary_rank4":
                    decomposition = dict(zip(("central_spectrum_contribution", "neighbor_P_L_contribution",
                                              "boundary_cross_P_Lb_contribution", "neighbor_P_R_contribution"), terms))
                    row = {"run": run, "family": family, "probe": probe, **decomposition,
                           "reconstruction": reconstructed, "observed_response_contrast": estimate,
                           "common_cells_within_run": len(cells)}
                    for key in ("P_A", "P_L", "P_Lb", "P_R"):
                        row[f"delta_{key}"] = mean(delta[key] for _, delta in shifts)
                        row[f"D_weighted_delta_{key}"] = mean(factor * delta[key] for factor, delta in shifts)
                    decompositions.append(row)
    manifest = {
        "schema_version": 1,
        "generator": "scripts/analysis/reproduce_supporting_records.py",
        "source_member_sha256": SOURCE_SHA256,
        "source_archive": "entanglement-data.zip",
        "row_filter": {"split": "confirmatory", "variant": "equalized_rank4", "p_measure": [P_LOW, P_HIGH]},
        "runs": list(RUNS),
        "archive_run_labels": ARCHIVE_RUN,
        "estimand": "chi2: normalized linear-entropy change; NOT divided by input purity",
        "contrast": "mean over supported (n,tau) cells of mean(p=.24) minus mean(p=.08)",
        "support": "two-rate nonempty cells separately within each run/family, not cross-run intersection",
        "weighting": "equal (n,tau) cells; equal eligible state rows within each rate cell",
        "normalization": "D/(D-1) applied within each n cell, D=2**(n//2)",
        "sampling_unit": "physical trajectory; observations at different tau are dependent",
        "reference_and_support_uncertainty": "not propagated",
        "coefficients_order": ["P_L", "P_A", "P_Lb", "P_R"],
        "coefficients_exact": {key: [str(x) for x in values] for key, values in COEFFICIENTS.items()},
        "uncertainty": {
            "status": "archived endpoint intervals only; no new bootstrap draws",
            "source_member": ARCHIVED_ENDPOINTS,
            "source_generator": "studies/checkpoint_04/scripts/build_consolidated_checkpoint04_analysis.py:balanced_bootstrap",
            "procedure": "4000 trajectory-stratified draws; undefined cells omitted within a draw; linear 2.5/97.5 percentiles",
            "scope": "older post-hoc pointwise supporting diagnostic, not simultaneous or exact-coverage intervals",
            "not_current_figure1": "no full-support proposal rejection; chi2 instead of chi_rel; within-run support",
            "historical_execution": "matching archived point verified; historical invocation and draw vectors not recovered here",
        },
        "tolerance": TOLERANCE,
        "checks": {"endpoint_rows": len(endpoints), "decomposition_rows": len(decompositions),
                   "maximum_row_stencil_error": maximum_row_error,
                   "maximum_archived_point_error": maximum_archived_error},
    }
    return endpoints, decompositions, support, manifest


def csv_text(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def export(archive, output):
    endpoints, decompositions, support, manifest = reconstruct(archive)
    contents = {"intervention_cross_architecture.csv": csv_text(endpoints),
                "response_stencil_decomposition.csv": csv_text(decompositions),
                "intervention_comparison_support.csv": csv_text(support)}
    manifest["output_sha256"] = {name: hashlib.sha256(value.encode()).hexdigest() for name, value in contents.items()}
    contents["supporting_records_manifest.json"] = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    output.mkdir(parents=True, exist_ok=True)
    for name, value in contents.items():
        (output / name).write_text(value, encoding="utf-8")
    return manifest


def check_canonical(output, canonical=CANONICAL):
    for name in FILES:
        if (output / name).read_bytes() != (canonical / name).read_bytes():
            raise ValueError(f"Canonical supporting export differs: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=ROOT / "entanglement-data.zip")
    parser.add_argument("--output", type=Path, default=Path("reproduced_supporting_records"))
    parser.add_argument("--check", "--check-canonical", dest="check_canonical", action="store_true",
                        help="Require exact equality to all four active generated supporting files")
    args = parser.parse_args()
    if args.output.resolve() == CANONICAL.resolve():
        parser.error("Generate outside canonical results, then review any proposed adoption")
    manifest = export(args.archive, args.output)
    if args.check_canonical:
        check_canonical(args.output)
    print(json.dumps(manifest["checks"], indent=2))


if __name__ == "__main__":
    main()
