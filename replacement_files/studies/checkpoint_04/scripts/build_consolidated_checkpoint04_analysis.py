#!/usr/bin/env python3
"""Build compact, deterministic Checkpoint 04 analysis tables.

This script intentionally omits the superseded nearest-neighbour physical-state
matching arm from the core tables.  Physically reachable exact-spectrum evidence
is supplied instead by the stabilizer-state arm.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

PROBES = (
    "haar_or_clifford_2design",
    "cartan_xy_pi8",
    "cartan_xx_pi4",
)
P_VALUES = (0.08, 0.16, 0.24)
PAIRS = ((0.08, 0.16), (0.16, 0.24), (0.08, 0.24))
FAMILIES = (
    "haar_z",
    "clifford_z",
    "floquet_cartan_z",
    "haar_random_pauli",
    "haar_weak_z_eta06",
)


def stable_seed(*items: object) -> int:
    return int.from_bytes(hashlib.blake2b(repr(items).encode(), digest_size=8).digest(), "little") & 0xFFFFFFFF


def response_col(probe: str) -> str:
    return f"probe_{probe}_delta_linear_norm"


def trajectory_matrices(sub: pd.DataFrame, col: str, p_values: tuple[float, ...]):
    taus = sorted(sub.tau.unique())
    mats = {}
    for n in sorted(sub.n.unique()):
        for p in p_values:
            g = sub[(sub.n == n) & np.isclose(sub.p_measure, p)]
            if len(g) == 0:
                continue
            pivot = g.pivot_table(index="trajectory_index", columns="tau", values=col, aggfunc="first")
            mats[(int(n), float(p))] = pivot.reindex(columns=taus).to_numpy(float)
    return taus, mats


def balanced_bootstrap(
    sub: pd.DataFrame,
    col: str,
    low: float,
    high: float,
    reps: int,
    seed: int,
    n_filter: int | None = None,
):
    x = sub.copy()
    if n_filter is not None:
        x = x[x.n == n_filter]
    taus, mats = trajectory_matrices(x, col, (low, high))
    sizes = sorted({n for n, _ in mats})

    observed_cells = []
    for n in sizes:
        if (n, low) not in mats or (n, high) not in mats:
            continue
        lo = np.nanmean(mats[(n, low)], axis=0)
        hi = np.nanmean(mats[(n, high)], axis=0)
        d = hi - lo
        observed_cells.extend(d[np.isfinite(d)].tolist())
    obs = float(np.mean(observed_cells)) if observed_cells else math.nan

    rng = np.random.default_rng(seed)
    cell_boot = []
    for n in sizes:
        if (n, low) not in mats or (n, high) not in mats:
            continue
        means = {}
        for p in (low, high):
            arr = mats[(n, p)]
            ntraj = len(arr)
            weights = rng.multinomial(ntraj, np.full(ntraj, 1.0 / ntraj), size=reps).astype(float)
            finite = np.isfinite(arr).astype(float)
            values = np.nan_to_num(arr, nan=0.0)
            denom = weights @ finite
            numer = weights @ values
            means[p] = np.divide(numer, denom, out=np.full_like(numer, np.nan), where=denom > 0)
        diff = means[high] - means[low]
        for j in range(diff.shape[1]):
            if np.isfinite(np.nanmean(diff[:, j])):
                cell_boot.append(diff[:, j])
    if cell_boot:
        stack = np.vstack(cell_boot)
        valid = np.sum(np.isfinite(stack), axis=0)
        boot = np.divide(np.nansum(stack, axis=0), valid,
                         out=np.full(reps, np.nan), where=valid > 0)
        boot = boot[np.isfinite(boot)]
        lo_ci, hi_ci = np.quantile(boot, [0.025, 0.975])
    else:
        boot = np.empty(0)
        lo_ci = hi_ci = math.nan
    return {
        "estimate": obs,
        "ci_low": float(lo_ci),
        "ci_high": float(hi_ci),
        "bootstrap_reps": int(len(boot)),
        "rows": int(len(x)),
        "size_cells": int(len(sizes)),
        "time_cells": int(len(taus)),
    }


def intervention_tables(path: Path, variant: str, run: str, reps: int):
    df = pd.read_csv(path)
    sub = df[(df.split == "confirmatory") & (df.variant == variant)].copy()
    summary = []
    sizes = []
    adjacent = []
    for family in FAMILIES:
        g = sub[sub.family == family]
        for probe in PROBES:
            col = response_col(probe)
            summary.append({
                "run": run, "family": family, "probe": probe, "p_low": 0.08, "p_high": 0.24,
                **balanced_bootstrap(g, col, 0.08, 0.24, reps, stable_seed(run, family, probe, "primary")),
            })
            for n in sorted(g.n.unique()):
                sizes.append({
                    "run": run, "family": family, "probe": probe, "n": int(n),
                    **balanced_bootstrap(g, col, 0.08, 0.24, reps, stable_seed(run, family, probe, n), int(n)),
                })
            for low, high in PAIRS[:2]:
                adjacent.append({
                    "run": run, "family": family, "probe": probe, "p_low": low, "p_high": high,
                    **balanced_bootstrap(g, col, low, high, reps, stable_seed(run, family, probe, low, high)),
                })
    return pd.DataFrame(summary), pd.DataFrame(sizes), pd.DataFrame(adjacent), df


def physical_original_table(df: pd.DataFrame, run: str, reps: int):
    sub = df[(df.split == "confirmatory") & (df.variant == "original")]
    rows = []
    for family in FAMILIES:
        g = sub[sub.family == family]
        for probe in PROBES:
            rows.append({
                "run": run, "family": family, "probe": probe, "p_low": 0.08, "p_high": 0.24,
                **balanced_bootstrap(g, response_col(probe), 0.08, 0.24, reps,
                                     stable_seed(run, "physical", family, probe)),
            })
    return pd.DataFrame(rows)


def equal_cell_mean_contrast(sub: pd.DataFrame, col: str, low: float, high: float):
    means = sub.groupby(["n", "tau", "p_measure"])[col].mean()
    vals = []
    for n in sorted(sub.n.unique()):
        for tau in sorted(sub.tau.unique()):
            try:
                vals.append(float(means.loc[(n, tau, high)] - means.loc[(n, tau, low)]))
            except KeyError:
                continue
    return float(np.mean(vals))


def response_decomposition(df: pd.DataFrame, variant: str, run: str):
    sub = df[(df.split == "confirmatory") & (df.variant == variant)]
    rows = []
    for family in FAMILIES:
        g = sub[sub.family == family].copy()
        # Each contribution is evaluated rowwise because d depends on n.
        factor = np.power(2.0, g.n.to_numpy(float) / 2.0)
        factor = factor / (factor - 1.0)
        g["central_headroom"] = factor * g.P_A
        g["left_neighbor"] = -0.4 * factor * g.P_L
        g["right_neighbor"] = -0.4 * factor * g.P_R
        g["reconstructed"] = g.central_headroom + g.left_neighbor + g.right_neighbor
        direct = response_col("haar_or_clifford_2design")
        rows.append({
            "run": run,
            "variant": variant,
            "family": family,
            "central_spectrum_headroom": equal_cell_mean_contrast(g, "central_headroom", 0.08, 0.24),
            "left_neighboring_cut": equal_cell_mean_contrast(g, "left_neighbor", 0.08, 0.24),
            "right_neighboring_cut": equal_cell_mean_contrast(g, "right_neighbor", 0.08, 0.24),
            "reconstructed_total": equal_cell_mean_contrast(g, "reconstructed", 0.08, 0.24),
            "direct_total": equal_cell_mean_contrast(g, direct, 0.08, 0.24),
            "maximum_rowwise_reconstruction_error": float(np.max(np.abs(g.reconstructed - g[direct]))),
        })
    return pd.DataFrame(rows)


def equalization_audit(df: pd.DataFrame, variant: str, run: str):
    sub = df[df.variant == variant]
    rows = []
    for keys, g in sub.groupby(["family", "n", "tau", "split"]):
        rows.append({
            "run": run, "family": keys[0], "n": keys[1], "tau": keys[2], "split": keys[3],
            "rows": len(g),
            "purity_range": float(g.pre_purity.max() - g.pre_purity.min()),
            "entropy_range": float(g.pre_entropy_bits.max() - g.pre_entropy_bits.min()),
            "lambda1_range": float(g.pre_lambda1.max() - g.pre_lambda1.min()),
        })
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--primary", type=Path, required=True)
    ap.add_argument("--independent", type=Path, required=True)
    ap.add_argument("--rank2", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--bootstrap-reps", type=int, default=4000)
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    configs = [
        (args.primary / "state_response_rows.csv.gz", "equalized_rank4", "primary_rank4"),
        (args.independent / "state_response_rows.csv.gz", "equalized_rank4", "independent_rank4"),
        (args.rank2 / "state_response_rows.csv.gz", "equalized_rank2", "posthoc_rank2"),
    ]
    summaries=[]; size_tables=[]; adjacent_tables=[]; physical_tables=[]; decomps=[]; invariances=[]
    raw_dfs={}
    for path, variant, run in configs:
        s,z,a,df = intervention_tables(path, variant, run, args.bootstrap_reps)
        summaries.append(s); size_tables.append(z); adjacent_tables.append(a)
        raw_dfs[run] = df
        physical_tables.append(physical_original_table(df, run, args.bootstrap_reps))
        decomps.append(response_decomposition(df, variant, run))
        invariances.append(equalization_audit(df, variant, run))

    summary = pd.concat(summaries, ignore_index=True)
    sizes = pd.concat(size_tables, ignore_index=True)
    adjacent = pd.concat(adjacent_tables, ignore_index=True)
    physical = pd.concat(physical_tables, ignore_index=True)
    decomp = pd.concat(decomps, ignore_index=True)
    invariance = pd.concat(invariances, ignore_index=True)

    summary.to_csv(args.outdir / "intervention_cross_architecture.csv", index=False)
    sizes.to_csv(args.outdir / "intervention_size_consistency.csv", index=False)
    adjacent.to_csv(args.outdir / "intervention_adjacent_contrasts.csv", index=False)
    physical.to_csv(args.outdir / "physical_original_contrasts.csv", index=False)
    decomp.to_csv(args.outdir / "response_stencil_decomposition.csv", index=False)
    invariance.to_csv(args.outdir / "equalization_invariance.csv", index=False)

    primary = summary[summary.run == "primary_rank4"]
    independent = summary[summary.run == "independent_rank4"]
    rank2 = summary[summary.run == "posthoc_rank2"]
    primary_sizes = sizes[sizes.run == "primary_rank4"]
    independent_sizes = sizes[sizes.run == "independent_rank4"]
    primary_adj = adjacent[adjacent.run == "primary_rank4"]
    independent_adj = adjacent[adjacent.run == "independent_rank4"]
    audit = {
        "primary_rank4": {
            "all_15_primary_ci_below_zero": bool((primary.ci_high < 0).all()),
            "all_45_size_ci_below_zero": bool((primary_sizes.ci_high < 0).all()),
            "all_30_adjacent_ci_below_zero": bool((primary_adj.ci_high < 0).all()),
        },
        "independent_rank4": {
            "all_15_primary_ci_below_zero": bool((independent.ci_high < 0).all()),
            "all_45_size_points_negative": bool((independent_sizes.estimate < 0).all()),
            "all_30_adjacent_points_negative": bool((independent_adj.estimate < 0).all()),
        },
        "posthoc_rank2": {
            "all_15_primary_ci_below_zero": bool((rank2.ci_high < 0).all()),
        },
        "maximum_equalization_purity_range": float(invariance.purity_range.max()),
        "maximum_equalization_entropy_range": float(invariance.entropy_range.max()),
        "maximum_response_decomposition_error": float(decomp.maximum_rowwise_reconstruction_error.max()),
        "bootstrap_reps": args.bootstrap_reps,
    }
    (args.outdir / "intervention_analysis_summary.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))

if __name__ == "__main__":
    main()
