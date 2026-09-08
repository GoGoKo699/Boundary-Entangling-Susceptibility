"""Small independent regression checks for two Figure 1 interpretation risks.

These tests confirm declared limitations, rather than asserting a baseline bug.
Run explicitly with pytest; no baseline test configuration is changed.
"""
import itertools
from fractions import Fraction
import numpy as np
from figure1_independent import exact_survival
from figure1_trajectory_replay import purity

def test_support_survival_matches_all_ordered_small_draws():
    patterns=[(1,0),(0,1),(0,0)]
    surviving=sum(all(any(patterns[i][j] for i in draws) for j in range(2))
                  for draws in itertools.product(range(3),repeat=3))
    assert exact_survival(patterns)==Fraction(surviving,27)==Fraction(4,9)

def test_equal_schmidt_input_has_gauge_dependent_reweighting():
    """Same 2-Bell-pair input, same replacement spectrum, two SVD gauges."""
    mu=np.array([.4,.3,.2,.1]); outputs=[]
    identity=np.eye(4)
    for ordering in [[0,1,2,3],[0,3,2,1]]:
        U=identity[:,ordering]; Vh=U.T
        np.testing.assert_allclose(U@np.diag([.5]*4)@Vh,identity/2,atol=0,rtol=0)
        M=U@np.diag(np.sqrt(mu))@Vh
        v=M.T.reshape(-1)
        np.testing.assert_allclose(np.linalg.eigvalsh(M@M.T),sorted(mu),atol=1e-15,rtol=0)
        Pc=purity(v,[0,1]);PL=purity(v,[0]);PR=purity(v,[3])
        outputs.append(4/3*(1-.4*(PL+PR)/Pc))
    np.testing.assert_allclose(outputs,[-28/45,-12/25],atol=1e-14,rtol=0)
    assert abs(outputs[0]-outputs[1])>.1

def test_normalization_is_input_purity_not_average_logarithm():
    # Algebraic two-point ensemble, independent of physical gate reachability.
    D=4; P=.5; post=np.array([.3,.7])
    relative_linear=D/(D-1)*(P-post.mean())/P
    mean_log_increment=np.mean(np.log2(P/post))
    assert abs(relative_linear)<1e-15
    assert mean_log_increment>.12
