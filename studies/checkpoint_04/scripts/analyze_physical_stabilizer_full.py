#!/usr/bin/env python3
"""Analyze the predeclared Checkpoint 04 physical-stabilizer arm."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

OUTCOMES = {
    "haar_or_clifford_2design": "exact_delta_linear_haar_clifford",
    "xx_pi8": "exact_delta_linear_xx_pi8",
    "xx_pi4": "exact_delta_linear_xx_pi4",
    "finite_clifford_12": "finite_clifford_mean_delta_linear",
    "neighboring_cut_purity_sum": "Q_neighbor",
}
P_VALUES = (0.08, 0.12, 0.16, 0.20, 0.24)
P_STEP = 0.04


def stable_seed(*items: object) -> int:
    import hashlib
    raw = repr(items).encode("utf-8")
    return int.from_bytes(hashlib.blake2b(raw, digest_size=8).digest(), "little") & 0xFFFFFFFF


def prepare_eligible(df: pd.DataFrame, min_total: int = 8) -> pd.DataFrame:
    work = df.copy()
    work["stratum"] = (
        "n" + work["n"].astype(str)
        + "|tau" + work["tau"].map(lambda x: f"{x:g}")
        + "|r" + work["log2_schmidt_rank"].astype(int).astype(str)
    )
    support = work.groupby("stratum").agg(rows=("state_id", "size"), p_levels=("p_measure", "nunique"))
    eligible = support[(support.rows >= min_total) & (support.p_levels >= 2)].index
    return work[work.stratum.isin(eligible)].copy()


def fixed_effect_result(df: pd.DataFrame, outcome: str, protocol: str, split: str, min_total: int = 8) -> dict[str, Any]:
    sub = df[(df.measurement_protocol == protocol) & (df.split == split)].copy()
    sub = prepare_eligible(sub, min_total=min_total)
    sub["p_step"] = (sub.p_measure - 0.16) / P_STEP
    if len(sub) < 20 or sub.p_step.nunique() < 2:
        return {
            "measurement_protocol": protocol, "split": split, "outcome": outcome,
            "estimate_per_0p04": np.nan, "se_cluster": np.nan, "ci_low": np.nan,
            "ci_high": np.nan, "p_value": np.nan, "rows": len(sub),
            "trajectory_clusters": sub.trajectory_id.nunique(), "strata": sub.stratum.nunique(),
        }
    fit = smf.ols(f"{outcome} ~ p_step + C(stratum)", data=sub).fit(
        cov_type="cluster", cov_kwds={"groups": sub["trajectory_id"], "use_correction": True}
    )
    beta = float(fit.params["p_step"])
    se = float(fit.bse["p_step"])
    ci = fit.conf_int().loc["p_step"].to_numpy(float)
    return {
        "measurement_protocol": protocol,
        "split": split,
        "outcome": outcome,
        "estimate_per_0p04": beta,
        "se_cluster": se,
        "ci_low": float(ci[0]),
        "ci_high": float(ci[1]),
        "p_value": float(fit.pvalues["p_step"]),
        "rows": len(sub),
        "trajectory_clusters": int(sub.trajectory_id.nunique()),
        "strata": int(sub.stratum.nunique()),
        "rank_min": int(sub.log2_schmidt_rank.min()),
        "rank_max": int(sub.log2_schmidt_rank.max()),
        "p_levels": int(sub.p_measure.nunique()),
        "r_squared": float(fit.rsquared),
    }


def size_fixed_effect_result(df: pd.DataFrame, outcome: str, protocol: str, split: str, n: int) -> dict[str, Any]:
    sub = df[(df.measurement_protocol == protocol) & (df.split == split) & (df.n == n)].copy()
    sub = prepare_eligible(sub, min_total=6)
    sub["p_step"] = (sub.p_measure - 0.16) / P_STEP
    if len(sub) < 15 or sub.p_step.nunique() < 2:
        return {"measurement_protocol": protocol, "split": split, "n": n, "outcome": outcome,
                "estimate_per_0p04": np.nan, "se_cluster": np.nan, "ci_low": np.nan, "ci_high": np.nan,
                "p_value": np.nan, "rows": len(sub), "strata": sub.stratum.nunique()}
    fit = smf.ols(f"{outcome} ~ p_step + C(stratum)", data=sub).fit(
        cov_type="cluster", cov_kwds={"groups": sub["trajectory_id"], "use_correction": True}
    )
    ci = fit.conf_int().loc["p_step"].to_numpy(float)
    return {
        "measurement_protocol": protocol, "split": split, "n": n, "outcome": outcome,
        "estimate_per_0p04": float(fit.params["p_step"]), "se_cluster": float(fit.bse["p_step"]),
        "ci_low": float(ci[0]), "ci_high": float(ci[1]), "p_value": float(fit.pvalues["p_step"]),
        "rows": len(sub), "trajectory_clusters": int(sub.trajectory_id.nunique()),
        "strata": int(sub.stratum.nunique()),
    }


def supported_strata(df: pd.DataFrame, low: float, high: float, strict_min_each: int = 1) -> list[str]:
    tab = df[df.p_measure.isin([low, high])].groupby(["stratum", "p_measure"]).size().unstack(fill_value=0)
    if low not in tab.columns or high not in tab.columns:
        return []
    return tab[(tab[low] >= strict_min_each) & (tab[high] >= strict_min_each)].index.tolist()


def contrast_from_sample(df: pd.DataFrame, outcome: str, low: float, high: float, strata: list[str]) -> float:
    if not strata:
        return np.nan
    g = df[df.stratum.isin(strata) & df.p_measure.isin([low, high])]
    means = g.groupby(["stratum", "p_measure"])[outcome].mean().unstack()
    if low not in means.columns or high not in means.columns:
        return np.nan
    means = means.dropna(subset=[low, high])
    if len(means) == 0:
        return np.nan
    return float((means[high] - means[low]).mean())


def make_cluster_bootstrap_context(sub: pd.DataFrame, reps: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Return trajectory multiplicities and each row's cluster column.

    Trajectories are resampled independently within each `(n,p)` cell.  Both
    probe-time rows of a trajectory receive the same bootstrap multiplicity.
    """
    clusters = sub[["trajectory_id", "n", "p_measure"]].drop_duplicates().reset_index(drop=True)
    cluster_col = {tid: i for i, tid in enumerate(clusters.trajectory_id)}
    row_cluster = sub.trajectory_id.map(cluster_col).to_numpy(int)
    weights = np.zeros((reps, len(clusters)), dtype=np.int16)
    rng = np.random.default_rng(seed)
    for _, idx_series in clusters.groupby(["n", "p_measure"]).groups.items():
        idx = np.asarray(list(idx_series), dtype=int)
        ncl = len(idx)
        draw = rng.multinomial(ncl, np.full(ncl, 1.0 / ncl), size=reps)
        weights[:, idx] = draw.astype(np.int16, copy=False)
    return weights, row_cluster


def fast_bootstrap_contrast(
    sub: pd.DataFrame, outcome: str, low: float, high: float, strata: list[str],
    weights: np.ndarray, row_cluster: np.ndarray,
) -> np.ndarray:
    if not strata:
        return np.empty(0, float)
    y = sub[outcome].to_numpy(float)
    p = sub.p_measure.to_numpy(float)
    st = sub.stratum.to_numpy(str)
    diffs = []
    for name in strata:
        il = np.flatnonzero((st == name) & np.isclose(p, low))
        ih = np.flatnonzero((st == name) & np.isclose(p, high))
        if len(il) == 0 or len(ih) == 0:
            continue
        wl = weights[:, row_cluster[il]].astype(float, copy=False)
        wh = weights[:, row_cluster[ih]].astype(float, copy=False)
        dl = wl.sum(axis=1)
        dh = wh.sum(axis=1)
        ml = np.divide(wl @ y[il], dl, out=np.full(len(weights), np.nan), where=dl > 0)
        mh = np.divide(wh @ y[ih], dh, out=np.full(len(weights), np.nan), where=dh > 0)
        diffs.append(mh - ml)
    if not diffs:
        return np.empty(0, float)
    arr = np.vstack(diffs)
    valid = np.sum(np.isfinite(arr), axis=0)
    sums = np.nansum(arr, axis=0)
    return np.divide(sums, valid, out=np.full(arr.shape[1], np.nan), where=valid > 0)


def cluster_bootstrap_adjacent(
    sub: pd.DataFrame, outcome: str, protocol: str, split: str, low: float, high: float,
    strict_min_each: int, weights: np.ndarray, row_cluster: np.ndarray,
) -> dict[str, Any]:
    strata = supported_strata(sub, low, high, strict_min_each=strict_min_each)
    point = contrast_from_sample(sub, outcome, low, high, strata)
    arr = fast_bootstrap_contrast(sub, outcome, low, high, strata, weights, row_cluster)
    arr = arr[np.isfinite(arr)]
    ci = np.quantile(arr, [0.025, 0.975]) if len(arr) else [np.nan, np.nan]
    support_table = (
        sub[sub.stratum.isin(strata) & sub.p_measure.isin([low, high])]
        .groupby(["stratum", "p_measure"]).size().unstack(fill_value=0)
    )
    return {
        "measurement_protocol": protocol, "split": split, "outcome": outcome,
        "p_low": low, "p_high": high, "strict_min_each": strict_min_each,
        "estimate": point, "ci_low": float(ci[0]), "ci_high": float(ci[1]),
        "bootstrap_reps_valid": int(len(arr)), "strata": int(len(strata)),
        "rows": int(support_table.to_numpy().sum()) if len(support_table) else 0,
        "minimum_count_per_rate_included": int(support_table.min(axis=1).min()) if len(support_table) else 0,
    }

def exact_stratum_invariance(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["measurement_protocol", "split", "n", "tau", "log2_schmidt_rank"], as_index=False)
        .agg(
            states=("state_id", "size"),
            p_levels=("p_measure", "nunique"),
            purity_range=("pre_purity", lambda x: float(x.max() - x.min())),
            entropy_range=("pre_entropy_bits", lambda x: float(x.max() - x.min())),
            lambda1_range=("pre_lambda1", lambda x: float(x.max() - x.min())),
            flatness_max=("spectrum_flatness_max_abs", "max"),
        )
    )


def reliability_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for protocol, g in df[(df.split == "confirmatory")].groupby("measurement_protocol"):
        for tau, h in g.groupby("tau"):
            rows.append({
                "measurement_protocol": protocol, "tau": tau, "rows": len(h),
                "half_bank_correlation": float(np.corrcoef(h.finite_clifford_half1_delta_linear, h.finite_clifford_half2_delta_linear)[0, 1]),
                "exact_vs_finite_correlation": float(np.corrcoef(h.exact_delta_linear_haar_clifford, h.finite_clifford_mean_delta_linear)[0, 1]),
                "finite_minus_exact_mean": float(np.mean(h.finite_clifford_mean_delta_linear - h.exact_delta_linear_haar_clifford)),
                "finite_minus_exact_rmse": float(np.sqrt(np.mean(np.square(h.finite_clifford_mean_delta_linear - h.exact_delta_linear_haar_clifford)))),
            })
    return pd.DataFrame(rows)


def plot_slope_forest(results: pd.DataFrame, outpath: Path) -> None:
    probes = ["haar_or_clifford_2design", "xx_pi8", "xx_pi4"]
    protocols = ["z_projective", "random_pauli"]
    g = results[(results.split == "confirmatory") & results.outcome.isin([OUTCOMES[p] for p in probes])].copy()
    label_map = {OUTCOMES[p]: p.replace("_", " ") for p in probes}
    ylabels = []
    ys = []
    fig, ax = plt.subplots(figsize=(9.4, 5.4))
    y = 0
    protocol_names = {"z_projective": "Z projective", "random_pauli": "Random Pauli"}
    probe_names = {
        "haar_or_clifford_2design": "Haar / Clifford 2-design",
        "xx_pi8": r"locally dressed $XX(\pi/8)$",
        "xx_pi4": r"locally dressed $XX(\pi/4)$",
    }
    marker_colors = ["#1f4e79", "#4f81bd", "#8fb9d9", "#1f4e79", "#4f81bd", "#8fb9d9"]
    color_index = 0
    for protocol in protocols:
        for probe in probes:
            row = g[(g.measurement_protocol == protocol) & (g.outcome == OUTCOMES[probe])].iloc[0]
            ax.errorbar(row.estimate_per_0p04, y,
                        xerr=[[row.estimate_per_0p04-row.ci_low], [row.ci_high-row.estimate_per_0p04]],
                        fmt="o", capsize=3, color=marker_colors[color_index])
            ylabels.append(f"{protocol_names[protocol]} — {probe_names[probe]}")
            ys.append(y)
            y += 1
            color_index += 1
        y += 0.5
    ax.axvline(0, linewidth=0.9, color="#4a4a4a")
    ax.set_yticks(ys, ylabels)
    ax.set_xlabel(r"Fixed-spectrum response change per $\Delta p=0.04$")
    ax.set_title("Exact-spectrum response in physical stabilizer states", pad=10)
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.18)
    fig.subplots_adjust(left=0.43, right=0.98, top=0.90, bottom=0.17)
    fig.savefig(outpath, dpi=220)
    plt.close(fig)


def plot_adjacent(adj: pd.DataFrame, outpath: Path) -> None:
    g = adj[(adj.split == "confirmatory") & (adj.outcome == OUTCOMES["haar_or_clifford_2design"]) & (adj.strict_min_each == 1)].copy()
    g["pair"] = g.apply(lambda r: f"{r.p_low:.2f}→{r.p_high:.2f}", axis=1)
    pairs = [f"{P_VALUES[i]:.2f}→{P_VALUES[i+1]:.2f}" for i in range(len(P_VALUES)-1)]
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    x = np.arange(len(pairs))
    offsets = {"z_projective": -0.12, "random_pauli": 0.12}
    for protocol in ["z_projective", "random_pauli"]:
        h = g[g.measurement_protocol == protocol].set_index("pair").loc[pairs]
        ax.errorbar(x + offsets[protocol], h.estimate,
                    yerr=[h.estimate-h.ci_low, h.ci_high-h.estimate],
                    fmt="o", capsize=3, label=protocol.replace("_", " "))
    ax.axhline(0, linewidth=0.8)
    ax.set_xticks(x, pairs)
    ax.set_xlabel("Adjacent monitoring-rate pair")
    ax.set_ylabel("High-p minus low-p exact response")
    ax.set_title("Exact full-spectrum matched adjacent contrasts")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(outpath, dpi=220)
    plt.close(fig)


def plot_rank_support(df: pd.DataFrame, outpath: Path) -> None:
    g = df[df.split == "confirmatory"].groupby(["measurement_protocol", "p_measure", "log2_schmidt_rank"]).size().reset_index(name="states")
    protocols = ["z_projective", "random_pauli"]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3), sharey=True)
    for ax, protocol in zip(axes, protocols):
        h = g[g.measurement_protocol == protocol]
        piv = h.pivot(index="log2_schmidt_rank", columns="p_measure", values="states").fillna(0)
        bottom = np.zeros(len(piv.columns))
        for rank, row in piv.iterrows():
            vals = row.to_numpy(float)
            ax.bar(np.arange(len(piv.columns)), vals, bottom=bottom, label=f"log2 rank={int(rank)}")
            bottom += vals
        ax.set_xticks(np.arange(len(piv.columns)), [f"{x:.2f}" for x in piv.columns])
        ax.set_title(protocol.replace("_", " "))
        ax.set_xlabel("Monitoring rate p")
    axes[0].set_ylabel("Confirmatory state count")
    axes[1].legend(frameon=False, fontsize=8, ncol=2)
    fig.suptitle("Exact-spectrum common support in the stabilizer arm")
    fig.tight_layout()
    fig.savefig(outpath, dpi=220)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--bootstrap-reps", type=int, default=3000)
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    figdir = args.outdir / "figures"
    figdir.mkdir(exist_ok=True)

    df = pd.read_csv(args.run_dir / "physical_stabilizer_states.csv.gz")
    protocols = sorted(df.measurement_protocol.unique())

    result_rows = []
    size_rows = []
    for split in ["discovery", "confirmatory"]:
        for protocol in protocols:
            for _, outcome in OUTCOMES.items():
                result_rows.append(fixed_effect_result(df, outcome, protocol, split))
                for n in sorted(df.n.unique()):
                    size_rows.append(size_fixed_effect_result(df, outcome, protocol, split, int(n)))
    results = pd.DataFrame(result_rows)
    sizes = pd.DataFrame(size_rows)
    results.to_csv(args.outdir / "physical_stabilizer_fixed_effect_tests.csv", index=False)
    sizes.to_csv(args.outdir / "physical_stabilizer_size_specific_tests.csv", index=False)

    adjacent_rows = []
    pairs = list(zip(P_VALUES[:-1], P_VALUES[1:])) + [(0.08, 0.24)]
    for split in ["discovery", "confirmatory"]:
        for protocol in protocols:
            boot_sub = df[(df.measurement_protocol == protocol) & (df.split == split)].copy()
            boot_sub = prepare_eligible(boot_sub, min_total=2).reset_index(drop=True)
            weights, row_cluster = make_cluster_bootstrap_context(
                boot_sub, args.bootstrap_reps,
                stable_seed("physical_stabilizer_boot_context", protocol, split, args.bootstrap_reps),
            )
            for key in ["haar_or_clifford_2design", "xx_pi8", "xx_pi4", "neighboring_cut_purity_sum"]:
                outcome = OUTCOMES[key]
                for low, high in pairs:
                    for strict in [1, 5]:
                        adjacent_rows.append(cluster_bootstrap_adjacent(
                            boot_sub, outcome, protocol, split, low, high, strict, weights, row_cluster
                        ))
    adjacent = pd.DataFrame(adjacent_rows)
    adjacent.to_csv(args.outdir / "physical_stabilizer_exact_stratum_contrasts.csv", index=False)

    invariance = exact_stratum_invariance(df)
    invariance.to_csv(args.outdir / "physical_stabilizer_spectrum_invariance.csv", index=False)
    reliability = reliability_table(df)
    reliability.to_csv(args.outdir / "physical_stabilizer_gate_bank_reliability.csv", index=False)

    # Exact algebraic audits.
    d = np.power(2.0, df.n.to_numpy(float) / 2.0)
    reconstructed = d / (d - 1.0) * (df.P_center.to_numpy(float) - 0.4 * df.Q_neighbor.to_numpy(float))
    formula_err = df.exact_delta_linear_haar_clifford.to_numpy(float) - reconstructed
    flatness_pass = bool(df.spectrum_flatness_max_abs.max() < 1e-10 and df.rank_power_of_two_error.max() < 1e-10)

    confirm = results[results.split == "confirmatory"].copy()
    primary = confirm[confirm.outcome == OUTCOMES["haar_or_clifford_2design"]]
    mechanism = confirm[confirm.outcome == OUTCOMES["neighboring_cut_purity_sum"]]
    probe = confirm[confirm.outcome.isin([OUTCOMES["haar_or_clifford_2design"], OUTCOMES["xx_pi8"], OUTCOMES["xx_pi4"]])]
    discovery_primary = results[(results.split == "discovery") & (results.outcome == OUTCOMES["haar_or_clifford_2design"])]

    primary_pass = bool((primary.ci_high < 0).all())
    mechanism_pass = bool((mechanism.ci_low > 0).all())
    all_probe_pass = bool((probe.ci_high < 0).all())
    discovery_pass = bool((discovery_primary.ci_high < 0).all())
    size_primary = sizes[(sizes.split == "confirmatory") & (sizes.outcome == OUTCOMES["haar_or_clifford_2design"])]

    summary = {
        "purpose": "physically reachable exact-central-spectrum matching in monitored stabilizer circuits",
        "primary_confirmatory": {
            "both_protocols_ci_below_zero": primary_pass,
            "tests": primary.to_dict("records"),
            "all_size_estimates_negative": bool((size_primary.estimate_per_0p04 < 0).all()),
        },
        "mechanism": {
            "Q_neighbor_ci_above_zero_both_protocols": mechanism_pass,
            "tests": mechanism.to_dict("records"),
            "max_haar_formula_error": float(np.max(np.abs(formula_err))),
        },
        "probe_robustness": {
            "all_three_probe_ci_below_zero_both_protocols": all_probe_pass,
        },
        "discovery_replication": {
            "both_protocols_ci_below_zero": discovery_pass,
        },
        "exact_spectrum_checks": {
            "passes": flatness_pass,
            "max_flatness_error": float(df.spectrum_flatness_max_abs.max()),
            "max_rank_power_of_two_error": float(df.rank_power_of_two_error.max()),
            "max_within_stratum_purity_range": float(invariance.purity_range.max()),
            "max_within_stratum_entropy_range": float(invariance.entropy_range.max()),
        },
        "support": {
            "rows": int(len(df)),
            "confirmatory_rows": int((df.split == "confirmatory").sum()),
            "trajectory_clusters": int(df.trajectory_id.nunique()),
            "confirmatory_clusters": int(df[df.split == "confirmatory"].trajectory_id.nunique()),
        },
        "bootstrap_reps": args.bootstrap_reps,
        "interpretation_guardrail": "Matched physical-state comparison at exactly equal stabilizer Schmidt spectra; not a randomized causal effect of monitoring rate conditional on a post-dynamics rank.",
    }
    (args.outdir / "physical_stabilizer_analysis_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    plot_slope_forest(results, figdir / "figure_physical_stabilizer_slope_forest.png")
    plot_adjacent(adjacent, figdir / "figure_physical_stabilizer_adjacent_contrasts.png")
    plot_rank_support(df, figdir / "figure_physical_stabilizer_rank_support.png")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
