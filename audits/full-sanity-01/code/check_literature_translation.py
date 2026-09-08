#!/usr/bin/env python3
"""Exact rational check of the EF-to-four-purity coefficient translation.

No scientific baseline code is imported. This checks algebra given published
transfer operators, not the physical validity of those operators independently.
Run: python audits/full-sanity-01/code/check_literature_translation.py
"""
from fractions import Fraction as F
import json


def transfer_row(q, operator_entropy, swapped_operator_entropy):
    """Kuo et al. (1910.11351v2), Eqs. 17, 19, 60, expanded on a cut."""
    A = q**4 * operator_entropy
    B = q**4 * (1 - F(1, q*q) - swapped_operator_entropy)
    norm = (q*q - 1)**2
    u = (A - B / (q*q)) / norm
    v = (A - B) / (q * norm)
    w = (A / (q*q) - B) / norm
    return (v, 1-u, -w, v)


def invariant_row(ep, gt):
    return (F(2,3)*ep, 1-gt-F(5,6)*ep, gt-F(5,6)*ep, F(2,3)*ep)


def run():
    # Tests of rational linear expressions at their affine basis determine
    # their identity for arbitrary ep,gt; basis points need not be physical.
    affine_basis = [(F(0),F(0)), (F(1),F(0)), (F(0),F(1))]
    for ep, gt in affine_basis:
        E = F(3,8)*(ep+2*gt)
        ES = F(3,8)*(ep-2*gt+2)
        assert transfer_row(2,E,ES) == invariant_row(ep,gt)
    cases = {
        "identity": (F(0),F(0)),
        "swap": (F(0),F(1)),
        "CNOT_class": (F(2,3),F(1,3)),
        "sqrt_swap": (F(1,2),F(1,2)),
        "Haar_mean": (F(3,5),F(1,2)),
        "XX_YY_pi_over_8": (F(1,2),F(1,3)),
    }
    result = {name: [str(v) for v in invariant_row(ep,gt)]
              for name,(ep,gt) in cases.items()}
    for q in range(2,9):
        E = F(q*q-1,q*q+1)
        got = transfer_row(q,E,E)
        expected = (F(q,q*q+1),F(0),F(0),F(q,q*q+1))
        assert got == expected
    assert result["identity"] == ["0","1","0","0"]
    assert result["swap"] == ["0","0","1","0"]
    assert result["Haar_mean"] == ["2/5","0","0","2/5"]
    assert result["CNOT_class"] == ["4/9","1/9","-2/9","4/9"]
    assert result["XX_YY_pi_over_8"] == ["1/3","1/4","-1/12","1/3"]
    return {"status":"pass", "arithmetic":"exact fractions", "seed":None,
            "affine_basis_points":3, "Haar_local_dimensions":list(range(2,9)),
            "coefficient_order":["P_L","P_La","P_Lb","P_Lab"],
            "cases":result,
            "independence_limit":"Uses published EF operators and invariant definitions; no independent physical twirl validation."}


if __name__ == "__main__":
    print(json.dumps(run(),indent=2))
