#!/usr/bin/env python3
"""New, support-conditioned Figure 1 trajectory-bootstrap intervals.

This is NOT recovery of the accepted figure's missing historical resamples.
Read the locked plan before interpreting the conditional percentile intervals.
No accepted input or artwork is modified. All used proposal multiplicities,
validity flags, and retained replicates are saved for RNG-independent replay.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import io
import itertools
import json
from pathlib import Path
import platform
import zipfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / 'analysis_plans/figure1_uncertainty_2026-09-08.json'
PLAN_SHA256 = '5514e46d1ed2bbba54237fb98d5bf7ab7f0da312d6c0f8a22ef1a18c26413d93'
LOCK_COMMIT = 'fc1f3c56693ebf52e207e5b251758fe3dbd35ca3'


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def save_arrays(path: Path, arrays: dict[str, np.ndarray]) -> None:
    """Deterministic NPZ, including fixed ZIP metadata; never uses pickle."""
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for key in sorted(arrays):
            buffer = io.BytesIO()
            np.save(buffer, np.asarray(arrays[key]), allow_pickle=False)
            member = zipfile.ZipInfo(key + '.npy', date_time=(2026, 9, 8, 0, 0, 0))
            member.compress_type = zipfile.ZIP_DEFLATED
            member.external_attr = 0o100644 << 16
            z.writestr(member, buffer.getvalue(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)


def read_inputs(plan: dict, source_dir: Path | None = None) -> dict[str, bytes]:
    if source_dir is not None:
        raw = {name: (source_dir / name).read_bytes() for name in plan['source_member_sha256']}
    else:
        archive = ROOT / 'entanglement-data.zip'
        with archive.open('rb') as f:
            if hashlib.file_digest(f, 'sha256').hexdigest() != plan['archive_sha256']:
                raise ValueError('Wrong original-study archive')
        with zipfile.ZipFile(archive) as z:
            raw = {name: z.read(name) for name in plan['source_member_sha256']}
    for name, expected in plan['source_member_sha256'].items():
        if sha(raw[name]) != expected:
            raise ValueError(f'Source integrity failure: {name}')
    return raw


@dataclass
class Stratum:
    name: str
    n: int
    p: float
    taus: np.ndarray
    ids: np.ndarray
    values: np.ndarray
    sign: int


def valid_probability(values: np.ndarray) -> Fraction:
    """Exact probability that all time cells survive an N-out-of-N draw."""
    present = np.isfinite(values)
    N, J = present.shape
    if not N or not J or not present.any(axis=0).all():
        raise ValueError('Unsupported stratum')
    probability = Fraction(0)
    for mask in itertools.product([False, True], repeat=J):
        chosen = np.flatnonzero(mask)
        union = int(present[:, chosen].any(axis=1).sum()) if len(chosen) else 0
        probability += (-1) ** len(chosen) * Fraction(N-union, N) ** N
    return probability


def weighted_estimates(strata: list[Stratum], counts: list[np.ndarray], cells: int) -> np.ndarray:
    """Fixed-cell estimator; undefined replicate => NaN, never drop a cell."""
    if len(strata) != len(counts) or not strata or cells <= 0:
        raise ValueError('Invalid estimator configuration')
    B = counts[0].shape[0]
    estimate = np.zeros(B, dtype=np.float64)
    valid = np.ones(B, dtype=bool)
    for s, w in zip(strata, counts):
        if w.shape != (B, len(s.ids)):
            raise ValueError('Wrong multiplicity shape')
        present = np.isfinite(s.values)
        y = np.where(present, s.values, 0.)
        # Explicit ordered sums avoid platform-dependent BLAS reductions.
        sums = (w[:, :, None] * y[None, :, :]).sum(axis=1)
        nums = (w[:, :, None] * present[None, :, :]).sum(axis=1)
        local = np.divide(sums, nums, out=np.zeros_like(sums), where=nums > 0)
        valid &= (nums > 0).all(axis=1)
        estimate += s.sign * local.sum(axis=1) / cells
    estimate[~valid] = np.nan
    return estimate


def sample(strata: list[Stratum], cells: int, seed: list[int], B: int,
           batch: int = 1000, max_proposals: int = 1000000) -> tuple[dict, np.ndarray, dict]:
    if B <= 0 or batch <= 0 or max_proposals < B:
        raise ValueError('Invalid resampling budget')
    rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(seed)))
    pieces = {s.name: [] for s in strata}
    proposals = []
    accepted = attempted = 0
    while accepted < B:
        b = min(batch, max_proposals-attempted)
        if b <= 0:
            raise RuntimeError('Fixed proposal cap reached; do not alter support or impute')
        weights = []
        for s in strata:
            N = len(s.ids)
            if not 0 < N < 256:
                raise ValueError('Multiplicity encoding requires 1..255 trajectories')
            draw = rng.integers(0, N, size=(b, N), dtype=np.int64)
            count = (draw[:, :, None] == np.arange(N)[None, None, :]).sum(axis=1).astype(np.uint8)
            weights.append(count)
        estimates = weighted_estimates(strata, weights, cells)
        keep = np.flatnonzero(np.isfinite(estimates))
        needed = B-accepted
        if len(keep) >= needed:
            stop = int(keep[needed-1])+1
            estimates = estimates[:stop]
            weights = [w[:stop] for w in weights]
        for s, w in zip(strata, weights):
            pieces[s.name].append(w)
        proposals.append(estimates)
        attempted += len(estimates)
        accepted += int(np.isfinite(estimates).sum())
    all_estimates = np.concatenate(proposals)
    validity = np.isfinite(all_estimates)
    values = all_estimates[validity]
    if len(values) != B:
        raise AssertionError('Incorrect bootstrap count')
    stored = {'proposal_estimates': all_estimates, 'valid': validity,
              'accepted_indices': np.flatnonzero(validity), 'bootstrap': values}
    for s in strata:
        stored[s.name+'_counts'] = np.concatenate(pieces[s.name])
        stored[s.name+'_trajectory_indices'] = s.ids
        stored[s.name+'_times'] = s.taus
        stored[s.name+'_response_matrix'] = s.values
    prob = np.prod([float(valid_probability(s.values)) for s in strata])
    info = {'seed_sequence': seed, 'bootstrap_replicates': B, 'proposals': attempted,
            'rejected': attempted-B, 'rejected_fraction': (attempted-B)/attempted,
            'expected_rejected_fraction': 1-float(prob),
            'trajectory_clusters': sum(len(s.ids) for s in strata),
            'eligible_state_rows': sum(int(np.isfinite(s.values).sum()) for s in strata)}
    return stored, values, info


def prepare(plan: dict, sources: dict) -> tuple[dict, dict, pd.DataFrame, list[dict]]:
    filtered, originals, support = {}, {}, []
    for run in plan['runs']:
        folder = plan['folders'][run]
        name = f'checkpoint_04/data/intervention/{folder}/state_response_rows.csv.gz'
        raw = pd.read_csv(io.BytesIO(sources[name]), compression='gzip')
        common = raw[(raw.split == 'confirmatory') & raw.p_measure.isin([.08, .24])].copy()
        if common.duplicated(['state_id', 'variant']).any():
            raise ValueError('Duplicated trajectory/time/variant records')
        originals[run] = common[common.variant == 'original'].copy()
        selected = common[common.variant == 'equalized_rank4'].copy()
        selected['response'] = selected[plan['response_numerator']] / selected[plan['response_denominator']]
        if not np.isfinite(selected.response).all() or not (selected.pre_purity > 0).all():
            raise ValueError('Nonfinite or invalid response input')
        expected = (1-selected.probe_haar_or_clifford_2design_post_purity/selected.pre_purity)/(1-2.**(-selected.n/2))
        np.testing.assert_allclose(selected.response, expected, atol=2e-12, rtol=0)
        refs = json.loads(sources[f'checkpoint_04/data/intervention/{folder}/equalization_reference_spectra.json'])
        for (family,n,tau), g in selected.groupby(['family','n','tau'],sort=True):
            mu = np.asarray(refs[f'{family}|n{n}|tau{tau:g}'])
            np.testing.assert_allclose(g.pre_purity, np.sum(mu*mu),atol=2e-12,rtol=0)
        filtered[run] = selected
    for family in plan['families']:
        found = []
        for run in plan['runs']:
            sub = filtered[run][filtered[run].family == family]
            means = sub.groupby(['n','tau','p_measure']).response.mean().unstack('p_measure')
            found.append(set(means.dropna().index))
        actual = found[0].intersection(found[1])
        if actual != set(map(tuple,plan['common_support'][family])):
            raise ValueError(f'The observed common support changed: {family}')
        for run in plan['runs']:
            for n,tau in plan['common_support'][family]:
                for p in [.08,.24]:
                    s = filtered[run]
                    a = s[(s.family==family)&(s.n==n)&(s.tau==tau)&(s.p_measure==p)]
                    o = originals[run]
                    b = o[(o.family==family)&(o.n==n)&(o.tau==tau)&(o.p_measure==p)]
                    support.append({'run':run,'family':family,'n':n,'tau':tau,'p_measure':p,
                                    'eligible_trajectories':len(a),'original_confirmatory_trajectories':len(b),
                                    'cell_mean':float(a.response.mean())})
    historical = pd.read_csv(io.BytesIO(sources['accepted_figure1/figure_01_panel_b_data.csv']))
    if sha(sources['accepted_figure1/figure_01_panel_b_data.csv']) != plan['canonical_table_sha256']:
        raise ValueError('Wrong accepted table')
    return filtered, originals, historical, support


def strata_for(plan: dict, filtered: dict, originals: dict, run: str, family: str, pool: str) -> list[Stratum]:
    result = []
    cells = plan['common_support'][family]
    for n in sorted({n for n,tau in cells}):
        taus = np.asarray(sorted(t for nn,t in cells if nn==n),dtype=np.int64)
        for p,sign in [(.08,-1),(.24,1)]:
            sub = filtered[run]
            sub = sub[(sub.family==family)&(sub.n==n)&(sub.p_measure==p)&sub.tau.isin(taus)]
            mat = sub.pivot(index='trajectory_index',columns='tau',values='response').reindex(columns=taus)
            if pool == 'all_confirmatory':
                origin = originals[run]
                ids = sorted(origin[(origin.family==family)&(origin.n==n)&(origin.p_measure==p)].trajectory_index.unique())
                mat = mat.reindex(index=ids)
            elif pool != 'eligible_union':
                raise ValueError(pool)
            mat = mat.sort_index()
            result.append(Stratum(f'n{n}_p{int(round(p*100)):02d}', n,p,taus,
                                  mat.index.to_numpy(np.int64),mat.to_numpy(np.float64),sign))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'reproduced_figure1_uncertainty')
    parser.add_argument('--source-dir',type=Path,help='Optional hash-verified standalone subset of the original archive')
    args = parser.parse_args()
    if sha(PLAN.read_bytes()) != PLAN_SHA256:
        raise ValueError('Locked analysis plan differs from the recorded plan')
    plan = json.loads(PLAN.read_text())
    sources = read_inputs(plan,args.source_dir)
    filtered,originals,historical,support = prepare(plan,sources)
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise FileExistsError('Output must be empty: never overwrite accepted or previous outputs')
    output.mkdir(parents=True,exist_ok=True)
    (output/'resamples').mkdir()
    comparisons=[];stability=[];patterns=[];manifests={}
    max_point_error=0.
    for pi,pool in enumerate(plan['pool_order']):
        for ri,run in enumerate(plan['runs']):
            for fi,family in enumerate(plan['families']):
                strata = strata_for(plan,filtered,originals,run,family,pool)
                cells = len(plan['common_support'][family])
                point = float(weighted_estimates(strata,[np.ones((1,len(s.ids)),dtype=np.uint8) for s in strata],cells)[0])
                old = historical[(historical.run==run)&(historical.family==family)].iloc[0]
                error=abs(point-float(old.estimate));max_point_error=max(max_point_error,error)
                if error>2e-12 or cells!=int(old.common_cells):
                    raise AssertionError('Point estimate or support differs from accepted definition')
                seed=[plan['seed'],pi,ri,fi]
                stored,draws,info=sample(strata,cells,seed,plan['bootstrap_replicates'],
                                        plan['proposal_batch'],plan['max_proposals'])
                filename=f'{pool}__{run}__{family}'
                file=output/'resamples'/(filename+'.npz')
                save_arrays(file,stored)
                lo,hi=np.quantile(draws,[.025,.975],method='linear')
                row={'pool':pool,'run':run,'family':family,'family_label':old.family_label,
                     'estimate':point,'accepted_estimate':float(old.estimate),'common_cells':cells,
                     'historical_ci_low':float(old.ci_low),'historical_ci_high':float(old.ci_high),
                     'ci_low':float(lo),'ci_high':float(hi),'ci_low_shift':float(lo-old.ci_low),
                     'ci_high_shift':float(hi-old.ci_high),'width_ratio':float((hi-lo)/(old.ci_high-old.ci_low)),
                     'ci_below_zero':bool(hi<0),'bootstrap_standard_error':float(draws.std(ddof=1)),**info}
                comparisons.append(row)
                for k,block in enumerate(np.split(draws,5)):
                    blo,bhi=np.quantile(block,[.025,.975],method='linear')
                    stability.append({'pool':pool,'run':run,'family':family,'batch':k+1,
                                      'draws':len(block),'ci_low':blo,'ci_high':bhi})
                for s in strata:
                    present=np.isfinite(s.values)
                    for pattern in np.unique(present,axis=0):
                        patterns.append({'pool':pool,'run':run,'family':family,'n':s.n,'p_measure':s.p,
                                         'times':','.join(map(str,s.taus)),
                                         'eligibility_pattern':''.join('1' if v else '0' for v in pattern),
                                         'trajectory_count':int((present==pattern).all(axis=1).sum())})
                manifests[filename]={'path':str(file.relative_to(output)),'sha256':sha(file.read_bytes()),
                                     'pool':pool,'run':run,'family':family,'cells':cells,
                                     'strata':[{'key':s.name,'sign':s.sign,'n':s.n,'p_measure':s.p} for s in strata],**info}
                print(f'{pool}/{run}/{family}: {point:+.8f} [{lo:+.8f},{hi:+.8f}], rejected {info["rejected"]}/{info["proposals"]}',flush=True)
    df=pd.DataFrame(comparisons)
    # Seed lists remain in manifest JSON; use readable CSV scalar fields only.
    df.drop(columns=['seed_sequence']).to_csv(output/'interval_comparison.csv',index=False,float_format='%.17g')
    pd.DataFrame(support).to_csv(output/'cell_support.csv',index=False,float_format='%.17g')
    pd.DataFrame(stability).to_csv(output/'monte_carlo_batches.csv',index=False,float_format='%.17g')
    pd.DataFrame(patterns).to_csv(output/'eligibility_patterns.csv',index=False)
    candidate=pd.read_csv(io.BytesIO(sources['accepted_figure1/figure_01_panel_b_data.csv']),dtype=str)
    for i,row in candidate.iterrows():
        new=df[(df.pool=='eligible_union')&(df.run==row.run)&(df.family==row.family)].iloc[0]
        candidate.loc[i,['ci_low','ci_high']]=[format(new.ci_low,'.17g'),format(new.ci_high,'.17g')]
    candidate.to_csv(output/'figure_01_candidate_intervals.csv',index=False,float_format='%.17g')
    summary={'analysis_id':plan['analysis_id'],'plan_sha256':PLAN_SHA256,'plan_commit':LOCK_COMMIT,
             'baseline_commit':plan['baseline_commit'],'new_intervals_adopted':False,
             'historical_resamples_recovered':False,'max_point_discrepancy':max_point_error,
             'primary_intervals_below_zero':int(df[df.pool=='eligible_union'].ci_below_zero.sum()),
             'sensitivity_intervals_below_zero':int(df[df.pool=='all_confirmatory'].ci_below_zero.sum()),
             'sampling_scope':'Conditional on frozen references, common support and full-cell survival. No new trajectories.',
             'bootstrap_draws_per_result':plan['bootstrap_replicates'],
             'source_member_hashes':plan['source_member_sha256'],
             'environment':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__},
             'outputs':manifests}
    (output/'ANALYSIS_STATUS.json').write_text(json.dumps(summary,indent=2)+'\n')
    (output/'RUN_PLAN.json').write_bytes(PLAN.read_bytes())
    files={str(p.relative_to(output)):sha(p.read_bytes()) for p in sorted(output.rglob('*')) if p.is_file()}
    (output/'OUTPUT_SHA256.json').write_text(json.dumps(files,indent=2)+'\n')

if __name__=='__main__':
    main()
