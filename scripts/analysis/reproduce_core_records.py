#!/usr/bin/env python3
"""Recompute the accepted four figures' statistics from immutable stored records.

Figure 1 reconstructs unchanged current points and verifies the historical table.
Its exact accepted bootstrap seed and resamples have not been recovered. Figures
3 and 4 use the original archived resamples for their original intervals. All
point estimates and Figure 2 probability slopes are recalculated from state or
intervention records. This does not rerun random-circuit generation, change the
estimands, replace the accepted tables, or estimate a new decay law.
"""
from __future__ import annotations
import argparse
import io
import json
from pathlib import Path
import platform
import numpy as np
import pandas as pd
from boundary_susceptibility.records import RecordBundle, ROOT
FAMILIES=['haar_z','clifford_z','floquet_cartan_z','haar_random_pauli','haar_weak_z_eta06']
from reassess_evidence import fe_slope, response, KEY, DISTANCES

TOL = 2e-11  # accepted CSVs were rounded at export


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('reproduced_records'))
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
    records=RecordBundle(); checks=[]; sources={}; output_rows=[]
    def read(name):
        sources[name]=records.entries[name]['sha256']
        return records.read(name)
    def csv(name):
        return pd.read_csv(io.BytesIO(read(name)),compression='gzip' if name.endswith('.gz') else None)
    def arrays(name):
        with np.load(io.BytesIO(read(name)),allow_pickle=False) as z:
            return {k:z[k].copy() for k in z.files}
    def check(name,actual,expected,tolerance=TOL):
        actual=np.asarray(actual,dtype=float);expected=np.asarray(expected,dtype=float)
        if actual.shape!=expected.shape:raise ValueError(f'{name}: shape mismatch')
        if not np.isfinite(actual).all() or not np.isfinite(expected).all():raise ValueError(f'{name}: nonfinite')
        delta=float(np.max(np.abs(actual-expected))) if actual.size else 0.
        if delta>tolerance:raise ValueError(f'{name}: discrepancy {delta} exceeds {tolerance}')
        checks.append({'check':name,'max_abs_error':delta,'tolerance':tolerance})
    def add(fig,selection,value,expected,kind):
        check(f'{fig}: {selection}',value,expected)
        output_rows.append({'figure':fig,'selection':selection,'recalculated':float(value),
                            'accepted':float(expected),'provenance_kind':kind})

    canon=ROOT/'data/processed/core_figures'
    current_f1=pd.read_csv(canon/'figure_01_panel_b.csv')
    accepted=csv('accepted_figure1/figure_01_panel_b_data.csv')
    f1=pd.read_csv(ROOT/'results/historical_figure1/figure_01_panel_b.csv')
    for field in ['estimate','ci_low','ci_high']:
        check('Figure 1 historical source table/'+field,f1[field],accepted[field],0)
    for field in ['estimate','common_cells','p_low','p_high']:
        check('Figure 1 unchanged current field/'+field,current_f1[field],accepted[field],0)
    filtered={}
    for run,folder in [('primary','primary_rank4'),('independent','independent_seed_rank4')]:
        raw=csv(f'checkpoint_04/data/intervention/{folder}/state_response_rows.csv.gz')
        keep=raw[(raw.split=='confirmatory')&(raw.variant=='equalized_rank4')&raw.p_measure.isin([.08,.24])].copy()
        keep['chi_rel']=keep.probe_haar_or_clifford_2design_delta_linear_norm/keep.pre_purity
        filtered[run]=keep
    # Reconstruct the common cell support recorded by the accepted hybrid figure.
    # This matches all ten point estimates; it is not recovery of its missing RNG seed.
    support_rows=[]
    for family in FAMILIES:
        per_run={}
        for run,keep in filtered.items():
            sub=keep[keep.family==family]
            per_run[run]=sub.groupby(['n','tau','p_measure']).chi_rel.mean().unstack('p_measure')
        common=per_run['primary'].dropna().index.intersection(per_run['independent'].dropna().index)
        for run,means in per_run.items():
            target=f1[(f1.run==run)&(f1.family==family)].iloc[0]
            contrast=means.loc[common,.24]-means.loc[common,.08]
            add('1',f'{run}/{family}/estimate',contrast.mean(),target.estimate,
                'state rows on common family/size/time support across both runs')
            check(f'Figure 1 common cells {run}/{family}',len(common),target.common_cells,0)
            for (n,tau),val in contrast.items():support_rows.append({'run':run,'family':family,'n':n,'tau':tau,'contrast':val})
            for field in ['ci_low','ci_high']:
                output_rows.append({'figure':'1','selection':f'{run}/{family}/{field}',
                    'recalculated':None,'accepted':float(target[field]),
                    'provenance_kind':'accepted hybrid source table verified; original accepted resamples not recovered'})
    pd.DataFrame(support_rows).to_csv(args.output/'figure1_reconstructed_support.csv',index=False)
    print('Figure 1: current points and historical provenance verified; run the dedicated workflow for current intervals',flush=True)

    f2=pd.read_csv(canon/'figure_02_boundary_codes.csv')
    f3=pd.read_csv(canon/'figure_03_size_scaling.csv')
    state_counts={}
    for run,folder in [('primary','primary_scaling'),('replication','independent_replication')]:
        raw=csv(f'checkpoint_05/data/{folder}/stabilizer_scaling_states.csv.gz')
        state_counts[run]=len(raw)
        raw['recomputed']=response(raw.n,raw.S_central-raw.S_left_neighbor,raw.S_central-raw.S_right_neighbor)
        check(f'{run}: all statewise responses',raw.recomputed,raw.chi_relative,1e-12)
        bs=arrays(f'checkpoint_05/analysis/{run}/bootstrap_primary_slopes.npz')
        fitted={}
        for (protocol,n),group in raw.groupby(['protocol','n'],observed=True,sort=True):
            beta,count=fe_slope(group)
            target=f3[(f3.run==run)&(f3.protocol==protocol)&(f3.n==n)&(f3.kind=='finite_size')].iloc[0]
            add('3',f'{run}/{protocol}/{n}/beta',beta,target.beta,'recalculated from state rows')
            check(f'{run}/{protocol}/{n}/eligible rows',count,target.rows,0)
            boot=bs[f'{protocol}_n{n}_chi_relative']
            lo,hi=np.quantile(boot,[.025,.975])
            for field,val in [('ci_low',lo),('ci_high',hi)]:
                add('3',f'{run}/{protocol}/{n}/{field}',val,target[field],'percentiles of archived original resamples')
            fitted[(protocol,int(n))]=(beta,lo,hi)
            if run=='primary' and protocol=='z_projective' and n==256:
                slopes=[];contributions=[]
                for row in f2.itertuples(index=False):
                    g=group.copy()
                    g['recomputed']=((g.S_central-g.S_left_neighbor==row.delta_L)&
                                     (g.S_central-g.S_right_neighbor==row.delta_R)).astype(float)
                    slope,_=fe_slope(g); slopes.append(slope)
                    r=1-.4*(2.**row.delta_L+2.**row.delta_R)
                    contribution=slope*r/(1-2.**(-n/2));contributions.append(contribution)
                    add('2',f'{row.delta_L},{row.delta_R}/probability slope',slope,row.display_probability_slope,
                        'indicator fixed-effect regression on identical state support')
                    add('2',f'{row.delta_L},{row.delta_R}/response',r,row.display_response,'exact formula')
                check('Figure 2: slope conservation',sum(slopes),0,1e-12)
                check('Figure 2: response reconstruction',sum(contributions),beta,1e-12)
        for protocol in sorted(raw.protocol.unique()):
            ns=np.array([32,64,128,256]); y=np.array([fitted[(protocol,int(n))][0] for n in ns])
            se=np.array([(fitted[(protocol,int(n))][2]-fitted[(protocol,int(n))][1])/3.92 for n in ns])
            X=np.column_stack([np.ones(4),1/ns]); w=1/se**2
            operator=np.linalg.solve(X.T@(w[:,None]*X),X.T*w)
            coefficients=operator@y
            boot=np.column_stack([bs[f'{protocol}_n{n}_chi_relative'] for n in ns])@operator.T
            lo,hi=np.quantile(boot[:,0],[.025,.975])
            target=f3[(f3.run==run)&(f3.protocol==protocol)&(f3.kind=='thermodynamic_limit')].iloc[0]
            for field,value in [('beta',coefficients[0]),('a_over_n',coefficients[1]),('ci_low',lo),('ci_high',hi)]:
                add('3',f'{run}/{protocol}/locked fit/{field}',value,target[field],
                    'locked WLS from recalculated slopes and original archived bootstrap arrays')
        print(f'Figures 2/3 {run}: rows, coefficients, archived intervals, and locked fits verified',flush=True)

    raw=csv('checkpoint_05/data/measurement_location_intervention/paired_measurement_interventions.csv.gz')
    pre=csv('checkpoint_05/data/measurement_location_intervention/stabilizer_scaling_states.csv.gz')
    base=pre.set_index('trajectory_id').chi_relative
    predicted=response(raw.n,raw.post_delta_left,raw.post_delta_right)-raw.trajectory_id.map(base)
    check('Figure 4: all intervention responses',predicted,raw.delta_chi_relative,1e-12)
    bs=arrays('checkpoint_05/analysis/intervention/intervention_bootstraps.npz')
    f4c=pd.read_csv(canon/'figure_04_conditioning_contrast.csv')
    for conditional,label in [(False,'unconditional'),(True,'central_spectrum_unchanged')]:
        selected=raw[raw.delta_S_central==0] if conditional else raw
        td=selected.groupby(KEY+['distance'],observed=True).delta_chi_relative.mean().reset_index()
        near=td[td.distance==0].set_index(KEY).delta_chi_relative
        far=td[td.distance>=td.n/4].groupby(KEY,observed=True).delta_chi_relative.mean()
        pair=pd.concat({'near':near,'far':far},axis=1).dropna()
        values=pair.near-pair.far
        estimate=values.groupby(level=['n','p_measure']).mean().mean()
        target=f4c[f4c.condition==label].iloc[0]
        lo,hi=np.quantile(bs[f'conditional_{conditional}_D_relative'],[.025,.975])
        for field,value in [('estimate',estimate),('ci_low',lo),('ci_high',hi)]:
            add('4',f'{label}/{field}',value,target[field],
                'paired intervention records' if field=='estimate' else 'original archived resamples')
        check(f'Figure 4: {label} pre-states',len(values),target.trajectories,0)
    f4d=pd.read_csv(canon/'figure_04_distance_decay.csv')
    selected=raw[(raw.delta_S_central==0)&raw.distance.isin(DISTANCES)]
    values=selected.groupby(KEY+['distance'],observed=True).delta_chi_relative.mean().reset_index()
    means=values.groupby(['n','p_measure','distance'],observed=True).delta_chi_relative.mean().groupby('distance').mean()
    bounds=np.quantile(bs['distance'],[.025,.975],axis=0)
    for i,distance in enumerate(DISTANCES):
        target=f4d[f4d.distance==distance].iloc[0]
        for field,value in [('estimate',means.loc[distance]),('ci_low',bounds[0,i]),('ci_high',bounds[1,i])]:
            add('4',f'distance={distance}/{field}',value,target[field],
                'equal-cell means from intervention records' if field=='estimate' else 'original archived resamples')
    pd.DataFrame(output_rows).to_csv(args.output/'core_values_replay.csv',index=False,float_format='%.17g')
    summary={'passed':True,'checks':len(checks),'max_error':max(x['max_abs_error'] for x in checks),
             'bundle_sha256':records.sha256,'state_rows':state_counts,'intervention_rows':len(raw),
             'figure1_contrasts':10,'figure1_historical_interval_replay':False,
             'figure1_current_interval_command':'See docs/FIGURE1_UNCERTAINTY.md: separate sampler, replay verifier, and adoption check',
             'interval_scope':'Figure 1 historical intervals source-verified only; current Figure 1 is checked in its separate complete workflow; Figures 3/4 reuse archived original resamples',
             'simulation_scope':'No circuit-generation campaign or new statistical estimand',
             'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,
             'source_member_hashes':sources,'details':checks}
    (args.output/'CORE_RECORD_REPLAY.json').write_text(json.dumps(summary,indent=2)+'\n')
    records.close()
    print(json.dumps({k:v for k,v in summary.items() if k not in ['source_member_hashes','details']},indent=2))

if __name__=='__main__':main()
