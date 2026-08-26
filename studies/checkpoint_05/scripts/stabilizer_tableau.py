#!/usr/bin/env python3
"""Bit-packed phase-free stabilizer simulator for monitored Clifford circuits.

The simulator tracks the n-dimensional binary stabilizer row space. Stabilizer
signs are omitted because all observables in Checkpoint 05 depend only on the
Pauli support subspace: bipartite stabilizer entropies, Schmidt ranks, and the
response-purity stencil. Projective Pauli outcomes change signs but not this
subspace.

Representation
--------------
``cols[c, w]`` stores column ``c`` of the n x 2n binary generator matrix as a
bitset over generator rows. Columns 0..n-1 are X bits and n..2n-1 are Z bits.
This makes Clifford column transformations word-parallel.
"""
from __future__ import annotations

import math
from typing import Iterable

import numpy as np
from numba import njit

U64 = np.uint64
MASK64 = U64(0xFFFFFFFFFFFFFFFF)


@njit(cache=True, inline='always')
def _rng_next(state: np.uint64) -> tuple[np.uint64, np.uint64]:
    """SplitMix64 step; returns (new_state, random_word)."""
    state = U64(state + U64(0x9E3779B97F4A7C15))
    z = state
    z = U64((z ^ (z >> U64(30))) * U64(0xBF58476D1CE4E5B9))
    z = U64((z ^ (z >> U64(27))) * U64(0x94D049BB133111EB))
    z = U64(z ^ (z >> U64(31)))
    return state, z


@njit(cache=True, inline='always')
def _rand_float01(state: np.uint64) -> tuple[np.uint64, float]:
    state, r = _rng_next(state)
    x = float(r >> U64(11)) * (1.0 / 9007199254740992.0)
    return state, x


@njit(cache=True, inline='always')
def _xor4(mask: int, a: np.uint64, b: np.uint64, c: np.uint64, d: np.uint64) -> np.uint64:
    out = U64(0)
    if mask & 1:
        out ^= a
    if mask & 2:
        out ^= b
    if mask & 4:
        out ^= c
    if mask & 8:
        out ^= d
    return out


@njit(cache=True)
def initialize_product_tableau(n: int, seed: np.uint64) -> tuple[np.ndarray, np.uint64]:
    """Random single-qubit stabilizer product state, ignoring eigenvalue signs."""
    words = (n + 63) // 64
    cols = np.zeros((2 * n, words), dtype=np.uint64)
    state = seed
    for q in range(n):
        state, r = _rng_next(state)
        axis = int(r % U64(3))
        w = q >> 6
        bit = U64(1) << U64(q & 63)
        if axis == 0 or axis == 1:
            cols[q, w] |= bit
        if axis == 1 or axis == 2:
            cols[n + q, w] |= bit
    return cols, state


@njit(cache=True, inline='always')
def apply_two_qubit_symplectic(cols: np.ndarray, n: int, q: int, masks: np.ndarray, gate_index: int) -> None:
    """Apply a 2-qubit Clifford support map on adjacent q (low), q+1 (high)."""
    i0 = q
    i1 = n + q
    i2 = q + 1
    i3 = n + q + 1
    m0 = int(masks[gate_index, 0])
    m1 = int(masks[gate_index, 1])
    m2 = int(masks[gate_index, 2])
    m3 = int(masks[gate_index, 3])
    for w in range(cols.shape[1]):
        a = cols[i0, w]
        b = cols[i1, w]
        c = cols[i2, w]
        d = cols[i3, w]
        cols[i0, w] = _xor4(m0, a, b, c, d)
        cols[i1, w] = _xor4(m1, a, b, c, d)
        cols[i2, w] = _xor4(m2, a, b, c, d)
        cols[i3, w] = _xor4(m3, a, b, c, d)


@njit(cache=True)
def measure_single_pauli(cols: np.ndarray, n: int, q: int, axis: int) -> int:
    """Projectively measure X/Y/Z on q. Return 1 if random, 0 if deterministic.

    ``axis``: 0=X, 1=Y, 2=Z. Outcome signs are intentionally omitted.
    """
    words = cols.shape[1]
    anti = np.empty(words, dtype=np.uint64)
    found_word = -1
    for w in range(words):
        if axis == 0:
            v = cols[n + q, w]
        elif axis == 1:
            v = cols[q, w] ^ cols[n + q, w]
        else:
            v = cols[q, w]
        anti[w] = v
        if found_word < 0 and v != 0:
            found_word = w
    if found_word < 0:
        return 0

    v = anti[found_word]
    offset = 0
    while (v & U64(1)) == 0:
        v >>= U64(1)
        offset += 1
    pivot = (found_word << 6) + offset
    pivot_bit = U64(1) << U64(offset)
    anti[found_word] &= ~pivot_bit

    for c in range(2 * n):
        pivot_has = (cols[c, found_word] & pivot_bit) != 0
        if pivot_has:
            for w in range(words):
                cols[c, w] ^= anti[w]
        cols[c, found_word] &= ~pivot_bit

    if axis == 0 or axis == 1:
        cols[q, found_word] |= pivot_bit
    if axis == 1 or axis == 2:
        cols[n + q, found_word] |= pivot_bit
    return 1


@njit(cache=True)
def simulate_trajectory_snapshots(
    n: int,
    p: float,
    probe_steps: np.ndarray,
    masks: np.ndarray,
    seed: np.uint64,
    protocol_code: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Simulate and return tableaus at requested post-measurement cycle indices.

    protocol_code: 0 = projective Z, 1 = independently random X/Y/Z.
    """
    cols, state = initialize_product_tableau(n, seed)
    nprobe = len(probe_steps)
    snapshots = np.empty((nprobe, 2 * n, cols.shape[1]), dtype=np.uint64)
    measurement_counts = np.zeros(nprobe, dtype=np.int64)
    random_measurement_counts = np.zeros(nprobe, dtype=np.int64)
    cut_measurement_counts = np.zeros(nprobe, dtype=np.int64)
    probe_index = 0
    max_cycle = int(probe_steps[-1])
    m = n // 2
    total_meas = 0
    total_random = 0
    total_cut = 0
    n_maps = masks.shape[0]

    for cycle in range(1, max_cycle + 1):
        state, r = _rng_next(state)
        first = np.int64(r & U64(1))
        for order_index in range(2):
            parity = np.int64(first if order_index == 0 else np.int64(1) - first)
            q = np.int64(parity)
            while q < n - 1:
                state, rg = _rng_next(state)
                gate_index = np.int64(rg % U64(n_maps))
                apply_two_qubit_symplectic(cols, n, q, masks, gate_index)
                q += 2
        for q in range(n):
            state, u = _rand_float01(state)
            if u < p:
                total_meas += 1
                if q == m - 1 or q == m:
                    total_cut += 1
                if protocol_code == 0:
                    axis = 2
                else:
                    state, ra = _rng_next(state)
                    axis = int(ra % U64(3))
                total_random += measure_single_pauli(cols, n, q, axis)

        if probe_index < nprobe and cycle == int(probe_steps[probe_index]):
            snapshots[probe_index, :, :] = cols
            measurement_counts[probe_index] = total_meas
            random_measurement_counts[probe_index] = total_random
            cut_measurement_counts[probe_index] = total_cut
            probe_index += 1

    return snapshots, measurement_counts, random_measurement_counts, cut_measurement_counts


@njit(cache=True, inline='always')
def _ctz64(v: np.uint64) -> int:
    c = 0
    while (v & U64(1)) == 0:
        v >>= U64(1)
        c += 1
    return c


@njit(cache=True)
def gf2_rank_selected_sites(cols: np.ndarray, n: int, site_mask: np.ndarray) -> int:
    """Rank of generator restriction to selected qubit sites."""
    words = cols.shape[1]
    basis = np.zeros((n, words), dtype=np.uint64)
    used = np.zeros(n, dtype=np.uint8)
    rank = 0
    for q in range(n):
        if site_mask[q] == 0:
            continue
        for which in range(2):
            c = q if which == 0 else n + q
            v = np.empty(words, dtype=np.uint64)
            for w in range(words):
                v[w] = cols[c, w]
            while True:
                pivot = -1
                for w in range(words):
                    if v[w] != 0:
                        pivot = (w << 6) + _ctz64(v[w])
                        break
                if pivot < 0 or pivot >= n:
                    break
                if used[pivot] == 0:
                    used[pivot] = 1
                    for w in range(words):
                        basis[pivot, w] = v[w]
                    rank += 1
                    break
                for w in range(words):
                    v[w] ^= basis[pivot, w]
    return rank


@njit(cache=True)
def entropy_interval(cols: np.ndarray, n: int, start: int, end: int) -> int:
    mask = np.zeros(n, dtype=np.uint8)
    for q in range(start, end):
        mask[q] = 1
    rank = gf2_rank_selected_sites(cols, n, mask)
    return rank - (end - start)


@njit(cache=True)
def entropy_site_mask(cols: np.ndarray, n: int, mask: np.ndarray) -> int:
    k = 0
    for q in range(n):
        k += int(mask[q])
    rank = gf2_rank_selected_sites(cols, n, mask)
    return rank - k


@njit(cache=True)
def central_observables(cols: np.ndarray, n: int) -> np.ndarray:
    """Return central/neighbor entropies and exact response observables."""
    m = n // 2
    sl = entropy_interval(cols, n, 0, m - 1)
    sm = entropy_interval(cols, n, 0, m)
    sr = entropy_interval(cols, n, 0, m + 1)
    pm = 2.0 ** (-sm)
    pl = 2.0 ** (-sl)
    pr = 2.0 ** (-sr)
    norm = 1.0 / (1.0 - 2.0 ** (-m))
    chi = norm * (pm - 0.4 * (pl + pr))
    chi_rel = chi / pm
    dl = sm - sl
    dr = sm - sr
    return np.array([float(sl), float(sm), float(sr), pm, pl, pr, chi, chi_rel, float(dl), float(dr)], dtype=np.float64)


@njit(cache=True)
def tripartite_information_quarters(cols: np.ndarray, n: int) -> np.ndarray:
    """I3(A:B:C) for four contiguous quarters A,B,C,D of an open chain."""
    qn = n // 4
    A = np.zeros(n, dtype=np.uint8)
    B = np.zeros(n, dtype=np.uint8)
    C = np.zeros(n, dtype=np.uint8)
    for q in range(0, qn): A[q] = 1
    for q in range(qn, 2 * qn): B[q] = 1
    for q in range(2 * qn, 3 * qn): C[q] = 1
    AB = A | B
    AC = A | C
    BC = B | C
    ABC = AB | C
    sA = entropy_site_mask(cols, n, A)
    sB = entropy_site_mask(cols, n, B)
    sC = entropy_site_mask(cols, n, C)
    sAB = entropy_site_mask(cols, n, AB)
    sAC = entropy_site_mask(cols, n, AC)
    sBC = entropy_site_mask(cols, n, BC)
    sABC = entropy_site_mask(cols, n, ABC)
    i3 = sA + sB + sC - sAB - sAC - sBC + sABC
    return np.array([sA,sB,sC,sAB,sAC,sBC,sABC,i3],dtype=np.float64)


@njit(cache=True)
def window_entropy_features(cols: np.ndarray, n: int, half_widths: np.ndarray) -> np.ndarray:
    """Nested window entropies and local-stabilizer counts around central bond."""
    m = n // 2
    out = np.empty((len(half_widths), 4), dtype=np.float64)
    for i in range(len(half_widths)):
        h = int(half_widths[i])
        if h > m:
            h = m
        start = m - h
        end = m + h
        sw = entropy_interval(cols, n, start, end)
        sl = entropy_interval(cols, n, start, m)
        sr = entropy_interval(cols, n, m, end)
        local_stabs = (end - start) - sw
        out[i,0] = float(sw)
        out[i,1] = float(local_stabs)
        out[i,2] = float(sl)
        out[i,3] = float(sr)
    return out


@njit(cache=True)
def paired_single_measurement_interventions(
    cols: np.ndarray,
    n: int,
    distances: np.ndarray,
    axis: int,
) -> np.ndarray:
    """Paired one-measurement interventions on left/right sites at each distance.

    Columns: distance, side(-1 left/+1 right), random_flag, delta_Sm,
    delta_chi, delta_chi_relative, post_Sm, post_delta_left, post_delta_right.
    """
    base = central_observables(cols, n)
    m = n // 2
    out = np.empty((2 * len(distances), 9), dtype=np.float64)
    row = 0
    for i in range(len(distances)):
        d = int(distances[i])
        for side_index in range(2):
            if side_index == 0:
                q = m - 1 - d
                side = -1.0
            else:
                q = m + d
                side = 1.0
            out[row,0] = float(d)
            out[row,1] = side
            if q < 0 or q >= n:
                for j in range(2,9): out[row,j] = np.nan
                row += 1
                continue
            tmp = cols.copy()
            rnd = measure_single_pauli(tmp, n, q, axis)
            post = central_observables(tmp, n)
            out[row,2] = float(rnd)
            out[row,3] = post[1] - base[1]
            out[row,4] = post[6] - base[6]
            out[row,5] = post[7] - base[7]
            out[row,6] = post[1]
            out[row,7] = post[8]
            out[row,8] = post[9]
            row += 1
    return out


def load_symplectic_masks(path: str) -> np.ndarray:
    return np.asarray(np.load(path)['masks'], dtype=np.uint8)


def stable_seed_u64(*items: object) -> np.uint64:
    import hashlib
    raw = repr(items).encode('utf-8')
    return np.uint64(int.from_bytes(hashlib.blake2b(raw,digest_size=8).digest(),'little'))
