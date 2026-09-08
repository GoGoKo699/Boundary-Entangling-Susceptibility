"""Run unchanged Figure 1 generation and both readers in one uninterrupted job.

This diagnostic changes neither source code, hashes, estimator nor RNG. It
isolates output-file handling after two separately invoked runs lost ZIP tails.
All commands run sequentially and failures propagate.
"""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
output = 'repairs/full-sanity-01/reproduced_figure1_uncertainty_sequential'
report = 'repairs/full-sanity-01/figure1_review_verification/independent_replay_sequential.json'
commands = [
    ['scripts/analysis/complete_figure1_uncertainty.py', '--output', output],
    ['scripts/analysis/verify_figure1_uncertainty.py', '--output', output,
     '--report', report],
    ['scripts/analysis/check_figure1_adoption.py', '--resamples', output],
]
for command in commands:
    print('COMMAND:', [sys.executable, *command], flush=True)
    subprocess.run([sys.executable, *command], cwd=root, check=True)
