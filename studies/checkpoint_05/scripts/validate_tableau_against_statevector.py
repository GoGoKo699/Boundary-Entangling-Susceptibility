#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from stabilizer_tableau import (
    simulate_trajectory_snapshots, central_observables,
    tripartite_information_quarters, stable_seed_u64, load_symplectic_masks,
)
from cp04_common import apply_adjacent_2q_inplace, apply_1q_inplace

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.array([[1,0],[0,-1]],complex)
PAULIS=(X,Y,Z)
PLUS=(np.array([1,1],complex)/math.sqrt(2), np.array([1,1j],complex)/math.sqrt(2), np.array([1,0],complex))
MASK=(1<<64)-1

def rng_next(state:int):
    state=(state+0x9E3779B97F4A7C15)&MASK
    z=state
    z=((z^(z>>30))*0xBF58476D1CE4E5B9)&MASK
    z=((z^(z>>27))*0x94D049BB133111EB)&MASK
    z=(z^(z>>31))&MASK
    return state,z

def rand01(state:int):
    state,r=rng_next(state)
    return state,(r>>11)/9007199254740992.0

def random_product(n,state):
    psi=np.array([1+0j])
    for _ in range(n):
        state,r=rng_next(state); axis=r%3
        v=PLUS[axis]
        psi=np.concatenate([v[0]*psi,v[1]*psi])
    return psi,state

def measure_pauli_nonzero(psi,q,axis):
    P=PAULIS[axis]
    for sign in (1,-1):
        M=(I+sign*P)/2
        tmp=psi.copy(); apply_1q_inplace(tmp,M,q)
        p=float(np.vdot(tmp,tmp).real)
        if p>1e-12:
            return tmp/math.sqrt(p)
    raise RuntimeError('zero projection both outcomes')

def entropy_subset(psi,n,sites):
    sites=list(sites)
    axes=[n-1-q for q in sites]
    rest=[a for a in range(n) if a not in axes]
    mat=psi.reshape([2]*n).transpose(axes+rest).reshape(1<<len(sites),-1)
    s=np.linalg.svd(mat,compute_uv=False)
    lam=np.square(np.clip(s.real,0,None)); lam=lam/lam.sum(); nz=lam[lam>1e-12]
    return int(round(-np.sum(nz*np.log2(nz))))

def sv_metrics(psi,n):
    m=n//2
    sl=entropy_subset(psi,n,range(0,m-1)); sm=entropy_subset(psi,n,range(0,m)); sr=entropy_subset(psi,n,range(0,m+1))
    pm=2.0**(-sm);pl=2.0**(-sl);pr=2.0**(-sr);norm=1/(1-2.0**(-m))
    chi=norm*(pm-.4*(pl+pr)); rel=chi/pm
    q=n//4
    A=range(0,q); B=range(q,2*q); C=range(2*q,3*q)
    def E(s):return entropy_subset(psi,n,s)
    Aset=set(A);Bset=set(B);Cset=set(C)
    vals=[E(Aset),E(Bset),E(Cset),E(Aset|Bset),E(Aset|Cset),E(Bset|Cset),E(Aset|Bset|Cset)]
    i3=vals[0]+vals[1]+vals[2]-vals[3]-vals[4]-vals[5]+vals[6]
    return np.array([sl,sm,sr,pm,pl,pr,chi,rel,sm-sl,sm-sr],float),np.array(vals+[i3],float)

def simulate_sv(n,p,probe_steps,gates,reps,seed,protocol):
    state=int(seed); psi,state=random_product(n,state); out=[]; probe_i=0
    for cycle in range(1,int(probe_steps[-1])+1):
        state,r=rng_next(state); first=r&1
        for oi in range(2):
            parity=first if oi==0 else 1-first
            for q in range(parity,n-1,2):
                state,rg=rng_next(state); mi=rg%len(reps)
                apply_adjacent_2q_inplace(psi,gates[reps[mi]],q)
        for q in range(n):
            state,u=rand01(state)
            if u<p:
                if protocol==0: axis=2
                else: state,ra=rng_next(state); axis=ra%3
                psi=measure_pauli_nonzero(psi,q,axis)
        if cycle==int(probe_steps[probe_i]):
            out.append(psi.copy());probe_i+=1
            if probe_i==len(probe_steps):break
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--clifford-table',type=Path,required=True)
    ap.add_argument('--maps',type=Path,required=True)
    ap.add_argument('--report',type=Path,required=True)
    args=ap.parse_args()
    gates=np.load(args.clifford_table)['gates']
    z=np.load(args.maps); masks=z['masks']; reps=z['representative_gate_indices']
    max_c=max_i3=0.0;cases=[]
    for n in (4,6,8,10):
      for p in (0.0,.08,.2,.5):
       for protocol in (0,1):
        for tr in range(4):
            seed=stable_seed_u64('cp05_tableau_validation',n,p,protocol,tr)
            steps=np.array([n,2*n],np.int64)
            snaps,*_=simulate_trajectory_snapshots(n,p,steps,masks,seed,protocol)
            svs=simulate_sv(n,p,steps,gates,reps,seed,protocol)
            for snap,psi in zip(snaps,svs):
                a=central_observables(snap,n);b,i3b=sv_metrics(psi,n)
                i3a=tripartite_information_quarters(snap,n)
                dc=float(np.max(np.abs(a-b)));di=float(np.max(np.abs(i3a-i3b)))
                max_c=max(max_c,dc);max_i3=max(max_i3,di)
                cases.append({'n':n,'p':p,'protocol':protocol,'trajectory':tr,'central_error':dc,'tmi_error':di})
    report={'case_count':len(cases),'max_central_observable_error':max_c,'max_tripartite_vector_error':max_i3,'passed':max(max_c,max_i3)<1e-10,'cases':cases}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
    if not report['passed']:raise SystemExit(1)
if __name__=='__main__':main()
