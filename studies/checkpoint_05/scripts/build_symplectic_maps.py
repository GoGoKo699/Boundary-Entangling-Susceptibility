#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np

I=np.eye(2,dtype=np.complex128)
X=np.array([[0,1],[1,0]],dtype=np.complex128)
Y=np.array([[0,-1j],[1j,0]],dtype=np.complex128)
Z=np.array([[1,0],[0,-1]],dtype=np.complex128)
SINGLE={(0,0):I,(1,0):X,(0,1):Z,(1,1):Y}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--clifford-table',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--report',type=Path,required=True)
    args=ap.parse_args()
    gates=np.load(args.clifford_table)['gates']
    paulis=[]
    labels=[]
    for code in range(16):
        xl=(code>>0)&1; zl=(code>>1)&1; xh=(code>>2)&1; zh=(code>>3)&1
        paulis.append(np.kron(SINGLE[(xh,zh)],SINGLE[(xl,zl)]))
        labels.append((xl,zl,xh,zh))
    paulis=np.asarray(paulis)
    basis_codes=(1,2,4,8)
    transformations=[]
    max_error=0.0
    for U in gates:
        T=np.zeros((4,4),dtype=np.uint8)
        for i,code in enumerate(basis_codes):
            Q=U@paulis[code]@U.conj().T
            overlaps=np.array([abs(np.trace(P.conj().T@Q))/4.0 for P in paulis])
            j=int(np.argmax(overlaps))
            max_error=max(max_error,float(1-overlaps[j]))
            T[i,:]=labels[j]
        transformations.append(T)
    unique=[]; seen={}
    multiplicities=[]
    representatives=[]
    for gate_i,T in enumerate(transformations):
        key=bytes(T.reshape(-1).tolist())
        if key not in seen:
            seen[key]=len(unique); unique.append(T.copy()); multiplicities.append(0); representatives.append(gate_i)
        multiplicities[seen[key]]+=1
    unique=np.asarray(unique,dtype=np.uint8)
    mult=np.asarray(multiplicities,dtype=np.int64)
    masks=np.zeros((len(unique),4),dtype=np.uint8)
    for g,T in enumerate(unique):
        for out in range(4):
            mask=0
            for inp in range(4):
                if T[inp,out]: mask |= (1<<inp)
            masks[g,out]=mask
    J=np.array([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],dtype=np.uint8)
    symp_ok=True
    for T in unique:
        if not np.array_equal((T@J@T.T)%2,J):
            symp_ok=False; break
    args.out.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(args.out,masks=masks,transformations=unique,multiplicity=mult,representative_gate_indices=np.asarray(representatives,dtype=np.int64))
    report={
        'input_gate_count':int(len(gates)),
        'unique_binary_symplectic_maps':int(len(unique)),
        'multiplicity_min':int(mult.min()),
        'multiplicity_max':int(mult.max()),
        'all_multiplicities_equal':bool(np.all(mult==mult[0])),
        'max_pauli_identification_error':max_error,
        'all_maps_symplectic':bool(symp_ok),
        'bit_order':['x_low','z_low','x_high','z_high'],
    }
    args.report.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
