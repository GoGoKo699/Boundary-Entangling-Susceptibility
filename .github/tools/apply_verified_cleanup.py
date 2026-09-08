#!/usr/bin/env python3
"""Apply one reviewed cleanup transfer on the isolated cleanup branch only.

The archive is authenticated before parsing. Every replaced/deleted original
file and every protected figure/input is checked before any write. This tool
never changes refs, pushes, merges, downloads input data, or edits Git history.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import zipfile

EXPECTED = 'a14638afdf3fbe8a8d71f36f1a61a7a68bea2e85a64f7c89a228b8099f97dd15'
BRANCH = 'refs/heads/cleanup/entanglement-only-2026-09-08'
ROOT = Path.cwd().resolve()
PACKAGE = ROOT/'entanglement-cleanup-transfer.zip'


def digest(path: Path) -> str:
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def target(name: str) -> Path:
    p=PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '.git' in p.parts or '\\' in name:
        raise ValueError('Unsafe transfer path')
    path=ROOT/name
    if not path.resolve().is_relative_to(ROOT):
        raise ValueError('Transfer path escapes checkout')
    return path


def main() -> None:
    if os.environ.get('GITHUB_REF') != BRANCH:
        raise RuntimeError('This importer is restricted to the isolated cleanup branch')
    if digest(PACKAGE) != EXPECTED:
        raise ValueError('Transfer archive SHA-256 mismatch; no files changed')
    with zipfile.ZipFile(PACKAGE) as z:
        m=json.loads(z.read('transfer_manifest.json'))
        if m['repository']!='GoGoKo699/Boundary-Entangling-Susceptibility' or m['branch']!=BRANCH.removeprefix('refs/heads/'):
            raise ValueError('Wrong repository/branch manifest')
        expected={'transfer_manifest.json'}|{'replacement_files/'+r['path'] for r in m['replacement_files']}
        if set(z.namelist())!=expected or len(z.namelist())!=len(expected):
            raise ValueError('Unexpected or duplicate transfer members')
        prepared={}
        for row in m['replacement_files']:
            path=target(row['path']); old=row['before_sha256']
            if old is None:
                if path.exists():raise FileExistsError(f'Refusing to overwrite a newly existing path: {path}')
            elif not path.is_file() or digest(path)!=old:
                raise ValueError(f'Existing file changed since the audited baseline: {path}')
            raw=z.read('replacement_files/'+row['path'])
            if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:
                raise ValueError(f'Replacement integrity mismatch: {path}')
            prepared[row['path']]=raw
        for row in m['delete_files']:
            path=target(row['path'])
            if not path.is_file() or digest(path)!=row['before_sha256']:
                raise ValueError(f'Refusing to delete a changed original file: {path}')
        for row in m['protected_baseline']:
            if digest(target(row['path']))!=row['sha256']:
                raise ValueError(f'Protected figure/input changed: {row["path"]}')
        for name,raw in prepared.items():
            path=target(name);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
        for row in m['delete_files']:
            target(row['path']).unlink()
        for row in m['protected_baseline']:
            if digest(target(row['path']))!=row['sha256']:
                raise ValueError('Protected figure/input changed during cleanup')
    # The final reviewed tree contains neither an opaque import ZIP nor an auto-committing workflow.
    for name in ['entanglement-cleanup-transfer.zip', 'CLEANUP_UPLOAD.md',
                 '.github/workflows/export-cleanup-baseline.yml',
                 '.github/workflows/import-reviewed-cleanup.yml',
                 '.github/tools/apply_verified_cleanup.py']:
        target(name).unlink(missing_ok=True)
    print(f'Applied {len(prepared)} verified replacements and {len(m["delete_files"])} removals; protected panels/inputs unchanged.')


if __name__=='__main__':main()
