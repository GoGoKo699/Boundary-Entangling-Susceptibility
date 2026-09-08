"""Earlier figure-design trajectory-bootstrap routines, separated from old artwork code.

Numerical functions are preserved verbatim from the earlier figure-design source.
They reproduce its saved resamples, NOT the later accepted hybrid-panel intervals.
"""
from __future__ import annotations
import math
import numpy as np
import pandas as pd
P_LOW=0.08
P_HIGH=0.24
FAMILIES=['haar_z','clifford_z','floquet_cartan_z','haar_random_pauli','haar_weak_z_eta06']
def build_cluster_matrices(sub: pd.DataFrame, col: str) -> tuple[list[float], dict[tuple[int, float], np.ndarray]]:
    taus = sorted(float(x) for x in sub["tau"].unique())
    mats: dict[tuple[int, float], np.ndarray] = {}
    for n in sorted(int(x) for x in sub["n"].unique()):
        for p in (P_LOW, P_HIGH):
            g = sub[(sub["n"] == n) & np.isclose(sub["p_measure"], p)]
            if g.empty:
                continue
            pivot = g.pivot_table(index="trajectory_index", columns="tau", values=col, aggfunc="first")
            pivot = pivot.reindex(columns=taus)
            mats[(n, p)] = pivot.to_numpy(float)
    return taus, mats

def _nanmean_axis0(arr: np.ndarray) -> np.ndarray:
    counts = np.sum(np.isfinite(arr), axis=0)
    sums = np.nansum(arr, axis=0)
    out = np.full(arr.shape[1], np.nan, dtype=float)
    np.divide(sums, counts, out=out, where=counts > 0)
    return out

def balanced_contrast(sub: pd.DataFrame, bootstrap: int, seed: int) -> tuple[dict[str, float | int], np.ndarray]:
    taus, mats = build_cluster_matrices(sub, "chi_rel")
    sizes = sorted({n for n, _ in mats})

    def estimate(means: dict[tuple[int, float], np.ndarray]) -> float:
        vals: list[float] = []
        for n in sizes:
            low = means.get((n, P_LOW))
            high = means.get((n, P_HIGH))
            if low is None or high is None:
                continue
            delta = high - low
            vals.extend(delta[np.isfinite(delta)].tolist())
        return float(np.mean(vals)) if vals else math.nan

    observed_means = {key: _nanmean_axis0(arr) for key, arr in mats.items()}
    point = estimate(observed_means)
    rng = np.random.default_rng(seed)
    boot = np.empty(bootstrap, dtype=float)
    for b in range(bootstrap):
        sampled_means: dict[tuple[int, float], np.ndarray] = {}
        for key, arr in mats.items():
            idx = rng.integers(0, arr.shape[0], size=arr.shape[0])
            sampled_means[key] = _nanmean_axis0(arr[idx])
        boot[b] = estimate(sampled_means)
    finite = boot[np.isfinite(boot)]
    ci_low, ci_high = np.quantile(finite, [0.025, 0.975])
    return ({
        "estimate": point,
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "bootstrap_replicates": int(bootstrap),
        "bootstrap_valid": int(len(finite)),
        "sizes": int(len(sizes)),
        "time_cells": int(len(taus)),
        "state_rows": int(len(sub)),
        "trajectory_clusters": int(sub[["n", "p_measure", "trajectory_index"]].drop_duplicates().shape[0]),
    }, boot)
