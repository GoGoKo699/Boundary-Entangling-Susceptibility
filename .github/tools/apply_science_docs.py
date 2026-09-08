#!/usr/bin/env python3
"""Apply the reviewed, content-addressed documentation consolidation only."""
from __future__ import annotations
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import zlib

BASE = '8906b8024e53204d7fb55043ee5d446a25289fcf'
REF = 'refs/heads/docs/scientific-consolidation-2026-09-08'
REPO = 'GoGoKo699/Boundary-Entangling-Susceptibility'
PLAN_HASH = '76ed24538ba50d0df6bd3403494312136c7d95a4e9ee87ee50a56a3bb01de426'
PATHS = ['README.md', 'docs/CLAIM_EVIDENCE_MAP.md', 'docs/DIALOGUE_QUESTION_MAP.md',
 'docs/DIALOGUE_REPORT.md', 'docs/FAQ.md', 'docs/NOTATION.md', 'docs/NUMERICAL_METHODS.md',
 'docs/RELATED_WORK.md', 'docs/RESULTS_AT_A_GLANCE.md', 'docs/SCIENTIFIC_STORY.md',
 'docs/SCOPE_AND_LIMITATIONS.md', 'docs/THEORY.md', 'results/core_claims.csv',
 'provenance/SCIENTIFIC_CONSOLIDATION_2026-09-08.json']
TRANSIENT = ['.github/tools/apply_science_docs.py', '.github/workflows/apply-science-docs.yml'] + [
 f'.github/tools/bes_science_payload{i}.txt' for i in range(6)]


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], text=True).strip()


def main() -> None:
    if os.environ.get('GITHUB_REF') != REF or os.environ.get('GITHUB_REPOSITORY') != REPO:
        raise RuntimeError('Restricted to the isolated documentation branch')
    changed = set(git('diff', '--name-only', BASE, 'HEAD').splitlines())
    if changed != set(TRANSIENT):
        raise ValueError('Checkout differs from the frozen baseline beyond transfer helpers')
    encoded = ''.join(Path(f'.github/tools/bes_science_payload{i}.txt').read_text() for i in range(6))
    raw = zlib.decompress(base64.b64decode(encoded, validate=True))
    if hashlib.sha256(raw).hexdigest() != PLAN_HASH:
        raise ValueError('Documentation plan checksum mismatch')
    plan = json.loads(raw)
    if [r['path'] for r in plan] != PATHS:
        raise ValueError('Unexpected target paths')
    prepared = {}
    for row in plan:
        path = Path(row['path'])
        if path.is_symlink():
            raise ValueError('Symlink target not permitted')
        old = path.read_bytes() if path.exists() else b''
        before = hashlib.sha256(old).hexdigest() if path.exists() else None
        if before != row['before']:
            raise ValueError(f'Baseline mismatch: {path}')
        lines = old.decode('utf-8').splitlines(keepends=True)
        output = []
        last = 0
        for start, end, text in row['edits']:
            if not (last <= start <= end <= len(lines)):
                raise ValueError('Invalid or overlapping line edits')
            output.extend(lines[last:start])
            output.append(text)
            last = end
        output.extend(lines[last:])
        revised = ''.join(output).encode('utf-8')
        if hashlib.sha256(revised).hexdigest() != row['after']:
            raise ValueError(f'Revised text checksum mismatch: {path}')
        prepared[path] = revised
    # Nothing is written until every old and new content hash has passed.
    for path, raw in prepared.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    (Path(os.environ['RUNNER_TEMP']) / 'bes_science_paths.json').write_text(json.dumps(PATHS))
    print('Applied exactly 13 textual revisions and one provenance file; no data, figure, or executable changes.')


if __name__ == '__main__':
    main()
