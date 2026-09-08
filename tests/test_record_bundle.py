from pathlib import Path
import hashlib,json
import pytest
from boundary_susceptibility.records import RecordBundle, ROOT

def test_complete_original_records_are_present():
    with RecordBundle() as records:
        summary=records.verify()
        assert summary['members']==172
        assert 'checkpoint_05/data/primary_scaling/stabilizer_scaling_states.csv.gz' in records.entries
        assert 'checkpoint_04/data/intervention/primary_rank4/state_response_rows.csv.gz' in records.entries

def test_incomplete_data_cannot_silently_pass(tmp_path):
    with pytest.raises(FileNotFoundError,match='not yet self-contained'):
        RecordBundle(tmp_path/'missing.zip')

def test_altered_bundle_cannot_pass(tmp_path):
    p=tmp_path/'bad.zip';p.write_bytes(b'wrong historical data')
    with pytest.raises(ValueError,match='identity mismatch'):
        RecordBundle(p)

def test_accepted_figures_and_data_unchanged():
    manifest=json.loads((ROOT/'provenance/current_baseline_sha256.json').read_text())
    assert len(manifest['files'])==23
    for entry in manifest['files']:
        assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256']


def test_figure1_accepted_intervals_not_mislabeled_as_replayed():
    from boundary_susceptibility.records import ROOT
    code=(ROOT/'scripts/analysis/reproduce_core_records.py').read_text()
    assert "'figure1_historical_interval_replay':False" in code
    assert (ROOT/'docs/REPRODUCIBILITY_LIMITS.md').is_file()
