#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd


def fit_model(s:pd.DataFrame,boot:dict[int,np.ndarray],kind:str,min_n:int=0):
    s=s[s.n>=min_n].sort_values('n').copy();n=s.n.to_numpy(float);y=s.beta.to_numpy(float)
    se=(s.ci_high-s.ci_low).to_numpy(float)/(2*1.96);se=np.maximum(se,1e-12);w=1/se**2
    if kind=='constant': X=np.ones((len(n),1)); label='beta_n = beta_infinity'
    elif kind.startswith('power_'):
        omega=float(kind.split('_')[1]);X=np.column_stack([np.ones(len(n)),n**(-omega)]);label=f'beta_n = beta_infinity + a/n^{omega:g}'
    else: raise ValueError(kind)
    coef=np.linalg.lstsq(X*np.sqrt(w)[:,None],y*np.sqrt(w),rcond=None)[0]
    beta_inf=float(coef[0]);pred=X@coef
    chi2=float(np.sum(w*(y-pred)**2));dof=max(0,len(y)-len(coef))
    B=min(len(boot[int(nn)]) for nn in n);bb=np.empty(B)
    for b in range(B):
        yb=np.array([boot[int(nn)][b] for nn in n])
        bb[b]=np.linalg.lstsq(X*np.sqrt(w)[:,None],yb*np.sqrt(w),rcond=None)[0][0]
    lo,hi=np.quantile(bb,[.025,.975])
    return {'model':label,'min_n':int(min_n),'sizes':','.join(map(str,s.n.astype(int))),
            'beta_infinity':beta_inf,'ci_low':float(lo),'ci_high':float(hi),
            'weighted_chi2':chi2,'dof':dof,'bootstrap':B}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--outdir',type=Path,required=True)
    a=ap.parse_args();a.outdir.mkdir(parents=True,exist_ok=True)
    rows=[];repro=[]
    all_sizes={}
    for run in ['primary','replication']:
        d=pd.read_csv(a.root/'analysis'/run/'fixed_spectrum_size_slopes.csv')
        npz=np.load(a.root/'analysis'/run/'bootstrap_primary_slopes.npz')
        all_sizes[run]=d
        for (prot,outcome),s in d.groupby(['protocol','outcome']):
            boot={int(n):npz[f'{prot}_n{int(n)}_{outcome}'] for n in s.n}
            specs=[('power_1',0),('power_0.5',0),('power_2',0),('power_1',64),('constant',128)]
            for kind,min_n in specs:
                r=fit_model(s,boot,kind,min_n);r.update(run=run,protocol=prot,outcome=outcome);rows.append(r)
    out=pd.DataFrame(rows);out.to_csv(a.outdir/'finite_size_model_sensitivity.csv',index=False)
    p=all_sizes['primary'];r=all_sizes['replication']
    m=p.merge(r,on=['protocol','n','outcome'],suffixes=('_primary','_replication'))
    m['difference']=m.beta_replication-m.beta_primary
    m['combined_se']=np.sqrt(m.cluster_se_primary**2+m.cluster_se_replication**2)
    m['z_difference']=m.difference/m.combined_se
    m.to_csv(a.outdir/'cross_run_reproducibility.csv',index=False)
    summary={
      'primary_z_relative_predeclared':out[(out.run=='primary')&(out.protocol=='z_projective')&(out.outcome=='chi_relative')&(out.model=='beta_n = beta_infinity + a/n^1')&(out.min_n==0)].to_dict('records'),
      'replication_z_relative_predeclared':out[(out.run=='replication')&(out.protocol=='z_projective')&(out.outcome=='chi_relative')&(out.model=='beta_n = beta_infinity + a/n^1')&(out.min_n==0)].to_dict('records'),
      'max_abs_cross_run_z':float(m.z_difference.abs().max()),
    }
    (a.outdir/'finite_size_sensitivity_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
