"""Minimal fault injection for the frozen validator's confirmed exit-code flaw.

The baseline source is imported without edits. Only a subprocess's in-memory
dependency is patched. This tests the validator's error enforcement, not the
scientific gate identity. Remove xfail when an authorized repair is assessed.
"""
from pathlib import Path
import json
import subprocess
import sys

import pytest


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="MATH-C1: validator exits zero despite reporting passes=false",
)
def test_numerically_failed_gate_validator_must_exit_nonzero(tmp_path):
    root = Path(__file__).resolve().parents[3]
    validator = root / "studies/checkpoint_04/scripts/validate_gate_invariant_formula.py"
    output = tmp_path / "deliberately_failed_invariant_report.json"
    child_code = r'''
import importlib.util
import sys
import numpy as np

spec = importlib.util.spec_from_file_location("audited_validator", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
original = module.sim.locally_dressed_response_coefficients

def injected_coefficients(gate):
    return original(gate) + np.array([0.125, 0.0, 0.0, 0.0])

module.sim.locally_dressed_response_coefficients = injected_coefficients
sys.argv = [sys.argv[1], "--out", sys.argv[2], "--samples", "1", "--seed", "123"]
module.main()
'''
    completed = subprocess.run(
        [sys.executable, "-c", child_code, str(validator), str(output)],
        cwd=root, capture_output=True, text=True, timeout=30, check=False,
    )
    # Unexpected import/runtime/fault-injection failures must not count as xfail.
    if not output.exists():
        raise RuntimeError(f"Validator did not write the required report: {completed.stderr}")
    report = json.loads(output.read_text())
    if report.get("passes") is not False or report["maximum_coefficient_error"] < .12:
        raise RuntimeError(f"Fault injection did not cause the intended numeric failure: {report}")
    evidence = {
        "seed": report["seed"],
        "samples": report["samples"],
        "injected_first_coefficient_offset": .125,
        "maximum_coefficient_error": report["maximum_coefficient_error"],
        "validator_report_passes": report["passes"],
        "validator_process_returncode": completed.returncode,
    }
    print(json.dumps(evidence, sort_keys=True))
    assert completed.returncode != 0, (
        "Validator returned success despite a failed numerical validation: "
        + json.dumps(evidence, sort_keys=True)
    )
