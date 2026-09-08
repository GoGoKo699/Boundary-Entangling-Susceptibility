"""Audit package integrity and change-boundary check; no scientific source edits."""
from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / 'audits/full-sanity-01'
BASELINE = '00009cf7cc02104e4c776863b3ea551bd38e00f4'


def main():
    baseline = [r for r in csv.DictReader((AUDIT/'baseline_inventory.csv').open())
                if r['type'] == 'blob']
    for row in baseline:
        content = (ROOT / row['path']).read_bytes()
        git_hash = hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
        assert git_hash == row['git_sha'], row['path']
    changed = subprocess.check_output(
        ['git', 'diff', '--name-only', BASELINE], cwd=ROOT, text=True).splitlines()
    assert all(p.startswith('audits/full-sanity-01/') for p in changed), changed
    claims = list(csv.DictReader((AUDIT/'CLAIM_AUDIT.csv').open()))
    assert len({r['claim_id'] for r in claims}) == len(claims)
    for row in claims:
        for token in row['audit_evidence'].split(';'):
            relative = token.strip().split(' section ')[0]
            assert (AUDIT / relative).exists(), (row['claim_id'], relative)
        for path in re.findall(r'(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+\.(?:py|md|csv|json|npz)', row['baseline_sources']):
            assert (ROOT/path).exists(), (row['claim_id'], path)
    manifest = AUDIT/'file_manifest.csv'
    manifest_count = None
    if manifest.exists():
        entries = list(csv.DictReader(manifest.open()))
        for row in entries:
            data = (AUDIT/row['path']).read_bytes()
            assert len(data) == int(row['bytes']), row['path']
            assert hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
        manifest_count = len(entries)
    print(json.dumps(dict(baseline=BASELINE, unchanged_baseline_blobs=len(baseline),
                          claim_rows=len(claims), changed_paths_all_audit=True,
                          manifest_verified_files=manifest_count), indent=2))


if __name__ == '__main__':
    main()
