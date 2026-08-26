#!/usr/bin/env python3
"""Analyze Checkpoint 04 cross-architecture and physical-matching data."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

PROBES = (
    "haar_or_clifford_2design",
    "cartan_xy_pi8",
    "cartan_xx_pi4",
)
P_VALUES = (0.08, 0.16, 0.24)
PAIRINGS = ((0.08, 0.16), (0.16, 0.24), (0.08, 0.24))


def response_col(probe: str) -> str:
    return f"probe_{probe}_delta_linear_norm"


def percentile_interval(values: np.ndarray) -> tuple[float, float]:
    vals = np.asarray(values, float)
    vals = vals[np.isfinite(vals)]
    return float(np.quantile(vals, 0.025)), float(np.quantile(vals, 0.975))


def build_cluster_matrices(
    sub: pd.DataFrame, col: str, p_values: tuple[float, ...]
) -> tuple[list[float], dict[tuple[int, float], np.ndarray]]:
    taus = sorted(sub.tau.unique().tolist())
    mats: dict[tuple[int, float], np.ndarray] = {}
    for n in sorted(sub.n.unique()):
        for p in p_values:
            g = sub[(sub.n == n) & np.isclose(sub.p_measure, p)]
            if len(g) == 0:
                continue
            pivot = g.pivot_table(index="trajectory_index", columns="tau", values=col, aggfunc="first")
            pivot = pivot.reindex(columns=taus)
            mats[(int(n), float(p))] = pivot.to_numpy(float)
    return taus, mats


def balanced_contrast(
    sub: pd.DataFrame,
    col: str,
    p_low: float,
    p_high: float,
    bootstrap: int,
    seed: int,
    size_filter: int | None = None,
) -> dict[str, float | int]:
    x = sub.copy()
    if size_filter is not None:
        x = x[x.n == size_filter]
    taus, mats = build_cluster_matrices(x, col, (p_low, p_high))
    sizes = sorted({n for n, _ in mats})

    def estimate_from_means(means: dict[tuple[int, float], np.ndarray]) -> float:
        diffs = []
        for n in sizes:
            lo = means.get((n, p_low))
            hi = means.get((n, p_high))
            if lo is None or hi is None:
                continue
            d = hi - lo
            diffs.extend(d[np.isfinite(d)].tolist())
        return float(np.mean(diffs)) if diffs else math.nan

    observed_means = {key: np.nanmean(arr, axis=0) for key, arr in mats.items()}
    estimate = estimate_from_means(observed_means)
    rng = np.random.default_rng(seed)
    boot = np.empty(bootstrap, float)
    for b in range(bootstrap):
        means = {}
        for key, arr in mats.items():
            idx = rng.integers(0, arr.shape[0], size=arr.shape[0])
            means[key] = np.nanmean(arr[idx], axis=0)
        boot[b] = estimate_from_means(means)
    ci_low, ci_high = percentile_interval(boot)
    return {
        "estimate": estimate,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "bootstrap_replicates": bootstrap,
        "sizes": len(sizes),
        "time_cells": len(taus),
        "rows": len(x),
    }


def make_intervention_tables(df: pd.DataFrame, outdir: Path, bootstrap: int) -> dict:
    eq = df[(df.split == "confirmatory") & (df.variant == "equalized_rank4")].copy()
    families = sorted(eq.family.unique())
    summary_rows = []
    size_rows = []
    adjacent_rows = []
    for fi, family in enumerate(families):
        sub = eq[eq.family == family]
        for pi, probe in enumerate(PROBES):
            col = response_col(probe)
            res = balanced_contrast(sub, col, 0.08, 0.24, bootstrap, 42000 + 100 * fi + pi)
            summary_rows.append({"family": family, "probe": probe, "p_low": 0.08, "p_high": 0.24, **res})
            for n in sorted(sub.n.unique()):
                r = balanced_contrast(
                    sub, col, 0.08, 0.24, bootstrap,
                    43000 + 1000 * fi + 10 * pi + int(n), size_filter=int(n)
                )
                size_rows.append({"family": family, "probe": probe, "n": int(n), **r})
            for ai, (plo, phi) in enumerate(((0.08, 0.16), (0.16, 0.24))):
                r = balanced_contrast(
                    sub, col, plo, phi, bootstrap,
                    44000 + 1000 * fi + 100 * pi + ai
                )
                adjacent_rows.append({"family": family, "probe": probe, "p_low": plo, "p_high": phi, **r})
    summary = pd.DataFrame(summary_rows)
    size = pd.DataFrame(size_rows)
    adjacent = pd.DataFrame(adjacent_rows)
    summary.to_csv(outdir / "intervention_primary_contrasts.csv", index=False)
    size.to_csv(outdir / "intervention_size_specific_contrasts.csv", index=False)
    adjacent.to_csv(outdir / "intervention_adjacent_rate_contrasts.csv", index=False)

    architecture_families = ["haar_z", "clifford_z", "floquet_cartan_z"]
    measurement_families = ["haar_z", "haar_random_pauli", "haar_weak_z_eta06"]
    primary = "haar_or_clifford_2design"
    arch_summary = summary[(summary.probe == primary) & summary.family.isin(architecture_families)]
    arch_size = size[(size.probe == primary) & size.family.isin(architecture_families)]
    meas_summary = summary[(summary.probe == primary) & summary.family.isin(measurement_families)]
    probe_robust = summary.groupby("family").apply(
        lambda g: bool((g.estimate < 0).all()), include_groups=False
    ).to_dict()
    audit = {
        "architecture_pooled_all_negative": bool((arch_summary.estimate < 0).all()),
        "architecture_all_size_points_negative": bool((arch_size.estimate < 0).all()),
        "architecture_all_pooled_ci_below_zero": bool((arch_summary.ci_high < 0).all()),
        "measurement_protocol_pooled_all_negative": bool((meas_summary.estimate < 0).all()),
        "measurement_protocol_all_pooled_ci_below_zero": bool((meas_summary.ci_high < 0).all()),
        "all_three_probes_negative_by_family": {str(k): bool(v) for k, v in probe_robust.items()},
    }
    (outdir / "intervention_success_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    return audit


def equalization_and_support(df: pd.DataFrame, outdir: Path) -> None:
    eq = df[df.variant == "equalized_rank4"].copy()
    rows = []
    for keys, g in eq.groupby(["family", "n", "tau", "split"]):
        rows.append({
            "family": keys[0], "n": keys[1], "tau": keys[2], "split": keys[3],
            "rows": len(g),
            "pre_purity_range": float(g.pre_purity.max() - g.pre_purity.min()),
            "pre_entropy_range": float(g.pre_entropy_bits.max() - g.pre_entropy_bits.min()),
            "pre_lambda1_range": float(g.pre_lambda1.max() - g.pre_lambda1.min()),
        })
    pd.DataFrame(rows).to_csv(outdir / "equalization_invariance.csv", index=False)
    support = (
        df[(df.variant == "equalized_rank4")]
        .groupby(["family", "split", "n", "p_measure", "tau"])
        .size().rename("supported_states").reset_index()
    )
    support.to_csv(outdir / "rank4_support_counts.csv", index=False)


def hellinger_cost(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    aa = np.sqrt(np.clip(a, 0.0, None))
    bb = np.sqrt(np.clip(b, 0.0, None))
    bc = np.clip(aa @ bb.T, 0.0, 1.0)
    return np.sqrt(np.maximum(0.0, 1.0 - bc))


def match_physical_states(
    state_df: pd.DataFrame,
    spectrum_meta: pd.DataFrame,
    spectra: np.ndarray,
    coeffs: pd.DataFrame,
    outdir: Path,
    bootstrap: int,
) -> dict:
    originals = state_df[(state_df.split == "confirmatory") & (state_df.variant == "original")].copy()
    spec_index = {sid: i for i, sid in enumerate(spectrum_meta.state_id.tolist())}
    coeff_map = {
        row.probe: np.asarray([row.c_I, row.c_Fa, row.c_Fb, row.c_Fab], float)
        for row in coeffs.itertuples(index=False)
    }
    pair_rows = []
    for family in sorted(originals.family.unique()):
        for n in sorted(originals.n.unique()):
            d = 1 << (int(n) // 2)
            factor = d / (d - 1.0)
            for tau in sorted(originals.tau.unique()):
                for p_low, p_high in PAIRINGS:
                    low = originals[
                        (originals.family == family) & (originals.n == n) & np.isclose(originals.tau, tau)
                        & np.isclose(originals.p_measure, p_low)
                    ].sort_values("state_id")
                    high = originals[
                        (originals.family == family) & (originals.n == n) & np.isclose(originals.tau, tau)
                        & np.isclose(originals.p_measure, p_high)
                    ].sort_values("state_id")
                    if len(low) == 0 or len(high) == 0:
                        continue
                    low_idx = [spec_index[s] for s in low.state_id]
                    high_idx = [spec_index[s] for s in high.state_id]
                    a = spectra[low_idx, :d]
                    b = spectra[high_idx, :d]
                    a = a / a.sum(axis=1, keepdims=True)
                    b = b / b.sum(axis=1, keepdims=True)
                    cost = hellinger_cost(a, b)
                    ilow, ihigh = linear_sum_assignment(cost)
                    for pair_number, (i, j) in enumerate(zip(ilow, ihigh)):
                        lo = low.iloc[int(i)]
                        hi = high.iloc[int(j)]
                        rec = {
                            "family": family, "n": int(n), "tau": float(tau),
                            "p_low": p_low, "p_high": p_high,
                            "cell_id": f"{family}|n{n}|tau{tau:g}|p{p_low:g}-{p_high:g}",
                            "pair_number": pair_number,
                            "state_id_low": lo.state_id, "state_id_high": hi.state_id,
                            "trajectory_low": int(lo.trajectory_index), "trajectory_high": int(hi.trajectory_index),
                            "hellinger_distance": float(cost[int(i), int(j)]),
                            "delta_central_purity": float(hi.P_A - lo.P_A),
                            "abs_delta_central_purity": abs(float(hi.P_A - lo.P_A)),
                            "delta_entropy_bits": float(hi.pre_entropy_bits - lo.pre_entropy_bits),
                        }
                        rec["strict_support"] = bool(
                            rec["hellinger_distance"] <= 0.12
                            and rec["abs_delta_central_purity"] <= 0.03
                        )
                        for probe in PROBES:
                            col = response_col(probe)
                            total = float(hi[col] - lo[col])
                            c = coeff_map[probe]
                            central = factor * (1.0 - c[1]) * float(hi.P_A - lo.P_A)
                            rec[f"{probe}_total_response_difference"] = total
                            rec[f"{probe}_central_spectrum_contribution"] = central
                            rec[f"{probe}_profile_contribution"] = total - central
                        pair_rows.append(rec)
    pairs = pd.DataFrame(pair_rows)
    pairs.to_csv(outdir / "physical_spectrum_matched_pairs.csv.gz", index=False, compression="gzip")

    def stratified_boot(g: pd.DataFrame, col: str, seed: int) -> tuple[float, float, float, int]:
        cells = [x for _, x in g.groupby("cell_id") if len(x)]
        if not cells:
            return math.nan, math.nan, math.nan, 0
        estimate = float(np.mean([c[col].mean() for c in cells]))
        rng = np.random.default_rng(seed)
        vals = np.empty(bootstrap, float)
        for b in range(bootstrap):
            vals[b] = np.mean([
                c.iloc[rng.integers(0, len(c), size=len(c))][col].mean() for c in cells
            ])
        lo, hi = percentile_interval(vals)
        return estimate, lo, hi, len(cells)

    summary_rows = []
    families = sorted(pairs.family.unique())
    for family in families:
        for p_low, p_high in PAIRINGS:
            base = pairs[(pairs.family == family) & np.isclose(pairs.p_low, p_low) & np.isclose(pairs.p_high, p_high)]
            for support_label, g0 in (("all_matches", base), ("strict_support", base[base.strict_support])):
                for pi, probe in enumerate(PROBES):
                    for component in ("total_response_difference", "central_spectrum_contribution", "profile_contribution"):
                        col = f"{probe}_{component}"
                        est, lo, hi, cells = stratified_boot(
                            g0, col,
                            51000 + 10000 * families.index(family)
                            + 1000 * list(PAIRINGS).index((p_low, p_high)) + 100 * pi
                            + (0 if component.startswith("total") else 1 if component.startswith("central") else 2)
                        )
                        summary_rows.append({
                            "family": family, "p_low": p_low, "p_high": p_high,
                            "support": support_label, "probe": probe, "component": component,
                            "estimate": est, "ci_low": lo, "ci_high": hi,
                            "cells": cells, "pairs": len(g0),
                            "mean_hellinger": float(g0.hellinger_distance.mean()) if len(g0) else math.nan,
                            "mean_abs_delta_purity": float(g0.abs_delta_central_purity.mean()) if len(g0) else math.nan,
                        })
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(outdir / "physical_matching_contrasts.csv", index=False)

    balance = (
        pairs.groupby(["family", "p_low", "p_high"])
        .agg(
            pairs=("pair_number", "size"),
            mean_hellinger=("hellinger_distance", "mean"),
            median_hellinger=("hellinger_distance", "median"),
            max_hellinger=("hellinger_distance", "max"),
            mean_abs_delta_purity=("abs_delta_central_purity", "mean"),
            strict_support_fraction=("strict_support", "mean"),
        ).reset_index()
    )
    balance.to_csv(outdir / "physical_matching_balance.csv", index=False)

    primary = summary[
        (summary.support == "strict_support")
        & (summary.probe == "haar_or_clifford_2design")
        & (summary.component == "total_response_difference")
    ]
    adjacent = primary[((np.isclose(primary.p_low, 0.08)) & (np.isclose(primary.p_high, 0.16)))
                       | ((np.isclose(primary.p_low, 0.16)) & (np.isclose(primary.p_high, 0.24)))]
    audit = {
        "strict_support_rows": int(pairs.strict_support.sum()),
        "total_matched_rows": int(len(pairs)),
        "strict_support_fraction": float(pairs.strict_support.mean()),
        "all_adjacent_family_total_contrasts_negative": bool((adjacent.estimate < 0).all()) if len(adjacent) else False,
        "all_adjacent_family_total_ci_below_zero": bool((adjacent.ci_high < 0).all()) if len(adjacent) else False,
        "family_level_rows": int(len(adjacent)),
    }
    (outdir / "physical_matching_success_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    return audit


def profile_means(df: pd.DataFrame, outdir: Path) -> None:
    eq = df[(df.split == "confirmatory") & (df.variant == "equalized_rank4")].copy()
    cols = [
        "P_L", "P_A", "P_Lb", "P_R", "neighboring_cut_purity_sum",
        *[response_col(p) for p in PROBES],
    ]
    means = eq.groupby(["family", "n", "p_measure", "tau"])[cols].mean().reset_index()
    means.to_csv(outdir / "equalized_profile_means.csv", index=False)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--datadir", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--bootstrap", type=int, default=4000)
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.datadir / "state_response_rows.csv.gz")
    meta = pd.read_csv(args.datadir / "physical_spectrum_metadata.csv.gz")
    spectra = np.load(args.datadir / "physical_spectra.npz")["spectra"]
    coeffs = pd.read_csv(args.datadir / "probe_response_coefficients.csv")

    equalization_and_support(df, args.outdir)
    intervention_audit = make_intervention_tables(df, args.outdir, args.bootstrap)
    matching_audit = match_physical_states(df, meta, spectra, coeffs, args.outdir, args.bootstrap)
    profile_means(df, args.outdir)

    formula_errors = []
    for probe in PROBES:
        coeff = coeffs[coeffs.probe == probe].iloc[0]
        post_formula = (
            coeff.c_I * df.P_L + coeff.c_Fa * df.P_A
            + coeff.c_Fb * df.P_Lb + coeff.c_Fab * df.P_R
        )
        formula_errors.append(float(np.max(np.abs(post_formula - df[f"probe_{probe}_post_purity"]))))
    summary = {
        "state_rows": len(df),
        "physical_spectrum_rows": len(meta),
        "maximum_stored_formula_error": max(formula_errors),
        "intervention_audit": intervention_audit,
        "physical_matching_audit": matching_audit,
        "bootstrap_replicates": args.bootstrap,
    }
    (args.outdir / "analysis_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
