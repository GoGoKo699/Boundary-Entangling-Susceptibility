#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
from typing import Any
import numpy as np
import pandas as pd
import statsmodels.api as sm


def stable_seed(*items:object)->int:
    raw=repr(items).encode();return int.from_bytes(hashlib.blake2b(raw,digest_size=8).digest(),'little')&0xffffffff


def prepare_fe(df:pd.DataFrame,outcome:str,p_center:float=.26,p_step:float=.02,min_per_p:int=10,min_levels:int=3):
    x=df.copy()
    counts=x.groupby(['tau','S_central','p_measure'],observed=True).size().rename('count').reset_index()
    good=counts[counts['count']>=min_per_p].copy()
    levels=good.groupby(['tau','S_central'],observed=True)['p_measure'].nunique()
    valid=set(levels[levels>=min_levels].index.tolist())
    good=good[good.apply(lambda r:(r.tau,r.S_central) in valid,axis=1)]
    keep=good[['tau','S_central','p_measure']].assign(_keep=1)
    x=x.merge(keep,on=['tau','S_central','p_measure'],how='inner')
    x=x[np.isfinite(x[outcome])].copy()
    x['group_code']=pd.factorize(list(zip(x.tau,x.S_central)),sort=True)[0]
    x['cluster_code']=pd.factorize(x.trajectory_id,sort=True)[0]
    x['x']=(x.p_measure-p_center)/p_step
    return x.drop(columns=['_keep']),good


def weighted_fe_beta(group:np.ndarray,x:np.ndarray,y:np.ndarray,w:np.ndarray|None=None)->float:
    if w is None:w=np.ones(len(y),float)
    ng=int(group.max())+1 if len(group) else 0
    sw=np.bincount(group,weights=w,minlength=ng)
    sx=np.bincount(group,weights=w*x,minlength=ng)
    sy=np.bincount(group,weights=w*y,minlength=ng)
    sxy=np.bincount(group,weights=w*x*y,minlength=ng)
    sx2=np.bincount(group,weights=w*x*x,minlength=ng)
    ok=sw>0
    num=np.sum(sxy[ok]-sx[ok]*sy[ok]/sw[ok])
    den=np.sum(sx2[ok]-sx[ok]*sx[ok]/sw[ok])
    return float(num/den) if den>1e-15 else np.nan


def fe_fit(df:pd.DataFrame,outcome:str,bootstrap:int,seed:int,p_center:float=.26,p_step:float=.02,min_per_p:int=10,min_levels:int=3):
    x,good=prepare_fe(df,outcome,p_center,p_step,min_per_p,min_levels)
    g=x.group_code.to_numpy(int);xx=x.x.to_numpy(float);yy=x[outcome].to_numpy(float)
    beta=weighted_fe_beta(g,xx,yy)
    gx=pd.Series(xx).groupby(g).transform('mean').to_numpy();gy=pd.Series(yy).groupby(g).transform('mean').to_numpy()
    xr=xx-gx;yr=yy-gy
    fit=sm.OLS(yr,xr[:,None]).fit(cov_type='cluster',cov_kwds={'groups':x.cluster_code.to_numpy(int),'use_correction':True})
    se=float(fit.bse[0])
    clusters=x[['cluster_code','p_measure']].drop_duplicates().sort_values('cluster_code')
    C=int(x.cluster_code.max())+1
    p_to_clusters={p:sub.cluster_code.to_numpy(int) for p,sub in clusters.groupby('p_measure')}
    row_cluster=x.cluster_code.to_numpy(int)
    rng=np.random.default_rng(seed);boots=np.empty(bootstrap,float)
    for b in range(bootstrap):
        cw=np.zeros(C,dtype=np.int16)
        for p,ids in p_to_clusters.items():
            draw=rng.integers(0,len(ids),size=len(ids))
            cnt=np.bincount(draw,minlength=len(ids)).astype(np.int16)
            cw[ids]=cnt
        boots[b]=weighted_fe_beta(g,xx,yy,cw[row_cluster].astype(float))
    valid=boots[np.isfinite(boots)]
    lo,hi=np.quantile(valid,[.025,.975]) if len(valid) else (np.nan,np.nan)
    result={
        'outcome':outcome,'beta':beta,'cluster_se':se,'ci_low':float(lo),'ci_high':float(hi),
        'rows':int(len(x)),'trajectories':int(x.trajectory_id.nunique()),
        'eligible_strata':int(x[['tau','S_central']].drop_duplicates().shape[0]),
        'eligible_p_stratum_cells':int(len(good)),'min_p':float(x.p_measure.min()),'max_p':float(x.p_measure.max()),
        'bootstrap_valid':int(len(valid)),
    }
    return result,valid,x


def adjacent_fits(df:pd.DataFrame,outcome:str,bootstrap:int,seed:int,min_per_p:int=10):
    ps=sorted(df.p_measure.unique());rows=[];bootmap={}
    for j,(lo,hi) in enumerate(zip(ps[:-1],ps[1:])):
        sub=df[df.p_measure.isin([lo,hi])].copy()
        r,b,_=fe_fit(sub,outcome,bootstrap,stable_seed(seed,outcome,lo,hi),p_center=lo,p_step=hi-lo,min_per_p=min_per_p,min_levels=2)
        r.update({'p_low':lo,'p_high':hi,'delta_p':hi-lo})
        rows.append(r);bootmap[(lo,hi)]=b
    return pd.DataFrame(rows),bootmap


def find_crossing(ps:np.ndarray,diff:np.ndarray,target:float=.26,window=(.235,.295)):
    candidates=[]
    for i in range(len(ps)-1):
        if ps[i]<window[0] or ps[i+1]>window[1]:continue
        a,b=diff[i],diff[i+1]
        if not np.isfinite(a+b):continue
        if a==0: candidates.append(ps[i])
        elif a*b<0 or b==0:
            candidates.append(ps[i]-a*(ps[i+1]-ps[i])/(b-a))
    if not candidates:return np.nan
    return float(min(candidates,key=lambda x:abs(x-target)))


def transition_crossings(df:pd.DataFrame,bootstrap:int,seed:int):
    f=df[(df.tau==df.tau.max()) & df.I3_quarters.notna()].copy()
    rows=[];boot_store={}
    for protocol,pdf in f.groupby('protocol'):
        sizes=sorted(pdf.n.unique());ps=np.array(sorted(pdf.p_measure.unique()),float)
        vals={(n,p):g.I3_quarters.to_numpy(float) for (n,p),g in pdf.groupby(['n','p_measure'])}
        means={(n,p):float(np.mean(vals[(n,p)])) for n in sizes for p in ps}
        rng=np.random.default_rng(stable_seed(seed,protocol,'pc'))
        for n1,n2 in zip(sizes[:-1],sizes[1:]):
            diff=np.array([means[(n2,p)]-means[(n1,p)] for p in ps])
            pc=find_crossing(ps,diff)
            boots=[]
            for _ in range(bootstrap):
                d=[]
                for p in ps:
                    a=vals[(n1,p)];b=vals[(n2,p)]
                    ma=float(np.mean(a[rng.integers(0,len(a),len(a))]));mb=float(np.mean(b[rng.integers(0,len(b),len(b))]))
                    d.append(mb-ma)
                boots.append(find_crossing(ps,np.asarray(d)))
            vv=np.asarray(boots,float);valid=vv[np.isfinite(vv)]
            q=np.quantile(valid,[.025,.975]) if len(valid) else [np.nan,np.nan]
            rows.append({'protocol':protocol,'n_low':n1,'n_high':n2,'p_cross':pc,'ci_low':q[0],'ci_high':q[1],
                         'valid_bootstrap_fraction':len(valid)/bootstrap})
            boot_store[(protocol,n1,n2)]=valid
    return pd.DataFrame(rows),boot_store


def fit_size_limit(size_df:pd.DataFrame,boot_by_n:dict[int,np.ndarray],outcome:str,protocol:str):
    s=size_df.sort_values('n');n=s.n.to_numpy(float);y=s.beta.to_numpy(float)
    se=(s.ci_high-s.ci_low).to_numpy(float)/(2*1.96);se=np.where(se>1e-10,se,1e-10)
    X=np.column_stack([np.ones(len(n)),1/n]);w=1/se**2
    coef=np.linalg.solve(X.T@(w[:,None]*X),X.T@(w*y))
    beta_inf,a=coef
    B=min(len(v) for v in boot_by_n.values());boots=np.empty(B,float)
    for b in range(B):
        yb=np.array([boot_by_n[int(nn)][b] for nn in n])
        boots[b]=np.linalg.solve(X.T@(w[:,None]*X),X.T@(w*yb))[0]
    lo,hi=np.quantile(boots,[.025,.975])
    return {'protocol':protocol,'outcome':outcome,'beta_infinity':float(beta_inf),'a_over_n':float(a),
            'ci_low':float(lo),'ci_high':float(hi),'sizes':','.join(map(str,s.n.astype(int))),
            'model':'beta_n = beta_infinity + a/n','bootstrap_replicates':int(B)},boots


def majority_map(train:pd.DataFrame,keys:list[str],target:str):
    tab=train.groupby(keys+[target],observed=True).size().rename('count').reset_index()
    idx=tab.sort_values('count').groupby(keys,observed=True)['count'].idxmax()
    best=tab.loc[idx,keys+[target,'count']]
    return {tuple(r[k] for k in keys):r[target] for _,r in best.iterrows()}


def mean_map(train:pd.DataFrame,keys:list[str],target:str):
    s=train.groupby(keys,observed=True)[target].mean()
    return {k if isinstance(k,tuple) else (k,):v for k,v in s.items()}


def window_analysis(df:pd.DataFrame,train_cut:int=400):
    rows=[]
    hvals=sorted({int(c.split('_')[1][1:]) for c in df.columns if c.startswith('window_h') and c.endswith('_entropy')})
    for (protocol,n),sub in df.groupby(['protocol','n']):
        train=sub[sub.trajectory_index<train_cut].copy();test=sub[sub.trajectory_index>=train_cut].copy()
        target='boundary_code';global_class=train[target].mode().iloc[0];global_mean=train.chi_relative.mean()
        base_keys=['tau','S_central']
        base_class=majority_map(train,base_keys,target);base_mean=mean_map(train,base_keys,'chi_relative')
        for h in [0]+[x for x in hvals if x<=n//2]:
            keys=base_keys.copy()
            if h>0:
                for hh in hvals:
                    if hh<=h and hh<=n//2:
                        keys += [f'window_h{hh}_entropy',f'window_h{hh}_left_entropy',f'window_h{hh}_right_entropy']
            cmap=majority_map(train,keys,target);mmap=mean_map(train,keys,'chi_relative')
            pred=[];predmean=[];seen=[]
            for _,r in test.iterrows():
                key=tuple(r[k] for k in keys);bk=tuple(r[k] for k in base_keys)
                if key in cmap:
                    pred.append(cmap[key]);predmean.append(mmap[key]);seen.append(1)
                else:
                    pred.append(base_class.get(bk,global_class));predmean.append(base_mean.get(bk,global_mean));seen.append(0)
            acc=float(np.mean(np.asarray(pred)==test[target].to_numpy()))
            residual=test.chi_relative.to_numpy(float)-np.asarray(predmean,float)
            tmp=test.copy();tmp['residual']=residual
            try:
                rr,_,_=fe_fit(tmp,'residual',0,1,min_per_p=5,min_levels=3)
                rb=rr['beta'];rse=rr['cluster_se']
            except Exception:
                rb=rse=np.nan
            rows.append({'protocol':protocol,'n':n,'max_half_width':h,'test_rows':len(test),
                         'signature_seen_fraction':float(np.mean(seen)),'boundary_code_accuracy':acc,
                         'residual_fixed_rank_beta_per_dp02':rb,'residual_cluster_se':rse})
    return pd.DataFrame(rows)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--states',type=Path,required=True);ap.add_argument('--outdir',type=Path,required=True)
    ap.add_argument('--bootstrap',type=int,default=2000);ap.add_argument('--seed',type=int,default=2026082309)
    ap.add_argument('--skip-window',action='store_true');ap.add_argument('--train-cut',type=int,default=400)
    args=ap.parse_args();args.outdir.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(args.states)
    size_rows=[];boot_primary={}
    adjacent_all=[]
    for (protocol,n),sub in df.groupby(['protocol','n']):
        for outcome in ['chi_relative','chi_linear']:
            r,b,_=fe_fit(sub,outcome,args.bootstrap,stable_seed(args.seed,protocol,n,outcome))
            r.update({'protocol':protocol,'n':n});size_rows.append(r);boot_primary[(protocol,n,outcome)]=b
            adj,_=adjacent_fits(sub,outcome,max(500,args.bootstrap//2),stable_seed(args.seed,'adj',protocol,n,outcome))
            adj.insert(0,'n',n);adj.insert(0,'protocol',protocol);adjacent_all.append(adj)
    size_df=pd.DataFrame(size_rows);size_df.to_csv(args.outdir/'fixed_spectrum_size_slopes.csv',index=False)
    adj_df=pd.concat(adjacent_all,ignore_index=True);adj_df.to_csv(args.outdir/'fixed_spectrum_adjacent_contrasts.csv',index=False)
    limits=[];limit_boot={}
    for protocol in sorted(df.protocol.unique()):
        for outcome in ['chi_relative','chi_linear']:
            s=size_df[(size_df.protocol==protocol)&(size_df.outcome==outcome)]
            bb={int(n):boot_primary[(protocol,int(n),outcome)] for n in s.n}
            r,b=fit_size_limit(s,bb,outcome,protocol);limits.append(r);limit_boot[(protocol,outcome)]=b
    limit_df=pd.DataFrame(limits);limit_df.to_csv(args.outdir/'thermodynamic_limit_fits.csv',index=False)
    pc,pcboot=transition_crossings(df,args.bootstrap,args.seed);pc.to_csv(args.outdir/'independent_I3_crossings.csv',index=False)
    win=(pd.DataFrame() if args.skip_window else window_analysis(df,args.train_cut));win.to_csv(args.outdir/'window_entropy_reconstruction.csv',index=False)
    means=df.groupby(['protocol','n','p_measure','tau'],observed=True).agg(
        S_central_mean=('S_central','mean'),S_central_sd=('S_central','std'),
        chi_relative_mean=('chi_relative','mean'),chi_linear_mean=('chi_linear','mean'),
        I3_mean=('I3_quarters','mean'),rows=('trajectory_id','size')).reset_index()
    means.to_csv(args.outdir/'descriptive_means.csv',index=False)
    support=df.groupby(['protocol','n','tau','S_central','p_measure'],observed=True).size().rename('count').reset_index()
    support.to_csv(args.outdir/'exact_rank_support.csv.gz',index=False,compression='gzip')
    np.savez_compressed(args.outdir/'bootstrap_primary_slopes.npz',**{f'{k[0]}_n{k[1]}_{k[2]}':v for k,v in boot_primary.items()},
                        **{f'limit_{k[0]}_{k[1]}':v for k,v in limit_boot.items()})
    summary={'state_rows':len(df),'trajectory_count':df.trajectory_id.nunique(),'bootstrap':args.bootstrap,
             'primary_limit':limit_df[(limit_df.protocol=='z_projective')&(limit_df.outcome=='chi_relative')].to_dict('records')[0],
             'transition_crossings':pc.to_dict('records')}
    (args.outdir/'analysis_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
