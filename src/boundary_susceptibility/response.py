from __future__ import annotations

def haar_clifford_relative_response(p_left: float, p_center: float, p_right: float, d: int) -> float:
    """Relative Renyi-2 response to a fresh Haar/uniform-Clifford two-qubit probe."""
    if d <= 1 or p_center <= 0:
        raise ValueError("d must exceed one and p_center must be positive")
    return d / (d - 1.0) * (1.0 - 0.4 * (p_left + p_right) / p_center)
