from __future__ import annotations

def stabilizer_boundary_response(delta_left: int, delta_right: int, d: int | None = None) -> float:
    """Exact stabilizer response for delta_left, delta_right in {-1,0,+1}."""
    if delta_left not in (-1,0,1) or delta_right not in (-1,0,1):
        raise ValueError("boundary increments must be -1, 0, or +1")
    base = 1.0 - 0.4 * (2.0**delta_left + 2.0**delta_right)
    return base if d is None else d/(d-1.0)*base
