#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def seed32(*x):
    return int.from_bytes(hashlib.blake2b(repr(x).encode(),digest_size=8).digest(),'little') & 0xffffffff


def summarize_trajectory_distance(df:pd.DataFrame, conditional:bool)->pd.DataFrame:
    x=df[df.delta_S_central.eq(0)].copy() if conditional else df.copy()
    return (x.groupby(['n','p_measure','trajectory_id','distance'],observed=True)
             .agg(delta_chi_relative=('delta_chi_relative','mean'),
                  delta_chi_linear=('delta_chi_linear','mean'),
                  sides=('side','size'))
             .reset_index())


def paired_table(df:pd.DataFrame, conditional:bool)->pd.DataFrame:
    td=summarize_trajectory_distance(df,conditional)
    out=[]
    for (n,p),g in td.groupby(['n','p_measure'],observed=True):
        near=g[g.distance.eq(0)][['trajectory_id','delta_chi_relative','delta_chi_linear']].rename(
            columns={'delta_chi_relative':'near_relative','delta_chi_linear':'near_linear'})
        far=(g[g.distance.ge(n/4)].groupby('trajectory_id',observed=True)
             [['delta_chi_relative','delta_chi_linear']].mean().reset_index().rename(
                 columns={'delta_chi_relative':'far_relative','delta_chi_linear':'far_linear'}))
        m=near.merge(far,on='trajectory_id',how='inner')
        m['D_relative']=m.near_relative-m.far_relative
        m['D_linear']=m.near_linear-m.far_linear
        m['n']=n;m['p_measure']=p;m['conditional_fixed_spectrum']=conditional
        out.append(m)
    return pd.concat(out,ignore_index=True)


def boot_mean(v,rng,B):
    v=np.asarray(v,float); n=len(v)
    if n==0:return np.nan,np.nan,np.nan,np.array([])
    bs=np.empty(B,float)
    for b in range(B):bs[b]=np.mean(v[rng.integers(0,n,n)])
    return float(np.mean(v)),float(np.quantile(bs,.025)),float(np.quantile(bs,.975)),bs


def cell_and_pooled(paired:pd.DataFrame,B:int,seed:int):
    rows=[];boots={}
    for cond in sorted(paired.conditional_fixed_spectrum.unique()):
      d=paired[paired.conditional_fixed_spectrum.eq(cond)]
      for outcome in ['D_relative','D_linear']:
        cell_bs=[]
        for (n,p),g in d.groupby(['n','p_measure'],observed=True):
            est,lo,hi,bs=boot_mean(g[outcome].to_numpy(),np.random.default_rng(seed32(seed,cond,outcome,n,p)),B)
            rows.append({'scope':'cell','conditional_fixed_spectrum':cond,'outcome':outcome,'n':n,'p_measure':p,
                         'estimate':est,'ci_low':lo,'ci_high':hi,'trajectories':len(g),'bootstrap':B})
            cell_bs.append(bs)
        bmat=np.stack(cell_bs)
        pooled=bmat.mean(axis=0)
        cellmeans=[g[outcome].mean() for _,g in d.groupby(['n','p_measure'],observed=True)]
        rows.append({'scope':'equal_cell_pooled','conditional_fixed_spectrum':cond,'outcome':outcome,'n':np.nan,'p_measure':np.nan,
                     'estimate':float(np.mean(cellmeans)),'ci_low':float(np.quantile(pooled,.025)),
                     'ci_high':float(np.quantile(pooled,.975)),'trajectories':len(d),'bootstrap':B})
        boots[(cond,outcome)]=pooled
    return pd.DataFrame(rows),boots


def distance_summary(df:pd.DataFrame,B:int,seed:int):
    rows=[]
    for cond in [False,True]:
      td=summarize_trajectory_distance(df,cond)
      for (n,p,d),g in td.groupby(['n','p_measure','distance'],observed=True):
        for outcome in ['delta_chi_relative','delta_chi_linear']:
          est,lo,hi,bs=boot_mean(g[outcome].to_numpy(),np.random.default_rng(seed32(seed,cond,n,p,d,outcome)),B)
          rows.append({'conditional_fixed_spectrum':cond,'n':n,'p_measure':p,'distance':d,'outcome':outcome,
                       'estimate':est,'ci_low':lo,'ci_high':hi,'trajectories':len(g),'bootstrap':B})
    cell=pd.DataFrame(rows)
    pooled=[]
    for (cond,d,outcome),g in cell.groupby(['conditional_fixed_spectrum','distance','outcome'],observed=True):
        pooled.append({'conditional_fixed_spectrum':cond,'distance':d,'outcome':outcome,
                       'estimate':g.estimate.mean(),'ci_low':np.nan,'ci_high':np.nan,
                       'cells':len(g),'min_trajectories':g.trajectories.min()})
    return cell,pd.DataFrame(pooled)


def pooled_distance_bootstrap(df:pd.DataFrame,B:int,seed:int):
    td=summarize_trajectory_distance(df,True)
    cells=[]
    for (n,p),g in td.groupby(['n','p_measure'],observed=True):
        piv=g.pivot(index='trajectory_id',columns='distance',values='delta_chi_relative')
        cells.append((n,p,piv))
    dists=sorted(set.intersection(*[set(x.columns) for _,_,x in cells]))
    est=[]
    for d in dists:
        est.append(np.mean([piv[d].mean(skipna=True) for _,_,piv in cells]))
    est=np.asarray(est,float)
    rng=np.random.default_rng(seed);arr=np.empty((B,len(dists)),float)
    for b in range(B):
        vals=[]
        for _,_,piv in cells:
            ids=np.arange(len(piv));draw=rng.integers(0,len(ids),len(ids));s=piv.iloc[draw]
            vals.append([s[d].mean(skipna=True) for d in dists])
        arr[b]=np.nanmean(np.asarray(vals,float),axis=0)
    lo=np.nanquantile(arr,.025,axis=0);hi=np.nanquantile(arr,.975,axis=0)
    out=pd.DataFrame({'distance':dists,'estimate':est,'ci_low':lo,'ci_high':hi,'bootstrap':B,'cells':len(cells)})
    return out,arr


def fit_decay(d,y):
    d=np.asarray(d,float);y=np.asarray(y,float)
    use=(d<=16)&np.isfinite(y)&(y<0)
    def f(x,A,xi):return -A*np.exp(-x/xi)
    try:
        popt,_=curve_fit(f,d[use],y[use],p0=(max(1e-4,-y[use][0]),1.5),bounds=([0,.05],[1,100]),maxfev=100000)
        return np.array([popt[0],popt[1],0.0])
    except Exception:return np.array([np.nan,np.nan,0.0])


def collapse_summary(df:pd.DataFrame):
    x=df.copy();x['central_rank_reduced']=x.delta_S_central.eq(-1)
    return (x.groupby(['n','p_measure','distance'],observed=True)
             .agg(probability_rank_reduced=('central_rank_reduced','mean'),interventions=('central_rank_reduced','size'))
             .reset_index())


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--interventions',type=Path,required=True);ap.add_argument('--outdir',type=Path,required=True)
    ap.add_argument('--bootstrap',type=int,default=5000);ap.add_argument('--seed',type=int,default=2026082509)
    a=ap.parse_args();a.outdir.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(a.interventions)
    paired=pd.concat([paired_table(df,False),paired_table(df,True)],ignore_index=True)
    paired.to_csv(a.outdir/'paired_trajectory_endpoints.csv.gz',index=False,compression='gzip')
    summ,boots=cell_and_pooled(paired,a.bootstrap,a.seed);summ.to_csv(a.outdir/'paired_near_far_effects.csv',index=False)
    cell,pooled=distance_summary(df,max(1000,a.bootstrap//2),a.seed);cell.to_csv(a.outdir/'distance_effects_by_cell.csv',index=False)
    pooled_boot,arr=pooled_distance_bootstrap(df,a.bootstrap,seed32(a.seed,'distance'))
    popt=fit_decay(pooled_boot.distance,pooled_boot.estimate)
    xis=[]
    for b in range(a.bootstrap):
        q=fit_decay(pooled_boot.distance,arr[b]);xis.append(q[1])
    vv=np.asarray(xis,float);vv=vv[np.isfinite(vv)&(vv<100)]
    decay={'amplitude':float(popt[0]),'decay_length':float(popt[1]),'offset':float(popt[2]),
           'ci_low':float(np.quantile(vv,.025)),'ci_high':float(np.quantile(vv,.975)),
           'bootstrap_valid':int(len(vv)),'model':'-A exp(-d/xi)','fit_distances':'0,1,2,4,8,16'}
    pooled_boot.to_csv(a.outdir/'fixed_spectrum_distance_decay.csv',index=False)
    (a.outdir/'fixed_spectrum_distance_decay_fit.json').write_text(json.dumps(decay,indent=2))
    collapse=collapse_summary(df);collapse.to_csv(a.outdir/'central_rank_reduction_probability.csv',index=False)
    np.savez_compressed(a.outdir/'intervention_bootstraps.npz',**{f'conditional_{k[0]}_{k[1]}':v for k,v in boots.items()},distance=arr)
    primary=summ[(summ.scope=='equal_cell_pooled')&(summ.conditional_fixed_spectrum==True)&(summ.outcome=='D_relative')].iloc[0]
    unconditional=summ[(summ.scope=='equal_cell_pooled')&(summ.conditional_fixed_spectrum==False)&(summ.outcome=='D_relative')].iloc[0]
    report={'rows':len(df),'trajectories':df.trajectory_id.nunique(),'primary_fixed_spectrum_near_minus_far':primary.to_dict(),
            'secondary_unconditional_near_minus_far':unconditional.to_dict(),'fixed_spectrum_decay':decay}
    (a.outdir/'analysis_summary.json').write_text(json.dumps(report,indent=2,default=lambda z:float(z) if hasattr(z,'item') else str(z)))
    print(json.dumps(report,indent=2,default=lambda z:float(z) if hasattr(z,'item') else str(z)))
if __name__=='__main__':main()
