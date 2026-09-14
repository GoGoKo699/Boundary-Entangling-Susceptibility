> Historical source document, preserved for the recorded run conventions. Current claim strength and reproducibility status are in the root `docs/` guides; historical fit language is not an active claim.

# Methods and definitions

## 1. State and cut conventions

All simulations use pure state vectors with little-endian qubit indexing. For
an even chain $n=2m$, the central cut lies between qubits $a=m-1$ and
$b=m$. The left half is $A=La=\{0,\ldots,m-1\}$, and the right half is
$B=bR=\{m,\ldots,n-1\}$.

The central Schmidt decomposition is

```math
|\psi\rangle
=
\sum_j\sqrt{\lambda_j}
|u_j\rangle_A|v_j\rangle_B,
\qquad
\lambda_1\ge\lambda_2\ge\cdots\ge0,
\qquad
\sum_j\lambda_j=1.
```

For any subsystem $X$,

$$
P_X=\mathop{\mathrm{Tr}}\nolimits\rho_X^2.
$$

The normalized linear entropy of the half chain is

```math
S_{2,\mathrm{lin}}
=
\frac{d}{d-1}(1-P_A),
\qquad d=2^{n/2}.
```

The entangling susceptibility $\chi$ is the expected change in this quantity
after a fresh two-qubit probe gate crossing the central cut.

## 2. Purity stencil

Write

- $P_L$: purity of qubits $0,\ldots,m-2$;
- $P_A=P_{La}$: central half-chain purity;
- $P_R$: purity of qubits $m+1,\ldots,n-1$, equivalently of
  $L\cup a\cup b$ for a global pure state;
- $P_{L\cup b}$: purity of the noncontiguous subsystem containing the left
  interior and the right boundary qubit.

For a Haar or uniformly random two-qubit Clifford probe,

```math
\chi_{\mathrm{Haar}}
=
\frac{d}{d-1}
\left[P_A-\frac25(P_L+P_R)\right].
```

For the two locally dressed Cartan probes, the exact coefficients are stored in
`probe_response_coefficients.csv` and derived in
`GENERAL_RESPONSE_OPERATOR_THEOREM.md`.

## 3. Primary cross-architecture simulation

### 3.1 Grid

- sizes: $n=10,12,14$;
- monitoring rates: $p=0.08,0.16,0.24$;
- probe times: $\tau=6,8$;
- trajectories per $(\mathrm{family},n,p)$: 24;
- discovery trajectories: 0--11;
- confirmatory trajectories: 12--23;
- base seed: `2026081804`.

The internal evolution step count is $\tau n$. Each step applies both
brickwork sublayers and then the monitoring layer. Sublayer order alternates
between cycles in the locked primary simulator.

### 3.2 Circuit and measurement families

`haar_z`
: Fresh Haar-random $U(4)$ gates on every active bond; projective Z
  measurements.

`clifford_z`
: Fresh uniformly sampled two-qubit Clifford gates; projective Z measurements.

`floquet_cartan_z`
: A generic non-Clifford Cartan entangler with fixed bond-dependent local
  dressings, repeated as a Floquet brickwork circuit; projective Z measurements.

`haar_random_pauli`
: Fresh Haar gates; each selected site is projectively measured in an
  independently sampled X, Y, or Z basis.

`haar_weak_z_eta06`
: Fresh Haar gates; each selected site receives the two-outcome weak Z POVM

  $$
  E_{\pm}=\frac12(I\pm0.6Z).
  $$

Measurement locations are independently selected with probability $p$ after
each complete brickwork cycle.

### 3.3 Two-qubit Clifford sampling

The complete two-qubit Clifford group, modulo global phase, contains 11,520
matrices. Two independently checked samplers are retained:

- the primary intervention uses the four local-equivalence classes with class
  weights $1:9:9:1$ and independent one-qubit Clifford factors on both sides;
- the physical stabilizer arm samples uniformly by integer index from the
  explicit table `data/two_qubit_clifford_group.npz`.

The explicit table was generated from Clifford generators and checked for:

- 11,520 phase-distinct elements;
- maximum unitarity error below $9\times10^{-16}$;
- Pauli-conjugation error below $2\times10^{-15}$;
- exact two-copy response coefficients equal to the Haar values within
  $6\times10^{-17}$.

The class-weighted sampler has the same exact two-copy coefficients. Its purpose
in the primary intervention is the response-level Clifford architecture test;
the explicit table provides an independent implementation in the physical arm.

## 4. Central-spectrum intervention

For each physical state, compute

$$
M=U\,\mathop{\mathrm{diag}}\nolimits(\sqrt{\lambda})V^\dagger.
$$

For every $(\mathrm{family},n,\tau)$ cell, the discovery trajectories define a
rank-4 target spectrum

```math
\mu^{(4)}
=
\mathop{\mathrm{mean}}\nolimits_{\mathrm{discovery}}
\frac{(\lambda_1,\ldots,\lambda_4)}{\sum_{j=1}^4\lambda_j},
```

renormalized to unit sum. A confirmatory state with rank at least four is
reconstructed as

```math
M_{\mathrm{eq}}
=
U_{[:,1:4]}
\mathop{\mathrm{diag}}\nolimits(\sqrt{\mu^{(4)}})
V^\dagger_{[1:4,:]}.
```

This makes the complete nonzero central spectrum identical within the cell
while retaining the original leading Schmidt vectors. Confirmatory states are
never used to construct the target spectrum.

The maximum within-cell purity, entropy, and leading-eigenvalue range after
equalization is zero at stored precision.

The independent-seed rank-4 run uses base seed `2026081805`, 16 trajectories
per cell, and an 8/8 discovery-confirmatory split.

The rank-2 run uses the primary grid and seed but constructs rank-2 targets. It
was added after inspecting rank support and is explicitly post hoc.

## 5. Primary intervention statistic

For every family and probe, the primary contrast is

```math
\Delta\chi
=
\chi(p=0.24)-\chi(p=0.08)
```

on confirmatory equalized states.

The mean is first computed within each of the six $(n,\tau)$ cells and then
averaged equally across cells. This prevents cells with more rank-eligible
states from receiving greater weight.

Uncertainty uses a trajectory-cluster bootstrap:

1. trajectories are resampled with replacement independently within each
   $(\mathrm{family},n,p)$ cell;
2. both probe-time rows of a trajectory receive the same bootstrap weight;
3. cell contrasts are recomputed;
4. the six cell contrasts are averaged;
5. percentile 95% intervals use 4,000 replicates.

Size-specific and adjacent-rate tables use the same procedure.

## 6. Physical exact-spectrum stabilizer arm

### 6.1 Why the spectrum is exactly matched

The physical arm uses only:

- random single-qubit stabilizer product states;
- uniformly random two-qubit Clifford gates;
- projective Pauli measurements.

Every trajectory therefore remains a pure stabilizer state. Across a
bipartition, its nonzero Schmidt eigenvalues are flat. If the Schmidt rank is
$r=2^k$, then

$$
\lambda_1=\cdots=\lambda_r=\frac1r,
\qquad
\lambda_{j>r}=0.
$$

Thus fixing $(n,\tau,k)$ fixes the complete central spectrum exactly. No
counterfactual state construction is used.

### 6.2 Main run

- dynamics: uniform two-qubit Clifford;
- measurement protocols: projective Z and projective random Pauli;
- sizes: $n=10,12,14$;
- monitoring rates: $p=0.08,0.12,0.16,0.20,0.24$;
- probe times: $\tau=6,8$;
- trajectories per cell: 160;
- discovery/confirmatory split: 80/80;
- base seed: `2026082019`;
- total trajectories: 4,800;
- saved state rows: 9,600.

The independent physical run uses 80 trajectories per cell, a 40/40 split,
base seed `2026082107`, 2,400 trajectories, and 4,800 state rows.

### 6.3 Fixed-stratum model

For each measurement protocol and split, define

$$
\text{stratum}
=(n,\tau,\log_2 r).
$$

Eligible strata contain at least two monitoring-rate levels and at least eight
states. The confirmatory primary model is

$$
y_i=\alpha_{\text{stratum}(i)}+\beta p_{\mathrm{step},i}+\varepsilon_i,
\qquad
p_{\mathrm{step}}=\frac{p-0.16}{0.04},
$$

with trajectory-cluster robust covariance. The reported coefficient $\beta$
is therefore the response change per $\Delta p=0.04$ after exact full-spectrum
stratification.

The same model is fit to the neighboring-cut purity sum and to the two
non-Haar exact probe endpoints. Size-specific fits are also reported.

This is a conditional comparison, not a randomized causal estimate, because
central Schmidt rank is generated by the monitored dynamics and is therefore a
post-dynamics variable.

## 7. Finite probe-bank validation

The physical stabilizer arm also applies a fixed 12-gate Clifford bank within
each $(n,\tau)$ cell. The exact Haar/Clifford-2-design endpoint is primary.
Finite-bank means, half-bank correlations, and exact-versus-finite correlations
are retained as implementation checks.

## 8. Algebra and simulator validation

The package checks:

- state normalization after every monitored trajectory;
- unitary errors for Haar, Clifford, and Cartan gates;
- projective and weak-measurement normalization;
- Schmidt reconstruction and equalization;
- exact Clifford 2-design response coefficients;
- Monte Carlo agreement with the response-operator formula;
- gate-invariant coefficient identity on 100 random two-qubit unitaries;
- rowwise reconstruction of every stored exact response;
- stabilizer-spectrum flatness and power-of-two Schmidt rank;
- file hashes and archive integrity.

## 9. Software environment

The package was tested with:

- Python 3.13.5;
- NumPy 2.3.5;
- pandas 2.2.3;
- SciPy 1.17.0;
- Matplotlib 3.10.8.

The final runs use exact state-vector simulation. Checkpoint 05 proposes a
stabilizer-tableau implementation for substantially larger systems.
