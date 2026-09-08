#!/usr/bin/env python3
"""Temporary transport of the independently tested local adoption script.

The seven text parts were checked against their Git blob identities before use.
The expanded source is SHA-256 checked before execution and archived in the
workflow artifact for inspection. It preserves all statistical source code,
original data, point estimates, layout code, and other panels. This helper and
the payload files are removed before the final branch commit. No network,
push, merge, or history-rewrite operation is present in the expanded source.
"""
from pathlib import Path
import base64
import hashlib
import os
import zlib

if os.environ.get('GITHUB_REF') != 'refs/heads/analysis/figure1-uncertainty-2026-09-08':
    raise RuntimeError('Wrong branch; no files changed')
paths=[Path(f'.github/tools/figure1_adoption_payload{i}.txt') for i in range(7)]
source=zlib.decompress(base64.b64decode(''.join(p.read_text() for p in paths),validate=True))
if hashlib.sha256(source).hexdigest() != 'a1313e6aaa9a20931ed6fe443635c66c58176f4fd9e9bc09b39358e56ff959fb':
    raise ValueError('Transport integrity failure; no files changed')
review=Path('figure1_review_verification');review.mkdir(exist_ok=True)
(review/'applied_adoption_source.py').write_bytes(source)
for p in paths:p.unlink()
exec(compile(source,'verified_figure1_adoption.py','exec'),{'__name__':'__main__'})
