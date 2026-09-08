"""Regression checks for approved Figure 1 only; no coverage claim."""
import importlib.util
from pathlib import Path
import json
import pandas as pd
import pytest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('figure1_adoption_check',ROOT/'scripts/analysis/check_figure1_adoption.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def tables():
    return (pd.read_csv(ROOT/'data/processed/core_figures/figure_01_panel_b.csv',dtype=str),
            pd.read_csv(ROOT/'results/historical_figure1/figure_01_panel_b.csv',dtype=str))

def test_adopted_baseline():
    assert module.verify()['adopted']

def test_points_and_metadata_unchanged():
    module.check_tables(*tables())

def test_reject_changed_point():
    current,historical=tables();current.loc[0,'estimate']='-0.2'
    with pytest.raises(ValueError,match='Only'):module.check_tables(current,historical)

def test_reject_invalid_interval():
    current,historical=tables();current.loc[0,'ci_low']='1'
    with pytest.raises(ValueError,match='Invalid'):module.check_tables(current,historical)

def test_primary_recipe_not_sensitivity():
    info=json.loads((ROOT/'provenance/FIGURE1_ADOPTION_2026-09-08.json').read_text())
    assert info['primary_pool']=='eligible_union' and info['historical_resamples_recovered'] is False
    comparison=pd.read_csv(ROOT/'results/figure1_uncertainty/interval_comparison.csv')
    current,_=tables()
    for row in current.itertuples(index=False):
        match=comparison[(comparison.pool=='eligible_union')&(comparison.run==row.run)&(comparison.family==row.family)].iloc[0]
        assert abs(float(row.ci_low)-match.ci_low)<2e-15
        assert abs(float(row.ci_high)-match.ci_high)<2e-15


def test_plot_changes_only_interval_coordinates(monkeypatch,tmp_path):
    import sys
    import numpy as np
    sys.path.insert(0,str(ROOT/'scripts/figures'))
    spec=importlib.util.spec_from_file_location('figure1_plot_check',ROOT/'scripts/figures/make_figure_01_frozen.py')
    plot=importlib.util.module_from_spec(spec);spec.loader.exec_module(plot)
    captured=[]
    monkeypatch.setattr(plot,'save_formats',lambda fig,pdf,png:captured.append(fig))
    for name in ['results/historical_figure1/figure_01_panel_b.csv','data/processed/core_figures/figure_01_panel_b.csv']:
        monkeypatch.setattr(sys,'argv',['plot','--csv',str(ROOT/name),'--pdf',str(tmp_path/'p.pdf'),'--png',str(tmp_path/'p.png')])
        plot.main()
    old,new=captured
    np.testing.assert_array_equal(old.get_size_inches(),new.get_size_inches())
    a,b=old.axes[0],new.axes[0]
    np.testing.assert_array_equal(a.get_position().bounds,b.get_position().bounds)
    assert a.get_xlim()==b.get_xlim() and a.get_ylim()==b.get_ylim()
    assert a.get_xlabel()==b.get_xlabel()
    assert [t.get_text() for t in a.get_yticklabels()]==[t.get_text() for t in b.get_yticklabels()]
    for marker in ['o','s']:
        la=next(x for x in a.lines if x.get_marker()==marker)
        lb=next(x for x in b.lines if x.get_marker()==marker)
        np.testing.assert_array_equal(la.get_xydata(),lb.get_xydata())
        assert la.get_markersize()==lb.get_markersize()
    table=pd.read_csv(ROOT/'data/processed/core_figures/figure_01_panel_b.csv')
    for i,run in enumerate(['primary','independent']):
        rows=table[table.run==run].sort_values('family_order')
        segments=b.collections[i].get_segments()
        np.testing.assert_allclose([x[0,0] for x in segments],rows.ci_low)
        np.testing.assert_allclose([x[1,0] for x in segments],rows.ci_high)
