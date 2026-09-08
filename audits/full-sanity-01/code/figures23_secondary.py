#!/usr/bin/env python3
"""Bounded secondary-record checks using only audit-owned estimators."""
import argparse
import hashlib
import io
import json
import resource
import time
import zipfile
import numpy as np
import pandas as pd
from figures23_audit import eligible_cells,pairwise_fit


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=str,required=True);ap.add_argument('--output',type=str,required=True)
    a=ap.parse_args()
    from pathlib import Path
    root=Path(a.root);out=Path(a.output);start=time.monotonic();checks=[];source_hashes={};slopes=[];limits=[];hinges=[];crossings=[];means=[]
    manifest=json.loads((root/'data/record_bundle_manifest.json').read_text());entries={r['member']:r for r in manifest['members']}
    archive=root/manifest['bundle'];assert hashlib.sha256(archive.read_bytes()).hexdigest()==manifest['sha256']
    z=zipfile.ZipFile(archive)
    def read(name):
        raw=z.read(name);sha=hashlib.sha256(raw).hexdigest();assert sha==entries[name]['sha256'];source_hashes[name]=sha;return raw
    def csv(name):return pd.read_csv(io.BytesIO(read(name)),compression='gzip' if name.endswith('.gz') else None)
    def check(name,x,y,tol=1e-11):
        x=np.asarray(x,float);y=np.asarray(y,float);assert x.shape==y.shape and np.isfinite(x).all() and np.isfinite(y).all()
        err=float(np.max(np.abs(x-y)));assert err<=tol,(name,err);checks.append(dict(name=name,max_abs_error=err,tolerance=tol))
    ht=csv('checkpoint_05/analysis/synthesis/transition_crossover_hinge_fits.csv')
    with np.load(io.BytesIO(read('checkpoint_05/analysis/synthesis/transition_crossover_bootstraps.npz')),allow_pickle=False) as f:hb={k:f[k].copy() for k in f.files}
    for run,folder in [('primary','primary_scaling'),('replication','independent_replication')]:
        raw=csv(f'checkpoint_05/data/{folder}/stabilizer_scaling_states.csv.gz')
        pc=np.exp2(-raw.S_central.to_numpy(float));pl=np.exp2(-raw.S_left_neighbor.to_numpy(float));pr=np.exp2(-raw.S_right_neighbor.to_numpy(float))
        raw['audit_y']=(pc-.4*(pl+pr))/(1-np.exp2(-raw.n.to_numpy(float)/2))
        raw['audit_relative']=raw.audit_y/pc
        orig=csv(f'checkpoint_05/analysis/{run}/fixed_spectrum_size_slopes.csv');lt=csv(f'checkpoint_05/analysis/{run}/thermodynamic_limit_fits.csv')
        ct=csv(f'checkpoint_05/analysis/{run}/independent_I3_crossings.csv')
        with np.load(io.BytesIO(read(f'checkpoint_05/analysis/{run}/bootstrap_primary_slopes.npz')),allow_pickle=False) as f:bs={k:f[k].copy() for k in f.files}
        for (protocol,n),frame in raw.groupby(['protocol','n']):
            sel=eligible_cells(frame);beta,_=pairwise_fit(sel,'audit_y')
            t=orig[(orig.protocol==protocol)&(orig.n==n)&(orig.outcome=='chi_linear')].iloc[0]
            check(f'{run}/{protocol}/{n}: secondary beta',beta,t.beta)
            q=np.quantile(bs[f'{protocol}_n{n}_chi_linear'],[.025,.975])
            check(f'{run}/{protocol}/{n}: secondary archived interval',q,[t.ci_low,t.ci_high])
            slopes.append(dict(run=run,protocol=protocol,n=int(n),beta=beta,ci_low=q[0],ci_high=q[1]))
            if n in [128,256]:
                hs=eligible_cells(frame,levels=4)
                c=hs.groupby(['tau','S_central','p_measure']).audit_relative.agg(['mean','count']).reset_index()
                strata=list(zip(c.tau,c.S_central));keys={k:i for i,k in enumerate(sorted(set(strata)))}
                X=np.zeros((len(c),len(keys)+2))
                for i,s in enumerate(strata):X[i,keys[s]]=1
                X[:,-2]=(c.p_measure-.26)/.02;X[:,-1]=np.maximum(0,(c.p_measure-.27)/.02)
                w=np.sqrt(c['count'].to_numpy());co=np.linalg.lstsq(X*w[:,None],c['mean']*w,rcond=None)[0][-2:]
                target=ht[(ht.run==run)&(ht.protocol==protocol)&(ht.n==n)].iloc[0]
                check(f'{run}/{protocol}/{n}: hinge coefficients',[co[0],co[1],co.sum()],[target.pre_transition_slope_per_dp02,target.slope_change_after_p027,target.post_transition_slope_per_dp02])
                check(f'{run}/{protocol}/{n}: hinge retained rows',len(hs),target.rows,0)
                b=hb[f'{run}_{protocol}_n{n}'];q1=np.quantile(b[:,0],[.025,.975]);q2=np.quantile(b[:,1],[.025,.975]);q3=np.quantile(b.sum(axis=1),[.025,.975])
                check(f'{run}/{protocol}/{n}: hinge archived intervals',np.r_[q1,q2,q3],[target.pre_ci_low,target.pre_ci_high,target.change_ci_low,target.change_ci_high,target.post_ci_low,target.post_ci_high])
                hinges.append(dict(run=run,protocol=protocol,n=int(n),pre=co[0],change=co[1],post=co.sum(),pre_ci_low=q1[0],pre_ci_high=q1[1],change_ci_low=q2[0],change_ci_high=q2[1],post_ci_low=q3[0],post_ci_high=q3[1],rows=len(hs)))
        for protocol,frame in raw.groupby('protocol'):
            sizes=np.array([32,64,128,256]);s=pd.DataFrame([v for v in slopes if v['run']==run and v['protocol']==protocol]).sort_values('n')
            X=np.column_stack([np.ones(4),1/sizes]);w=3.92/(s.ci_high-s.ci_low).to_numpy();operator=np.linalg.pinv(X*w[:,None])*w
            co=operator@s.beta.to_numpy();b=np.column_stack([bs[f'{protocol}_n{n}_chi_linear'] for n in sizes])@operator.T;q=np.quantile(b[:,0],[.025,.975])
            target=lt[(lt.protocol==protocol)&(lt.outcome=='chi_linear')].iloc[0]
            check(f'{run}/{protocol}: secondary limit',[co[0],co[1],q[0],q[1]],[target.beta_infinity,target.a_over_n,target.ci_low,target.ci_high])
            limits.append(dict(run=run,protocol=protocol,beta_infinity=co[0],a=co[1],ci_low=q[0],ci_high=q[1]))
            f=frame[frame.tau==10].copy()
            f['audit_I3']=f.S_A+f.S_B+f.S_C-f.S_AB-f.S_AC-f.S_BC+f.S_ABC
            check(f'{run}/{protocol}: quarter I3 identity',f.audit_I3,f.I3_quarters,0)
            mean=f.groupby(['n','p_measure']).audit_I3.mean()
            for (n,p),v in mean.items():means.append(dict(run=run,protocol=protocol,n=n,p_measure=p,I3_mean=v))
            for n1,n2 in zip(sizes[:-1],sizes[1:]):
                d=mean.loc[n2]-mean.loc[n1];candidates=[]
                rates=d.index.to_numpy()
                for p,qv in zip(rates[:-1],rates[1:]):
                    if p<.235 or qv>.295:continue
                    u,v=d.loc[p],d.loc[qv]
                    if u==0:candidates.append(float(p))
                    elif u*v<0 or v==0:candidates.append(float(p-u*(qv-p)/(v-u)))
                chosen=min(candidates,key=lambda x:abs(x-.26))
                target=ct[(ct.protocol==protocol)&(ct.n_low==n1)&(ct.n_high==n2)].iloc[0]
                check(f'{run}/{protocol}/{n1}-{n2}: I3 crossing point',chosen,target.p_cross)
                crossings.append(dict(run=run,protocol=protocol,n_low=int(n1),n_high=int(n2),crossing=chosen,candidates=json.dumps(candidates),ci_low=target.ci_low,ci_high=target.ci_high,valid_bootstrap_fraction=target.valid_bootstrap_fraction,interval_source='archived table; original crossing draws not in bundle, not regenerated'))
    for name,rows in [('secondary_slopes',slopes),('secondary_limits',limits),('hinge',hinges),('I3_crossings',crossings),('I3_means',means)]:pd.DataFrame(rows).to_csv(out/f'figures23_{name}.csv',index=False,float_format='%.17g')
    result=dict(passed=True,checks=checks,source_member_sha256=source_hashes,wall_seconds=time.monotonic()-start,max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_random_draws=0,dependencies='audit-owned cell estimator; original raw quarter entropies; original archived size and hinge bootstrap arrays; crossing intervals merely copied from source table')
    (out/'figures23_secondary_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['checks','source_member_sha256']},indent=2));print(len(checks),'checks passed')


if __name__=='__main__':main()
