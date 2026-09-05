#!/usr/bin/env python3
"""Replay stored-row estimates and run explicitly post-hoc sensitivity checks.

Input is the original Checkpoint 05 ZIP, verified before reading. No simulator,
original estimator, manuscript, or network access is used. Archived bootstraps
are reused for size/model diagnostics; new trajectory-cluster bootstraps are
used for location estimands. This does not rerun circuit generation.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import platform
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.linalg import cholesky, solve_triangular
from scipy.optimize import least_squares

ARCHIVE_SHA256 = "284a92bfac08af6194cd576ce07c4be90e1e760fcc7b0fc7951eaacd1fa975ce"
PREFIX = "entanglement_project_checkpoint_05/"
DISTANCES = [0, 1, 2, 4, 8, 16]
KEY = ["n", "p_measure", "trajectory_id"]


class Source:
    def __init__(self, path: Path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != ARCHIVE_SHA256:
            raise ValueError(f"Archive identity mismatch: {digest}")
        self.zip = zipfile.ZipFile(path)
        self.used: dict[str, dict] = {}

    def read(self, path: str) -> bytes:
        content = self.zip.read(PREFIX + path)
        self.used[path] = {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
        return content

    def csv(self, path: str) -> pd.DataFrame:
        return pd.read_csv(io.BytesIO(self.read(path)), compression="gzip" if path.endswith(".gz") else None)

    def npz(self, path: str) -> dict[str, np.ndarray]:
        with np.load(io.BytesIO(self.read(path)), allow_pickle=False) as z:
            return {k: z[k].copy() for k in z.files}

    def json(self, path: str) -> dict:
        return json.loads(self.read(path))


def save_csv(frame: pd.DataFrame, output: Path, name: str) -> None:
    frame.to_csv(output / name, index=False, float_format="%.15g")


def response(n, dl, dr):
    return (1.0 - 0.4 * (np.exp2(dl) + np.exp2(dr))) / (1.0 - np.exp2(-np.asarray(n, float) / 2))


def fe_slope(frame: pd.DataFrame):
    """Within-stratum OLS, with source eligibility frozen before estimation."""
    keys = ["tau", "S_central", "p_measure"]
    counts = frame.groupby(keys, observed=True).size().rename("count").reset_index()
    eligible = counts[counts["count"] >= 10].copy()
    levels = eligible.groupby(keys[:2], observed=True).p_measure.transform("nunique")
    selected = frame.merge(eligible.loc[levels >= 3, keys], on=keys, how="inner")
    selected["x"] = (selected.p_measure - .26) / .02
    groups = selected.groupby(keys[:2], observed=True)
    x = selected.x - groups.x.transform("mean")
    y = selected.recomputed - groups.recomputed.transform("mean")
    return float(x.dot(y) / x.dot(x)), len(selected)


def exponential_diagnostic(x, y, covariance, weighting="covariance"):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if weighting == "unweighted":
        L = np.eye(len(x))
    elif weighting == "diagonal":
        L = np.diag(np.sqrt(np.diag(covariance)))
    else:
        L = cholesky(covariance, lower=True)
    def residual(theta):
        return solve_triangular(L, y + theta[0] * np.exp(-x / theta[1]), lower=True)
    fit = least_squares(residual, [.05, 2.], bounds=([0, .05], [1, 100]),
                        xtol=1e-11, ftol=1e-11, gtol=1e-11, max_nfev=10000)
    if not fit.success:
        raise RuntimeError(f"Exponential fitting failed: {fit.message}")
    prediction = -fit.x[0] * np.exp(-x / fit.x[1])
    whitened = solve_triangular(cholesky(covariance, lower=True), y - prediction, lower=True)
    return {"amplitude": float(fit.x[0]), "xi": float(fit.x[1]),
            "Q_covariance": float(whitened @ whitened), "residual_dimension": len(x) - 2,
            "max_abs_marginal_z": float(np.max(np.abs(y - prediction) / np.sqrt(np.diag(covariance))))}


def bootstrap_matrix(values, repetitions, rng):
    """Resample whole trajectories, preserving their joint distance outcomes."""
    values = np.asarray(values, float)
    if values.ndim == 1:
        values = values[:, None]
    result = np.empty((repetitions, values.shape[1]))
    n = len(values)
    for start in range(0, repetitions, 100):
        end = min(start + 100, repetitions)
        ids = rng.integers(0, n, size=(end-start, n))
        draws = values[ids]
        count = np.isfinite(draws).sum(axis=1)
        if (count == 0).any():
            raise ValueError("A bootstrap distance has no eligible trajectories")
        result[start:end] = np.nansum(draws, axis=1) / count
    return result


def curve_analysis(table, label, output, repetitions, rng):
    """table has one row per trajectory and one column per displayed distance."""
    cell_rows, cell_boot, cell_values, fit_rows = [], [], [], []
    for (n,p), group in table.groupby(level=["n", "p_measure"], sort=True):
        values = group[DISTANCES].to_numpy(float)
        mean = np.nanmean(values, axis=0)
        draws = bootstrap_matrix(values, repetitions, rng)
        cell_boot.append(draws); cell_values.append(mean)
        low, high = np.quantile(draws, [.025, .975], axis=0)
        for j, distance in enumerate(DISTANCES):
            cell_rows.append({"curve": label, "n": n, "p": p, "distance": distance,
                              "estimate": mean[j], "ci_low": low[j], "ci_high": high[j],
                              "trajectories": int(np.isfinite(values[:, j]).sum()),
                              "nonzero_trajectories": int((np.abs(values[:,j]) > 1e-12).sum())})
        # Cell diagnostics use d<=4: far cells can have identically zero bootstrap variance.
        C = np.cov(draws[:, :4], rowvar=False)
        if np.linalg.eigvalsh(C).min() > 0:
            fit_rows.append({"curve": label, "n": n, "p": p,
                             "distances": "0,1,2,4", **exponential_diagnostic(DISTANCES[:4], mean[:4], C)})
    pooled = np.mean(cell_boot, axis=0)
    means = np.mean(cell_values, axis=0)
    low, high = np.quantile(pooled, [.025,.975], axis=0)
    # A joint band for the six means, not for a presumed exponential curve.
    se = pooled.std(axis=0, ddof=1)
    max_z = np.max(np.abs(pooled-pooled.mean(axis=0))/se, axis=1)
    q = np.quantile(max_z, .95)
    result = pd.DataFrame({"curve": label,"distance": DISTANCES,"estimate": means,
                           "ci_low": low,"ci_high": high,"simultaneous_low": means-q*se,
                           "simultaneous_high": means+q*se,"bootstrap_se": se})
    save_csv(pd.DataFrame(cell_rows), output, f"{label}_cell_profiles.csv")
    save_csv(pd.DataFrame(fit_rows), output, f"{label}_cell_fit_diagnostics.csv")
    save_csv(result, output, f"{label}_profile.csv")
    ratios = np.abs(pooled[:,1:] / pooled[:,[0]])
    rlo,rhi = np.quantile(ratios,[.025,.975],axis=0)
    save_csv(pd.DataFrame({"distance":DISTANCES[1:],"fraction_of_adjacent_effect":np.abs(means[1:]/means[0]),
                          "ci_low":rlo,"ci_high":rhi}),output,f"{label}_relative_magnitude.csv")
    return means, pooled, result


def location_analysis(src, output, repetitions, rng):
    raw = src.csv("data/measurement_location_intervention/paired_measurement_interventions.csv.gz")
    pre = src.csv("data/measurement_location_intervention/stabilizer_scaling_states.csv.gz")
    base = pre.set_index("trajectory_id").chi_relative
    predicted = response(raw.n, raw.post_delta_left, raw.post_delta_right) - raw.trajectory_id.map(base).to_numpy()
    discrepancy = float(np.max(np.abs(predicted - raw.delta_chi_relative)))
    if discrepancy > 1e-12:
        raise ValueError("Intervention row response mismatch")
    endpoints = {}
    for cond in [False,True]:
        filtered = raw[raw.delta_S_central.eq(0)] if cond else raw
        td = filtered.groupby(KEY+["distance"], observed=True).delta_chi_relative.mean().reset_index()
        near = td[td.distance.eq(0)].set_index(KEY).delta_chi_relative
        far = td[td.distance.ge(td.n/4)].groupby(KEY, observed=True).delta_chi_relative.mean()
        joined = pd.concat({"near":near,"far":far},axis=1).dropna()
        endpoints["original_conditional" if cond else "original_unconditional"] = joined.near-joined.far
    pair_keys=KEY+["side"]
    near=raw[raw.distance.eq(0)].set_index(pair_keys)
    far=raw[raw.distance.eq(raw.n/4)].set_index(pair_keys)
    pairs=near[["delta_S_central","delta_chi_relative"]].join(
        far[["delta_S_central","delta_chi_relative"]],lsuffix="_near",rsuffix="_far",how="inner")
    pairs=pairs[(pairs.delta_S_central_near==0)&(pairs.delta_S_central_far==0)]
    endpoints["strict_same_side"]=(pairs.delta_chi_relative_near-pairs.delta_chi_relative_far).groupby(level=KEY).mean()
    rows=[]; endpoint_draws={}
    for label, values in endpoints.items():
        means,draws=[],[]
        for (n,p),group in values.groupby(level=["n","p_measure"],sort=True):
            b=bootstrap_matrix(group.to_numpy(),repetitions,rng)[:,0]
            lo,hi=np.quantile(b,[.025,.975]);means.append(group.mean());draws.append(b)
            rows.append({"estimand":label,"scope":"cell","n":n,"p":p,"estimate":group.mean(),
                         "ci_low":lo,"ci_high":hi,"trajectories":len(group)})
        b=np.mean(draws,axis=0);lo,hi=np.quantile(b,[.025,.975])
        endpoint_draws[label]=b
        rows.append({"estimand":label,"scope":"equal_cell_pooled","n":None,"p":None,
                     "estimate":np.mean(means),"ci_low":lo,"ci_high":hi,"trajectories":len(values)})
    save_csv(pd.DataFrame(rows),output,"paired_endpoint_bootstraps.csv")
    # Original curve: distance-dependent eligibility, with the same trajectory cluster sampled jointly.
    selected=raw[raw.distance.isin(DISTANCES)&raw.delta_S_central.eq(0)]
    original=selected.groupby(KEY+["distance"],observed=True).delta_chi_relative.mean().unstack("distance")
    original_mean,original_boot,_=curve_analysis(original,"original",output,repetitions,rng)
    reference=src.csv("analysis/intervention/fixed_spectrum_distance_decay.csv")
    err=float(np.max(np.abs(original_mean-reference.estimate.to_numpy())))
    if err > 1e-12: raise ValueError("Original distance means do not replay")
    # Strict common side/pre-state eligibility is imposed across all six distances BEFORE averaging.
    displayed=raw[raw.distance.isin(DISTANCES)]
    delta=displayed.pivot(index=pair_keys,columns="distance",values="delta_S_central").reindex(columns=DISTANCES)
    ids=delta.index[delta.notna().all(axis=1)&delta.eq(0).all(axis=1)]
    common=displayed.set_index(pair_keys).loc[ids].reset_index()
    common_table=common.groupby(KEY+["distance"],observed=True).delta_chi_relative.mean().unstack("distance")
    common_mean,common_boot,_=curve_analysis(common_table,"common",output,repetitions,rng)
    np.savez_compressed(output/"new_location_bootstraps.npz",original_profile=original_boot,
                        common_profile=common_boot,**endpoint_draws)
    archived=src.npz("analysis/intervention/intervention_bootstraps.npz")["distance"]
    frozen=src.json("analysis/intervention/fixed_spectrum_distance_decay_fit.json")
    fit_rows=[]
    for label,mean,draws in [("original_archived_bootstrap",original_mean,archived),("common",common_mean,common_boot)]:
        for distances in [DISTANCES,[0,1,2,4,8],[0,1,2,4],[1,2,4,8,16],[2,4,8,16],[4,8,16]]:
            ids2=[DISTANCES.index(d) for d in distances]
            C=np.cov(draws[:,ids2],rowvar=False)
            for weighting in ["unweighted","diagonal","covariance"]:
                fit_rows.append({"curve":label,"distances":','.join(map(str,distances)),"weighting":weighting,
                                 **exponential_diagnostic(distances,mean[ids2],C,weighting)})
    save_csv(pd.DataFrame(fit_rows),output,"distance_fit_sensitivity.csv")
    prediction=-frozen["amplitude"]*np.exp(-np.array(DISTANCES)/frozen["decay_length"])
    save_csv(pd.DataFrame({"distance":DISTANCES,"observed":original_mean,"frozen_fit":prediction,
                          "ci_low":reference.ci_low,"ci_high":reference.ci_high,
                          "residual_over_marginal_se":(original_mean-prediction)/archived.std(axis=0,ddof=1)}),output,"frozen_distance_fit_residuals.csv")
    return {"intervention_rows":len(raw),"pre_states":raw.trajectory_id.nunique(),
            "max_response_error":discrepancy,"profile_replay_error":err,
            "strict_eligible_side_pairs":len(pairs),"common_eligible_side_pre_states":len(ids),
            "common_trajectories":len(common_table),"conditional_max_delta":float(selected.delta_chi_relative.max()),
            "bootstrap_repetitions":repetitions,"interval_scope":"pointwise percentile; simultaneous bands separately labeled",
            "model_diagnostic_scope":"Q is descriptive; no exact chi-square p-value is asserted"}


def size_analysis(src,output):
    rows=[]; fit_rows=[]; validation={}; strata_rows=[]
    for run,folder in [("primary","primary_scaling"),("replication","independent_replication")]:
        raw=src.csv(f"data/{folder}/stabilizer_scaling_states.csv.gz")
        raw["recomputed"]=response(raw.n,raw.S_central-raw.S_left_neighbor,raw.S_central-raw.S_right_neighbor)
        error=float(np.max(np.abs(raw.recomputed-raw.chi_relative)))
        if error>1e-12:raise ValueError("State response mismatch")
        validation[run]={"rows":len(raw),"response_error":error}
        stored=src.csv(f"analysis/{run}/fixed_spectrum_size_slopes.csv")
        draws=src.npz(f"analysis/{run}/bootstrap_primary_slopes.npz")
        for (protocol,n),group in raw.groupby(["protocol","n"],observed=True):
            beta,count=fe_slope(group)
            target=stored[(stored.protocol==protocol)&(stored.n==n)&(stored.outcome=="chi_relative")].iloc[0]
            rows.append({"run":run,"protocol":protocol,"n":n,"recomputed_beta":beta,"stored_beta":target.beta,
                         "error":abs(beta-target.beta),"rows":count,"ci_low":target.ci_low,"ci_high":target.ci_high})
        for protocol,g in stored[stored.outcome.eq("chi_relative")].groupby("protocol",observed=True):
            g=g.sort_values("n"); ns=g.n.to_numpy(); y=g.beta.to_numpy()
            bs=np.column_stack([draws[f"{protocol}_n{n}_chi_relative"] for n in ns])
            frozen_se=(g.ci_high-g.ci_low).to_numpy()/3.92
            se=bs.std(axis=0,ddof=1)
            # Primary replay plus pre-enumerated sensitivity menu, not a best-model search.
            menu=[("locked",1.,[0,1,2,3],True)]
            menu += [(f"power_{power}",power,[0,1,2,3],False) for power in [.5,1.,1.5,2.]]
            menu += [(f"leave_out_{ns[k]}",1.,[i for i in range(4) if i!=k],False) for k in range(4)]
            for label,power,indices,is_locked in menu:
                ni=ns[indices];yi=y[indices];bi=bs[:,indices];si=(frozen_se if is_locked else se)[indices]
                X=np.column_stack([np.ones(len(indices)),ni.astype(float)**(-power)]);w=1/si**2
                operator=np.linalg.solve(X.T@(w[:,None]*X),X.T*w)
                co=operator@yi;pred=X@co;bootco=bi@operator.T
                lo,hi=np.quantile(bootco[:,0],[.025,.975]); z=(yi-pred)/si
                fit_rows.append({"run":run,"protocol":protocol,"model":label,"power":power,
                                 "sizes":','.join(map(str,ni)),"beta_infinity":co[0],"ci_low":lo,"ci_high":hi,
                                 "Q_diagonal":z@z,"residual_dimension":len(indices)-2,
                                 "weight_basis":"source_CI_width" if is_locked else "archived_bootstrap_SD"})
    slopes=pd.DataFrame(rows)
    if slopes.error.max()>1e-12:raise ValueError("Fixed-effect slope replay mismatch")
    save_csv(slopes,output,"finite_size_replay.csv")
    save_csv(pd.DataFrame(fit_rows),output,"finite_size_model_sensitivity.csv")
    validation["max_slope_error"]=float(slopes.error.max())
    validation["intervals"]="archived trajectory bootstraps reused, not fresh finite-size bootstrap simulations"
    return validation


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--archive",type=Path,required=True)
    ap.add_argument("--output",type=Path,default=Path("reproduced_evidence"))
    ap.add_argument("--bootstrap",type=int,default=5000)
    ap.add_argument("--seed",type=int,default=2026090501)
    args=ap.parse_args()
    if args.bootstrap<100:ap.error("Use at least 100 bootstrap draws (5000 for reported results)")
    args.output.mkdir(parents=True,exist_ok=True)
    source=Source(args.archive)
    summary={"analysis_status":"post-hoc sensitivity and archived-row replay, not a replacement primary analysis",
             "seed":args.seed,"archive_sha256":ARCHIVE_SHA256}
    summary["sizes"]=size_analysis(source,args.output)
    summary["locations"]=location_analysis(source,args.output,args.bootstrap,np.random.default_rng(args.seed))
    summary["environment"]={"python":platform.python_version(),"numpy":np.__version__,"pandas":pd.__version__,"scipy":scipy.__version__}
    (args.output/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    (args.output/"input_manifest.json").write_text(json.dumps(source.used,indent=2)+"\n")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
