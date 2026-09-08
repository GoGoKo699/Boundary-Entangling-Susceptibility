"""Strict expected failures documenting baseline supporting-table defects.

An unexpected pass requires reviewing this audit finding. The tests neither
change the scientific baseline nor claim its current Figure 1 panel is wrong.
"""
import csv
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[3]

@pytest.mark.xfail(strict=True,reason='Confirmed baseline defect: compact four-purity table does not reconstruct its own stated endpoint')
def test_compact_exact_stencil_reconstructs_stated_floquet_xy_endpoint():
    rows=list(csv.DictReader((ROOT/'studies/checkpoint_04/results/response_stencil_decomposition.csv').open()))
    row=next(r for r in rows if r['family']=='floquet_cartan_z' and r['probe']=='cartan_xy_pi8')
    # This identity should hold independently of original source provenance.
    assert abs(float(row['reconstruction'])-float(row['observed_response_contrast']))<2e-11, row

@pytest.mark.xfail(strict=True,reason='Confirmed baseline defect: compact extension endpoint differs from included original rows and consolidated archive')
def test_compact_replication_haar_xy_matches_record_reconstruction():
    rows=list(csv.DictReader((ROOT/'studies/checkpoint_04/results/intervention_cross_architecture.csv').open()))
    row=next(r for r in rows if r['run']=='independent_seed_rank4' and r['family']=='haar_z' and r['probe']=='cartan_xy_pi8')
    # Value independently reconstructed in figure1_extensions.py from archived rows,
    # and verified there against archive analysis/consolidated without using this CSV.
    expected=-0.05625102837528647
    assert abs(float(row['estimate'])-expected)<2e-11, row
