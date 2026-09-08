#!/usr/bin/env python3
"""Independent kernel audit. No campaign or baseline file is modified.

The oracle uses integer ROW masks and highest-pivot elimination, unlike the
production column-packed, lowest-pivot implementation. Dense measurement
oracles explicitly embed projectors in the computational basis. Shared inputs:
the archived group/maps and the production routines under test, NumPy/LAPACK.
"""
from pathlib import Path
import argparse, collections, hashlib, importlib.util, io, json, sys, time, zipfile
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
MASK64 = (1 << 64) - 1
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
H = (X + Z) / np.sqrt(2)
S = np.diag([1, 1j])


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def rank(rows):
    basis = {}
    for row in rows:
        r = int(row)
        while r:
            p = r.bit_length() - 1
            if p in basis:
                r ^= basis[p]
            else:
                basis[p] = r
                break
    return len(basis)


def unpack(cols, n):
    return [sum(((int(cols[c, r // 64]) >> (r % 64)) & 1) << c
                for c in range(2 * n)) for r in range(n)]


def pack(rows, n):
    cols = np.zeros((2 * n, (n + 63) // 64), np.uint64)
    for r, row in enumerate(rows):
        for c in range(2 * n):
            if row >> c & 1:
                cols[c, r // 64] |= np.uint64(1 << (r % 64))
    return cols


def entropy(rows, n, sites):
    # Independent group counting identity: S(A)=|A|-dim(S supported in A).
    complement = set(range(n)) - set(sites)
    mask = sum((1 << q) | (1 << (n + q)) for q in complement)
    local_stabilizers = n - rank([r & mask for r in rows])
    return len(sites) - local_stabilizers


def row_measure(rows, n, q, axis):
    p = ((1 << q) if axis in (0, 1) else 0) | ((1 << (n + q)) if axis in (1, 2) else 0)
    xmask = (1 << n) - 1
    anti = [i for i, r in enumerate(rows)
            if (((r & xmask) & (p >> n)).bit_count() + ((r >> n) & (p & xmask)).bit_count()) % 2]
    if not anti:
        return rows[:], 0
    pivot = anti[-1]  # Deliberately different basis choice from production.
    out = rows[:]
    for i in anti[:-1]:
        out[i] ^= rows[pivot]
    out[pivot] = p
    return out, 1


def elementary(rows, n, kind, q, t):
    out = []
    for r in rows:
        xq, zq = (r >> q) & 1, (r >> (n + q)) & 1
        if kind == 0:  # H
            if xq != zq:
                r ^= (1 << q) | (1 << (n + q))
        elif kind == 1:  # S
            r ^= xq << (n + q)
        else:  # CNOT q -> t
            r ^= xq << t
            r ^= ((r >> (n + t)) & 1) << (n + q)
        out.append(r)
    return out


def integer_tableau_checks(tab, rng):
    output = []
    for n in (4, 8, 63, 64, 65, 127, 128, 129, 256):
        rows = [1 << (n + q) for q in range(n)]
        for _ in range(12 * n):
            kind, q, t = map(int, (rng.integers(3), rng.integers(n), rng.integers(n)))
            if q != t:
                rows = elementary(rows, n, kind, q, t)
        cols = pack(rows, n)
        assert unpack(cols, n) == rows
        assert rank(rows) == n
        subsets = [[], list(range(n)), list(range(n // 2))]
        subsets += [list(np.flatnonzero(rng.integers(0, 2, n))) for _ in range(12)]
        for sites in subsets:
            site_mask = np.zeros(n, np.uint8)
            site_mask[sites] = 1
            got = int(tab.entropy_site_mask(cols, n, site_mask))
            assert got == entropy(rows, n, sites), (n, sites, got)
        random = deterministic = 0
        for q in sorted(set([0, n - 1, n // 2, 63 if n > 63 else 0, 64 if n > 64 else 0])):
            for axis in range(3):
                want, flag = row_measure(rows, n, q, axis)
                actual = cols.copy()
                got_flag = int(tab.measure_single_pauli(actual, n, q, axis))
                got = unpack(actual, n)
                assert got_flag == flag
                assert rank(want) == rank(got) == rank(want + got) == n
                assert int(tab.measure_single_pauli(actual, n, q, axis)) == 0
                assert rank(unpack(actual, n) + want) == n
                random += flag
                deterministic += 1 - flag
        output.append(dict(n=n, subsets=len(subsets), random_measurements=random,
                           deterministic_measurements=deterministic, passed=True))
    return output


def embed(gate, n, sites):
    matrix = np.zeros((1 << n, 1 << n), complex)
    mask = sum(1 << q for q in sites)
    for before in range(1 << n):
        local_in = sum(((before >> q) & 1) << j for j, q in enumerate(sites))
        for local_out in range(1 << len(sites)):
            after = (before & ~mask) | sum(((local_out >> j) & 1) << q for j, q in enumerate(sites))
            matrix[after, before] = gate[local_out, local_in]
    return matrix


class FixedDraw:
    def __init__(self, u): self.u = u
    def random(self): return self.u


def dense_kernels(modules, rng):
    report = []
    for name, mod in modules:
        max_gate = max_state = max_prob = 0.
        count = 0
        for n in (2, 4, 6):
            state = rng.normal(size=1 << n) + 1j * rng.normal(size=1 << n)
            state /= np.linalg.norm(state)
            for q in range(n):
                for axis, pauli in enumerate((X, Y, Z)):
                    projectors = [embed((I + sign * pauli) / 2, n, [q]) for sign in (1, -1)]
                    probabilities = [float(np.linalg.norm(m @ state) ** 2) for m in projectors]
                    for expected, draw in [(0, probabilities[0] / 2), (1, (1 + probabilities[0]) / 2)]:
                        result = state.copy()
                        out, prob = mod.measure_pauli_inplace(result, q, axis, FixedDraw(draw))
                        want = projectors[expected] @ state / np.sqrt(probabilities[expected])
                        max_state = max(max_state, float(np.max(np.abs(want - result))))
                        max_prob = max(max_prob, abs(prob - probabilities[expected]))
                        assert out == expected
                        count += 1
                for eta in (0., .6, 1.):
                    for sign in (1, -1):
                        kraus = embed(np.diag(np.sqrt([(1 + sign * eta) / 2,
                                                      (1 - sign * eta) / 2])), n, [q])
                        want = kraus @ state
                        prob = float(np.vdot(want, want).real)
                        want /= np.sqrt(prob)
                        pplus = prob if sign == 1 else 1 - prob
                        draw = pplus / 2 if sign == 1 else (1 + pplus) / 2
                        result = state.copy()
                        if hasattr(mod, 'weak_measure_z_inplace'):
                            out, gotp = mod.weak_measure_z_inplace(result, q, eta, FixedDraw(draw))
                            assert out == int(sign == -1)
                        else:
                            out, gotp = mod.weak_z_measure_inplace(result, q, eta, FixedDraw(draw))
                            assert out == sign
                        max_state = max(max_state, float(np.max(np.abs(want - result))))
                        max_prob = max(max_prob, abs(prob - gotp))
                        count += 1
            for q in range(n - 1):
                z = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
                gate = np.linalg.qr(z)[0]
                want = embed(gate, n, [q, q + 1]) @ state
                result = state.copy()
                mod.apply_adjacent_2q_inplace(result, gate, q)
                max_gate = max(max_gate, float(np.max(np.abs(want - result))))
        assert max(max_gate, max_state, max_prob) < 2e-12
        report.append(dict(module=name, measurement_cases=count, max_gate_error=max_gate,
                           max_state_error=max_state, max_probability_error=max_prob, passed=True))
    return report


def support_map(unitary):
    paulis = [np.kron((I, X, Z, Y)[code >> 2], (I, X, Z, Y)[code & 3]) for code in range(16)]
    labels, error = [], 0.
    for code in (1, 2, 4, 8):
        transformed = unitary @ paulis[code] @ unitary.conj().T
        overlaps = np.array([np.trace(p @ transformed) / 4 for p in paulis])
        out = int(np.argmax(abs(overlaps)))
        labels.append(out)
        error = max(error, float(np.linalg.norm(transformed - np.sign(overlaps[out].real) * paulis[out])))
    return tuple(labels), error


def compose(a, b):
    # a after b, each stores image of input binary basis vector.
    return tuple(np.bitwise_xor.reduce([a[j] for j in range(4) if x >> j & 1], initial=0).item() for x in b)


def closure(generators):
    seen = {(1, 2, 4, 8)}
    todo = list(seen)
    while todo:
        b = todo.pop()
        for a in generators:
            c = compose(a, b)
            if c not in seen:
                seen.add(c)
                todo.append(c)
    return seen


def gate_maps_checks(tab, cross, z):
    raw = z.read('checkpoint_05/data/two_qubit_clifford_group.npz')
    gates = np.load(io.BytesIO(raw))['gates']
    archived = np.load(io.BytesIO(z.read('checkpoint_05/data/two_qubit_clifford_symplectic_maps.npz')))
    masks, transformations = archived['masks'], archived['transformations']
    canonicals = [np.eye(4), embed(X, 2, [0]), np.kron(I, H)]
    cn = np.zeros((4, 4))
    for i in range(4): cn[i ^ (((i >> 1) & 1) << 0), i] = 1
    generators = [support_map(g)[0] for g in [np.kron(I, H), np.kron(H, I), np.kron(I, S), np.kron(S, I), cn]]
    independent = closure(generators)
    table = collections.Counter()
    max_identification = 0.
    phase_keys = set()
    for u in gates:
        label, error = support_map(u)
        table[label] += 1
        max_identification = max(max_identification, error)
        flat = u.ravel()
        first = flat[np.flatnonzero(abs(flat) > 1e-10)[0]]
        canonical = u / (first / abs(first))
        phase_keys.add(tuple(np.round(np.concatenate([canonical.real.ravel(), canonical.imag.ravel()]), 10)))
    stored = [tuple(sum(int(t[i, j]) << j for j in range(4)) for i in range(4)) for t in transformations]
    assert len(gates) == len(phase_keys) == 11520
    assert set(table) == independent == set(stored)
    assert len(independent) == 720 and set(table.values()) == {16}
    # Exhaustively compare every archived support map on every two-site Pauli.
    cases = 0
    for gi, label in enumerate(stored):
        for code in range(16):
            input_row = ((code & 1) << 0) | (((code >> 2) & 1) << 1) | (((code >> 1) & 1) << 2) | (((code >> 3) & 1) << 3)
            cols = pack([input_row, 0], 2)
            tab.apply_two_qubit_symplectic(cols, 2, 0, masks, gi)
            expected_code = 0
            for j in range(4):
                if code >> j & 1: expected_code ^= label[j]
            expected_row = ((expected_code & 1) << 0) | (((expected_code >> 2) & 1) << 1) | (((expected_code >> 1) & 1) << 2) | (((expected_code >> 3) & 1) << 3)
            assert unpack(cols, 2)[0] == expected_row
            cases += 1
    local = closure(generators[:-1])
    assert len(local) == 36
    class_counts = []
    weights = collections.defaultdict(float)
    for weight, gate in zip((1, 9, 9, 1), cross.CLIFFORD_CANONICALS):
        center = support_map(gate)[0]
        orbit = collections.Counter(compose(a, compose(center, b)) for a in local for b in local)
        class_counts.append(dict(support_maps=len(orbit), minimum_multiplicity=min(orbit.values()), maximum_multiplicity=max(orbit.values())))
        for key, mult in orbit.items(): weights[key] += weight / 20 * mult / (36 * 36)
    assert set(weights) == independent
    assert max(abs(w - 1 / 720) for w in weights.values()) < 1e-16
    assert max_identification < 1e-10
    return dict(gates=len(gates), unique_projective_unitaries=len(phase_keys), support_maps=len(table),
                multiplicities=sorted(set(table.values())), independently_generated_group_matches=True,
                exhaustive_map_pauli_cases=cases, class_support_counts=class_counts,
                max_pauli_identification_error=max_identification,
                max_unitarity_error=float(np.max(abs(gates.conj().transpose(0, 2, 1) @ gates - np.eye(4)))),
                uniform_class_weight_max_error=max(abs(w - 1 / 720) for w in weights.values()), passed=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, default=ROOT / 'audits/full-sanity-01/results/simulator_independent.json')
    args = ap.parse_args()
    started = time.perf_counter()
    sys.path.insert(0, str(ROOT / 'studies/checkpoint_05/scripts'))
    import stabilizer_tableau as tab
    cross = module('audit_cross', 'studies/checkpoint_04/scripts/cross_architecture_simulation.py')
    flex = module('audit_flex', 'studies/checkpoint_04/scripts/cross_architecture_rankflex.py')
    common = module('audit_common', 'studies/checkpoint_04/scripts/cp04_common.py')
    rng = np.random.default_rng(2026090819)
    out = dict(seed=2026090819, tolerance=2e-12,
               packed_tableau=integer_tableau_checks(tab, rng),
               dense_kernels=dense_kernels([('cross_architecture_simulation', cross), ('cross_architecture_rankflex', flex), ('cp04_common', common)], rng))
    with zipfile.ZipFile(ROOT / 'entanglement-data.zip') as z:
        out['gate_maps'] = gate_maps_checks(tab, cross, z)
    out['elapsed_seconds'] = time.perf_counter() - started
    out['passed'] = True
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
