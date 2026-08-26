#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, multiprocessing as mp, os, sys, time
from pathlib import Path
from typing import Any

os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('MKL_NUM_THREADS','1')
os.environ.setdefault('NUMEXPR_NUM_THREADS','1')

import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from stabilizer_tableau import (
    load_symplectic_masks,stable_seed_u64,simulate_trajectory_snapshots,
    central_observables,tripartite_information_quarters,window_entropy_features,
    paired_single_measurement_interventions,
)

_MASKS=None

def _init_worker(maps_path:str):
    global _MASKS
    _MASKS=load_symplectic_masks(maps_path)
    n=8;steps=np.array([2],dtype=np.int64)
    snaps,*_=simulate_trajectory_snapshots(n,.1,steps,_MASKS,stable_seed_u64('warmup',os.getpid()),0)
    central_observables(snaps[0],n)


def _worker(task:tuple[Any,...]):
    (run_label,protocol,n,p,tr,probe_taus,base_seed,half_widths,distances,
     do_tmi,do_interventions)=task
    protocol_code=0 if protocol=='z_projective' else 1
    seed=stable_seed_u64('checkpoint05',run_label,base_seed,protocol,n,p,tr)
    probe_steps=np.asarray([int(round(t*n)) for t in probe_taus],dtype=np.int64)
    snaps,meas,random_meas,cut_meas=simulate_trajectory_snapshots(n,p,probe_steps,_MASKS,seed,protocol_code)
    state_rows=[]; intervention_rows=[]
    trajectory_id=f'{run_label}|{protocol}|n{n}|p{p:.5f}|tr{tr}'
    for j,(tau,snap) in enumerate(zip(probe_taus,snaps)):
        c=central_observables(snap,n)
        wfeat=window_entropy_features(snap,n,np.asarray(half_widths,dtype=np.int64))
        row={
            'run_label':run_label,'protocol':protocol,'n':n,'p_measure':p,
            'trajectory_index':tr,'trajectory_id':trajectory_id,'tau':float(tau),
            'cycle':int(probe_steps[j]),'measurements_to_probe':int(meas[j]),
            'random_measurements_to_probe':int(random_meas[j]),
            'cut_measurements_to_probe':int(cut_meas[j]),
            'S_left_neighbor':int(round(c[0])),'S_central':int(round(c[1])),
            'S_right_neighbor':int(round(c[2])),'P_central':c[3],
            'P_left_neighbor':c[4],'P_right_neighbor':c[5],
            'chi_linear':c[6],'chi_relative':c[7],
            'delta_left':int(round(c[8])),'delta_right':int(round(c[9])),
            'boundary_code':f'{int(round(c[8])):+d},{int(round(c[9])):+d}',
        }
        for i,h in enumerate(half_widths):
            hh=min(int(h),n//2)
            row[f'window_h{h}_entropy']=int(round(wfeat[i,0]))
            row[f'window_h{h}_local_stabilizers']=int(round(wfeat[i,1]))
            row[f'window_h{h}_left_entropy']=int(round(wfeat[i,2]))
            row[f'window_h{h}_right_entropy']=int(round(wfeat[i,3]))
            row[f'window_h{h}_effective_halfwidth']=hh
        if do_tmi and j==len(probe_taus)-1 and n%4==0:
            tmi=tripartite_information_quarters(snap,n)
            names=['S_A','S_B','S_C','S_AB','S_AC','S_BC','S_ABC','I3_quarters']
            row.update({k:float(v) for k,v in zip(names,tmi)})
        else:
            for k in ['S_A','S_B','S_C','S_AB','S_AC','S_BC','S_ABC','I3_quarters']:
                row[k]=np.nan
        state_rows.append(row)
        if do_interventions and j==len(probe_taus)-1:
            axes=[2] if protocol=='z_projective' else [0,1,2]
            for axis in axes:
                ints=paired_single_measurement_interventions(snap,n,np.asarray(distances,dtype=np.int64),axis)
                for x in ints:
                    if not np.isfinite(x[2]):
                        continue
                    intervention_rows.append({
                        'run_label':run_label,'protocol':protocol,'n':n,'p_measure':p,
                        'trajectory_index':tr,'trajectory_id':trajectory_id,'tau':float(tau),
                        'axis':int(axis),'distance':int(x[0]),'side':int(x[1]),
                        'measurement_random':int(x[2]),'delta_S_central':int(round(x[3])),
                        'delta_chi_linear':float(x[4]),'delta_chi_relative':float(x[5]),
                        'post_S_central':int(round(x[6])),'post_delta_left':int(round(x[7])),
                        'post_delta_right':int(round(x[8])),
                    })
    return state_rows,intervention_rows


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--outdir',type=Path,required=True)
    ap.add_argument('--maps',type=Path,required=True)
    ap.add_argument('--run-label',required=True)
    ap.add_argument('--protocols',nargs='+',default=['z_projective'])
    ap.add_argument('--sizes',type=int,nargs='+',required=True)
    ap.add_argument('--p-values',type=float,nargs='+',required=True)
    ap.add_argument('--trajectories',type=int,required=True)
    ap.add_argument('--probe-taus',type=float,nargs='+',default=[4.,6.,8.])
    ap.add_argument('--base-seed',type=int,required=True)
    ap.add_argument('--half-widths',type=int,nargs='+',default=[1,2,4,8,16,32])
    ap.add_argument('--intervention-distances',type=int,nargs='+',default=[0,1,2,4,8,16,32])
    ap.add_argument('--tmi',action='store_true')
    ap.add_argument('--interventions',action='store_true')
    ap.add_argument('--workers',type=int,default=5)
    ap.add_argument('--chunksize',type=int,default=4)
    args=ap.parse_args()
    args.outdir.mkdir(parents=True,exist_ok=True)
    tasks=[(args.run_label,protocol,n,p,tr,tuple(args.probe_taus),args.base_seed,
            tuple(args.half_widths),tuple(args.intervention_distances),args.tmi,args.interventions)
           for protocol in args.protocols for n in args.sizes for p in args.p_values
           for tr in range(args.trajectories)]
    start=time.time();states=[];interventions=[]
    ctx=mp.get_context('fork')
    with ctx.Pool(processes=args.workers,initializer=_init_worker,initargs=(str(args.maps.resolve()),)) as pool:
        for i,(a,b) in enumerate(pool.imap_unordered(_worker,tasks,chunksize=args.chunksize),1):
            states.extend(a);interventions.extend(b)
            if i%max(1,len(tasks)//20)==0 or i==len(tasks):
                print(f'[{args.run_label}] {i}/{len(tasks)} trajectories in {time.time()-start:.1f}s',flush=True)
    sdf=pd.DataFrame(states).sort_values(['protocol','n','p_measure','trajectory_index','tau'])
    sdf.to_csv(args.outdir/'stabilizer_scaling_states.csv.gz',index=False,compression='gzip')
    if interventions:
        idf=pd.DataFrame(interventions).sort_values(['protocol','n','p_measure','trajectory_index','axis','distance','side'])
        idf.to_csv(args.outdir/'paired_measurement_interventions.csv.gz',index=False,compression='gzip')
    else:idf=pd.DataFrame()
    manifest={
        'run_label':args.run_label,'protocols':args.protocols,'sizes':args.sizes,
        'p_values':args.p_values,'trajectories_per_cell':args.trajectories,
        'probe_taus':args.probe_taus,'base_seed':args.base_seed,
        'half_widths':args.half_widths,'intervention_distances':args.intervention_distances,
        'tmi':args.tmi,'interventions':args.interventions,'state_rows':len(sdf),
        'intervention_rows':len(idf),'trajectory_count':len(tasks),
        'elapsed_seconds':time.time()-start,
        'maps_sha256':hashlib.sha256(args.maps.read_bytes()).hexdigest(),
        'simulator':'phase-free bit-packed binary stabilizer tableau',
        'matching_principle':'fixed (n,tau,S_central) exactly fixes the full flat stabilizer Schmidt spectrum',
    }
    (args.outdir/'simulation_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':main()
