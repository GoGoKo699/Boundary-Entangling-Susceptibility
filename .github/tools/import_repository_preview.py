#!/usr/bin/env python3
"""One-time import of the locally reviewed website source; never deploys it."""
import base64
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import subprocess

BASE = '1059662eb7a8ad8bb3262ff4feddd9d95da71d00'
TREE = '4157908c3aa8f216c8ad7ffa0764c8a7928cb542'
BRANCH = 'refs/heads/presentation/repository-preview-2026-09-08'
EXPECTED = 'b7f704f394835afc805eab6b0449a014171229060f2551648fba2d8217ee906f'
MANIFEST = '70386c2978a9ff72da62fa4e643290f80aa401baaf23e6350afaae204faf047c'
ROOT = Path.cwd().resolve()

def git(*args):
    return subprocess.check_output(['git', *args])

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

if os.environ.get('GITHUB_REF') != BRANCH:
    raise RuntimeError('Restricted to the authorized presentation branch')
if git('rev-parse', BASE + '^{tree}').decode().strip() != TREE:
    raise ValueError('Wrong scientific baseline')
raw = base64.b64decode(''.join((ROOT/f'.github/tools/preview-part{i}.txt').read_text().strip() for i in range(4)), validate=True)
if digest(raw) != EXPECTED:
    raise ValueError('Reviewed transfer hash mismatch')
payload = json.loads(lzma.decompress(raw, memlimit=268435456))
if payload['base'] != BASE or len(payload['files']) != 19:
    raise ValueError('Unexpected import specification')
paths = git('ls-tree', '-r', '--name-only', BASE).decode().splitlines()
if len(paths) != 200:
    raise ValueError('Unexpected original file count')
rows = []
for name in sorted(paths):
    original = git('show', BASE + ':' + name)
    if (ROOT/name).read_bytes() != original:
        raise ValueError('Original file changed before import: ' + name)
    rows.append({'path':name, 'sha256':digest(original), 'bytes':len(original)})
for name in payload['files']:
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or '\\' in name:
        raise ValueError('Unsafe import path')
    if name != 'README.md' and not name.startswith(('website/', 'scripts/site/')):
        raise ValueError('Out-of-scope import path')
    if name != 'README.md' and (ROOT/name).exists():
        raise ValueError('Refusing to replace existing source: ' + name)
manifest = {'commit':BASE, 'tree':TREE, 'files':rows,
    'source_overrides':{'README.md':'website/source_snapshots/original_README.md.txt'},
    'presentation_note':'The 199 other baseline files remain in place. The original README is preserved in a byte-identical snapshot so the current README may serve as the editable project entrance. Scientific source links still point to the frozen commit.'}
manifest_bytes = (json.dumps(manifest, indent=2)+'\n').encode()
if digest(manifest_bytes) != MANIFEST:
    raise ValueError('Reconstructed scientific manifest differs from reviewed manifest')
snapshot = ROOT/'website/source_snapshots/original_README.md.txt'
snapshot.parent.mkdir(parents=True, exist_ok=True)
snapshot.write_bytes((ROOT/'README.md').read_bytes())
for name, text in payload['files'].items():
    path = ROOT/name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
(ROOT/'website/scientific_baseline.json').write_bytes(manifest_bytes)
(ROOT/'website/IMPORT.json').write_text(json.dumps({
    'scientific_base':BASE, 'reviewed_source_xz_sha256':EXPECTED,
    'unchanged_in_place_baseline_files':199,
    'original_readme_preserved':str(snapshot.relative_to(ROOT)),
    'scope':'Website source and in-repository preview only; no public deployment, statistical revision, license change, or canonical recoloring.'
}, indent=2)+'\n')
print('Imported 19 reviewed text files; preserved the scientific baseline.')
