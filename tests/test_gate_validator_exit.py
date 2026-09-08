"""The gate validator must enforce numerical failure at the process boundary."""
import json
import math
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / 'studies/checkpoint_04/scripts/validate_gate_invariant_formula.py'

CHILD = r'''
import importlib.util
import sys
import numpy as np
spec = importlib.util.spec_from_file_location('gate_validator_under_test', sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
original = module.sim.locally_dressed_response_coefficients
offset = float(sys.argv[3])
count = 0
def injected(gate):
    global count
    count += 1
    # A later NaN must fail too: built-in max can ignore it after a finite error.
    return original(gate) + np.array([offset if count == 2 else 0., 0., 0., 0.])
module.sim.locally_dressed_response_coefficients = injected
sys.argv = [sys.argv[1], '--out', sys.argv[2], '--samples', '2', '--seed', '123']
module.main()
'''


@pytest.mark.parametrize('offset,expected_exit,expected_pass', [
    (0., 0, True), (.125, 1, False), (float('nan'), 1, False), (float('inf'), 1, False)])
def test_validator_exit_agrees_with_report(tmp_path, offset, expected_exit, expected_pass):
    output = tmp_path / 'gate_report.json'
    run = subprocess.run(
        [sys.executable, '-c', CHILD, str(VALIDATOR), str(output), str(offset)],
        cwd=ROOT, capture_output=True, text=True, timeout=30, check=False)
    assert output.is_file(), run.stderr
    report = json.loads(output.read_text())
    assert json.loads(run.stdout)['passes'] is expected_pass
    assert report['passes'] is expected_pass
    assert run.returncode == expected_exit, run.stderr
    if math.isfinite(offset):
        assert abs(report['maximum_coefficient_error'] - offset) < 5e-13
    else:
        assert not math.isfinite(report['mean_coefficient_error'])
