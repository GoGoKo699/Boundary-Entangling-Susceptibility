#!/usr/bin/env python3
"""Validate the Checkpoint 04 response-operator identities numerically."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np

from cp04_common import (
    H, S, X, Y, Z, I2, haar_unitary, apply_adjacent_2q_inplace,
    random_product_state, schmidt_decomposition, purity_stencil,
    response_haar_linear, response_xx_twirl_linear, load_clifford_gates,
    xx_twirl_coefficients, measure_pauli_inplace,
)


def central_linear(psi: np.ndarray, n: int) -> float:
    from cp04_common import subset_purity
    d = 1 << (n // 2)
    p = subset_purity(psi, n, range(0, n//2))
    return d / (d - 1.0) * (1.0 - p)


def canonical_swap_matrices() -> tuple[np.ndarray, np.ndarray]:
    def perm_matrix(order):
        P = np.zeros((16, 16), complex)
        for idx in range(16):
            bits = [(idx >> (3-j)) & 1 for j in range(4)]
            new = [bits[i] for i in order]
            out = 0
            for b in new:
                out = (out << 1) | b
            P[out, idx] = 1
        return P
    return perm_matrix([2,1,0,3]), perm_matrix([0,3,2,1])


def response_coefficients_from_ensemble(gates: np.ndarray) -> tuple[np.ndarray, float]:
    Sa, Sb = canonical_swap_matrices()
    I = np.eye(16, dtype=complex)
    Sab = Sa @ Sb
    basis = [I, Sa, Sb, Sab]
    gram = np.array([[np.trace(A.conj().T @ B).real for B in basis] for A in basis])
    K = np.zeros((16,16), complex)
    for U in gates:
        U2 = np.kron(U, U)
        K += U2.conj().T @ Sa @ U2
    K /= len(gates)
    rhs = np.array([np.trace(B.conj().T @ K).real for B in basis])
    coeff = np.linalg.solve(gram, rhs)
    resid = float(np.linalg.norm(K - sum(c*B for c,B in zip(coeff,basis))))
    return coeff, resid


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--clifford-path',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    rng=np.random.default_rng(2026082001)

    pauli_errors=[]
    for b,P in enumerate([X,Y,Z]):
        for _ in range(20):
            psi=haar_unitary(2,rng)[:,0].copy()
            outcome,_=measure_pauli_inplace(psi,0,b,rng)
            exp=float(np.real(np.vdot(psi,P@psi)))
            target=1.0 if outcome==0 else -1.0
            pauli_errors.append(abs(exp-target))

    cliffs=load_clifford_gates(args.clifford_path)
    coeff_cliff,resid_cliff=response_coefficients_from_ensemble(cliffs)
    haar_gates=np.stack([haar_unitary(4,rng) for _ in range(5000)])
    coeff_haar,resid_haar=response_coefficients_from_ensemble(haar_gates)

    n=8; qcut=n//2-1
    state_errors_haar=[]; state_z_haar=[]
    state_errors_xx={str(theta):[] for theta in [math.pi/16,math.pi/8,math.pi/4]}
    for _ in range(5):
        psi=random_product_state(n,rng)
        for parity in (0,1):
            for q in range(parity,n-1,2):
                apply_adjacent_2q_inplace(psi,haar_unitary(4,rng),q)
        _,lam,_=schmidt_decomposition(psi,n)
        pre=central_linear(psi,n)
        stencil=purity_stencil(psi,n,float(np.sum(lam*lam)))
        exact=response_haar_linear(stencil,n)
        vals=[]
        for _ in range(600):
            out=psi.copy(); apply_adjacent_2q_inplace(out,haar_unitary(4,rng),qcut)
            vals.append(central_linear(out,n)-pre)
        vals=np.asarray(vals)
        se=float(vals.std(ddof=1)/math.sqrt(len(vals)))
        state_errors_haar.append(float(vals.mean()-exact))
        state_z_haar.append(float((vals.mean()-exact)/se))
        for theta in [math.pi/16,math.pi/8,math.pi/4]:
            exact_x=response_xx_twirl_linear(stencil,n,theta)
            vals=[]
            V=math.cos(theta)*np.eye(4)-1j*math.sin(theta)*np.kron(X,X)
            for _ in range(600):
                preloc=np.kron(haar_unitary(2,rng),haar_unitary(2,rng))
                postloc=np.kron(haar_unitary(2,rng),haar_unitary(2,rng))
                gate=postloc@V@preloc
                out=psi.copy(); apply_adjacent_2q_inplace(out,gate,qcut)
                vals.append(central_linear(out,n)-pre)
            vals=np.asarray(vals)
            se=float(vals.std(ddof=1)/math.sqrt(len(vals)))
            state_errors_xx[str(theta)].append({
                'bias':float(vals.mean()-exact_x),'z':float((vals.mean()-exact_x)/se),
                'exact':float(exact_x),'mc':float(vals.mean()),'se':se,
            })

    result={
        'pauli_measurement_max_eigenvalue_error':float(max(pauli_errors)),
        'clifford_group_size':int(len(cliffs)),
        'clifford_response_coefficients_order_I_Sa_Sb_Sab':coeff_cliff.tolist(),
        'clifford_projection_residual_fro':resid_cliff,
        'clifford_target_max_abs_error':float(np.max(np.abs(coeff_cliff-np.array([.4,0,0,.4])))),
        'haar_mc_response_coefficients_order_I_Sa_Sb_Sab':coeff_haar.tolist(),
        'haar_mc_projection_residual_fro':resid_haar,
        'haar_state_mc_max_abs_bias':float(max(abs(x) for x in state_errors_haar)),
        'haar_state_mc_max_abs_z':float(max(abs(x) for x in state_z_haar)),
        'xx_coefficients':{str(t):xx_twirl_coefficients(t) for t in [math.pi/16,math.pi/8,math.pi/4]},
        'xx_state_mc':state_errors_xx,
    }
    result['passes']=bool(
        result['pauli_measurement_max_eigenvalue_error']<1e-12 and
        result['clifford_group_size']==11520 and
        result['clifford_target_max_abs_error']<1e-12 and
        result['haar_state_mc_max_abs_z']<5 and
        all(max(abs(x['z']) for x in rows)<5 for rows in state_errors_xx.values())
    )
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
    if not result['passes']:
        raise SystemExit('validation failed')

if __name__=='__main__': main()
