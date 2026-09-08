"""Audit-owned tests of estimator identities on heterogeneous synthetic cells."""
import numpy as np
import pandas as pd
from figures23_audit import eligible_cells, explicit_fit, pairwise_fit


def test_pairwise_weighting_matches_explicit_fe_with_unequal_support():
    rows=[]
    for s, rates, sizes, slope in [(0,[.20,.24,.28],[12,30,18],-.1),(1,[.24,.28,.34],[15,11,25],.03)]:
        for p,count in zip(rates,sizes):
            for j in range(count):
                rows.append(dict(tau=6,S_central=s,p_measure=p,y=5*s+slope*(p-.26)/.02 + (j-(count-1)/2)/100))
    d=pd.DataFrame(rows);keep=eligible_cells(d);beta,pairs=pairwise_fit(keep,'y')
    assert np.isclose(beta,explicit_fit(keep,'y'),atol=1e-13)
    assert (pairs.normalized_weight>=0).all()
    assert np.isclose(pairs.normalized_weight.sum(),1)
    assert not np.isclose(beta,(-.1+.03)/2)
    # An unstratified regression confounds the large stratum intercept shift.
    unadjusted=np.polyfit((d.p_measure-.26)/.02,d.y,1)[0]
    assert abs(unadjusted-beta)>.1


def test_low_count_cell_is_removed_and_indicator_conservation_is_linear():
    d=pd.DataFrame([dict(tau=6,S_central=0,p_measure=p,y=float(p>=.25))
                    for p,count in zip([.20,.24,.28,.34],[20,9,20,20]) for _ in range(count)])
    keep=eligible_cells(d);assert .24 not in keep.p_measure.unique()
    keep['complement']=1-keep.y
    a,_=pairwise_fit(keep,'y');b,_=pairwise_fit(keep,'complement')
    assert np.isclose(a+b,0,atol=1e-13)
    keep['response']=.6*keep.y-.2*keep.complement
    c,_=pairwise_fit(keep,'response');assert np.isclose(c,.6*a-.2*b,atol=1e-13)
