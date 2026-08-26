from boundary_susceptibility.boundary_codes import stabilizer_boundary_response
from boundary_susceptibility.response import haar_clifford_relative_response
import pytest

def test_boundary_alphabet():
    assert stabilizer_boundary_response(-1, -1) == pytest.approx(0.6, abs=1e-12)
    assert stabilizer_boundary_response(1, 1) == pytest.approx(-0.6, abs=1e-12)

def test_response_formula():
    value = haar_clifford_relative_response(0.125, 0.25, 0.125, 4)
    assert abs(value - 0.8) < 1e-12
