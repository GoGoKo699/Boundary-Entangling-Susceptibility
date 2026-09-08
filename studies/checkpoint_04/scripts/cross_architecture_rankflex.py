#!/usr/bin/env python3
"""Checkpoint 04: cross-architecture fixed-spectrum susceptibility experiment.

This is a clean, independent state-vector implementation.  It extends the
Checkpoint 03 intervention to multiple circuit and measurement families and
uses exact two-copy response operators for several probe ensembles.

Qubit convention
----------------
The state-vector index is little endian.  For n=2m, the central cut lies
between qubits a=m-1 and b=m.  The lower m qubits form subsystem A.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Iterable

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import numpy as np
import pandas as pd
import scipy.linalg as sla

I2 = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
H = np.array([[1, 1], [1, -1]], dtype=np.complex128) / math.sqrt(2.0)
S = np.diag([1.0, 1.0j]).astype(np.complex128)

FAMILIES = (
    "haar_z",
    "clifford_z",
    "floquet_cartan_z",
    "haar_random_pauli",
    "haar_weak_z_eta06",
)


def stable_seed(*items: object) -> int:
    raw = repr(items).encode("utf-8")
    return int.from_bytes(hashlib.blake2b(raw, digest_size=8).digest(), "little") & 0xFFFFFFFF


def haar_unitary(dim: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(z)
    diag = np.diag(r)
    phase = np.divide(diag, np.abs(diag), out=np.ones_like(diag), where=np.abs(diag) > 0)
    return q * phase.conj()


def cartan_gate(alpha: float, beta: float, gamma: float) -> np.ndarray:
    h = alpha * np.kron(X, X) + beta * np.kron(Y, Y) + gamma * np.kron(Z, Z)
    return sla.expm(-1j * h)


def canonical_phase_key(u: np.ndarray, decimals: int = 10) -> tuple[float, ...]:
    flat = u.ravel()
    nz = np.flatnonzero(np.abs(flat) > 1e-10)
    if len(nz) == 0:
        raise ValueError("zero matrix")
    phase = flat[nz[0]] / abs(flat[nz[0]])
    v = u / phase
    v = np.round(v.real, decimals) + 1j * np.round(v.imag, decimals)
    return tuple(np.concatenate([v.real.ravel(), v.imag.ravel()]).tolist())


def build_single_qubit_cliffords() -> list[np.ndarray]:
    identity = np.eye(2, dtype=np.complex128)
    found = {canonical_phase_key(identity): identity}
    queue: collections.deque[np.ndarray] = collections.deque([identity])
    while queue:
        u = queue.popleft()
        for g in (H, S):
            v = g @ u
            key = canonical_phase_key(v)
            if key not in found:
                found[key] = v
                queue.append(v)
    values = list(found.values())
    if len(values) != 24:
        raise RuntimeError(f"Expected 24 one-qubit Cliffords, found {len(values)}")
    return values


LOCAL_CLIFFORDS = build_single_qubit_cliffords()

# Pair basis is |high,low>, matching little-endian adjacent-gate application.
I4 = np.eye(4, dtype=np.complex128)
CNOT_HIGH_TO_LOW = np.array(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
    dtype=np.complex128,
)
ISWAP = np.array(
    [[1, 0, 0, 0], [0, 0, 1j, 0], [0, 1j, 0, 0], [0, 0, 0, 1]],
    dtype=np.complex128,
)
SWAP = np.array(
    [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]],
    dtype=np.complex128,
)
CLIFFORD_CANONICALS = (I4, CNOT_HIGH_TO_LOW, ISWAP, SWAP)
CLIFFORD_CLASS_PROBS = np.asarray([1, 9, 9, 1], dtype=float) / 20.0


def sample_two_qubit_clifford(rng: np.random.Generator) -> np.ndarray:
    """Sample by the four local-equivalence classes of the two-qubit Clifford group.

    Class sizes are 576, 5184, 5184, 576, hence weights 1:9:9:1.
    Independent local Clifford factors are applied on both sides.
    """
    cls = int(rng.choice(4, p=CLIFFORD_CLASS_PROBS))
    left = np.kron(
        LOCAL_CLIFFORDS[int(rng.integers(24))],
        LOCAL_CLIFFORDS[int(rng.integers(24))],
    )
    right = np.kron(
        LOCAL_CLIFFORDS[int(rng.integers(24))],
        LOCAL_CLIFFORDS[int(rng.integers(24))],
    )
    return left @ CLIFFORD_CANONICALS[cls] @ right


def apply_1q_inplace(psi: np.ndarray, gate: np.ndarray, q: int) -> None:
    stride = 1 << q
    period = stride << 1
    blocks = psi.reshape(-1, period)
    a = blocks[:, :stride].copy()
    b = blocks[:, stride:].copy()
    blocks[:, :stride] = gate[0, 0] * a + gate[0, 1] * b
    blocks[:, stride:] = gate[1, 0] * a + gate[1, 1] * b


def apply_adjacent_2q_inplace(psi: np.ndarray, gate: np.ndarray, q: int) -> None:
    stride = 1 << q
    period = stride << 2
    blocks = psi.reshape(-1, period)
    v = np.stack([blocks[:, i * stride:(i + 1) * stride].copy() for i in range(4)], axis=1)
    out = np.einsum("ij,bjs->bis", gate, v, optimize=True)
    for i in range(4):
        blocks[:, i * stride:(i + 1) * stride] = out[:, i, :]


def random_product_state(n: int, rng: np.random.Generator) -> np.ndarray:
    psi = np.array([1.0 + 0.0j])
    for _ in range(n):
        u, v = rng.random(2)
        theta = math.acos(1.0 - 2.0 * u)
        phi = 2.0 * math.pi * v
        a0 = math.cos(theta / 2.0)
        a1 = np.exp(1j * phi) * math.sin(theta / 2.0)
        psi = np.concatenate([a0 * psi, a1 * psi])
    return psi.astype(np.complex128, copy=False)


def measure_z_inplace(psi: np.ndarray, q: int, rng: np.random.Generator) -> tuple[int, float]:
    stride = 1 << q
    period = stride << 1
    blocks = psi.reshape(-1, period)
    p0 = float(np.sum(np.abs(blocks[:, :stride]) ** 2))
    p0 = min(1.0, max(0.0, p0))
    outcome = 0 if rng.random() < p0 else 1
    prob = p0 if outcome == 0 else 1.0 - p0
    if prob <= 1e-15:
        outcome = 1 - outcome
        prob = 1.0 - prob
    if outcome == 0:
        blocks[:, stride:] = 0.0
    else:
        blocks[:, :stride] = 0.0
    psi /= math.sqrt(prob)
    return outcome, prob


def measure_pauli_inplace(psi: np.ndarray, q: int, axis: int, rng: np.random.Generator) -> tuple[int, float]:
    if axis == 0:  # X
        rot = H
    elif axis == 1:  # Y; rot^dagger Z rot = Y
        rot = H @ S.conj().T
    elif axis == 2:  # Z
        rot = I2
    else:
        raise ValueError("axis must be 0,1,2")
    if axis != 2:
        apply_1q_inplace(psi, rot, q)
    outcome, prob = measure_z_inplace(psi, q, rng)
    if axis != 2:
        apply_1q_inplace(psi, rot.conj().T, q)
    return outcome, prob


def weak_measure_z_inplace(
    psi: np.ndarray, q: int, eta: float, rng: np.random.Generator
) -> tuple[int, float]:
    if not (0.0 <= eta <= 1.0):
        raise ValueError("eta outside [0,1]")
    stride = 1 << q
    period = stride << 1
    blocks = psi.reshape(-1, period)
    p0 = float(np.sum(np.abs(blocks[:, :stride]) ** 2))
    p1 = max(0.0, 1.0 - p0)
    prob_plus = 0.5 * ((1.0 + eta) * p0 + (1.0 - eta) * p1)
    outcome = 0 if rng.random() < prob_plus else 1
    if outcome == 0:
        a0 = math.sqrt((1.0 + eta) / 2.0)
        a1 = math.sqrt((1.0 - eta) / 2.0)
        prob = prob_plus
    else:
        a0 = math.sqrt((1.0 - eta) / 2.0)
        a1 = math.sqrt((1.0 + eta) / 2.0)
        prob = 1.0 - prob_plus
    blocks[:, :stride] *= a0
    blocks[:, stride:] *= a1
    if prob <= 1e-15:
        raise FloatingPointError("weak-measurement outcome has zero probability")
    psi /= math.sqrt(prob)
    return outcome, float(prob)


def schmidt_decomposition(psi: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    m = n // 2
    d = 1 << m
    norm = float(np.vdot(psi, psi).real)
    if not np.isfinite(norm) or norm <= 0:
        raise FloatingPointError(f"invalid norm {norm}")
    matrix = (psi / math.sqrt(norm)).reshape(-1, d).T
    # Use the conservative QR-based LAPACK driver throughout. Exact stabilizer
    # spectra contain large degeneracies that can occasionally stall divide-and-
    # conquer SVD implementations. Matrices here are at most 128x128.
    u, s, vh = sla.svd(matrix, full_matrices=False, lapack_driver="gesvd", check_finite=True)
    lam = np.square(np.clip(s.real, 0.0, None))
    lam /= lam.sum()
    return u, lam, vh


def reconstruct_from_schmidt(u: np.ndarray, vh: np.ndarray, mu: np.ndarray) -> np.ndarray:
    k = len(mu)
    matrix = (u[:, :k] * np.sqrt(mu)[None, :]) @ vh[:k, :]
    psi = matrix.T.reshape(-1)
    psi /= math.sqrt(float(np.vdot(psi, psi).real))
    return psi


def spectrum_entropy(lam: np.ndarray) -> float:
    x = np.asarray(lam, float)
    x = np.clip(x, 0.0, None)
    x /= x.sum()
    nz = x[x > 1e-15]
    return -float(np.sum(nz * np.log2(nz)))


def reduced_density_matrix(psi: np.ndarray, n: int, sites: Iterable[int]) -> np.ndarray:
    sites = list(sites)
    if len(set(sites)) != len(sites):
        raise ValueError("repeated site")
    selected_axes = [n - 1 - q for q in sites]
    rest_axes = [a for a in range(n) if a not in selected_axes]
    matrix = psi.reshape([2] * n).transpose(selected_axes + rest_axes).reshape(1 << len(sites), -1)
    rho = matrix @ matrix.conj().T
    return (rho + rho.conj().T) / 2.0


def subsystem_purity(psi: np.ndarray, n: int, sites: Iterable[int]) -> float:
    rho = reduced_density_matrix(psi, n, sites)
    return float(np.sum(np.abs(rho) ** 2).real)


def central_purity_after_gate(psi: np.ndarray, n: int, gate: np.ndarray) -> float:
    out = psi.copy()
    apply_adjacent_2q_inplace(out, gate, n // 2 - 1)
    m = n // 2
    d = 1 << m
    matrix = out.reshape(-1, d).T
    rho = matrix @ matrix.conj().T
    return float(np.sum(np.abs(rho) ** 2).real)


def local_two_copy_swaps() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    mats = []
    for which in ("I", "a", "b", "ab"):
        mat = np.zeros((16, 16), dtype=np.complex128)
        for pair1 in range(4):
            for pair2 in range(4):
                a1, b1 = pair1 % 2, pair1 // 2
                a2, b2 = pair2 % 2, pair2 // 2
                if which == "I":
                    na1, nb1, na2, nb2 = a1, b1, a2, b2
                elif which == "a":
                    na1, nb1, na2, nb2 = a2, b1, a1, b2
                elif which == "b":
                    na1, nb1, na2, nb2 = a1, b2, a2, b1
                else:
                    na1, nb1, na2, nb2 = a2, b2, a1, b1
                new1 = na1 + 2 * nb1
                new2 = na2 + 2 * nb2
                mat[new1 * 4 + new2, pair1 * 4 + pair2] = 1.0
        mats.append(mat)
    return tuple(mats)  # type: ignore[return-value]


SWAP_BASIS = local_two_copy_swaps()
SWAP_GRAM = np.asarray(
    [[np.trace(a.conj().T @ b) for b in SWAP_BASIS] for a in SWAP_BASIS],
    dtype=np.complex128,
)


def locally_dressed_response_coefficients(v: np.ndarray) -> np.ndarray:
    """Exact coefficients after independent local two-copy twirls on the input."""
    vv = np.kron(v, v)
    x = vv.conj().T @ SWAP_BASIS[1] @ vv
    rhs = np.asarray([np.trace(b.conj().T @ x) for b in SWAP_BASIS], dtype=np.complex128)
    coeff = np.linalg.solve(SWAP_GRAM, rhs)
    coeff = np.real_if_close(coeff, tol=1000).astype(float)
    return coeff


def probe_coefficients() -> dict[str, np.ndarray]:
    haar = np.asarray([0.4, 0.0, 0.0, 0.4], dtype=float)
    xy = locally_dressed_response_coefficients(cartan_gate(math.pi / 8, math.pi / 8, 0.0))
    xx = locally_dressed_response_coefficients(cartan_gate(math.pi / 4, 0.0, 0.0))
    return {
        "haar_or_clifford_2design": haar,
        "cartan_xy_pi8": xy,
        "cartan_xx_pi4": xx,
    }


PROBE_COEFFS = probe_coefficients()


def stencil_purities(psi: np.ndarray, n: int, central_purity: float) -> dict[str, float]:
    m = n // 2
    p_l = subsystem_purity(psi, n, range(0, m - 1))
    p_r = subsystem_purity(psi, n, range(m + 1, n))
    p_lb = subsystem_purity(psi, n, list(range(0, m - 1)) + [m])
    return {
        "P_L": p_l,
        "P_A": float(central_purity),
        "P_Lb": p_lb,
        "P_R": p_r,
    }


def response_from_stencil(stencil: dict[str, float], n: int, coeff: np.ndarray) -> tuple[float, float]:
    vals = np.asarray([stencil["P_L"], stencil["P_A"], stencil["P_Lb"], stencil["P_R"]], float)
    post = float(np.dot(coeff, vals))
    d = 1 << (n // 2)
    delta = d / (d - 1.0) * (stencil["P_A"] - post)
    return post, float(delta)


def fixed_floquet_gates(n: int, base_seed: int) -> dict[int, np.ndarray]:
    # A generic non-Clifford Cartan entangler with fixed quenched local dressings.
    v = cartan_gate(0.37, 0.23, 0.11)
    gates: dict[int, np.ndarray] = {}
    for q in range(n - 1):
        rng = np.random.default_rng(stable_seed("checkpoint04_floquet_gate", base_seed, n, q))
        left = np.kron(haar_unitary(2, rng), haar_unitary(2, rng))
        right = np.kron(haar_unitary(2, rng), haar_unitary(2, rng))
        gates[q] = left @ v @ right
    return gates


def family_gate(family: str, rng: np.random.Generator, q: int, floquet: dict[int, np.ndarray]) -> np.ndarray:
    if family.startswith("haar_"):
        return haar_unitary(4, rng)
    if family == "clifford_z":
        return sample_two_qubit_clifford(rng)
    if family == "floquet_cartan_z":
        return floquet[q]
    raise ValueError(f"unknown family {family}")


def apply_monitoring(
    psi: np.ndarray,
    n: int,
    p: float,
    family: str,
    rng: np.random.Generator,
) -> tuple[int, int]:
    selected = np.flatnonzero(rng.random(n) < p).tolist()
    cut = n // 2
    cut_count = sum(q in (cut - 1, cut) for q in selected)
    if family in ("haar_z", "clifford_z", "floquet_cartan_z"):
        for q in selected:
            measure_z_inplace(psi, int(q), rng)
    elif family == "haar_random_pauli":
        for q in selected:
            axis = int(rng.integers(3))
            measure_pauli_inplace(psi, int(q), axis, rng)
    elif family == "haar_weak_z_eta06":
        for q in selected:
            weak_measure_z_inplace(psi, int(q), 0.6, rng)
    else:
        raise ValueError(f"unknown family {family}")
    return len(selected), cut_count


def evolve_probe_states(
    family: str,
    n: int,
    p: float,
    trajectory_index: int,
    probe_taus: tuple[float, ...],
    base_seed: int,
) -> list[tuple[float, np.ndarray, int, int]]:
    seed = stable_seed("checkpoint04_trajectory", base_seed, family, n, p, trajectory_index)
    rng = np.random.default_rng(seed)
    psi = random_product_state(n, rng)
    floquet = fixed_floquet_gates(n, base_seed) if family == "floquet_cartan_z" else {}
    max_step = int(round(max(probe_taus) * n))
    probe_steps = {int(round(tau * n)): tau for tau in probe_taus}
    saved: list[tuple[float, np.ndarray, int, int]] = []
    measurement_count = 0
    cut_measurement_count = 0
    for cycle in range(1, max_step + 1):
        parity_order = (0, 1) if cycle % 2 else (1, 0)
        for parity in parity_order:
            for q in range(parity, n - 1, 2):
                gate = family_gate(family, rng, q, floquet)
                apply_adjacent_2q_inplace(psi, gate, q)
        mcount, ccount = apply_monitoring(psi, n, p, family, rng)
        measurement_count += mcount
        cut_measurement_count += ccount
        if cycle in probe_steps:
            saved.append((probe_steps[cycle], psi.copy(), measurement_count, cut_measurement_count))
    norm = float(np.vdot(psi, psi).real)
    if abs(norm - 1.0) > 5e-10:
        raise RuntimeError(f"norm failure {family=} {n=} {p=} {trajectory_index=}: {norm}")
    return saved


def spectrum_worker(task: tuple[str, int, float, int, tuple[float, ...], int]) -> list[dict[str, Any]]:
    family, n, p, tr, probe_taus, base_seed = task
    out: list[dict[str, Any]] = []
    for tau, psi, mcount, ccount in evolve_probe_states(family, n, p, tr, probe_taus, base_seed):
        _, lam, _ = schmidt_decomposition(psi, n)
        out.append({
            "family": family,
            "n": n,
            "p_measure": p,
            "trajectory_index": tr,
            "tau": tau,
            "rank_1e12": int(np.sum(lam > 1e-12)),
            "measurements_to_probe": mcount,
            "cut_measurements_to_probe": ccount,
            "spectrum": lam,
        })
    return out


def process_variant(
    psi: np.ndarray,
    n: int,
    variant: str,
    lam: np.ndarray,
) -> dict[str, Any]:
    purity = float(np.sum(lam * lam))
    stencil = stencil_purities(psi, n, purity)
    row: dict[str, Any] = {
        "variant": variant,
        "pre_purity": purity,
        "pre_entropy_bits": spectrum_entropy(lam),
        "pre_lambda1": float(lam[0]),
        "pre_lambda2": float(lam[1]) if len(lam) > 1 else 0.0,
        **stencil,
        "neighboring_cut_purity_sum": stencil["P_L"] + stencil["P_R"],
        "boundary_noncontiguous_purity": stencil["P_Lb"],
    }
    for name, coeff in PROBE_COEFFS.items():
        post, delta = response_from_stencil(stencil, n, coeff)
        row[f"probe_{name}_post_purity"] = post
        row[f"probe_{name}_delta_linear_norm"] = delta
    return row


def main_worker(task: tuple[Any, ...]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    family, n, p, tr, probe_taus, base_seed, split_cut, reference_spectra, equalize_rank = task
    split = "discovery" if tr < split_cut else "confirmatory"
    state_rows: list[dict[str, Any]] = []
    spectrum_rows: list[dict[str, Any]] = []
    trajectory_id = f"{family}|n{n}|p{p:.5f}|tr{tr}"
    for tau, psi, mcount, ccount in evolve_probe_states(family, n, p, tr, probe_taus, base_seed):
        u, lam, vh = schmidt_decomposition(psi, n)
        rank = int(np.sum(lam > 1e-12))
        state_id = f"{trajectory_id}|tau{tau:g}"
        spectrum_rows.append({
            "state_id": state_id,
            "family": family,
            "n": n,
            "p_measure": p,
            "trajectory_index": tr,
            "tau": tau,
            "split": split,
            "rank_1e12": rank,
            "spectrum": lam,
        })
        common = {
            "state_id": state_id,
            "trajectory_id": trajectory_id,
            "family": family,
            "n": n,
            "p_measure": p,
            "trajectory_index": tr,
            "tau": tau,
            "split": split,
            "rank_1e12": rank,
            "measurements_to_probe": mcount,
            "cut_measurements_to_probe": ccount,
            "measurements_per_site_time": mcount / (n * tau),
            "cut_measurements_per_time": ccount / tau,
        }
        original = process_variant(psi, n, "original", lam)
        state_rows.append({**common, **original})
        if rank >= equalize_rank:
            mu = np.asarray(reference_spectra[(family, n, tau)], float)
            eqpsi = reconstruct_from_schmidt(u, vh, mu)
            eq_lam = np.zeros_like(lam)
            eq_lam[:equalize_rank] = mu
            equalized = process_variant(eqpsi, n, f"equalized_rank{equalize_rank}", eq_lam)
            state_rows.append({**common, **equalized})
    return state_rows, spectrum_rows


def run_parallel(tasks: list[tuple[Any, ...]], worker, workers: int, progress_every: int, label: str):
    outputs = []
    started = time.time()
    if workers == 1:
        for i, task in enumerate(tasks, start=1):
            try:
                outputs.append(worker(task))
            except Exception as exc:
                raise RuntimeError(f"{label} task failed: {task[:6]}") from exc
            if progress_every and (i % progress_every == 0 or i == len(tasks)):
                print(f"[{label}] {i}/{len(tasks)} in {time.time()-started:.1f}s", flush=True)
        return outputs
    # Use spawn rather than fork because validation has already called LAPACK/BLAS.
    import multiprocessing as mp
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as ex:
        futures = {ex.submit(worker, task): task for task in tasks}
        for i, fut in enumerate(as_completed(futures), start=1):
            task = futures[fut]
            try:
                outputs.append(fut.result())
            except Exception as exc:
                raise RuntimeError(f"{label} task failed: {task[:6]}") from exc
            if progress_every and (i % progress_every == 0 or i == len(futures)):
                print(f"[{label}] {i}/{len(futures)} in {time.time()-started:.1f}s", flush=True)
    return outputs


def validate_response_operator(rng: np.random.Generator) -> dict[str, Any]:
    n = 8
    psi = random_product_state(n, rng)
    # Scramble state before probing.
    for parity in (0, 1):
        for q in range(parity, n - 1, 2):
            apply_adjacent_2q_inplace(psi, haar_unitary(4, rng), q)
    _, lam, _ = schmidt_decomposition(psi, n)
    stencil = stencil_purities(psi, n, float(np.sum(lam * lam)))
    results: dict[str, Any] = {}
    for name, params in {
        "cartan_xy_pi8": (math.pi / 8, math.pi / 8, 0.0),
        "cartan_xx_pi4": (math.pi / 4, 0.0, 0.0),
    }.items():
        v = cartan_gate(*params)
        coeff = PROBE_COEFFS[name]
        expected_post = response_from_stencil(stencil, n, coeff)[0]
        vals = []
        for _ in range(3000):
            vin = np.kron(haar_unitary(2, rng), haar_unitary(2, rng))
            gate = v @ vin
            vals.append(central_purity_after_gate(psi, n, gate))
        vals_arr = np.asarray(vals, float)
        mean = float(vals_arr.mean())
        se = float(vals_arr.std(ddof=1) / math.sqrt(len(vals_arr)))
        results[name] = {
            "coefficients_I_Fa_Fb_Fab": coeff.tolist(),
            "formula_post_purity": expected_post,
            "monte_carlo_post_purity": mean,
            "monte_carlo_se": se,
            "z_score": (mean - expected_post) / se,
        }
    return results


def validation_suite() -> dict[str, Any]:
    rng = np.random.default_rng(2026081804)
    unitary_errors = []
    for _ in range(32):
        for gate in (haar_unitary(4, rng), sample_two_qubit_clifford(rng)):
            unitary_errors.append(float(np.max(np.abs(gate.conj().T @ gate - I4))))
    # Exact class-average response of the two-qubit Clifford group.
    canonical_coeffs = np.asarray([
        locally_dressed_response_coefficients(I4),
        locally_dressed_response_coefficients(cartan_gate(math.pi / 4, 0, 0)),
        locally_dressed_response_coefficients(cartan_gate(math.pi / 4, math.pi / 4, 0)),
        locally_dressed_response_coefficients(cartan_gate(math.pi / 4, math.pi / 4, math.pi / 4)),
    ])
    clifford_coeff = CLIFFORD_CLASS_PROBS @ canonical_coeffs
    response_validation = validate_response_operator(rng)

    measurement_norm_errors = []
    for family in ("haar_z", "haar_random_pauli", "haar_weak_z_eta06"):
        for _ in range(20):
            psi = random_product_state(6, rng)
            if family == "haar_z":
                measure_z_inplace(psi, 2, rng)
            elif family == "haar_random_pauli":
                measure_pauli_inplace(psi, 2, int(rng.integers(3)), rng)
            else:
                weak_measure_z_inplace(psi, 2, 0.6, rng)
            measurement_norm_errors.append(abs(float(np.vdot(psi, psi).real) - 1.0))

    psi = random_product_state(8, rng)
    for q in range(7):
        apply_adjacent_2q_inplace(psi, haar_unitary(4, rng), q)
    u, lam, vh = schmidt_decomposition(psi, 8)
    mu = np.asarray([0.4, 0.3, 0.2, 0.1])
    eq = reconstruct_from_schmidt(u, vh, mu)
    _, lam_eq, _ = schmidt_decomposition(eq, 8)
    equalization_error = float(np.max(np.abs(lam_eq[:4] - mu)))
    equalization_tail = float(np.sum(lam_eq[4:]))

    max_response_z = max(abs(v["z_score"]) for v in response_validation.values())
    passes = bool(
        len(LOCAL_CLIFFORDS) == 24
        and max(unitary_errors) < 2e-12
        and np.max(np.abs(clifford_coeff - PROBE_COEFFS["haar_or_clifford_2design"])) < 2e-12
        and max(measurement_norm_errors) < 2e-12
        and equalization_error < 2e-12
        and equalization_tail < 2e-12
        and max_response_z < 5.0
    )
    return {
        "single_qubit_clifford_count": len(LOCAL_CLIFFORDS),
        "max_two_qubit_unitarity_error": max(unitary_errors),
        "clifford_class_average_coefficients": clifford_coeff.tolist(),
        "haar_coefficients": PROBE_COEFFS["haar_or_clifford_2design"].tolist(),
        "clifford_2design_coefficient_max_abs_error": float(np.max(np.abs(clifford_coeff - PROBE_COEFFS["haar_or_clifford_2design"]))),
        "max_measurement_norm_error": max(measurement_norm_errors),
        "equalization_top4_max_abs_error": equalization_error,
        "equalization_tail_weight": equalization_tail,
        "response_operator_validation": response_validation,
        "passes": passes,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--families", nargs="+", default=list(FAMILIES))
    ap.add_argument("--sizes", type=int, nargs="+", default=[10, 12, 14])
    ap.add_argument("--p-values", type=float, nargs="+", default=[0.08, 0.16, 0.24])
    ap.add_argument("--trajectories", type=int, default=24)
    ap.add_argument("--discovery-trajectories", type=int, default=12)
    ap.add_argument("--probe-taus", type=float, nargs="+", default=[6.0, 8.0])
    ap.add_argument("--equalize-rank", type=int, default=4)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--base-seed", type=int, default=2026081804)
    ap.add_argument("--progress-every", type=int, default=25)
    args = ap.parse_args()

    if not (0 < args.discovery_trajectories < args.trajectories):
        raise ValueError("invalid discovery split")
    unknown = set(args.families) - set(FAMILIES)
    if unknown:
        raise ValueError(f"unknown families: {unknown}")
    args.outdir.mkdir(parents=True, exist_ok=True)
    probe_taus = tuple(float(x) for x in args.probe_taus)

    validation = validation_suite()
    (args.outdir / "validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    if not validation["passes"]:
        raise RuntimeError(f"validation failed: {validation}")
    print(json.dumps(validation, indent=2), flush=True)

    discovery_tasks = [
        (family, n, p, tr, probe_taus, args.base_seed)
        for family in args.families
        for n in args.sizes
        for p in args.p_values
        for tr in range(args.discovery_trajectories)
    ]
    discovery_outputs = run_parallel(
        discovery_tasks, spectrum_worker, args.workers, args.progress_every, "discovery"
    )
    discovery_rows = [row for part in discovery_outputs for row in part]
    max_d = 1 << (max(args.sizes) // 2)
    discovery_meta: list[dict[str, Any]] = []
    discovery_spectra: list[np.ndarray] = []
    for row0 in discovery_rows:
        row = dict(row0)
        lam = row.pop("spectrum")
        padded = np.zeros(max_d, dtype=float)
        padded[: len(lam)] = lam
        discovery_meta.append(row)
        discovery_spectra.append(padded)
    discovery_meta_df = pd.DataFrame(discovery_meta)
    discovery_spectra_arr = np.asarray(discovery_spectra, float)
    discovery_meta_df.to_csv(args.outdir / "discovery_spectrum_metadata.csv.gz", index=False, compression="gzip")
    np.savez_compressed(args.outdir / "discovery_spectra.npz", spectra=discovery_spectra_arr)

    references: dict[tuple[str, int, float], list[float]] = {}
    ref_rows = []
    for family in args.families:
        for n in args.sizes:
            for tau in probe_taus:
                mask = (
                    (discovery_meta_df.family == family)
                    & (discovery_meta_df.n == n)
                    & np.isclose(discovery_meta_df.tau, tau)
                    & (discovery_meta_df.rank_1e12 >= args.equalize_rank)
                )
                idx = np.flatnonzero(mask.to_numpy())
                if len(idx) == 0:
                    raise RuntimeError(f"no rank-{args.equalize_rank} discovery states for {(family,n,tau)}")
                top = discovery_spectra_arr[idx, :args.equalize_rank]
                top = top / top.sum(axis=1, keepdims=True)
                mu = top.mean(axis=0)
                mu /= mu.sum()
                references[(family, n, tau)] = mu.tolist()
                sub = discovery_meta_df.iloc[idx]
                counts = sub.groupby("p_measure").size().to_dict()
                ref_rows.append({
                    "family": family,
                    "n": n,
                    "tau": tau,
                    "states_used": len(idx),
                    "minimum_per_p": int(min(counts.values())),
                    "counts_by_p": json.dumps({str(k): int(v) for k, v in counts.items()}, sort_keys=True),
                    "reference_spectrum": json.dumps(mu.tolist()),
                    "reference_purity": float(np.sum(mu * mu)),
                    "reference_entropy_bits": spectrum_entropy(mu),
                })
    pd.DataFrame(ref_rows).to_csv(args.outdir / "equalization_reference_spectra.csv", index=False)
    serial_refs = {f"{f}|n{n}|tau{tau:g}": v for (f, n, tau), v in references.items()}
    (args.outdir / "equalization_reference_spectra.json").write_text(json.dumps(serial_refs, indent=2), encoding="utf-8")

    tasks = [
        (family, n, p, tr, probe_taus, args.base_seed, args.discovery_trajectories, references, args.equalize_rank)
        for family in args.families
        for n in args.sizes
        for p in args.p_values
        for tr in range(args.trajectories)
    ]
    outputs = run_parallel(tasks, main_worker, args.workers, args.progress_every, "main")
    state_rows = [row for part, _ in outputs for row in part]
    spectrum_rows0 = [row for _, part in outputs for row in part]
    state_df = pd.DataFrame(state_rows).sort_values(
        ["family", "n", "p_measure", "trajectory_index", "tau", "variant"]
    )
    state_df.to_csv(args.outdir / "state_response_rows.csv.gz", index=False, compression="gzip")

    spectrum_meta = []
    spectrum_arr = []
    for row0 in spectrum_rows0:
        row = dict(row0)
        lam = row.pop("spectrum")
        padded = np.zeros(max_d, dtype=float)
        padded[: len(lam)] = lam
        spectrum_meta.append(row)
        spectrum_arr.append(padded)
    spectrum_meta_df0 = pd.DataFrame(spectrum_meta)
    order = spectrum_meta_df0.sort_values(
        ["family", "n", "p_measure", "trajectory_index", "tau"]
    ).index.to_numpy()
    spectrum_meta_df = spectrum_meta_df0.iloc[order].reset_index(drop=True)
    spectrum_arr_np = np.asarray(spectrum_arr, float)[order]
    spectrum_meta_df.to_csv(args.outdir / "physical_spectrum_metadata.csv.gz", index=False, compression="gzip")
    np.savez_compressed(args.outdir / "physical_spectra.npz", spectra=spectrum_arr_np)

    coeff_rows = []
    for name, coeff in PROBE_COEFFS.items():
        coeff_rows.append({
            "probe": name,
            "c_I": coeff[0],
            "c_Fa": coeff[1],
            "c_Fb": coeff[2],
            "c_Fab": coeff[3],
            "coefficient_sum": float(coeff.sum()),
        })
    pd.DataFrame(coeff_rows).to_csv(args.outdir / "probe_response_coefficients.csv", index=False)

    manifest = {
        "model_warning": "Independent Checkpoint 04 simulator; not the unavailable original generator.",
        "families": args.families,
        "sizes": args.sizes,
        "p_values": args.p_values,
        "trajectories_per_cell": args.trajectories,
        "discovery_trajectories_per_cell": args.discovery_trajectories,
        "confirmatory_trajectories_per_cell": args.trajectories - args.discovery_trajectories,
        "probe_taus": list(probe_taus),
        "equalization_rank": args.equalize_rank,
        "base_seed": args.base_seed,
        "workers": args.workers,
        "state_response_rows": len(state_df),
        "physical_state_count": len(spectrum_meta_df),
        "probe_coefficients": {k: v.tolist() for k, v in PROBE_COEFFS.items()},
        "qubit_order": "little endian; central cut between n/2-1 and n/2",
        "validation": validation,
    }
    (args.outdir / "simulation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2), flush=True)


if __name__ == "__main__":
    main()
