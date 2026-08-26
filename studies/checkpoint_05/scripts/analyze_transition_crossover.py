#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import numpy as np,pandas as pd,statsmodels.api as sm

def s32(*x):return int.from_bytes(hashlib.blake2b(repr(x).encode(),digest_size=8).digest(),'little')&0xffffffff

def prepare(df,min_per_p=10,min_levels=4):
    counts=df.groupby(['tau','S_central','p_measure'],observed=True).size().rename('count').reset_index()
    good=counts[counts['count']>=min_per_p]
    levels=good.groupby(['tau','S_central'],observed=True).p_measure.nunique()
    valid=set(levels[levels>=min_levels].index)
    good=good[good.apply(lambda r:(r.tau,r.S_central) in valid,axis=1)]
    x=df.merge(good[['tau','S_central','p_measure']].assign(k=1),on=['tau','S_central','p_measure'],how='inner')
    x['g']=pd.factorize(pd.MultiIndex.from_frame(x[['tau','S_central']]),sort=True)[0]
    x['cl']=pd.factorize(x.trajectory_id,sort=True)[0]
    x['linear']=(x.p_measure-.26)/.02
    x['hinge']=np.maximum(0,(x.p_measure-.27)/.02)
    return x

def residualize(v,g,w=None):
    if w is None:
        return v-pd.Series(v).groupby(g).transform('mean').to_numpy()
    ng=g.max()+1;sw=np.bincount(g,weights=w,minlength=ng);sv=np.bincount(g,weights=w*v,minlength=ng)
    mean=np.divide(sv,sw,out=np.zeros_like(sv),where=sw>0);return v-mean[g]

def weighted_coef(y,X,g,w=None):
    if w is None:w=np.ones(len(y))
    yr=residualize(y,g,w);Xr=np.column_stack([residualize(X[:,j],g,w) for j in range(X.shape[1])])
    return np.linalg.lstsq(Xr*np.sqrt(w)[:,None],yr*np.sqrt(w),rcond=None)[0]

def fit(df,B,seed):
    x=prepare(df);g=x.g.to_numpy(int);y=x.chi_relative.to_numpy(float);X=x[['linear','hinge']].to_numpy(float)
    coef=weighted_coef(y,X,g);yr=residualize(y,g);Xr=np.column_stack([residualize(X[:,j],g) for j in range(2)])
    m=sm.OLS(yr,Xr).fit(cov_type='cluster',cov_kwds={'groups':x.cl.to_numpy(int),'use_correction':True})
    clusters=x[['cl','p_measure']].drop_duplicates();C=x.cl.max()+1;pmap={p:q.cl.to_numpy(int) for p,q in clusters.groupby('p_measure')}
    rc=x.cl.to_numpy(int);rng=np.random.default_rng(seed);boots=np.empty((B,2))
    for b in range(B):
        cw=np.zeros(C,np.int16)
        for p,ids in pmap.items():
            draw=rng.integers(0,len(ids),len(ids));cw[ids]=np.bincount(draw,minlength=len(ids)).astype(np.int16)
        boots[b]=weighted_coef(y,X,g,cw[rc].astype(float))
    pre=boots[:,0];change=boots[:,1];post=pre+change
    q=lambda z:np.quantile(z,[.025,.975])
    return {'pre_transition_slope_per_dp02':float(coef[0]),'pre_ci_low':float(q(pre)[0]),'pre_ci_high':float(q(pre)[1]),
            'slope_change_after_p027':float(coef[1]),'change_ci_low':float(q(change)[0]),'change_ci_high':float(q(change)[1]),
            'post_transition_slope_per_dp02':float(coef.sum()),'post_ci_low':float(q(post)[0]),'post_ci_high':float(q(post)[1]),
            'rows':len(x),'trajectories':x.trajectory_id.nunique(),'strata':x[['tau','S_central']].drop_duplicates().shape[0],
            'bootstrap':B},boots

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--outdir',type=Path,required=True);ap.add_argument('--bootstrap',type=int,default=2000)
    a=ap.parse_args();a.outdir.mkdir(parents=True,exist_ok=True);rows=[];bs={}
    for run,rel in [('primary','data/primary_scaling/stabilizer_scaling_states.csv.gz'),('replication','data/independent_replication/stabilizer_scaling_states.csv.gz')]:
      d=pd.read_csv(a.root/rel)
      for (prot,n),sub in d[d.n.isin([128,256])].groupby(['protocol','n']):
        r,b=fit(sub,a.bootstrap,s32(run,prot,n));r.update(run=run,protocol=prot,n=n);rows.append(r);bs[f'{run}_{prot}_n{n}']=b
    out=pd.DataFrame(rows);out.to_csv(a.outdir/'transition_crossover_hinge_fits.csv',index=False)
    np.savez_compressed(a.outdir/'transition_crossover_bootstraps.npz',**bs)
    summary={'fits':out.to_dict('records'),'all_change_positive':bool((out.slope_change_after_p027>0).all()),
             'change_ci_positive_count':int((out.change_ci_low>0).sum()),'fit_count':len(out)}
    (a.outdir/'transition_crossover_summary.json').write_text(json.dumps(summary,indent=2))
    print(out.to_string(index=False))
if __name__=='__main__':main()
