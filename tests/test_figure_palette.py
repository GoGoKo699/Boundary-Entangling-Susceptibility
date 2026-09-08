"""Regression checks for the approved figure-only palette, not new statistics."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import runpy
import sys

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/figures'))
import export_formats
from figure_palette import apply_palette


def plain(value):
    if isinstance(value, np.ndarray):return plain(value.tolist())
    if isinstance(value, (list, tuple)):return [plain(x) for x in value]
    if isinstance(value, dict):return {k:plain(v) for k,v in value.items()}
    if isinstance(value, np.generic):return value.item()
    return value


def geometry(fig):
    fig.canvas.draw()
    result={'size':fig.get_size_inches(), 'axes':[],
            'figure_text':[(t.get_text(),t.get_position(),t.get_fontsize()) for t in fig.texts]}
    for ax in fig.axes:
        result['axes'].append({
            'bbox':ax.get_position().bounds,'limits':(ax.get_xlim(),ax.get_ylim()),
            'ticks':(ax.get_xticks(),ax.get_yticks()),
            'ticklabels':[(t.get_text(),t.get_fontsize(),t.get_rotation()) for t in ax.get_xticklabels()+ax.get_yticklabels()],
            'labels':(ax.get_xlabel(),ax.get_ylabel(),ax.get_title()),
            'text':[(t.get_text(),t.get_position(),t.get_fontsize()) for t in ax.texts],
            'lines':[(x.get_xdata(),x.get_ydata(),x.get_marker(),x.get_markersize(),x.get_linestyle(),x.get_linewidth(),x.get_alpha()) for x in ax.lines],
            'collections':[(x.get_offsets(),[p.vertices for p in x.get_paths()],x.get_linewidths(),x.get_linestyles(),x.get_alpha()) for x in ax.collections],
            'images':[(np.asarray(x.get_array()),x.norm.vmin,x.norm.vmax,getattr(x.norm,'vcenter',None),x.get_extent()) for x in ax.images],
            'patches':[(p.get_path().vertices,p.get_transform().get_matrix(),p.get_linewidth(),p.get_alpha()) for p in ax.patches]})
    return plain(result)


def svg_bytes(fig):
    stream=io.BytesIO()
    with mpl.rc_context({'svg.fonttype':'none','svg.hashsalt':'boundary-susceptibility'}):
        fig.savefig(stream,format='svg',metadata={'Date':None})
    return stream.getvalue()


def test_all_six_panels_preserve_geometry_and_match_approved_exports(monkeypatch,tmp_path):
    data=ROOT/'data/processed/core_figures'
    commands=[
      ['make_figure_01_frozen.py','--csv',data/'figure_01_panel_b.csv','--pdf',tmp_path/'figure_01_panel_b.pdf','--png',tmp_path/'figure_01_panel_b.png'],
      ['make_figure_02.py','--csv',data/'figure_02_boundary_codes.csv','--outdir',tmp_path],
      ['make_figure_03.py','--csv',data/'figure_03_size_scaling.csv','--pdf',tmp_path/'figure_03_size_scaling.pdf','--png',tmp_path/'figure_03_size_scaling.png'],
      ['make_figure_04.py','--distance-csv',data/'figure_04_distance_decay.csv','--contrast-csv',data/'figure_04_conditioning_contrast.csv',
       '--distance-pdf',tmp_path/'figure_04_distance_decay.pdf','--distance-png',tmp_path/'figure_04_distance_decay.png',
       '--contrast-pdf',tmp_path/'figure_04_conditioning_contrast.pdf','--contrast-png',tmp_path/'figure_04_conditioning_contrast.png']]
    save=export_formats.save_formats
    captured=[];ratios=[]
    def checked_save(fig,pdf,png):
        before=geometry(fig)
        ratios.extend(item['contrast'] for item in apply_palette(fig))
        assert geometry(fig)==before
        first=svg_bytes(fig)
        apply_palette(fig)
        assert svg_bytes(fig)==first
        save(fig,pdf,png)
        captured.append(Path(pdf).stem)
    monkeypatch.setattr(export_formats,'save_formats',checked_save)
    with mpl.rc_context():
        for script,*args in commands:
            mpl.rcdefaults()
            monkeypatch.setattr(sys,'argv',[script,*map(str,args)])
            runpy.run_path(str(ROOT/'scripts/figures'/script),run_name='__main__')
            plt.close('all')
    assert len(captured)==6 and len(set(captured))==6
    assert len(ratios)==20 and min(ratios)>=4.5
    for stem in captured:
        for suffix in ('.pdf','.png','.svg'):
            folder='figures/core_svg' if suffix=='.svg' else 'figures/core'
            assert (tmp_path/(stem+suffix)).read_bytes()==(ROOT/folder/(stem+suffix)).read_bytes()


def test_native_repository_style():
    for path in ['website','scripts/site','.github/workflows/website-preview.yml']:
        assert not (ROOT/path).exists()
    readme=(ROOT/'README.md').read_text()
    assert 'docs/DIALOGUE_REPORT.md' in readme and 'docs/REPRODUCTION.md' in readme
    assert 'home-desktop.png' not in readme and 'website/preview' not in readme


def test_palette_cannot_override_scientific_inputs(tmp_path):
    spec=importlib.util.spec_from_file_location('palette_adoption_guard',ROOT/'scripts/analysis/check_figure1_adoption.py')
    check=importlib.util.module_from_spec(spec);spec.loader.exec_module(check)
    record=json.loads((ROOT/'provenance/FIGURE_PALETTE_2026-09-08.json').read_text())
    for entry in record['changed_files']:
        target=tmp_path/entry['path'];target.parent.mkdir(parents=True,exist_ok=True);target.touch()
    record=copy.deepcopy(record)
    record['changed_files'][0]['path']='data/processed/core_figures/figure_01_panel_b.csv'
    path=tmp_path/'provenance/FIGURE_PALETTE_2026-09-08.json';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(record))
    with pytest.raises(ValueError,match='only 18 panels'):
        check.palette_successors(tmp_path)
