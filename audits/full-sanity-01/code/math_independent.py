"""Independent finite-dimensional mathematical checks for the frozen audit.

No scientific repository module is imported. Sites use big-endian tensor order,
unlike the historical simulator. Dense SVD/matrix contractions supply purities;
Cliffords are generated here from H, S and CNOT, without archived gate tables.
Run with Python (writes JSON) or pytest this explicit file (targeted tests).
"""
from __future__ import annotations

import argparse
from collections import deque
import json
import math
from pathlib import Path
import platform
import time
import numpy as np

SEED = 202609080101
TOL = 2e-10
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
H = (X + Z) / np.sqrt(2)
S = np.diag([1, 1j])
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], complex)
SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], complex)


def ket(n, entries):
    out = np.zeros(2**n, complex)
    for bits, amplitude in entries.items():
        out[int(bits, 2)] = amplitude
    return out / np.linalg.norm(out)


def act(psi, gate, sites):
    n = int(round(np.log2(psi.size)))
    sites = list(sites)
    axes = sites + [q for q in range(n) if q not in sites]
    mat = psi.reshape([2] * n).transpose(axes).reshape(2**len(sites), -1)
    return (gate @ mat).reshape([2] * n).transpose(np.argsort(axes)).reshape(-1)


def purity(psi, sites):
    n = int(round(np.log2(psi.size)))
    sites = list(sites)
    axes = sites + [q for q in range(n) if q not in sites]
    mat = psi.reshape([2] * n).transpose(axes).reshape(2**len(sites), -1)
    singular = np.linalg.svd(mat, compute_uv=False)
    return float(np.sum(singular**4))


def spectrum(psi, sites):
    n = int(round(np.log2(psi.size)))
    sites = list(sites)
    axes = sites + [q for q in range(n) if q not in sites]
    mat = psi.reshape([2] * n).transpose(axes).reshape(2**len(sites), -1)
    return np.linalg.svd(mat, compute_uv=False)**2


def stencil(psi):
    n = int(round(np.log2(psi.size)))
    m = n // 2
    return np.array([purity(psi, range(m - 1)), purity(psi, range(m)),
                     purity(psi, list(range(m - 1)) + [m]),
                     purity(psi, range(m + 1, n))])


def response(psi):
    n = int(round(np.log2(psi.size)))
    d = 2**(n // 2)
    pl, pc, _, pr = stencil(psi)
    return d / (d - 1) * (1 - .4 * (pl + pr) / pc)


def measure(psi, q, pauli, sign):
    raw = .5 * (psi + sign * act(psi, pauli, [q]))
    probability = float(np.vdot(raw, raw).real)
    return probability, None if probability < 1e-13 else raw / np.sqrt(probability)


def swap_copies(n, sites):
    dimension = 2**(2*n)
    indices = np.arange(dimension).reshape([2] * (2*n))
    axes = list(range(2*n))
    for q in sites:
        axes[q], axes[n + q] = axes[n + q], axes[q]
    return np.eye(dimension)[indices.transpose(axes).reshape(-1)]


def local_basis():
    return [swap_copies(2, sites) for sites in [[], [0], [1], [0, 1]]]


def haar_unitary(rng, d):
    z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    q, r = np.linalg.qr(z)
    diag = np.diag(r)
    return q * (diag / np.abs(diag)).conj()


def clifford_one():
    def key(u):
        first = u.flat[np.flatnonzero(np.abs(u) > 1e-8)[0]]
        v = u * (first / abs(first)).conjugate()
        return tuple(np.round(v.real, 10).flat) + tuple(np.round(v.imag, 10).flat)
    found = {key(I): I}
    pending = deque([I])
    while pending:
        u = pending.popleft()
        for g in (H, S):
            v = g @ u
            k = key(v)
            if k not in found:
                found[k] = v
                pending.append(v)
    assert len(found) == 24
    return list(found.values())


def clifford_two_mod_pauli():
    # U and P U have identical U^{dagger tensor 2} F_a U^{tensor 2}.
    # Enumerating all 720 symplectic actions thus exactly averages 11520
    # phase-free Clifford unitaries for this observable.
    paulis = [np.kron(a, b) for a in (I, X, Z, Y) for b in (I, X, Z, Y)]
    bits = [np.array([a & 1, a >> 1, b & 1, b >> 1], np.uint8)
            for a in range(4) for b in range(4)]
    basic = [np.kron(X, I), np.kron(Z, I), np.kron(I, X), np.kron(I, Z)]
    generators = [np.kron(H, I), np.kron(S, I), np.kron(I, H), np.kron(I, S), CNOT]
    actions = []
    for g in generators:
        cols = []
        for p in basic:
            target = g @ p @ g.conj().T
            overlaps = [abs(np.trace(b.conj().T @ target)) for b in paulis]
            cols.append(bits[int(np.argmax(overlaps))])
        actions.append(np.column_stack(cols))
    identity = np.eye(4, dtype=np.uint8)
    found = {identity.tobytes(): (identity, np.eye(4, dtype=complex))}
    pending = deque(found.values())
    while pending:
        sym, u = pending.popleft()
        for g, action in zip(generators, actions):
            target = (action @ sym) % 2
            k = target.tobytes()
            if k not in found:
                found[k] = (target, g @ u)
                pending.append(found[k])
    assert len(found) == 720
    return [u for _, u in found.values()]


def op_entanglement(u):
    # Operator-Schmidt realignment: (out_a,in_a) | (out_b,in_b).
    realigned = u.reshape(2, 2, 2, 2).transpose(0, 2, 1, 3).reshape(4, 4)
    singular = np.linalg.svd(realigned, compute_uv=False)
    return float(1 - np.sum(singular**4) / 16)


def invariant_coefficients(u):
    e, es = op_entanglement(u), op_entanglement(u @ SWAP)
    ep = (e + es - .75) / .75
    gt = (e - es + .75) / 1.5
    return np.array([2*ep/3, 1-gt-5*ep/6, gt-5*ep/6, 2*ep/3]), ep, gt


def cartan(angles):
    out = np.eye(4, dtype=complex)
    for angle, p in zip(angles, (X, Y, Z)):
        pp = np.kron(p, p)
        out = out @ (np.cos(angle) * np.eye(4) - 1j * np.sin(angle) * pp)
    return out


def scope_examples():
    # Full central spectrum fixed at rank one, two very different geometries.
    product = ket(4, {"0000": 1})
    internal = ket(4, {"0000": 1, "0011": 1, "1100": 1, "1111": 1})
    # Same adjacent purities, distinct noncontiguous purity under SWAP.
    cross_a = ket(4, {"0000": 1, "0101": 1, "1010": 1, "1111": 1})
    cross_b = ket(4, {"0000": 1, "0110": 1, "1001": 1, "1111": 1})
    # Nonstabilizer local entanglement concentration inside the left half.
    generic = ket(6, {"000000": np.sqrt(.5), "101000": .5, "110000": .5})
    prob_g, post_g = measure(generic, 0, Z, -1)
    # A fixed gate, unlike its Haar average, can have a positive response change.
    fixed = ket(4, {"0000": 1, "1100": 1})
    prob_f, post_f = measure(fixed, 2, X, 1)
    fixed_gate_responses = [4/3*(purity(p, [0, 1]) - purity(act(p, CNOT, [2, 1]), [0, 1]))
                            / purity(p, [0, 1]) for p in (fixed, post_f)]
    # Both same-side Z locations preserve the spectrum; the farther one suppresses more.
    spatial = ket(6, {"000000": 1, "101100": 1})
    spatial = act(act(spatial, H, [0]), H, [2])
    _, near = measure(spatial, 2, Z, 1)
    _, far = measure(spatial, 0, Z, 1)
    same_invariants = [cartan([np.pi/8, np.pi/8, 0]),
                       cartan(.5*np.arcsin(np.sqrt([2/3, 1/6, 1/6])))]
    op_spectra = [np.linalg.svd(u.reshape(2, 2, 2, 2).transpose(0, 2, 1, 3).reshape(4, 4),
                              compute_uv=False)**2/4 for u in same_invariants]
    return {
        "fixed_spectrum_product_and_internal_bells": {
            "responses": [response(product), response(internal)],
            "central_spectra": [spectrum(p, [0, 1]).tolist() for p in (product, internal)]},
        "noncontiguous_required": {
            "stencils": [stencil(p).tolist() for p in (cross_a, cross_b)],
            "swap_post_purities": [purity(act(p, SWAP, [1, 2]), [0, 1]) for p in (cross_a, cross_b)]},
        "generic_input_outside_corollary": {
            "outcome_probability": prob_g, "central_purities": [stencil(p)[1] for p in (generic, post_g)],
            "responses": [response(generic), response(post_g)],
            "positive_change": response(post_g) - response(generic)},
        "individual_gate_outside_corollary": {
            "outcome_probability": prob_f, "fixed_cnot_responses": fixed_gate_responses,
            "averaged_responses": [response(p) for p in (fixed, post_f)]},
        "distance_not_ordered_by_corollary": {
            "central_purities": [stencil(p)[1] for p in (spatial, near, far)],
            "responses_before_near_far": [response(p) for p in (spatial, near, far)],
            "positive_near_minus_far": response(near) - response(far)},
        "mixed_input_pure_complement_substitution_fails": {
            "input": "I_16/16", "actual_post_purity": .25,
            "incorrect_pure_complement_haar_prediction": .4,
            "correct_P_Lab_form": .4*(.5 + .125)},
        "two_invariants_do_not_classify_all_gate_content": {
            "sin2_squared_cartan_coordinates": [[.5, .5, 0], [2/3, 1/6, 1/6]],
            "ep_gt": [list(invariant_coefficients(u)[1:]) for u in same_invariants],
            "normalized_operator_schmidt_spectra": [s.tolist() for s in op_spectra]},
    }


def run():
    started = time.perf_counter()
    rng = np.random.default_rng(SEED)
    single = clifford_one()
    double = clifford_two_mod_pauli()
    basis = local_basis()
    gram = np.array([[np.trace(a @ b).real for b in basis] for a in basis])
    omega = np.zeros((16, 16), complex)
    for u in double:
        uu = np.kron(u, u)
        omega += uu.conj().T @ basis[1] @ uu / len(double)
    haar_error = np.max(np.abs(omega - .4 * (basis[0] + basis[3])))

    coefficient_errors, cartan_errors, overlap_errors, twirl_errors, stencil_errors = [], [], [], [], []
    named = {"identity": np.eye(4), "swap": SWAP,
             "xy_pi8": cartan([np.pi/8, np.pi/8, 0]), "xx_pi4": cartan([np.pi/4, 0, 0])}
    gate_coefficients = {}
    random_gates = [haar_unitary(rng, 4) for _ in range(100)]
    for name, u in list(named.items()) + [(f"random_{i}", u) for i, u in enumerate(random_gates)]:
        uu = np.kron(u, u)
        raw = uu.conj().T @ basis[1] @ uu
        overlaps = np.array([np.trace(b @ raw).real for b in basis])
        projected = np.linalg.solve(gram, overlaps)
        expected, ep, gt = invariant_coefficients(u)
        coefficient_errors.append(float(np.max(np.abs(projected - expected))))
        overlap_errors.append(float(np.max(np.abs(overlaps - [8, 16*(1-op_entanglement(u)),
                                                              16*(1-op_entanglement(u @ SWAP)), 8]))))
        if name in named:
            gate_coefficients[name] = {"coefficients": projected.tolist(), "ep": ep, "gt": gt}
    for _ in range(100):
        angles = rng.uniform(-np.pi, np.pi, 3)
        u = cartan(angles)
        _, ep, gt = invariant_coefficients(u)
        a, b, c = np.sin(2*angles)**2
        cartan_errors.append(max(abs(ep-2/3*(a+b+c-a*b-a*c-b*c)), abs(gt-(a+b+c)/3)))
    # Finite, exact 2-design average independently verifies the projector algebra.
    for u in [*named.values(), *random_gates[:4]]:
        twirled = np.zeros((16, 16), complex)
        psi = rng.normal(size=16) + 1j*rng.normal(size=16)
        psi /= np.linalg.norm(psi)
        empirical = 0.
        for va in single:
            for vb in single:
                gate = u @ np.kron(va, vb)
                uu = np.kron(gate, gate)
                twirled += uu.conj().T @ basis[1] @ uu / len(single)**2
                empirical += purity(act(psi, gate, [1, 2]), [0, 1]) / len(single)**2
        coeff, _, _ = invariant_coefficients(u)
        reconstructed = sum(c*b for c, b in zip(coeff, basis))
        twirl_errors.append(float(np.max(np.abs(twirled - reconstructed))))
        stencil_errors.append(abs(empirical - float(coeff @ stencil(psi))))

    # General deterministic response operator, evaluated with full dense density matrices.
    swap_a = swap_copies(4, [0, 1])
    general_errors = []
    for _ in range(12):
        psi = rng.normal(size=16) + 1j*rng.normal(size=16)
        psi /= np.linalg.norm(psi)
        u = haar_unitary(rng, 4)
        full = np.kron(np.kron(I, u), I)
        full_two = np.kron(full, full)
        phi = np.kron(psi, psi)
        op = full_two.conj().T @ swap_a @ full_two
        predicted = float(np.vdot(phi, op @ phi).real)
        general_errors.append(abs(predicted - purity(act(psi, u, [1, 2]), [0, 1])))

    # Stabilizer inputs generated with dense H/S/CNOT circuits, no tableau calls.
    # Not uniform over all stabilizer states and not an exhaustive proof.
    tested_outcomes = eligible = equality = strict = 0
    max_integer_error = max_flat_error = max_sign = max_corollary_error = max_pair_error = 0.
    alphabet = set()
    state_counts = {4: 120, 6: 120, 8: 60}
    for n, count in state_counts.items():
        m = n//2
        for _ in range(count):
            psi = ket(n, {"0"*n: 1})
            for step in range(10*n):
                if step % 3 == 0:
                    a, b = rng.choice(n, 2, replace=False)
                    psi = act(psi, CNOT, [int(a), int(b)])
                else:
                    q = int(rng.integers(n))
                    psi = act(psi, H if rng.integers(2) else S, [q])
            psi /= np.linalg.norm(psi)
            p = [purity(psi, range(j)) for j in (m-1, m, m+1)]
            ent = -np.log2(p)
            max_integer_error = max(max_integer_error, float(np.max(np.abs(ent-np.round(ent)))))
            alphabet.add((int(round(ent[1]-ent[0])), int(round(ent[1]-ent[2]))))
            for j in range(n+1):
                lam = spectrum(psi, range(j))
                nz = lam[lam > 1e-10]
                max_flat_error = max(max_flat_error, float(np.max(np.abs(nz - 1/len(nz)))))
            for q in range(n):
                for pauli in (X, Y, Z):
                    valid = []
                    for sign in (-1, 1):
                        prob, post = measure(psi, q, pauli, sign)
                        if post is None:
                            continue
                        tested_outcomes += 1
                        after_p = np.array([purity(post, range(j)) for j in (m-1, m, m+1)])
                        after_e = -np.log2(after_p)
                        changes = after_e-ent
                        assert np.max(np.abs(changes-np.round(changes))) < TOL
                        assert np.max(changes) < TOL and np.min(changes) > -1-TOL
                        valid.append(after_p)
                        if abs(after_p[1]-p[1]) < TOL:
                            eligible += 1
                            change = response(post) - response(psi)
                            expected = -2*(2**m)/(5*(2**m-1)*p[1]) * (after_p[0]-p[0]+after_p[2]-p[2])
                            max_corollary_error = max(max_corollary_error, abs(change-expected))
                            max_sign = max(max_sign, change)
                            if abs(change) < TOL:
                                equality += 1
                                assert np.max(np.abs(after_p-np.array(p))) < TOL
                            else:
                                strict += 1
                                assert change < 0
                    if len(valid) == 2:
                        max_pair_error = max(max_pair_error, float(np.max(np.abs(valid[0]-valid[1]))))

    # Exact Clifford logarithmic-vs-linear comparison on a four-qubit product.
    product = ket(4, {"0000": 1})
    post_p = np.array([purity(act(product, u, [1, 2]), [0, 1]) for u in double])
    out = {
        "seed": SEED, "tolerance": TOL, "python": platform.python_version(), "numpy": np.__version__,
        "independence": "No baseline imports, archived rows, or archived gates. Dense SVD and NumPy linear algebra; mathematical identities shared by definition. Clifford average generated afresh from H/S/CNOT, with 720 exact Pauli cosets.",
        "single_clifford_count": len(single), "two_qubit_clifford_pauli_cosets": len(double),
        "gram": gram.tolist(), "named_gate_coefficients": gate_coefficients,
        "max_errors": {"haar_clifford_operator": float(haar_error), "invariant_coefficients_104_gates": max(coefficient_errors),
                       "invariant_overlaps": max(overlap_errors), "cartan_100_gates": max(cartan_errors),
                       "local_design_twirl_8_gates": max(twirl_errors), "four_purity_state_average": max(stencil_errors),
                       "general_response_12_dense_states": max(general_errors)},
        "stabilizer_checks": {"state_counts": state_counts, "outcomes": tested_outcomes, "central_preserving_outcomes": eligible,
                              "equality": equality, "strict": strict, "observed_codes": sorted(alphabet),
                              "max_entropy_integer_error": max_integer_error, "max_flat_eigenvalue_error": max_flat_error,
                              "max_positive_response_roundoff": max_sign, "max_corollary_residual": max_corollary_error,
                              "max_opposite_outcome_purity_difference": max_pair_error},
        "distinct_observables_product_n4": {"mean_post_purity": float(post_p.mean()), "relative_linear_response": response(product),
                                             "mean_finite_log2_increment": float(np.mean(-np.log2(post_p))),
                                             "minus_log2_mean_post_purity": float(-np.log2(post_p.mean()))},
        "examples": scope_examples(), "runtime_seconds": time.perf_counter()-started,
    }
    assert max(out["max_errors"].values()) < TOL
    assert len(alphabet) == 9
    assert max_sign < TOL
    return out


def test_scope_counterexamples_and_restrictions():
    e = scope_examples()
    assert np.allclose(e["fixed_spectrum_product_and_internal_bells"]["responses"], [4/15, 4/5])
    assert np.allclose(e["noncontiguous_required"]["swap_post_purities"], [1, .25])
    assert abs(e["generic_input_outside_corollary"]["positive_change"] - 2/35) < TOL
    assert np.allclose(e["individual_gate_outside_corollary"]["fixed_cnot_responses"], [0, 2/3])
    assert abs(e["distance_not_ordered_by_corollary"]["positive_near_minus_far"] - 16/35) < TOL


def test_dimension_and_input_purity_normalization():
    # The same boundary-code base response acquires D/(D-1), not a probe dimension.
    assert abs(response(ket(4, {"0000": 1})) - 4/15) < TOL
    bell_cross = ket(4, {"0000": 1, "0110": 1})
    assert abs(response(bell_cross) - (-4/5)) < TOL


def test_response_invariants_are_not_complete_gate_invariants():
    e = scope_examples()["two_invariants_do_not_classify_all_gate_content"]
    assert np.allclose(e["ep_gt"], [[.5, 1/3], [.5, 1/3]], atol=TOL)
    assert not np.allclose(*e["normalized_operator_schmidt_spectra"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("audits/full-sanity-01/results/math_independent.json"))
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
