#!/usr/bin/env python3
"""Shared simulation and response-operator utilities for Checkpoint 04.

Conventions
-----------
State-vector indices are little endian: qubit q is bit q.  For n=2m, the
central cut is between q=m-1 and q=m.  In 4x4 adjacent gates the computational
basis order is |q+1,q> = |00>,|01>,|10>,|11>.
"""
from __future__ import annotations

import hashlib
import math
import os
from pathlib import Path
from typing import Iterable

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import numpy as np
import scipy.linalg as sla

I2 = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
H = np.array([[1, 1], [1, -1]], dtype=np.complex128) / math.sqrt(2.0)
S = np.diag([1.0, 1.0j]).astype(np.complex128)
SDG = S.conj().T
PAULIS = (X, Y, Z)

_CLIFFORD_GATES: np.ndarray | None = None


def stable_seed(*items: object) -> int:
    raw = repr(items).encode("utf-8")
    return int.from_bytes(hashlib.blake2b(raw, digest_size=8).digest(), "little") & 0xFFFFFFFF


def haar_unitary(dim: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(z)
    diag = np.diag(r)
    phases = np.divide(diag, np.abs(diag), out=np.ones_like(diag), where=np.abs(diag) > 0)
    return q * phases.conj()


def load_clifford_gates(path: str | Path) -> np.ndarray:
    global _CLIFFORD_GATES
    if _CLIFFORD_GATES is None:
        arr = np.load(Path(path))["gates"]
        if arr.shape != (11520, 4, 4):
            raise ValueError(f"Unexpected two-qubit Clifford table shape: {arr.shape}")
        _CLIFFORD_GATES = np.asarray(arr, dtype=np.complex128)
    return _CLIFFORD_GATES


def apply_adjacent_2q_inplace(psi: np.ndarray, gate: np.ndarray, q: int) -> None:
    """Apply gate to adjacent little-endian qubits q (low) and q+1 (high)."""
    stride = 1 << q
    period = stride << 2
    blocks = psi.reshape(-1, period)
    v = np.stack([blocks[:, i * stride:(i + 1) * stride].copy() for i in range(4)], axis=1)
    out = np.einsum("ij,bjs->bis", gate, v, optimize=True)
    for i in range(4):
        blocks[:, i * stride:(i + 1) * stride] = out[:, i, :]


def apply_1q_inplace(psi: np.ndarray, gate: np.ndarray, q: int) -> None:
    stride = 1 << q
    period = stride << 1
    blocks = psi.reshape(-1, period)
    a = blocks[:, :stride].copy()
    b = blocks[:, stride:].copy()
    blocks[:, :stride] = gate[0, 0] * a + gate[0, 1] * b
    blocks[:, stride:] = gate[1, 0] * a + gate[1, 1] * b


def random_product_state(n: int, rng: np.random.Generator) -> np.ndarray:
    psi = np.array([1.0 + 0.0j])
    for _ in range(n):
        u, v = rng.random(2)
        theta = math.acos(1.0 - 2.0 * u)
        phi = 2.0 * math.pi * v
        a0 = math.cos(theta / 2.0)
        a1 = np.exp(1j * phi) * math.sin(theta / 2.0)
        psi = np.concatenate([a0 * psi, a1 * psi])
    return np.asarray(psi, dtype=np.complex128)


def random_stabilizer_product_state(n: int, rng: np.random.Generator) -> np.ndarray:
    single = [
        np.array([1, 0], complex), np.array([0, 1], complex),
        np.array([1, 1], complex) / math.sqrt(2), np.array([1, -1], complex) / math.sqrt(2),
        np.array([1, 1j], complex) / math.sqrt(2), np.array([1, -1j], complex) / math.sqrt(2),
    ]
    psi = np.array([1.0 + 0.0j])
    for _ in range(n):
        v = single[int(rng.integers(0, len(single)))]
        psi = np.concatenate([v[0] * psi, v[1] * psi])
    return np.asarray(psi, dtype=np.complex128)


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


def measure_pauli_inplace(psi: np.ndarray, q: int, pauli_index: int, rng: np.random.Generator) -> tuple[int, float]:
    """Projectively measure X (0), Y (1), or Z (2), retaining original basis."""
    if pauli_index == 0:
        basis = H
    elif pauli_index == 1:
        basis = H @ SDG
    elif pauli_index == 2:
        basis = I2
    else:
        raise ValueError("pauli_index must be 0, 1, or 2")
    apply_1q_inplace(psi, basis, q)
    outcome, prob = measure_z_inplace(psi, q, rng)
    apply_1q_inplace(psi, basis.conj().T, q)
    return outcome, prob


def weak_z_measure_inplace(psi: np.ndarray, q: int, eta: float, rng: np.random.Generator) -> tuple[int, float]:
    """Apply the two-outcome POVM E_s=(I+s eta Z)/2, 0<=eta<=1."""
    if not (0.0 <= eta <= 1.0):
        raise ValueError("weak-measurement eta must lie in [0,1]")
    stride = 1 << q
    period = stride << 1
    blocks = psi.reshape(-1, period)
    pop0 = float(np.sum(np.abs(blocks[:, :stride]) ** 2))
    pop1 = 1.0 - pop0
    p_plus = 0.5 * ((1.0 + eta) * pop0 + (1.0 - eta) * pop1)
    p_plus = min(1.0, max(0.0, p_plus))
    outcome = 1 if rng.random() < p_plus else -1
    prob = p_plus if outcome == 1 else 1.0 - p_plus
    if prob <= 1e-15:
        outcome *= -1
        prob = 1.0 - prob
    if outcome == 1:
        f0 = math.sqrt((1.0 + eta) / 2.0)
        f1 = math.sqrt((1.0 - eta) / 2.0)
    else:
        f0 = math.sqrt((1.0 - eta) / 2.0)
        f1 = math.sqrt((1.0 + eta) / 2.0)
    blocks[:, :stride] *= f0
    blocks[:, stride:] *= f1
    psi /= math.sqrt(prob)
    return outcome, prob


def sample_two_qubit_gate(
    family: str,
    rng: np.random.Generator,
    clifford_path: str | Path,
    xx_theta: float = math.pi / 4.0,
) -> np.ndarray:
    if family == "haar":
        return haar_unitary(4, rng)
    if family == "clifford":
        gates = load_clifford_gates(clifford_path)
        return gates[int(rng.integers(0, len(gates)))]
    if family == "xx_local":
        v = math.cos(xx_theta) * np.eye(4, dtype=np.complex128) - 1j * math.sin(xx_theta) * np.kron(X, X)
        pre = np.kron(haar_unitary(2, rng), haar_unitary(2, rng))
        post = np.kron(haar_unitary(2, rng), haar_unitary(2, rng))
        return post @ v @ pre
    raise ValueError(f"Unknown gate family: {family}")


def apply_measurement_protocol(
    psi: np.ndarray,
    q: int,
    protocol: str,
    rng: np.random.Generator,
    weak_eta: float = 0.75,
) -> tuple[int, float, int]:
    if protocol == "z_projective":
        out, prob = measure_z_inplace(psi, q, rng)
        return out, prob, 2
    if protocol == "random_pauli":
        basis = int(rng.integers(0, 3))
        out, prob = measure_pauli_inplace(psi, q, basis, rng)
        return out, prob, basis
    if protocol == "weak_z":
        out, prob = weak_z_measure_inplace(psi, q, weak_eta, rng)
        return out, prob, 2
    raise ValueError(f"Unknown measurement protocol: {protocol}")


def schmidt_decomposition(psi: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    m = n // 2
    da = 1 << m
    norm = float(np.vdot(psi, psi).real)
    if not np.isfinite(norm) or norm <= 0:
        raise FloatingPointError(f"Invalid state norm: {norm}")
    matrix = (psi / math.sqrt(norm)).reshape(-1, da).T
    U, s, Vh = sla.svd(matrix, full_matrices=False, lapack_driver="gesvd", check_finite=True)
    lam = np.square(np.clip(s.real, 0.0, None))
    lam /= lam.sum()
    return U, lam, Vh


def reconstruct_from_schmidt(U: np.ndarray, Vh: np.ndarray, mu: np.ndarray) -> np.ndarray:
    k = len(mu)
    matrix = (U[:, :k] * np.sqrt(mu)[None, :]) @ Vh[:k, :]
    psi = matrix.T.reshape(-1)
    psi /= math.sqrt(float(np.vdot(psi, psi).real))
    return psi


def spectrum_metrics(lam: np.ndarray) -> dict[str, float]:
    lam = np.clip(np.asarray(lam, float), 0.0, None)
    lam /= lam.sum()
    nz = lam[lam > 1e-15]
    d = len(lam)
    purity = float(np.sum(lam * lam))
    entropy = -float(np.sum(nz * np.log2(nz)))
    return {
        "purity": purity,
        "entropy_bits": entropy,
        "entropy_norm": entropy / math.log2(d),
        "rank_1e12": int(np.sum(lam > 1e-12)),
        "lambda1": float(lam[0]),
        "lambda2": float(lam[1]) if d > 1 else 0.0,
    }


def subset_purity(psi: np.ndarray, n: int, sites: Iterable[int]) -> float:
    sites = list(sites)
    if len(set(sites)) != len(sites):
        raise ValueError("Repeated site in subset")
    axes = [n - 1 - q for q in sites]
    rest = [a for a in range(n) if a not in axes]
    mat = psi.reshape([2] * n).transpose(axes + rest).reshape(1 << len(sites), -1)
    if mat.shape[0] <= mat.shape[1]:
        rho = mat @ mat.conj().T
    else:
        rho = mat.conj().T @ mat
    return float(np.sum(np.abs(rho) ** 2).real)


def purity_stencil(psi: np.ndarray, n: int, central_purity: float | None = None) -> dict[str, float]:
    m = n // 2
    p_left = subset_purity(psi, n, range(0, m - 1))
    p_center = subset_purity(psi, n, range(0, m)) if central_purity is None else float(central_purity)
    p_right = subset_purity(psi, n, range(0, m + 1))
    p_cross = subset_purity(psi, n, list(range(0, m - 1)) + [m])
    return {
        "P_left": p_left,
        "P_center": p_center,
        "P_right": p_right,
        "P_cross": p_cross,
        "Q_neighbor": p_left + p_right,
    }


def response_haar_linear(stencil: dict[str, float], n: int) -> float:
    d = 1 << (n // 2)
    return d / (d - 1.0) * (stencil["P_center"] - 0.4 * stencil["Q_neighbor"])


def xx_twirl_coefficients(theta: float) -> dict[str, float]:
    s = math.sin(2.0 * theta) ** 2
    return {
        "P_left": 4.0 * s / 9.0,
        "P_center": 1.0 - 8.0 * s / 9.0,
        "P_cross": -2.0 * s / 9.0,
        "P_right": 4.0 * s / 9.0,
    }


def response_xx_twirl_linear(stencil: dict[str, float], n: int, theta: float) -> float:
    c = xx_twirl_coefficients(theta)
    post_purity = sum(c[key] * stencil[key] for key in c)
    d = 1 << (n // 2)
    return d / (d - 1.0) * (stencil["P_center"] - post_purity)


def evolve_probe_states(
    *,
    n: int,
    p: float,
    trajectory_index: int,
    probe_taus: tuple[float, ...],
    base_seed: int,
    dynamics_gate: str,
    measurement_protocol: str,
    clifford_path: str | Path,
    initial_state: str = "haar_product",
    weak_eta: float = 0.75,
    xx_theta: float = math.pi / 4.0,
) -> list[tuple[float, np.ndarray, int, int]]:
    seed = stable_seed(
        "checkpoint04_trajectory", base_seed, dynamics_gate, measurement_protocol,
        initial_state, n, p, trajectory_index,
    )
    rng = np.random.default_rng(seed)
    if initial_state == "haar_product":
        psi = random_product_state(n, rng)
    elif initial_state == "stabilizer_product":
        psi = random_stabilizer_product_state(n, rng)
    else:
        raise ValueError(f"Unknown initial state family: {initial_state}")
    max_step = int(round(max(probe_taus) * n))
    probe_steps = {int(round(tau * n)): tau for tau in probe_taus}
    saved = []
    measurement_count = 0
    cut_measurement_count = 0
    m = n // 2
    for cycle in range(1, max_step + 1):
        parity_order = (0, 1) if rng.random() < 0.5 else (1, 0)
        for parity in parity_order:
            for q in range(parity, n - 1, 2):
                gate = sample_two_qubit_gate(dynamics_gate, rng, clifford_path, xx_theta=xx_theta)
                apply_adjacent_2q_inplace(psi, gate, q)
        selected = np.flatnonzero(rng.random(n) < p).tolist()
        measurement_count += len(selected)
        cut_measurement_count += sum(q in (m - 1, m) for q in selected)
        for q in selected:
            apply_measurement_protocol(psi, int(q), measurement_protocol, rng, weak_eta=weak_eta)
        if cycle in probe_steps:
            saved.append((probe_steps[cycle], psi.copy(), measurement_count, cut_measurement_count))
    norm = float(np.vdot(psi, psi).real)
    if abs(norm - 1.0) > 5e-10:
        raise RuntimeError(f"Norm failure: {norm}")
    return saved
