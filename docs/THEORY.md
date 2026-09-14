# General two-copy response operator for a gate crossing an entanglement cut

[Previous: notation](NOTATION.md) · [Return to README](../README.md) · [Next: claim evidence](CLAIM_EVIDENCE_MAP.md)

This document supplies the exact identities used in the [four-figure dialogue](DIALOGUE_REPORT.md). The first part treats general probe ensembles and retains the locally dressed extensions; the second treats stabilizer spectra, the finite response alphabet, and the single-measurement sign corollary. The [claim map](CLAIM_EVIDENCE_MAP.md) separates these deductions from the monitored-ensemble evidence. The [related-work account](RELATED_WORK.md) records the established ingredients; no independent priority claim is attached to the Haar transfer identity or the corollary.

**Conventions.** $D=2^{n/2}$ is the half-chain dimension; $d$ is reserved for the measurement distance in Figure 4. $\chi_2$ is the average normalized linear-entropy increment and $\chi_{\rm rel}=\chi_2/P_m$. Neither is an average finite increment of logarithmic Rényi-2 entropy. Original code arguments named `d` retain their historical meaning of dimension; no implementation or data field is renamed.

## 1. Setting

Let a pure state be partitioned as

$$
|\psi\rangle_{L a b R},
$$

where qubits $a$ and $b$ are adjacent to the central cut. The left half is
$A=La$, and the right half is $B=bR$. For any subsystem $X$, write

$$
P_X=\mathop{\mathrm{Tr}}\nolimits\rho_X^2
   =\mathop{\mathrm{Tr}}\nolimits\!\left(\rho^{\otimes 2}F_X\right),
$$

where $F_X$ swaps the two replicas on $X$.

A two-qubit unitary $U_{ab}$ is applied across the cut. We study the expected
post-gate purity of $A$, equivalently the expected change in normalized linear
entropy.

## 2. Exact response-operator theorem

For an arbitrary probability ensemble $\mathcal E$ of two-qubit gates, define

$$
\Omega_{\mathcal E}
=
\mathbb E_{U\sim\mathcal E}
\left[
U_{ab}^{\dagger\otimes2}F_aU_{ab}^{\otimes2}
\right].
$$

Then

$$
\boxed{
\mathbb E_{U\sim\mathcal E} P'_{La}
=
\mathop{\mathrm{Tr}}\nolimits\!\left[
\rho^{\otimes2}
\left(F_L\otimes\Omega_{\mathcal E}\otimes I_R\right)
\right].
}
$$

### Proof

The post-gate state is

$$
\rho'=(I_{LR}\otimes U_{ab})\rho(I_{LR}\otimes U_{ab}^{\dagger}).
$$

Using $P'_{La}=\mathop{\mathrm{Tr}}\nolimits[(\rho')^{\otimes2}F_{La}]$, cyclicity of the
trace, and $F_{La}=F_LF_a$,

$$
P'_{La}(U)
=
\mathop{\mathrm{Tr}}\nolimits\!\left[
\rho^{\otimes2}
\left(
F_L\otimes U_{ab}^{\dagger\otimes2}F_aU_{ab}^{\otimes2}\otimes I_R
\right)
\right].
$$

Averaging over $U$ proves the result. No Haar assumption is required.

## 3. Locally dressed fixed entanglers

This is the cut-row specialization of the entanglement-feature transfer rule
of [Kuo et al., Eqs. (19) and (60), arXiv:1910.11351v2](https://arxiv.org/abs/1910.11351v2).
The dictionary below makes the equivalence explicit.

Consider the ensemble

$$
U=(u_a\otimes u_b)V(v_a\otimes v_b),
$$

where $V$ is fixed and the one-qubit unitaries are independently Haar
distributed. Output dressings leave $F_a$ invariant and therefore disappear
from $\Omega$. Averaging over the input dressings is the Hilbert--Schmidt
projection onto the commutant of the local two-copy action. For two qubits,

$$
\mathop{\mathrm{Comm}}\nolimits\{v_a^{\otimes2}\otimes v_b^{\otimes2}\}
=
\mathop{\mathrm{span}}\nolimits\{I,F_a,F_b,F_aF_b\}.
$$

Hence

$$
\Omega_V=c_I I+c_aF_a+c_bF_b+c_{ab}F_aF_b.
$$

Substitution into the general theorem gives the exact four-purity stencil

$$
\boxed{
\mathbb E P'_{La}
=
 c_I P_L
+c_a P_{La}
+c_b P_{L\cup b}
+c_{ab}P_R.
}
$$

For the last term, purity of the global state was used:
$P_{L\cup a\cup b}=P_R$. The third term is the purity of the noncontiguous
subsystem consisting of the left interior and the right boundary qubit.

If $D=2^{n/2}$ is the left-half Hilbert-space dimension and

$$
S_{\mathrm{lin}}^{\mathrm{norm}}
=
\frac{D}{D-1}(1-P_{La}),
$$

then the exact expected response is

$$
\boxed{
\chi_V
=
\frac{D}{D-1}
\left[
P_{La}
-c_I P_L
-c_a P_{La}
-c_b P_{L\cup b}
-c_{ab}P_R
\right].
}
$$

The complete central Schmidt spectrum fixes $P_{La}$, but it does not fix
$P_L$, $P_R$, or $P_{L\cup b}$. Therefore the complete central spectrum
does not generally determine the response to a fresh cross-cut gate.

## 4. Coefficients from gate invariants

Use the rescaled definitions of
[Jonnadula et al., Eqs. (16) and (18), arXiv:1909.08139v2](https://arxiv.org/abs/1909.08139v2),
not the original unrescaled product-input entangling power. With
$V_{ij,kl}=\langle ij|V|kl\rangle$, define realignment by
$(V^R)_{ik,jl}=V_{ij,kl}$, where $i,j,k,l\in\{0,1\}$. Then

$$
E_{\mathrm{op}}(V)
=
1-\frac1{16}
\mathop{\mathrm{Tr}}\nolimits\!\left[(V^R V^{R\dagger})^2\right],
\qquad
E_{\mathrm{op}}(\mathrm{SWAP})=\frac34,
$$

$$
e_p(V)
=
\frac{E_{\mathrm{op}}(V)+E_{\mathrm{op}}(V\,\mathrm{SWAP})
      -E_{\mathrm{op}}(\mathrm{SWAP})}
     {E_{\mathrm{op}}(\mathrm{SWAP})},
$$

$$
g_t(V)
=
\frac{E_{\mathrm{op}}(V)-E_{\mathrm{op}}(V\,\mathrm{SWAP})
      +E_{\mathrm{op}}(\mathrm{SWAP})}
     {2E_{\mathrm{op}}(\mathrm{SWAP})}.
$$

For qubits, $e_p/3$ is the product-input average of the unnormalized
one-qubit linear-entropy production.

Evaluating the four Hilbert--Schmidt overlaps of the locally twirled response
operator gives

$$
\boxed{
(c_I,c_a,c_b,c_{ab})
=
\left(
\frac23 e_p,
1-g_t-\frac56 e_p,
g_t-\frac56 e_p,
\frac23 e_p
\right).
}
$$

These two established local-unitary invariants determine this averaged
purity response. They do not completely classify a two-qubit gate up to local
unitaries.

### Entanglement-feature dictionary

Write $q$ for the papers' single-site dimension $d$: here $q=2$, whereas
$D=2^{n/2}$ is the half-chain dimension and our $d$ labels measurement distance.
In the feature basis, a down spin includes a site in a subsystem; $X_a,X_b$
toggle inclusion and $Z_a,Z_b$ read the corresponding signs
($+1$ for exclusion, $-1$ for inclusion). These are not physical gates.
For the output region $La$:

| Transfer-row operation | Input region | Purity in this document |
|---|---|---|
| $I$ | $La$ | $P_{La}=P_m$ |
| $X_a$ | $L$ | $P_L=P_{m-1}$ |
| $X_b$ | $Lab$ | $P_{Lab}=P_{m+1}=P_R$ for pure global inputs |
| $X_aX_b$ | $Lb$ | noncontiguous $P_{L\cup b}$ |

Kuo et al.'s Eq. (19) propagates the purity-feature vector by
$T=\widehat{W}_V\widehat{W}_I^{-1}$, where the gate-feature matrix is
$(\widehat{W}_V)_{\sigma,\tau}=\mathop{\mathrm{Tr}}\nolimits(F_\sigma V^{\otimes2}F_\tau V^{\dagger\otimes2})$
and $\widehat{W}_I$ is its identity-gate Gram matrix. The labels
$\sigma,\tau$ specify subsystem swaps on $ab$. For a direct algebraic
translation of their Eqs. (17) and (60), put $E=E_{\mathrm{op}}(V)$ and
$E_s=E_{\mathrm{op}}(V\,\mathrm{SWAP})$. At $q=2$, their coefficients are
$A_{ab}=16E$ and $B_{ab}=16(3/4-E_s)$. Multiplication gives

$$
T=I-Q\left[u-v(X_a+X_b)+wX_aX_b\right],
\qquad Q=(I-Z_aZ_b)/2,
$$

$$
u=\frac{A_{ab}-B_{ab}/4}{9}=g_t+\frac56e_p,
\quad v=\frac{A_{ab}-B_{ab}}{18}=\frac23e_p,
\quad w=\frac{A_{ab}/4-B_{ab}}{9}=\frac56e_p-g_t.
$$

The cut row has coefficients $(v,1-u,-w,v)$ in the order
$(P_L,P_{La},P_{L\cup b},P_{Lab})$, exactly the displayed stencil. This is a
specialization and change of normalization, not an independent transfer identity. Negative
coefficients are allowed: they are not probabilities of separate experiments.
Only the fresh probe needs local input averaging; no locally scrambled or
equilibrium assumption is imposed on the preceding monitored preparation.
Output local rotations can be omitted because purity is invariant under them.

The identity was numerically checked on 100 Haar-random two-qubit gates.
Direct commutant projection and the invariant formula agreed with maximum
coefficient error

$$
1.17\times10^{-15}.
$$

## 5. Cartan specialization

For

$$
V(\alpha,\beta,\gamma)
=
\exp[-i(\alpha XX+\beta YY+\gamma ZZ)],
$$

let

$$
A=\sin^2(2\alpha),\qquad
B=\sin^2(2\beta),\qquad
C=\sin^2(2\gamma).
$$

Then

$$
e_p
=
\frac23(A+B+C-AB-AC-BC),
\qquad
g_t=\frac13(A+B+C).
$$

These are Jonnadula et al.'s Eq. (31) under
$(c_1,c_2,c_3)=2(\alpha,\beta,\gamma)$; the sign convention of the exponent
does not affect the squared sines.

The probes used in Checkpoint 04 have the exact coefficients

| Probe ensemble | $(c_I,c_a,c_b,c_{ab})$ |
|---|---|
| Haar $U(4)$, or a two-qubit unitary 2-design | $(2/5,0,0,2/5)$ |
| $e^{-i\pi(XX+YY)/8}$ with local input dressing | $(1/3,1/4,-1/12,1/3)$ |
| $e^{-i\pi XX/4}$ with local input dressing | $(4/9,1/9,-2/9,4/9)$ |

The Haar neighboring-cut identity is therefore one point in a larger exact
four-purity response family. More explicitly,
[Akhtar and You, Eq. (20), arXiv:2006.08797v2](https://arxiv.org/abs/2006.08797v2),
give

$$
T_{\mathrm{Haar}}=I-Q\left[I-\frac{q}{q^2+1}(X_a+X_b)\right].
$$

Its cut row is $\mathbb E P'_{La}=q(P_L+P_{Lab})/(q^2+1)$. For qubits this is
$\mathbb E P'_m=(2/5)(P_{m-1}+P_{m+1})$. The response normalization then gives
$\chi_2=D(P_m-\mathbb E P'_m)/(D-1)$ and
$\chi_{\rm rel}=\chi_2/P_m$, with **input** purity in the denominator.
No logarithm-of-average or average-logarithm approximation is used.

## 6. Fixed-spectrum gate-space criterion

Compare two state ensembles with identical central Schmidt spectrum. Define the
high-monitoring minus low-monitoring shifts

$$
A_\partial=\Delta(P_L+P_R),
\qquad
B_\times=\Delta P_{L\cup b}.
$$

Because $\Delta P_{La}=0$, substitution of the invariant coefficients gives

$$
\boxed{
\Delta\chi_V
=-\frac{D}{D-1}
\left[
 g_t B_\times
+\frac{e_p}{6}(4A_\partial-5B_\times)
\right].
}
$$

Since $e_p\ge0$ and $g_t\ge0$, the sufficient conditions

$$
B_\times\ge0,
\qquad
4A_\partial-5B_\times\ge0
$$

imply $\Delta\chi_V\le0$ for every locally dressed two-qubit probe. These
conditions are sufficient, not necessary.

In the extreme-rate Checkpoint 04 comparison, the archived equally pooled
raw-purity shifts satisfy both point inequalities in all five rank-4 dynamics.
The marginal bootstrap interval for the second raw-purity inequality is
positive in three of five primary rank-4 families and all five post-hoc rank-2
families. This is a post-hoc diagnostic, not the locked primary claim or a
simultaneous confidence guarantee over all probes. The
[historical extension estimator](../studies/checkpoint_04/scripts/analyze_gate_space_universality.py)
omits undefined cells within bootstrap draws. It also pools raw purity shifts
across sizes without $D/(D-1)$, unlike the normalized response criterion at
fixed dimension derived above. The archived intervals must not be assigned to
the dimension-weighted pooled criterion or to the adopted Figure 1 bootstrap.

## 7. Scope

The response-operator theorem is exact. The empirical statement that stronger
monitoring changes the required purities in a particular direction is separate.
Checkpoint 04 supports that state-side direction across several finite one-
dimensional circuit families and in exactly spectrum-matched physical
stabilizer states. It does not prove a thermodynamic universality class,
critical exponent, transition point, or nonlinear-entropy analogue.


---

# Stabilizer boundary code and exact fixed-spectrum susceptibility

## 1. Setting

Consider a pure stabilizer state on an even open chain of `n` qubits. Let

$$
S_j=S(1,\ldots,j)
$$

be the bipartite von Neumann entropy in bits across the cut after site `j`, and
let the central cut be `m=n/2`. Define

$$
\delta_L=S_m-S_{m-1},\qquad
\delta_R=S_m-S_{m+1}.
$$

The ordered pair

$$
\boldsymbol{\delta}=(\delta_L,\delta_R)
$$

is called the **boundary code**. It records how the central cut sits relative
to the two immediately neighboring cuts.

For a fresh Haar-random two-qubit gate, or a uniformly random two-qubit
Clifford gate, crossing the central bond, define the exact normalized
linear-entropy susceptibility

$$
\chi_2
=
\frac{D}{D-1}
\left[
P_m-\frac25(P_{m-1}+P_{m+1})
\right],
\qquad D=2^m,
$$

where `P_j=Tr rho_j^2` is the purity at cut `j`. Define the relative response

$$
\chi_{\rm rel}=\frac{\chi_2}{P_m}.
$$

The first displayed identity is the qubit cut-row specialization of the
[Haar transfer rule](https://arxiv.org/abs/2006.08797v2), Eq. (20), derived above.
Uniform Clifford averaging has the same two-copy moment by the established
unitary-design result. Neither step requires a stabilizer input.

## 2. Flat-spectrum lemma

For a pure stabilizer state, the nonzero eigenvalues of every reduced density
matrix are equal. If the entropy across a cut is `S_j`, then the Schmidt rank is
`2^{S_j}` and

$$
P_j=2^{-S_j}.
$$

Consequently, fixing `S_m` fixes the **complete** central Schmidt spectrum, not
only its entropy or purity.

This is the reduced-stabilizer-projector property of
[Fattal et al., Eqs. (4)-(6), quant-ph/0406168](https://arxiv.org/abs/quant-ph/0406168).
The finite alphabet below is a direct substitution into the established
transfer rule, not a separately observed physical law.

## 3. Finite-alphabet theorem

For adjacent cuts,

$$
|S_m-S_{m\pm1}|\le 1.
$$

The bound follows from the fact that adding or removing one qubit changes the
entropy by at most one bit. Stabilizer entropies are integers, so

$$
\delta_L,\delta_R\in\{-1,0,1\}.
$$

Substituting `P_j=2^{-S_j}` into the exact response gives

$$
\boxed{
\chi_{\rm rel}
=
\frac{D}{D-1}
\left[
1-\frac25\left(2^{\delta_L}+2^{\delta_R}\right)
\right].
}
$$

Thus the relative susceptibility belongs to a finite alphabet determined by
the boundary code:

| Boundary code | `chi_rel / [D/(D-1)]` |
|---|---:|
| `(-1,-1)` | `+0.6` |
| `(-1,0)` or `(0,-1)` | `+0.4` |
| `(0,0)` | `+0.2` |
| `(-1,+1)` or `(+1,-1)` | `0` |
| `(0,+1)` or `(+1,0)` | `-0.2` |
| `(+1,+1)` | `-0.6` |

This identity is exact. No gate sampling or state-vector approximation is
needed.

## 4. Exact decomposition of the monitoring dependence

Let

$$
q_p(\boldsymbol{\delta}\mid S_m,\tau,n)
$$

be the boundary-code distribution at monitoring rate `p`, conditional on the
complete central stabilizer spectrum through `S_m`, probe time `tau`, and size
`n`. Then

$$
\mathbb E[\chi_{\rm rel}\mid S_m,\tau,n,p]
=
\sum_{\boldsymbol{\delta}} q_p(\boldsymbol{\delta}\mid S_m,\tau,n)\,r_n(\boldsymbol{\delta}),
$$

where `r_n(delta_L,delta_R)` is the table value above including the finite-size factor
`D/(D-1)`.

Therefore every fixed-spectrum monitoring effect is exactly a redistribution
of boundary-code probabilities. In differential notation,

$$
\partial_p\mathbb E[\chi_{\rm rel}]
=
-\frac{2D}{5(D-1)}
\sum_{\boldsymbol{\delta}}
\left(2^{\delta_L}+2^{\delta_R}\right)
\partial_p q_p(\boldsymbol{\delta}\mid S_m,\tau,n).
$$

The differential expression assumes the conditional probabilities are differentiable in $p$; it is not a claim that the finite-grid regression directly measures a derivative at every rate. For the actual fixed-effect estimator, applying the same linear regression to the response and each code indicator gives an exact coefficient decomposition on identical rows and weights. That reconstruction is a consistency identity, not a statistically independent experiment.

In the representative $n=256$ projective-Z comparison displayed in Figure 2, Checkpoint 05 finds that stronger monitoring shifts probability away from
codes containing `-1` increments and toward codes containing `+1` increments.
At fixed central rank, the central cut therefore becomes more likely to be a
local entanglement maximum. The exact response formula converts that spatial
reshaping into reduced entangling susceptibility.

## 5. One-measurement corollary

A projective Pauli measurement on one side of a stabilizer bipartition changes
the stabilizer entropy across that cut by either zero or minus one:

$$
\Delta S_m\in\{0,-1\}.
$$

For a random measurement outcome, the two signs have the same phase-free
stabilizer support and hence the same entropy. Local operations cannot increase
the average bipartite entanglement, while replacing one stabilizer generator
changes the relevant binary ranks by at most one. Deterministic measurements
leave the stabilizer support unchanged.

On the branch $\Delta_M S_m=0$, the complete central Schmidt spectrum is exactly unchanged. The subscript $M$ distinguishes the effect of the measurement from the subsequent ensemble-averaged fresh-gate response. The same entropy argument applies at each neighboring cut: the measured site lies on one side of each bipartition. Therefore

$$
\Delta_M P_m=0,\qquad
\Delta_M P_{m-1}\geq0,\qquad
\Delta_M P_{m+1}\geq0,
$$

because the premeasurement state and each conditional postmeasurement state are pure stabilizer states and $P_j=2^{-S_j}$. Subtracting the Haar/uniform-Clifford response identity before and after measurement gives

$$
\boxed{
\Delta_M\chi_{\rm rel}
=-\frac{2D}{5(D-1)P_m}
\left(\Delta_M P_{m-1}+\Delta_M P_{m+1}\right)
\leq0.
}
$$

Here $P_m$ is the unchanged central purity. Equality holds precisely when both neighboring purities are unchanged; strict suppression requires at least one neighboring entropy to decrease. A deterministic measurement leaves the state unchanged and saturates the inequality.

This is a corollary of the two existing identities, not a new numerical result. It applies to every nonzero-probability outcome of a single-site projective Pauli measurement on a pure stabilizer input, followed by the stated Haar or uniform-Clifford **ensemble-averaged** probe. It is not a sign theorem for each individual gate, an arbitrary probe ensemble, weak measurements, or generic non-stabilizer inputs.

The sign alone does not determine the frequency, magnitude, or distance dependence of suppression. In particular,

$$
D_{\rm rel}
=\Delta_M\chi_{\rm rel}^{\rm near}
-\Delta_M\chi_{\rm rel}^{\rm far}
$$

is a difference between two nonpositive quantities and has no fixed sign from this corollary alone. Figure 4 supplies evidence for a negative paired location contrast and near-cut concentration within its declared spectrum-preserving populations. Its strict same-side joint-preservation and common-eligibility checks are specified in [the evidence reassessment](EVIDENCE_REASSESSMENT.md). These interventions do not quantitatively derive the long-run monitoring-rate coefficient in Figure 3.

## 6. Scope

The theorem establishes exact sufficiency of the three adjacent stabilizer
entropies for the Haar/Clifford purity-normalized linear-entropy response. It does not say that a
small physical window of qubits determines those entropies, nor that the new
susceptibility is an order parameter. The empirical claims concern how the
boundary-code distribution changes in the monitored circuit ensemble.

[Next: claim evidence](CLAIM_EVIDENCE_MAP.md) · [Return to README](../README.md)
