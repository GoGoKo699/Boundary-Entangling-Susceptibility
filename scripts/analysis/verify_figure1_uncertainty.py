#!/usr/bin/env python3
"""Recalculate new Figure 1 intervals from saved multiplicities, without its sampler.

This verifier does not import complete_figure1_uncertainty.py, rerun its RNG,
fit a seed, or substitute historical bootstrap arrays. It reconstructs the
original response matrices itself and checks all proposed and retained draws.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
EXPECTED_PLAN='5514e46d1ed2bbba54237fb98d5bf7ab7f0da312d6c0f8a22ef1a18c26413d93'


def verify(output:Path,source_dir:Path|None=None) -> dict:
    plan_raw=(output/'RUN_PLAN.json').read_bytes()
    if hashlib.sha256(plan_raw).hexdigest()!=EXPECTED_PLAN:
        raise ValueError('Unrecognized plan')
    plan=json.loads(plan_raw);status=json.loads((output/'ANALYSIS_STATUS.json').read_text())
    file_hashes=json.loads((output/'OUTPUT_SHA256.json').read_text())
    for name,digest in file_hashes.items():
        if hashlib.sha256((output/name).read_bytes()).hexdigest()!=digest:
            raise ValueError(f'Output integrity mismatch: {name}')
    if source_dir is None:
        raw_archive=(ROOT/'entanglement-data.zip').read_bytes()
        if hashlib.sha256(raw_archive).hexdigest()!=plan['archive_sha256']:
            raise ValueError('Archive integrity mismatch')
        with zipfile.ZipFile(io.BytesIO(raw_archive)) as z:
            raw={k:z.read(k) for k in plan['source_member_sha256']}
    else:
        raw={k:(source_dir/k).read_bytes() for k in plan['source_member_sha256']}
    for k,digest in plan['source_member_sha256'].items():
        if hashlib.sha256(raw[k]).hexdigest()!=digest:raise ValueError(k)
    dfs={run:pd.read_csv(io.BytesIO(raw[f'checkpoint_04/data/intervention/{folder}/state_response_rows.csv.gz']),compression='gzip')
         for run,folder in plan['folders'].items()}
    table=pd.read_csv(output/'interval_comparison.csv')
    accepted=pd.read_csv(io.BytesIO(raw['accepted_figure1/figure_01_panel_b_data.csv']))
    max_error=0.;explicit_error=0.;proposals=retained=0;details=[]
    for name,meta in status['outputs'].items():
        df=dfs[meta['run']]
        selected=df[(df.family==meta['family'])&(df.split=='confirmatory')]
        raw_y=selected[selected.variant=='equalized_rank4'].copy()
        raw_y['y']=raw_y.probe_haar_or_clifford_2design_delta_linear_norm/raw_y.pre_purity
        saved=np.load(output/meta['path'],allow_pickle=False)
        Q=len(saved['valid']);totals=np.zeros(Q);valid=np.ones(Q,dtype=bool)
        rows=[]
        for s in meta['strata']:
            key=s['key'];n=s['n'];p=s['p_measure']
            times=sorted(t for nn,t in plan['common_support'][meta['family']] if nn==n)
            part=raw_y[(raw_y.n==n)&(raw_y.p_measure==p)&raw_y.tau.isin(times)]
            if meta['pool']=='all_confirmatory':
                original=selected[(selected.variant=='original')&(selected.n==n)&(selected.p_measure==p)]
                ids=sorted(original.trajectory_index.unique())
            else:ids=sorted(part.trajectory_index.unique())
            matrix=np.full((len(ids),len(times)),np.nan)
            for row in part.itertuples():matrix[ids.index(row.trajectory_index),times.index(row.tau)]=row.y
            np.testing.assert_array_equal(ids,saved[key+'_trajectory_indices'])
            np.testing.assert_array_equal(times,saved[key+'_times'])
            np.testing.assert_allclose(matrix,saved[key+'_response_matrix'],atol=0,rtol=0,equal_nan=True)
            counts=saved[key+'_counts']
            if counts.shape!=(Q,len(ids)) or not np.issubdtype(counts.dtype,np.integer):raise ValueError('Bad counts')
            if (counts<0).any() or not (counts.sum(axis=1)==len(ids)).all():raise ValueError('Not an N-out-of-N resample')
            present=np.isfinite(matrix)
            # Independent matrix contraction, not the sampler's ordered broadcast sum.
            denominators=counts.astype(np.float64)@present.astype(np.float64)
            numerators=counts.astype(np.float64)@np.nan_to_num(matrix,nan=0.)
            ok=(denominators>0).all(axis=1);valid &=ok
            means=np.divide(numerators,denominators,out=np.zeros_like(numerators),where=denominators>0)
            totals+=s['sign']*means.sum(axis=1)/meta['cells']
            rows.append((matrix,counts,s['sign']))
        totals[~valid]=np.nan
        np.testing.assert_array_equal(valid,saved['valid'])
        np.testing.assert_array_equal(np.flatnonzero(valid),saved['accepted_indices'])
        if valid.sum()!=plan['bootstrap_replicates'] or not valid[-1]:raise ValueError('Incorrect stopping rule')
        max_error=max(max_error,float(np.max(np.abs(totals[valid]-saved['bootstrap']))))
        np.testing.assert_allclose(totals,saved['proposal_estimates'],atol=5e-14,rtol=0,equal_nan=True)
        for j in np.unique(np.linspace(0,Q-1,64,dtype=int)):
            val=0.;ok=True
            for matrix,counts,sign in rows:
                duplicated=np.repeat(matrix,counts[j].astype(int),axis=0)
                for col in range(duplicated.shape[1]):
                    observed=duplicated[:,col][np.isfinite(duplicated[:,col])]
                    if not len(observed):ok=False;break
                    val+=sign*sum(float(v) for v in observed)/len(observed)/meta['cells']
                if not ok:break
            if ok!=bool(valid[j]):raise ValueError('Explicit expansion changes validity')
            if ok:explicit_error=max(explicit_error,abs(val-totals[j]))
        lo,hi=np.quantile(totals[valid],[.025,.975],method='linear')
        entry=table[(table.pool==meta['pool'])&(table.run==meta['run'])&(table.family==meta['family'])].iloc[0]
        np.testing.assert_allclose([lo,hi],[entry.ci_low,entry.ci_high],atol=5e-14,rtol=0)
        old=accepted[(accepted.run==meta['run'])&(accepted.family==meta['family'])].iloc[0]
        np.testing.assert_allclose([entry.estimate,entry.historical_ci_low,entry.historical_ci_high],
                                   [old.estimate,old.ci_low,old.ci_high],atol=2e-12,rtol=0)
        proposals+=Q;retained+=int(valid.sum())
        details.append({'pool':meta['pool'],'run':meta['run'],'family':meta['family'],
                        'proposals_checked':Q,'retained':int(valid.sum()),'interval_replayed':True})
    if max_error>5e-14 or explicit_error>5e-14:raise ValueError('Replay discrepancy')
    candidate=pd.read_csv(output/'figure_01_candidate_intervals.csv')
    np.testing.assert_array_equal(candidate.estimate,accepted.estimate)
    return {'passed':True,'sampler_imported':False,'rng_used':False,'proposed_vectors_checked':proposals,
            'retained_contrasts_checked':retained,'explicit_row_expansions_checked':64*len(details),
            'max_vector_error':max_error,'max_explicit_error':explicit_error,'details':details}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--source-dir',type=Path)
    ap.add_argument('--report',type=Path)
    a=ap.parse_args();result=verify(a.output,a.source_dir)
    text=json.dumps(result,indent=2)+'\n'
    if a.report:a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(text)
    print(text)

if __name__=='__main__':main()
