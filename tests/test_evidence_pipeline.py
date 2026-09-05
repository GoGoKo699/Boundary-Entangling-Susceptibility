"""Software checks, distinct from frozen-result regression checks."""
from pathlib import Path
import importlib.util
import subprocess
import sys
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('evidence',ROOT/'scripts/analysis/reassess_evidence.py')
evidence=importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence)

def test_within_stratum_estimator_on_synthetic_data():
    rows=[]
    for tau,rank,intercept in [(6,1,3),(10,2,-7)]:
        for p in [.2,.26,.34]:
            for _ in range(10):
                rows.append({'tau':tau,'S_central':rank,'p_measure':p,'recomputed':intercept+2*(p-.26)/.02})
    beta,count=evidence.fe_slope(pd.DataFrame(rows))
    assert beta==pytest.approx(2.)
    assert count==60

def test_cluster_bootstrap_keeps_columns_paired():
    x=np.arange(20.)
    samples=evidence.bootstrap_matrix(np.column_stack([x,3*x]),100,np.random.default_rng(3))
    np.testing.assert_allclose(samples[:,1],3*samples[:,0],atol=1e-12)

def test_wrong_archive_is_rejected(tmp_path):
    path=tmp_path/'incorrect.zip';path.write_bytes(b'not the frozen data')
    with pytest.raises(ValueError,match='identity mismatch'):
        evidence.Source(path)

def test_all_six_panel_triples_are_generated(tmp_path):
    output=tmp_path/'figures'
    subprocess.run([sys.executable,str(ROOT/'reproduce.py'),'--core-figures','--output',str(output)],check=True)
    assert len(list(output.glob('*.pdf')))==6
    assert len(list(output.glob('*.png')))==6
    assert len(list(output.glob('*.svg')))==6
    svg=ET.parse(output/'figure_01_panel_b.svg').getroot()
    view=np.array([float(v) for v in svg.attrib['viewBox'].split()])
    np.testing.assert_allclose(view,[0,0,303.84,194.4],atol=1e-4)
    # Frozen PDF typography: the accepted peak/dip text is 9.2, not the earlier 9.1 reconstruction.
    source=(ROOT/'scripts/figures/make_figure_02.py').read_text()
    assert 'fontsize=9.2' in source
