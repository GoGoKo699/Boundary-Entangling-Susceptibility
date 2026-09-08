"""Verified, offline access to the immutable original-study records.

Only the data container changed. Every member is an unchanged source file.
No code is executed during archive validation or extraction.
"""
from __future__ import annotations
from pathlib import Path, PurePosixPath
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2]

class RecordBundle:
    def __init__(self, path: Path | None = None, root: Path = ROOT):
        self.root = Path(root)
        self.manifest = json.loads((self.root/'data/record_bundle_manifest.json').read_text())
        self.path = Path(path) if path is not None else self.root/self.manifest['bundle']
        if not self.path.is_file():
            raise FileNotFoundError(
                f'Required recorded data are absent: {self.path}. '
                'This checkout is not yet self-contained. Place entanglement-data.zip '
                'in the repository root; do not substitute regenerated or summary-only data.')
        with self.path.open('rb') as handle:
            digest = hashlib.file_digest(handle, 'sha256').hexdigest()
        if digest != self.manifest['sha256']:
            raise ValueError(f'Record bundle identity mismatch: {digest}')
        self.sha256 = digest
        self.entries = {r['member']: r for r in self.manifest['members']}
        self.zip = zipfile.ZipFile(self.path)
        if len(self.entries) != len(self.manifest['members']):
            raise ValueError('Duplicate member in record manifest')
        if len(self.zip.namelist()) != len(set(self.zip.namelist())) or set(self.zip.namelist()) != set(self.entries):
            raise ValueError('Record bundle member set differs from manifest')
        for name in self.entries:
            parts=PurePosixPath(name)
            if parts.is_absolute() or '..' in parts.parts or '\\' in name:
                raise ValueError(f'Unsafe archive member: {name}')

    def read(self, member: str) -> bytes:
        expected = self.entries[member]
        raw = self.zip.read(member)
        if len(raw) != expected['bytes'] or hashlib.sha256(raw).hexdigest() != expected['sha256']:
            raise ValueError(f'Record member integrity mismatch: {member}')
        return raw

    def verify(self) -> dict:
        for name in self.entries:
            self.read(name)
        return {'sha256': self.sha256, 'members':len(self.entries), 'bytes':self.path.stat().st_size,
                'all_members_verified': True}

    def materialize(self, destination: Path) -> None:
        destination = Path(destination).resolve()
        destination.mkdir(parents=True, exist_ok=True)
        # Existing different files are never silently overwritten.
        for name in self.entries:
            target = destination/name
            if not target.resolve().is_relative_to(destination):
                raise ValueError(f'Unsafe destination: {name}')
            raw=self.read(name)
            if target.exists() and target.read_bytes()!=raw:
                raise FileExistsError(f'Refusing to overwrite different file: {target}')
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(raw)
        for study in ['checkpoint_04','checkpoint_05']:
            src=self.root/'studies'/study/'scripts'
            dst=destination/study/'scripts'; dst.mkdir(parents=True,exist_ok=True)
            for path in src.glob('*.py'):
                target=dst/path.name
                if target.exists() and target.read_bytes()!=path.read_bytes():
                    raise FileExistsError(f'Refusing to overwrite different source: {target}')
                shutil.copy2(path,target)

    def close(self) -> None:
        self.zip.close()

    def __enter__(self):
        return self

    def __exit__(self,*args):
        self.close()
