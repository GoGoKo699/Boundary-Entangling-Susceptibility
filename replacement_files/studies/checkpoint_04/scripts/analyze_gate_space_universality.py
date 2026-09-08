#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib
from pathlib import Path
import numpy as np
import pandas as pd

PAIRS=[(0.08,0.16),(0.16,0.24),(0.08,0.24)]

def stable_seed(*items):
 return int.from_bytes(hashlib.blake2b(repr(items).encode(),digest_size=8).digest(),'little') & 0xFFFFFFFF

def trajectory_arrays(df,p,taus):
 out={}
 for n,g in df[np.isclose(df.p_measure,p)].groupby('n'):
  ids=sorted(g.trajectory_index.unique())
  arr=np.full((len(ids),len(taus),2),np.nan)
  for i,tr in enumerate(ids):
   h=g[g.trajectory_index==tr].set_index('tau')
   for j,tau in enumerate(taus):
    if tau in h.index:
     row=h.loc[tau]
     if isinstance(row,pd.DataFrame): row=row.iloc[0]
     arr[i,j,0]=row.P_L+row.P_R
     arr[i,j,1]=row.P_Lb
  out[int(n)]=arr
 return out

def observed(df,lo,hi):
 means=df.assign(A=df.P_L+df.P_R,B=df.P_Lb).groupby(['n','tau','p_measure'])[['A','B']].mean()
 cells=[]
 for (n,tau),g in means.groupby(level=[0,1]):
  try: l=g.xs(lo,level='p_measure').iloc[0]; h=g.xs(hi,level='p_measure').iloc[0]
  except Exception: continue
  A=h.A-l.A; B=h.B-l.B; cells.append((n,tau,A,B,4*A-5*B))
 c=pd.DataFrame(cells,columns=['n','tau','A','B','margin'])
 return c[['A','B','margin']].mean().to_dict(),c

def bootstrap(df,lo,hi,reps,seed):
 obs,cells=observed(df,lo,hi); taus=sorted(df.tau.unique()); L=trajectory_arrays(df,lo,taus); H=trajectory_arrays(df,hi,taus)
 rng=np.random.default_rng(seed); vecs=[]
 for n in sorted(set(L)&set(H)):
  l,h=L[n],H[n]; il=rng.integers(0,len(l),size=(reps,len(l))); ih=rng.integers(0,len(h),size=(reps,len(h)))
  ml=np.nanmean(l[il],axis=1); mh=np.nanmean(h[ih],axis=1); diff=mh-ml
  valid=set(cells[cells.n==n].tau)
  for j,tau in enumerate(taus):
   if tau in valid: vecs.append(diff[:,j,:])
 arr=np.stack(vecs,axis=1); mean=np.nanmean(arr,axis=1); A=mean[:,0]; B=mean[:,1]; M=4*A-5*B
 return {
  'delta_neighbor_sum':obs['A'],'delta_noncontiguous':obs['B'],'gate_space_margin':obs['margin'],
  'neighbor_ci_low':float(np.quantile(A,.025)),'neighbor_ci_high':float(np.quantile(A,.975)),
  'noncontig_ci_low':float(np.quantile(B,.025)),'noncontig_ci_high':float(np.quantile(B,.975)),
  'margin_ci_low':float(np.quantile(M,.025)),'margin_ci_high':float(np.quantile(M,.975)),
  'cell_count':len(cells),'negative_margin_cell_count':int((cells.margin<0).sum()),
  'all_local_dressed_gates_suppressed':bool(np.quantile(B,.025)>0 and np.quantile(M,.025)>0),
 }

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--full-run',type=Path,required=True)
 ap.add_argument('--rank2-run',type=Path,required=True)
 ap.add_argument('--replication-run',type=Path,required=True)
 ap.add_argument('--out',type=Path,required=True)
 ap.add_argument('--reps',type=int,default=4000)
 args=ap.parse_args()
 runs={
  'primary_rank4':(args.full_run/'state_response_rows.csv.gz','equalized_rank4'),
  'independent_rank4':(args.replication_run/'state_response_rows.csv.gz','equalized_rank4'),
  'posthoc_rank2':(args.rank2_run/'state_response_rows.csv.gz','equalized_rank2'),
 }
 rows=[]
 for run,(path,var) in runs.items():
  d=pd.read_csv(path);d=d[(d.split=='confirmatory')&(d.variant==var)].copy()
  for family,g in d.groupby('family'):
   for lo,hi in PAIRS:
    r=bootstrap(g,lo,hi,args.reps,stable_seed(run,family,lo,hi));rows.append({'run':run,'family':family,'pair_label':f'{lo:.2f}-{hi:.2f}',**r})
 out=pd.DataFrame(rows);args.out.parent.mkdir(parents=True,exist_ok=True);out.to_csv(args.out,index=False)
 print(out.to_string(index=False))
if __name__=='__main__':main()
