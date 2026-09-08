"""Verify immutable audit, observations, numerical core tables and other panels."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / 'audits/full-sanity-01'
MANIFEST_SHA256 = 'a3c300627ab36082d1fd8f6b3a09f9e63534e90f8589c9323efd4919553819e4'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = AUDIT / 'file_manifest.csv'
    assert sha(manifest) == MANIFEST_SHA256, 'Frozen audit manifest changed'
    audit_rows = list(csv.DictReader(manifest.open()))
    for row in audit_rows:
        file = AUDIT / row['path']
        assert file.stat().st_size == int(row['bytes']) and sha(file) == row['sha256'], row['path']
    originals = list(csv.DictReader((AUDIT/'baseline_inventory.csv').open()))
    fixed_sources = {
        'entanglement-data.zip', 'data/record_bundle_manifest.json',
        'analysis_plans/figure1_uncertainty_2026-09-08.json',
        'provenance/FIGURE1_ADOPTION_2026-09-08.json',
        'provenance/FIGURE_PALETTE_2026-09-08.json',
        'scripts/analysis/complete_figure1_uncertainty.py',
        'scripts/analysis/verify_figure1_uncertainty.py',
        'scripts/analysis/reproduce_core_records.py',
        'scripts/analysis/reassess_evidence.py',
    }
    checked = []
    for row in originals:
        p = row['path']
        if row['type'] != 'blob':
            continue
        other_panel = p.startswith(('figures/core/', 'figures/core_svg/')) and 'figure_03_' not in p
        source_plot = p.startswith('scripts/figures/') and p != 'scripts/figures/make_figure_03.py'
        if p in fixed_sources or p.startswith('data/processed/core_figures/') or other_panel or source_plot:
            content = (ROOT/p).read_bytes()
            digest = hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
            assert digest == row['git_sha'], p
            checked.append(p)
    print(json.dumps({'passed': True, 'immutable_audit_files': len(audit_rows)+1,
                      'unchanged_scientific_files': checked,
                      'figure3_change': 'label-only successor checked separately'}, indent=2))


if __name__ == '__main__':
    main()
