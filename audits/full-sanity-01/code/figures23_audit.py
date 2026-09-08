#!/usr/bin/env python3
"""Independent pairwise-cell FE reconstruction; no repository-code imports."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import platform
import resource
import time
import zipfile
from itertools import combinations, product
from pathlib import Path
import numpy as np
import pandas as pd


def eligible_cells(frame, minimum=10, levels=3):
    counts = frame.groupby(['tau', 'S_central', 'p_measure']).size()
    counts = counts[counts >= minimum]
    breadth = counts.groupby(level=[0, 1]).size()
    good = set(breadth[breadth >= levels].index)
    keys = [k for k in counts.index if k[:2] in good]
    row_keys = pd.MultiIndex.from_frame(frame[['tau', 'S_central', 'p_measure']])
    return frame.loc[row_keys.isin(keys)].copy()


def pairwise_fit(selected, outcome, step=.02):
    """Cell-pair form of FE normal equation; no original demeaning code."""
    pairs = []
    cells = selected.groupby(['tau', 'S_central', 'p_measure'])[outcome].agg(['count', 'mean'])
    for (tau, entropy), block in cells.groupby(level=[0, 1]):
        entries = [(key[2], int(row['count']), float(row['mean'])) for key, row in block.iterrows()]
        total = sum(x[1] for x in entries)
        for (p, ni, yi), (q, nj, yj) in combinations(entries, 2):
            dx = (q-p)/step
            weight = ni*nj/total * dx*dx
            pairs.append(dict(tau=tau, S_central=entropy, p_low=p, p_high=q,
                              rows_low=ni, rows_high=nj, denominator_weight=weight,
                              local_slope=(yj-yi)/dx))
    pairs = pd.DataFrame(pairs)
    pairs['normalized_weight'] = pairs.denominator_weight / pairs.denominator_weight.sum()
    beta = float((pairs.normalized_weight * pairs.local_slope).sum())
    return beta, pairs


def explicit_fit(selected, outcome):
    cells = selected.groupby(['tau', 'S_central', 'p_measure'])[outcome].agg(['count', 'mean']).reset_index()
    strata = list(zip(cells.tau, cells.S_central))
    keys = sorted(set(strata)); columns = {s: j for j, s in enumerate(keys)}
    design = np.zeros((len(cells), len(keys)+1))
    for i, s in enumerate(strata): design[i, columns[s]] = 1
    design[:, -1] = (cells.p_measure-.26)/.02
    w = np.sqrt(cells['count'].to_numpy(float))
    return float(np.linalg.lstsq(design*w[:, None], cells['mean']*w, rcond=None)[0][-1])


def cluster_se(selected, outcome, beta):
    x = (selected.p_measure-.26)/.02
    keys = [selected.tau, selected.S_central]
    xr = x-x.groupby(keys).transform('mean')
    yr = selected[outcome]-selected[outcome].groupby(keys).transform('mean')
    score = (xr*(yr-beta*xr)).groupby(selected.trajectory_id).sum()
    n = len(selected); c = len(score)
    var0 = np.square(score).sum()/np.square(np.square(xr).sum())
    # Source reports HC1 after a one-column absorbed fit. Also expose full FE df.
    s = selected[['tau', 'S_central']].drop_duplicates().shape[0]
    return np.sqrt(var0*c/(c-1)), np.sqrt(var0*c/(c-1)*(n-1)/(n-s-1))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    start=time.monotonic(); sources={}; checks=[]; support=[]; weights=[]; slopes=[]; code_rows=[]; adj_rows=[]; time_rows=[]; models=[]
    manifest=json.loads((args.root/'data/record_bundle_manifest.json').read_text())
    archive=args.root/manifest['bundle']; digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    assert digest == manifest['sha256']
    entries={r['member']:r for r in manifest['members']}
    z=zipfile.ZipFile(archive)
    def read(name):
        data=z.read(name);sha=hashlib.sha256(data).hexdigest();assert sha==entries[name]['sha256'];sources[name]=sha;return data
    def csv(name):
        return pd.read_csv(io.BytesIO(read(name)),compression='gzip' if name.endswith('.gz') else None)
    def check(name,a,b,tol=1e-11):
        a=np.asarray(a,dtype=float);b=np.asarray(b,dtype=float)
        assert a.shape==b.shape and np.isfinite(a).all() and np.isfinite(b).all(), name
        err=float(np.max(np.abs(a-b))) if a.size else 0
        assert err<=tol,(name,err,tol)
        checks.append(dict(name=name,max_abs_error=err,tolerance=tol))
    canon3=pd.read_csv(args.root/'data/processed/core_figures/figure_03_size_scaling.csv')
    canon2=pd.read_csv(args.root/'data/processed/core_figures/figure_02_boundary_codes.csv')
    sensitivity=pd.read_csv(args.root/'results/evidence_reassessment/finite_size_model_sensitivity.csv')
    time_table=csv('checkpoint_05/analysis/synthesis/fixed_spectrum_time_sensitivity.csv')
    all_selected={}
    for run,folder in [('primary','primary_scaling'),('replication','independent_replication')]:
        raw=csv(f'checkpoint_05/data/{folder}/stabilizer_scaling_states.csv.gz')
        dl=raw.S_central-raw.S_left_neighbor;dr=raw.S_central-raw.S_right_neighbor
        factor=1/(1-np.exp2(-raw.n.to_numpy(float)/2))
        raw['audit_response']=factor*(1-.4*(np.exp2(dl.to_numpy(float))+np.exp2(dr.to_numpy(float))))
        raw['audit_linear']=raw.audit_response*np.exp2(-raw.S_central.to_numpy(float))
        check(f'{run}: chi response all rows',raw.audit_response,raw.chi_relative,1e-12)
        check(f'{run}: linear response all rows',raw.audit_linear,raw.chi_linear,1e-12)
        for source,actual in [('P_central',-raw.S_central),('P_left_neighbor',-raw.S_left_neighbor),('P_right_neighbor',-raw.S_right_neighbor)]:
            check(f'{run}: {source} all rows',np.exp2(actual.to_numpy(float)),raw[source],1e-15)
        check(f'{run}: stored code increments L',dl,raw.delta_left,0)
        check(f'{run}: stored code increments R',dr,raw.delta_right,0)
        assert raw.groupby('trajectory_id').size().eq(3).all()
        assert not raw.duplicated(['trajectory_id','tau']).any()
        assert all(x in (-1,0,1) for x in set(dl)|set(dr))
        original=csv(f'checkpoint_05/analysis/{run}/fixed_spectrum_size_slopes.csv')
        original_adj=csv(f'checkpoint_05/analysis/{run}/fixed_spectrum_adjacent_contrasts.csv')
        with np.load(io.BytesIO(read(f'checkpoint_05/analysis/{run}/bootstrap_primary_slopes.npz')),allow_pickle=False) as data:
            boots={k:data[k].copy() for k in data.files}
        for (protocol,n),group in raw.groupby(['protocol','n']):
            sel=eligible_cells(group);key=dict(run=run,protocol=protocol,n=int(n));all_selected[(run,protocol,int(n))]=sel
            beta,pairs=pairwise_fit(sel,'audit_response'); direct=explicit_fit(sel,'audit_response')
            check(f'{run}/{protocol}/{n}: pairwise vs explicit dummy OLS',beta,direct,1e-12)
            target=canon3[(canon3.run==run)&(canon3.protocol==protocol)&(canon3.n==n)].iloc[0]
            check(f'{run}/{protocol}/{n}: canonical beta',beta,target.beta)
            check(f'{run}/{protocol}/{n}: selected rows',len(sel),target.rows,0)
            check(f'{run}/{protocol}/{n}: selected clusters',sel.trajectory_id.nunique(),target.trajectories,0)
            se,se_full=cluster_se(sel,'audit_response',beta)
            os=original[(original.protocol==protocol)&(original.n==n)&(original.outcome=='chi_relative')].iloc[0]
            check(f'{run}/{protocol}/{n}: score cluster SE',se,os.cluster_se,1e-12)
            q=np.quantile(boots[f'{protocol}_n{n}_chi_relative'],[.025,.975],method='linear')
            check(f'{run}/{protocol}/{n}: archived bootstrap interval',q,[target.ci_low,target.ci_high])
            slopes.append(dict(**key,beta=beta,explicit_dummy_beta=direct,cluster_se=se,full_fe_df_cluster_se=se_full,ci_low=q[0],ci_high=q[1]))
            byp=sel.groupby('p_measure').agg(rows=('trajectory_id','size'),clusters=('trajectory_id','nunique'))
            for p in sorted(group.p_measure.unique()):
                ps=byp.loc[p] if p in byp.index else {'rows':0,'clusters':0}
                support.append(dict(**key,p_measure=p,raw_trajectories=group[group.p_measure==p].trajectory_id.nunique(),eligible_rows=int(ps['rows']),eligible_trajectories=int(ps['clusters'])))
            for k,v in key.items(): pairs[k]=v
            weights.append(pairs)
            cb=[]
            for l,r in product([-1,0,1],repeat=2):
                sel['indicator']=((sel.delta_left==l)&(sel.delta_right==r)).astype(float)
                b,_=pairwise_fit(sel,'indicator');v=(1-.4*(2.**l+2.**r))/(1-2.**(-n/2))
                cb.append((b,v));code_rows.append(dict(**key,delta_left=l,delta_right=r,probability_slope=b,response=v,contribution=b*v))
                if run=='primary' and protocol=='z_projective' and n==256:
                    t=canon2[(canon2.delta_L==l)&(canon2.delta_R==r)].iloc[0]
                    check(f'Figure2 {l}/{r}: indicator slope',b,t.display_probability_slope)
                    check(f'Figure2 {l}/{r}: display response',1-.4*(2.**l+2.**r),t.display_response)
            check(f'{run}/{protocol}/{n}: code conservation',sum(b for b,v in cb),0,1e-13)
            check(f'{run}/{protocol}/{n}: weighted code reconstruction',sum(b*v for b,v in cb),beta,1e-13)
            for p,qv in zip(sorted(group.p_measure.unique())[:-1],sorted(group.p_measure.unique())[1:]):
                adjacent=eligible_cells(group[group.p_measure.isin([p,qv])],levels=2)
                if len(adjacent):
                    ab,_=pairwise_fit(adjacent,'audit_response',step=qv-p)
                    at=original_adj[(original_adj.protocol==protocol)&(original_adj.n==n)&(original_adj.outcome=='chi_relative')&np.isclose(original_adj.p_low,p)&np.isclose(original_adj.p_high,qv)].iloc[0]
                    check(f'{run}/{protocol}/{n}/{p}-{qv}: adjacent beta',ab,at.beta,1e-12)
                    adj_rows.append(dict(**key,p_low=p,p_high=qv,beta_per_pair=ab,rows=len(adjacent),strata=len(adjacent[['tau','S_central']].drop_duplicates()),ci_low=at.ci_low,ci_high=at.ci_high,interval_source='archived table; not freshly resampled'))
            for tau,sub in group.groupby('tau'):
                st=eligible_cells(sub,minimum=5)
                tb,_=pairwise_fit(st,'audit_response')
                tt=time_table[(time_table.run==run)&(time_table.protocol==protocol)&(time_table.n==n)&(time_table.tau==tau)].iloc[0]
                check(f'{run}/{protocol}/{n}/{tau}: time beta',tb,tt.beta,1e-12)
                time_rows.append(dict(**key,tau=tau,beta=tb,min_per_cell=5,ci_low=tt.ci_low,ci_high=tt.ci_high,interval_source='archived table; not freshly resampled'))
        for protocol in sorted(raw.protocol.unique()):
            sizes=np.array([32,64,128,256]);ss=pd.DataFrame([s for s in slopes if s['run']==run and s['protocol']==protocol]).sort_values('n')
            y=ss.beta.to_numpy();se=(ss.ci_high-ss.ci_low).to_numpy()/3.92
            samples=np.column_stack([boots[f'{protocol}_n{n}_chi_relative'] for n in sizes])
            specs=[('locked',1.,None)]+[(f'power_{power}',power,None) for power in [.5,1.,1.5,2.]]+[(f'leave_out_{n}',1.,n) for n in sizes]
            for label,power,omit in specs:
                keep=sizes!=omit if omit else np.ones(4,dtype=bool);ns=sizes[keep]
                design=np.column_stack([np.ones(len(ns)),ns.astype(float)**(-power)])
                se_used=se if label=='locked' else samples.std(axis=0,ddof=1)
                w=1/se_used[keep];operator=np.linalg.pinv(design*w[:,None])*w
                cf=operator@y[keep];bs=samples[:,keep]@operator.T
                q=np.quantile(bs[:,0],[.025,.975],method='linear');residual=(y[keep]-design@cf)*w
                models.append(dict(run=run,protocol=protocol,model=label,power=power,omit=omit,beta_infinity=cf[0],correction=cf[1],ci_low=q[0],ci_high=q[1],Q=float(residual@residual),residual_dimensions=len(ns)-2,weight_basis='source_CI_width' if label=='locked' else 'archived_bootstrap_SD'))
                st=sensitivity[(sensitivity.run==run)&(sensitivity.protocol==protocol)&(sensitivity.model==label)].iloc[0]
                check(f'{run}/{protocol}/{label}: reassessment intercept and interval',[cf[0],q[0],q[1]],[st.beta_infinity,st.ci_low,st.ci_high],1e-11)
                check(f'{run}/{protocol}/{label}: reassessment residual',float(residual@residual),st.Q_diagonal,1e-10)
                if label=='locked':
                    t=canon3[(canon3.run==run)&(canon3.protocol==protocol)&(canon3.kind=='thermodynamic_limit')].iloc[0]
                    check(f'{run}/{protocol}: locked intercept',cf[0],t.beta)
                    check(f'{run}/{protocol}: locked intercept interval',q,[t.ci_low,t.ci_high])
    common=[]
    for protocol,n in product(['random_pauli','z_projective'],[32,64,128,256]):
        a=all_selected[('primary',protocol,n)];b=all_selected[('replication',protocol,n)]
        cols=['tau','S_central','p_measure']
        keys=set(map(tuple,a[cols].drop_duplicates().values)) & set(map(tuple,b[cols].drop_duplicates().values))
        for run,sel in [('primary',a),('replication',b)]:
            keep=sel[pd.MultiIndex.from_frame(sel[cols]).isin(keys)]
            keep=eligible_cells(keep)
            beta,_=pairwise_fit(keep,'audit_response')
            common.append(dict(run=run,protocol=protocol,n=n,beta=beta,rows=len(keep),trajectories=keep.trajectory_id.nunique(),interpretation='diagnostic shared p-spectrum cells; record-count weights still differ; no fresh intervals'))
    outputs={'slopes':pd.DataFrame(slopes),'support':pd.DataFrame(support),'pair_weights':pd.concat(weights,ignore_index=True),'code_slopes':pd.DataFrame(code_rows),'adjacent':pd.DataFrame(adj_rows),'time_sensitivity':pd.DataFrame(time_rows),'finite_size_models':pd.DataFrame(models),'shared_run_support':pd.DataFrame(common)}
    positive=all_selected[('primary','z_projective',256)]
    positive=positive[(positive.tau==10)&(positive.S_central==0)]
    outputs['positive_response_example']=positive.groupby('p_measure').audit_response.agg(count='size',mean_response='mean',min_response='min',max_response='max').reset_index()
    graphs=[]
    for key,g in outputs['pair_weights'].groupby(['run','protocol','n']):
        edges=set(zip(g.p_low.round(5),g.p_high.round(5)));rates=sorted(set(g.p_low.round(5))|set(g.p_high.round(5)));seen={rates[0]}
        for _ in rates:seen|={q for p,q in edges if p in seen}|{p for p,q in edges if q in seen}
        strata=g.groupby(['tau','S_central']).normalized_weight.sum()
        levels=g.groupby(['tau','S_central']).apply(lambda x:len(set(x.p_low.round(5))|set(x.p_high.round(5))),include_groups=False)
        graphs.append(dict(run=key[0],protocol=key[1],n=int(key[2]),eligible_rates=rates,rate_graph_connected=bool(len(seen)==len(rates)),max_levels_in_one_stratum=int(levels.max()),effective_strata_inverse_Herfindahl=float(1/(strata**2).sum()),weight_touching_p020=float(g[(g.p_low.round(5)==.20)|(g.p_high.round(5)==.20)].normalized_weight.sum()),positive_pair_weight=float(g[g.local_slope>0].normalized_weight.sum())))
    interpretation=dict(weight_definition='n_sp*n_sq/N_s*((q-p)/.02)^2, normalized over all strata and pairs',graphs=graphs,all_16_finite_point_and_interval_negative=bool((outputs['slopes'].beta<0).all() and (outputs['slopes'].ci_high<0).all()),time_coefficients_negative=int((outputs['time_sensitivity'].beta<0).sum()),time_intervals_below_zero=int((outputs['time_sensitivity'].ci_high<0).sum()),adjacent_positive_count=int((outputs['adjacent'].beta_per_pair>0).sum()),adjacent_nonnegative_upper_interval_count=int((outputs['adjacent'].ci_high>=0).sum()),adjacent_count=len(outputs['adjacent']),all_sensitivity_upper_bounds_negative=bool((outputs['finite_size_models'].ci_high<0).all()),intercept_range=[float(outputs['finite_size_models'].beta_infinity.min()),float(outputs['finite_size_models'].beta_infinity.max())],max_full_FE_df_SE_fractional_increase=float((outputs['slopes'].full_fe_df_cluster_se/outputs['slopes'].cluster_se-1).max()))
    (args.output/'figures23_interpretation.json').write_text(json.dumps(interpretation,indent=2)+'\n')
    for name,frame in outputs.items():frame.to_csv(args.output/f'figures23_{name}.csv',index=False,float_format='%.17g')
    result=dict(passed=True,checks=checks,source_member_sha256=sources,archive_sha256=digest,python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,seed=None,new_bootstrap_draws=0,bootstrap_dependency='original archived arrays only for size/limit intervals',physical_dependency='original archived entropies and circuit generator',wall_seconds=time.monotonic()-start,max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (args.output/'figures23_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['checks','source_member_sha256']},indent=2))
    print(f'{len(checks)} numerical checks passed')


if __name__=='__main__':main()
