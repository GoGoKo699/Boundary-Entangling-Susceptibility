#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import pandas as pd

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from cross_architecture_simulation import main_worker, run_parallel, FAMILIES


def load_refs(path:Path):
    raw=json.loads(path.read_text())
    refs={}
    for key,val in raw.items():
        fam,npart,tpart=key.split('|')
        n=int(npart[1:]); tau=float(tpart[3:])
        refs[(fam,n,tau)]=val
    return refs


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--reference-json',type=Path,required=True); ap.add_argument('--outdir',type=Path,required=True); ap.add_argument('--families',nargs='+',default=list(FAMILIES)); ap.add_argument('--sizes',type=int,nargs='+',default=[10,12,14]); ap.add_argument('--p-values',type=float,nargs='+',default=[.08,.16,.24]); ap.add_argument('--trajectories',type=int,default=12); ap.add_argument('--probe-taus',type=float,nargs='+',default=[6.,8.]); ap.add_argument('--workers',type=int,default=4); ap.add_argument('--base-seed',type=int,default=2026081805); args=ap.parse_args()
    args.outdir.mkdir(parents=True,exist_ok=True)
    refs=load_refs(args.reference_json); taus=tuple(args.probe_taus)
    tasks=[(fam,n,p,tr,taus,args.base_seed,0,refs) for fam in args.families for n in args.sizes for p in args.p_values for tr in range(args.trajectories)]
    outputs=run_parallel(tasks,main_worker,args.workers,20,'independent-seed')
    rows=[r for part,_ in outputs for r in part]
    df=pd.DataFrame(rows).sort_values(['family','n','p_measure','trajectory_index','tau','variant'])
    df.to_csv(args.outdir/'replication_state_response_rows.csv.gz',index=False,compression='gzip')
    manifest={'families':args.families,'sizes':args.sizes,'p_values':args.p_values,'trajectories_per_cell':args.trajectories,'probe_taus':list(taus),'base_seed':args.base_seed,'reference_spectra_source':str(args.reference_json),'state_rows':len(df),'all_rows_labeled_confirmatory':bool((df.split=='confirmatory').all())}
    (args.outdir/'replication_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))
if __name__=='__main__': main()
