#!/usr/bin/env python3
"""Bounded archived Figure 1 generation replay; source generator is shared.

Two primary trajectories were specified in FIGURE1.md before execution.
Purity contraction is independent, no source response/stencil function reused.
"""
import csv
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import platform
import time
import zipfile
import numpy as np
import scipy

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'audits/full-sanity-01/results'

def purity(psi,sites):
    n=psi.size.bit_length()-1
    chosen=list(sites); rest=[i for i in range(n) if i not in chosen]
    labels=np.arange(psi.size)
    # Build explicitly indexed subsystem amplitudes, independent of source reshape/transpose.
    a=sum(((labels >> bit) & 1) << j for j,bit in enumerate(chosen))
    b=sum(((labels >> bit) & 1) << j for j,bit in enumerate(rest))
    M=np.empty((2**len(chosen),2**len(rest)),complex); M[a,b]=psi
    rho=M@M.conj().T
    return float(np.trace(rho@rho).real)

def main():
    start=time.perf_counter()
    path=ROOT/'studies/checkpoint_04/scripts/cross_architecture_simulation.py'
    spec=importlib.util.spec_from_file_location('audit_shared_state_generator',path)
    simulator=importlib.util.module_from_spec(spec);spec.loader.exec_module(simulator)
    with zipfile.ZipFile(ROOT/'entanglement-data.zip') as z:
        pre='checkpoint_04/data/intervention/primary_rank4/'
        data=list(csv.DictReader(io.StringIO(gzip.decompress(z.read(pre+'state_response_rows.csv.gz')).decode())))
        refs=json.loads(z.read(pre+'equalization_reference_spectra.json'))
    rows=[]
    for family in ['haar_z','clifford_z']:
        for tau,psi,mc,cc in simulator.evolve_probe_states(family,10,.08,12,(6.,8.),2026081804):
            original=next(r for r in data if r['family']==family and r['n']=='10' and float(r['p_measure'])==.08 and r['trajectory_index']=='12' and float(r['tau'])==tau and r['variant']=='original')
            assert int(original['measurements_to_probe'])==mc and int(original['cut_measurements_to_probe'])==cc
            u,lam,vh=simulator.schmidt_decomposition(psi,10)
            mu=np.asarray(refs[f'{family}|n10|tau{tau:g}'])
            rank=int(np.count_nonzero(lam>1e-12))
            assert rank==int(original['rank_1e12'])
            vectors=[('original',psi)]
            if rank>=4:vectors.append(('equalized_rank4',simulator.reconstruct_from_schmidt(u,vh,mu)))
            for variant,v in vectors:
                target=next(r for r in data if r['state_id']==original['state_id'] and r['variant']==variant)
                P=purity(v,range(5));PL=purity(v,range(4));PR=purity(v,range(6,10));PLb=purity(v,[0,1,2,3,5])
                response=32/31*(1-0.4*(PL+PR)/P)
                expected=float(target['probe_haar_or_clifford_2design_delta_linear_norm'])/float(target['pre_purity'])
                err=max(abs(actual-float(target[key])) for key,actual in [('pre_purity',P),('P_L',PL),('P_R',PR),('P_Lb',PLb)])
                rows.append(dict(family=family,n=10,p=.08,tr=12,tau=tau,variant=variant,rank=rank,recomputed_response=response,archived_response=expected,response_error=abs(response-expected),max_stencil_error=err))
    status={'rows':rows,'max_error':max(r['response_error'] for r in rows),'passed_at_2e-10':all(r['response_error']<2e-10 and r['max_stencil_error']<2e-10 for r in rows),'runtime_s':time.perf_counter()-start,'seed':2026081804,'environment':dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),'source_generator_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'independence':'Shared original state evolution, SVD and spectrum replacement; independent explicit-basis purity contractions. Not an independent simulator.'}
    (OUT/'figure1_trajectory_replay.json').write_text(json.dumps(status,indent=2)+'\n')
    print(json.dumps(status,indent=2))

if __name__=='__main__':main()
