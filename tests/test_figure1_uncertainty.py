"""Tests for the declared new uncertainty calculation, not old CI recovery."""
from fractions import Fraction
import importlib.util
import itertools
from pathlib import Path
import sys
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('f1_uncertainty',ROOT/'scripts/analysis/complete_figure1_uncertainty.py')
f1=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=f1
spec.loader.exec_module(f1)


def stratum(name,values,sign=1):
    array=np.asarray(values,dtype=float)
    return f1.Stratum(name,10,.24 if sign==1 else .08,np.arange(array.shape[1]),np.arange(len(array)),array,sign)


def test_same_trajectory_times_keep_common_weight():
    high=stratum('high',[[1,10],[3,30]])
    low=stratum('low',[[0,0],[0,0]],-1)
    counts=np.array([[2,0],[1,1],[0,2]],dtype=np.uint8)
    y=f1.weighted_estimates([low,high],[counts,counts],2)
    np.testing.assert_allclose(y,[5.5,11,16.5],atol=0,rtol=0)


def test_equal_cell_weights_not_row_weights():
    high=stratum('high',[[2,100],[4,np.nan],[6,np.nan]])
    low=stratum('low',[[0,0]],-1)
    result=f1.weighted_estimates([high,low],[np.ones((1,3),dtype=np.uint8),np.ones((1,1),dtype=np.uint8)],2)
    assert result[0]==52


def test_missing_required_cell_invalidates_entire_replicate():
    high=stratum('high',[[2,np.nan],[np.nan,8]])
    counts=np.array([[2,0],[1,1],[0,2]],dtype=np.uint8)
    y=f1.weighted_estimates([high],[counts],2)
    assert np.isnan(y[[0,2]]).all()
    assert y[1]==5


def test_inclusion_exclusion_against_exhaustive_draws():
    values=np.array([[1,np.nan],[np.nan,2],[np.nan,np.nan]])
    valid=0
    for draws in itertools.product(range(3),repeat=3):
        valid+=bool(np.isfinite(values[list(draws)]).any(axis=0).all())
    assert f1.valid_probability(values)==Fraction(valid,27)


def test_sampler_stores_exact_cluster_multiplicities_and_first_valid_draws():
    s=stratum('high',[[2,np.nan],[np.nan,8]])
    a,draws,info=f1.sample([s],2,[2026090801,0,0,0],1000,100,10000)
    assert info['rejected']>0
    assert len(draws)==1000
    assert a['valid'][-1]
    assert len(a['accepted_indices'])==1000
    assert (a['high_counts'].sum(axis=1)==2).all()
    assert a['valid'].sum()==1000
    np.testing.assert_array_equal(draws,np.full(1000,5.))


def test_sampler_is_deterministic_and_includes_missing_rows():
    s=stratum('high',[[1,np.nan],[np.nan,2],[3,4]])
    x=f1.sample([s],2,[99,1,0,3],1000,100,10000)
    y=f1.sample([s],2,[99,1,0,3],1000,100,10000)
    for k in x[0]:np.testing.assert_array_equal(x[0][k],y[0][k])
    assert x[2]==y[2]


def test_rejects_invalid_budget_or_population():
    s=stratum('high',[[1,2]])
    with pytest.raises(ValueError):f1.sample([s],2,[1],0)
    with pytest.raises(ValueError):f1.valid_probability(np.array([[1,np.nan]]))


def test_deterministic_npz_without_pickles(tmp_path):
    a={'x':np.array([[1,np.nan]]),'y':np.array([True,False])}
    f1.save_arrays(tmp_path/'a.npz',a);f1.save_arrays(tmp_path/'b.npz',a)
    assert (tmp_path/'a.npz').read_bytes()==(tmp_path/'b.npz').read_bytes()
    with np.load(tmp_path/'a.npz',allow_pickle=False) as z:
        for k in a:np.testing.assert_array_equal(a[k],z[k])


def test_declared_plan_hash_and_fixed_baseline():
    import json
    assert f1.sha(f1.PLAN.read_bytes())==f1.PLAN_SHA256
    plan=json.loads(f1.PLAN.read_text())
    assert plan['common_support']['clifford_z']==[[10,6],[10,8],[12,8],[14,6]]
    assert plan['bootstrap_replicates']==50000


def test_wrong_source_member_rejected(tmp_path):
    plan={'source_member_sha256':{'a':'0'*64}}
    (tmp_path/'a').write_text('not the authentic input')
    with pytest.raises(ValueError,match='Source integrity'):f1.read_inputs(plan,tmp_path)
