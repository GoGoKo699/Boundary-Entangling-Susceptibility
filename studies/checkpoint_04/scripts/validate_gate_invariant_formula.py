#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import cross_architecture_simulation as sim

def operator_entanglement(u: np.ndarray) -> float:
    t=u.reshape(2,2,2,2)
    reshuffled=t.transpose(0,2,1,3).reshape(4,4)
    gram=reshuffled@reshuffled.conj().T
    return float(1.0-np.trace(gram@gram).real/16.0)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path);ap.add_argument('--samples',type=int,default=100);ap.add_argument('--seed',type=int,default=123);args=ap.parse_args()
    rng=np.random.default_rng(args.seed); es=0.75; errors=[]; examples=[]
    for k in range(args.samples):
        u=sim.haar_unitary(4,rng)
        e=operator_entanglement(u); eus=operator_entanglement(u@sim.SWAP)
        ep=(e+eus-es)/es; gt=(e-eus+es)/(2*es)
        pred=np.array([2*ep/3,1-gt-5*ep/6,gt-5*ep/6,2*ep/3],float)
        actual=sim.locally_dressed_response_coefficients(u)
        err=float(np.max(np.abs(pred-actual))); errors.append(err)
        if k<3:
            examples.append({'entangling_power':ep,'gate_typicality':gt,'direct_coefficients':actual.tolist(),'invariant_formula_coefficients':pred.tolist(),'max_abs_error':err})
    result={'samples':args.samples,'seed':args.seed,'maximum_coefficient_error':max(errors),'mean_coefficient_error':float(np.mean(errors)),'examples':examples,'passes':bool(np.isfinite(errors).all() and max(errors)<5e-13)}
    text=json.dumps(result,indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(text+'\n',encoding='utf-8')
    print(text)
    if not result['passes']:
        raise SystemExit(1)
if __name__=='__main__':main()
