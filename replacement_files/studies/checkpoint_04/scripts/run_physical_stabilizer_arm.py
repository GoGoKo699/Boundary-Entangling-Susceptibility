#!/usr/bin/env python3
"""Checkpoint 04 physically reachable exact-spectrum matching arm.

Uniform two-qubit Clifford dynamics, stabilizer-product initial states, and
projective Pauli measurements keep every trajectory state stabilizer.  Across a
bipartition, a stabilizer state has a perfectly flat nonzero Schmidt spectrum.
Conditioning on the Schmidt rank therefore matches the *entire* central
spectrum exactly without constructing counterfactual states.
"""
from __future__ import annotations

import argparse, multiprocessing as mp, hashlib, json, math, os, time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
os.environ['NUMEXPR_NUM_THREADS']='1'

import numpy as np
import pandas as pd

from cp04_common import (
    stable_seed,evolve_probe_states,schmidt_decomposition,spectrum_metrics,
    purity_stencil,response_haar_linear,response_xx_twirl_linear,
    load_clifford_gates,apply_adjacent_2q_inplace,subset_purity,
)


def gate_bank(clifford_path:str,n:int,tau:float,count:int,base_seed:int):
    gates=load_clifford_gates(clifford_path)
    rng=np.random.default_rng(stable_seed('checkpoint04_physical_gatebank',base_seed,n,tau))
    idx=rng.integers(0,len(gates),size=count)
    return gates[idx]


def finite_bank_response(psi,n,gates,pre_purity):
    d=1<<(n//2);q=n//2-1
    vals=[]
    for gate in gates:
        out=psi.copy();apply_adjacent_2q_inplace(out,gate,q)
        post=subset_purity(out,n,range(0,n//2))
        vals.append(d/(d-1.0)*(pre_purity-post))
    vals=np.asarray(vals,float);h=len(vals)//2
    return {
        'finite_clifford_mean_delta_linear':float(vals.mean()),
        'finite_clifford_sd_delta_linear':float(vals.std(ddof=1)),
        'finite_clifford_half1_delta_linear':float(vals[:h].mean()),
        'finite_clifford_half2_delta_linear':float(vals[h:].mean()),
    }


def worker(task:tuple[Any,...]):
    n,p,tr,probe,base_seed,split_cut,meas,clifford_path,gate_count=task
    split='discovery' if tr<split_cut else 'confirmatory'
    tid=f'{meas}|n{n}|p{p:.5f}|tr{tr}'
    rows=[]
    states=evolve_probe_states(
        n=n,p=p,trajectory_index=tr,probe_taus=probe,base_seed=base_seed,
        dynamics_gate='clifford',measurement_protocol=meas,
        clifford_path=clifford_path,initial_state='stabilizer_product',
    )
    for tau,psi,mcount,ccount in states:
        _,lam,_=schmidt_decomposition(psi,n)
        metrics=spectrum_metrics(lam)
        active=lam[lam>1e-10];rank=len(active)
        if rank<1: raise RuntimeError('zero rank')
        flat_target=1.0/rank
        flat_err=max(float(np.max(np.abs(active-flat_target))),float(np.max(np.abs(lam[rank:]))) if rank<len(lam) else 0.0)
        log2rank=math.log2(rank)
        integer_rank_error=abs(log2rank-round(log2rank))
        stencil=purity_stencil(psi,n,metrics['purity'])
        bank=gate_bank(clifford_path,n,tau,gate_count,base_seed)
        rows.append({
            'state_id':f'{tid}|tau{tau:g}','trajectory_id':tid,
            'measurement_protocol':meas,'n':n,'p_measure':p,'trajectory_index':tr,
            'tau':tau,'split':split,'measurements_to_probe':mcount,
            'cut_measurements_to_probe':ccount,'schmidt_rank':rank,
            'log2_schmidt_rank':int(round(log2rank)),
            'spectrum_flatness_max_abs':flat_err,
            'rank_power_of_two_error':integer_rank_error,
            **{f'pre_{k}':v for k,v in metrics.items()},
            **stencil,
            'exact_delta_linear_haar_clifford':response_haar_linear(stencil,n),
            'exact_delta_linear_xx_pi8':response_xx_twirl_linear(stencil,n,math.pi/8),
            'exact_delta_linear_xx_pi4':response_xx_twirl_linear(stencil,n,math.pi/4),
            **finite_bank_response(psi,n,bank,metrics['purity']),
        })
    return rows


def run_parallel(tasks,workers,progress_every=100):
    out=[];t=time.time()
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as ex:
        futs={ex.submit(worker,x):x for x in tasks}
        for i,f in enumerate(as_completed(futs),1):
            try:out.extend(f.result())
            except Exception as exc:raise RuntimeError(f'failed {futs[f]}') from exc
            if i%progress_every==0 or i==len(futs):
                print(f'[physical] {i}/{len(futs)} in {time.time()-t:.1f}s',flush=True)
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--outdir',type=Path,required=True)
    ap.add_argument('--clifford-path',type=Path,required=True)
    ap.add_argument('--measurement-protocols',nargs='+',default=['z_projective','random_pauli'])
    ap.add_argument('--sizes',type=int,nargs='+',default=[10,12,14])
    ap.add_argument('--p-values',type=float,nargs='+',default=[.08,.12,.16,.20,.24])
    ap.add_argument('--trajectories',type=int,default=200)
    ap.add_argument('--discovery-trajectories',type=int,default=100)
    ap.add_argument('--probe-taus',type=float,nargs='+',default=[6.,8.])
    ap.add_argument('--gate-count',type=int,default=12)
    ap.add_argument('--base-seed',type=int,default=2026082007)
    ap.add_argument('--workers',type=int,default=5)
    ap.add_argument('--progress-every',type=int,default=100)
    args=ap.parse_args()
    if args.gate_count<4 or args.gate_count%2:raise ValueError('gate-count must be even >=4')
    args.outdir.mkdir(parents=True,exist_ok=True)
    cliff=str(args.clifford_path.resolve());probe=tuple(args.probe_taus)
    tasks=[(n,p,tr,probe,args.base_seed,args.discovery_trajectories,m,cliff,args.gate_count)
           for m in args.measurement_protocols for n in args.sizes for p in args.p_values
           for tr in range(args.trajectories)]
    rows=run_parallel(tasks,args.workers,args.progress_every)
    df=pd.DataFrame(rows).sort_values(['measurement_protocol','n','p_measure','trajectory_index','tau'])
    df.to_csv(args.outdir/'physical_stabilizer_states.csv.gz',index=False,compression='gzip')
    manifest={
        'purpose':'physically reachable exact-central-spectrum matching',
        'dynamics':'uniform two-qubit Clifford','initial_state':'random single-qubit stabilizer product',
        'measurement_protocols':args.measurement_protocols,'sizes':args.sizes,'p_values':args.p_values,
        'trajectories_per_cell':args.trajectories,'discovery_trajectories_per_cell':args.discovery_trajectories,
        'probe_taus':list(probe),'gate_count':args.gate_count,'base_seed':args.base_seed,
        'rows':len(df),'clifford_table_sha256':hashlib.sha256(Path(cliff).read_bytes()).hexdigest(),
        'matching_principle':'within fixed (n,tau,Schmidt rank), the complete nonzero central spectrum is exactly flat and identical',
        'max_spectrum_flatness_error':float(df.spectrum_flatness_max_abs.max()),
        'max_rank_power_of_two_error':float(df.rank_power_of_two_error.max()),
    }
    (args.outdir/'simulation_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':main()
