"""The label successor may not authorize changed data, geometry or other panels."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import types
import xml.etree.ElementTree as ET

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pytest

ROOT=Path(__file__).resolve().parents[1]
LABEL_RECORD='provenance/FIGURE3_LABEL_2026-09-08.json'
PALETTE_RECORD='provenance/FIGURE_PALETTE_2026-09-08.json'
ADOPTION_RECORD='provenance/FIGURE1_ADOPTION_2026-09-08.json'
spec=importlib.util.spec_from_file_location('figure3_label_guard',ROOT/'scripts/analysis/check_figure1_adoption.py')
guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)


def test_label_is_the_only_source_change_and_old_exports_survive():
    assert guard.verify()['figure3_label_successor']
    record=json.loads((ROOT/LABEL_RECORD).read_text())
    source=(ROOT/guard.FIGURE3_SOURCE).read_bytes()
    predecessor=source.replace(guard.FIGURE3_NEW_LABEL.encode(),guard.FIGURE3_OLD_LABEL.encode())
    old_source=next(r['before_sha256'] for r in record['changed_files'] if r['path']==guard.FIGURE3_SOURCE)
    assert hashlib.sha256(predecessor).hexdigest()==old_source
    for row in record['changed_files']:
        if row['path'] in guard.FIGURE3_OUTPUTS:
            historical=ROOT/'audits/full-sanity-01/reproduced_figures'/Path(row['path']).name
            assert guard.sha(historical)==row['before_sha256']


def test_svg_geometry_and_every_other_element_are_identical():
    old_path=ROOT/'audits/full-sanity-01/reproduced_figures/figure_03_size_scaling.svg'
    new_path=ROOT/'figures/core_svg/figure_03_size_scaling.svg'
    stripped=[]
    for path,label in [(old_path,guard.FIGURE3_OLD_LABEL),(new_path,guard.FIGURE3_NEW_LABEL)]:
        content=path.read_text()
        assert content.count('<!-- '+label+' -->')==1
        root=ET.fromstring(content)
        groups=root.findall('.//{http://www.w3.org/2000/svg}g[@id="text_10"]')
        assert len(groups)==1
        parent=next(p for p in root.iter() if groups[0] in list(p))
        parent.remove(groups[0])
        stripped.append(ET.tostring(root))
    # Includes plotted paths, numbers, uncertainty bars, limits, colors, all
    # remaining text and transforms, plus document dimensions and metadata.
    assert stripped[0]==stripped[1]


def test_old_and_new_plot_artist_geometry_match(monkeypatch,tmp_path):
    # Use the existing full artist snapshot, excluding only the specified ylabel.
    helper_spec=importlib.util.spec_from_file_location('label_geometry_helper',ROOT/'tests/test_figure_palette.py')
    helper=importlib.util.module_from_spec(helper_spec);helper_spec.loader.exec_module(helper)
    sys.path.insert(0,str(ROOT/'scripts/figures'))
    source=(ROOT/guard.FIGURE3_SOURCE).read_text()
    versions=[source.replace(guard.FIGURE3_NEW_LABEL,guard.FIGURE3_OLD_LABEL),source]
    snapshots=[]
    for index,version in enumerate(versions):
        module=types.ModuleType('figure3_label_geometry_'+str(index))
        exec(compile(version,guard.FIGURE3_SOURCE,'exec'),module.__dict__)
        captured=[]
        monkeypatch.setattr(module,'save_formats',lambda fig,pdf,png:captured.append(fig))
        monkeypatch.setattr(sys,'argv',['figure3','--csv',str(ROOT/'data/processed/core_figures/figure_03_size_scaling.csv'),
                                      '--pdf',str(tmp_path/'p.pdf'),'--png',str(tmp_path/'p.png')])
        with mpl.rc_context():
            mpl.rcdefaults();module.main()
            snapshot=helper.geometry(captured[0])
        assert snapshot['axes'][0]['labels'][1]==[guard.FIGURE3_OLD_LABEL,guard.FIGURE3_NEW_LABEL][index]
        snapshot['axes'][0]['labels'][1]='approved ylabel'
        snapshots.append(snapshot)
        plt.close('all')
    assert snapshots[0]==snapshots[1]


@pytest.fixture
def protected_copy(tmp_path):
    palette=json.loads((ROOT/PALETTE_RECORD).read_text())
    adoption=json.loads((ROOT/ADOPTION_RECORD).read_text())
    paths={LABEL_RECORD,PALETTE_RECORD,ADOPTION_RECORD,
           'data/processed/core_figures/figure_01_panel_b.csv'}
    for key in ['historical_files','protected_other_files','changed_panel_files']:
        paths.update(row['path'] for row in adoption[key])
    paths.update(adoption['locked_source_sha256'])
    paths.update(row['path'] for row in palette['changed_files'])
    paths.update(palette['unchanged_scientific_inputs'])
    paths.update(palette['supporting_files'])
    for name in paths:
        target=tmp_path/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/name,target)
    return tmp_path


def rewrite_record(root,edit):
    path=root/LABEL_RECORD
    record=json.loads(path.read_text());edit(record)
    path.write_text(json.dumps(record))


@pytest.mark.parametrize('name',[
    'data/processed/core_figures/figure_01_panel_b.csv',
    'data/processed/core_figures/figure_02_boundary_codes.csv',
    'data/processed/core_figures/figure_03_size_scaling.csv',
    'data/processed/core_figures/figure_04_conditioning_contrast.csv',
    'data/processed/core_figures/figure_04_distance_decay.csv',
    'figures/core/figure_02_response_matrix.png',
    'figures/core/figure_03_size_scaling.png',
])
def test_label_adoption_rejects_data_or_export_drift(protected_copy,name):
    path=protected_copy/name
    path.write_bytes(path.read_bytes()+b'\nchanged')
    with pytest.raises(ValueError):guard.verify(protected_copy)


def test_label_record_cannot_expand_its_allowed_file_set(protected_copy):
    def alter(record):record['changed_files'][0]['path']='data/processed/core_figures/figure_03_size_scaling.csv'
    rewrite_record(protected_copy,alter)
    with pytest.raises(ValueError,match='only Figure 3 source and three exports'):
        guard.verify(protected_copy)


def test_label_record_must_chain_to_old_asset_hash(protected_copy):
    def alter(record):record['changed_files'][1]['before_sha256']='0'*64
    rewrite_record(protected_copy,alter)
    with pytest.raises(ValueError,match='does not follow the palette baseline'):
        guard.verify(protected_copy)


@pytest.mark.parametrize('before,after',[
    ('0.0330','0.0340'),
    ("finite['beta'].to_numpy(float)","finite['beta'].to_numpy(float) + 0.01"),
])
def test_updated_successor_hash_cannot_authorize_geometry_or_value_change(protected_copy,before,after):
    path=protected_copy/guard.FIGURE3_SOURCE
    source=path.read_text();assert source.count(before)==1
    path.write_text(source.replace(before,after))
    def rehash(record):
        next(row for row in record['changed_files'] if row['path']==guard.FIGURE3_SOURCE)['sha256']=guard.sha(path)
    rewrite_record(protected_copy,rehash)
    with pytest.raises(ValueError,match='changes more than the approved ylabel'):
        guard.verify(protected_copy)


def test_predecessor_record_cannot_be_rewritten(protected_copy):
    path=protected_copy/PALETTE_RECORD
    path.write_text(path.read_text()+'\n')
    with pytest.raises(ValueError,match='Historical adoption record changed'):
        guard.verify(protected_copy)
