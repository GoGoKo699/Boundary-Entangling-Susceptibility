#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np,pandas as pd,statsmodels.api as sm
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from analyze_checkpoint05 import prepare_fe,weighted_fe_beta


def indicator_fit(x:pd.DataFrame,code:str):
    g=x.group_code.to_numpy(int);xx=x.x.to_numpy(float);yy=(x.boundary_code==code).to_numpy(float)
    b=weighted_fe_beta(g,xx,yy)
    gx=pd.Series(xx).groupby(g).transform('mean').to_numpy();gy=pd.Series(yy).groupby(g).transform('mean').to_numpy()
    fit=sm.OLS(yy-gy,(xx-gx)[:,None]).fit(cov_type='cluster',cov_kwds={'groups':x.cluster_code.to_numpy(int),'use_correction':True})
    se=float(fit.bse[0])
    return b,se

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--outdir',type=Path,required=True)
    a=ap.parse_args();a.outdir.mkdir(parents=True,exist_ok=True)
    rows=[]
    for run,rel in [('primary','data/primary_scaling/stabilizer_scaling_states.csv.gz'),('replication','data/independent_replication/stabilizer_scaling_states.csv.gz')]:
      df=pd.read_csv(a.root/rel)
      for (prot,n),sub in df.groupby(['protocol','n'],observed=True):
        x,_=prepare_fe(sub,'chi_relative')
        direct=weighted_fe_beta(x.group_code.to_numpy(int),x.x.to_numpy(float),x.chi_relative.to_numpy(float))
        for code in sorted(x.boundary_code.unique()):
            b,se=indicator_fit(x,code);val=float(x.loc[x.boundary_code.eq(code),'chi_relative'].iloc[0])
            rows.append({'run':run,'protocol':prot,'n':n,'boundary_code':code,
                         'probability_slope_per_dp02':b,'cluster_se':se,
                         'ci_low':b-1.96*se,'ci_high':b+1.96*se,
                         'chi_relative_value':val,'susceptibility_contribution':b*val,
                         'direct_total_beta':direct,'rows':len(x)})
    out=pd.DataFrame(rows);out.to_csv(a.outdir/'boundary_code_decomposition.csv',index=False)
    checks=(out.groupby(['run','protocol','n']).agg(sum_probability_slope=('probability_slope_per_dp02','sum'),
         sum_contribution=('susceptibility_contribution','sum'),direct_beta=('direct_total_beta','first')).reset_index())
    checks['reconstruction_error']=checks.sum_contribution-checks.direct_beta
    checks.to_csv(a.outdir/'boundary_code_decomposition_checks.csv',index=False)
    main=out[(out.run=='primary')&(out.n==256)].copy()
    summary={'max_probability_conservation_error':float(checks.sum_probability_slope.abs().max()),
             'max_susceptibility_reconstruction_error':float(checks.reconstruction_error.abs().max()),
             'primary_n256':main[['protocol','boundary_code','probability_slope_per_dp02','susceptibility_contribution']].to_dict('records')}
    (a.outdir/'boundary_code_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps({k:v for k,v in summary.items() if k!='primary_n256'},indent=2))
if __name__=='__main__':main()
