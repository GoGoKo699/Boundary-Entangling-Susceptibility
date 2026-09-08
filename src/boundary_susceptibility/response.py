from __future__ import annotations

def haar_clifford_relative_response(p_left: float, p_center: float, p_right: float, d: int) -> float:
    """Normalized linear-entropy change divided by the input central purity.

    The fresh two-qubit probe is Haar/uniform-Clifford averaged. This is not
    an average finite change of logarithmic Renyi-2 entropy; ``d`` denotes
    the half-chain Hilbert-space dimension, not distance from the cut.
    """
    if d <= 1 or p_center <= 0:
        raise ValueError("d must exceed one and p_center must be positive")
    return d / (d - 1.0) * (1.0 - 0.4 * (p_left + p_right) / p_center)
