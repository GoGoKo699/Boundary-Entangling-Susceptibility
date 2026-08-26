# General two-copy response operator for a gate crossing an entanglement cut

## 1. Setting

Let a pure state be partitioned as

\[
|\psi\rangle_{L a b R},
\]

where qubits \(a\) and \(b\) are adjacent to the central cut. The left half is
\(A=La\), and the right half is \(B=bR\). For any subsystem \(X\), write

\[
P_X=\operatorname{Tr}\rho_X^2
   =\operatorname{Tr}\!\left(\rho^{\otimes 2}F_X\right),
\]

where \(F_X\) swaps the two replicas on \(X\).

A two-qubit unitary \(U_{ab}\) is applied across the cut. We study the expected
post-gate purity of \(A\), equivalently the expected change in normalized linear
entropy.

## 2. Exact response-operator theorem

For an arbitrary probability ensemble \(\mathcal E\) of two-qubit gates, define

\[
\Omega_{\mathcal E}
=
\mathbb E_{U\sim\mathcal E}
\left[
U_{ab}^{\dagger\otimes2}F_aU_{ab}^{\otimes2}
\right].
\]

Then

\[
\boxed{
\mathbb E_{U\sim\mathcal E} P'_{La}
=
\operatorname{Tr}\!\left[
\rho^{\otimes2}
\left(F_L\otimes\Omega_{\mathcal E}\otimes I_R\right)
\right].
}
\]

### Proof

The post-gate state is

\[
\rho'=(I_{LR}\otimes U_{ab})\rho(I_{LR}\otimes U_{ab}^{\dagger}).
\]

Using \(P'_{La}=\operatorname{Tr}[(\rho')^{\otimes2}F_{La}]\), cyclicity of the
trace, and \(F_{La}=F_LF_a\),

\[
P'_{La}(U)
=
\operatorname{Tr}\!\left[
\rho^{\otimes2}
\left(
F_L\otimes U_{ab}^{\dagger\otimes2}F_aU_{ab}^{\otimes2}\otimes I_R
\right)
\right].
\]

Averaging over \(U\) proves the result. No Haar assumption is required.

## 3. Locally dressed fixed entanglers

Consider the ensemble

\[
U=(u_a\otimes u_b)V(v_a\otimes v_b),
\]

where \(V\) is fixed and the one-qubit unitaries are independently Haar
distributed. Output dressings leave \(F_a\) invariant and therefore disappear
from \(\Omega\). Averaging over the input dressings is the Hilbert--Schmidt
projection onto the commutant of the local two-copy action. For two qubits,

\[
\operatorname{Comm}\{v_a^{\otimes2}\otimes v_b^{\otimes2}\}
=
\operatorname{span}\{I,F_a,F_b,F_aF_b\}.
\]

Hence

\[
\Omega_V=c_I I+c_aF_a+c_bF_b+c_{ab}F_aF_b.
\]

Substitution into the general theorem gives the exact four-purity stencil

\[
\boxed{
\mathbb E P'_{La}
=
 c_I P_L
+c_a P_{La}
+c_b P_{L\cup b}
+c_{ab}P_R.
}
\]

For the last term, purity of the global state was used:
\(P_{L\cup a\cup b}=P_R\). The third term is the purity of the noncontiguous
subsystem consisting of the left interior and the right boundary qubit.

If \(d=2^{n/2}\) is the left-half Hilbert-space dimension and

\[
S_{\mathrm{lin}}^{\mathrm{norm}}
=
\frac{d}{d-1}(1-P_{La}),
\]

then the exact expected response is

\[
\boxed{
\chi_V
=
\frac{d}{d-1}
\left[
P_{La}
-c_I P_L
-c_a P_{La}
-c_b P_{L\cup b}
-c_{ab}P_R
\right].
}
\]

The complete central Schmidt spectrum fixes \(P_{La}\), but it does not fix
\(P_L\), \(P_R\), or \(P_{L\cup b}\). Therefore the complete central spectrum
does not generally determine the response to a fresh cross-cut gate.

## 4. Coefficients from gate invariants

Use the normalized two-qubit definitions

\[
E_{\mathrm{op}}(V)
=
1-\frac1{16}
\operatorname{Tr}\!\left[(V^R V^{R\dagger})^2\right],
\qquad
E_{\mathrm{op}}(\mathrm{SWAP})=\frac34,
\]

\[
e_p(V)
=
\frac{E_{\mathrm{op}}(V)+E_{\mathrm{op}}(V\,\mathrm{SWAP})
      -E_{\mathrm{op}}(\mathrm{SWAP})}
     {E_{\mathrm{op}}(\mathrm{SWAP})},
\]

\[
g_t(V)
=
\frac{E_{\mathrm{op}}(V)-E_{\mathrm{op}}(V\,\mathrm{SWAP})
      +E_{\mathrm{op}}(\mathrm{SWAP})}
     {2E_{\mathrm{op}}(\mathrm{SWAP})}.
\]

Evaluating the four Hilbert--Schmidt overlaps of the locally twirled response
operator gives

\[
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
\]

Thus the complete locally dressed second-Rényi response is governed by the same
two local-unitary invariants used to classify the nonlocal content of a
two-qubit gate.

The identity was independently audited on 100 Haar-random two-qubit gates.
Direct commutant projection and the invariant formula agreed with maximum
coefficient error

\[
1.17\times10^{-15}.
\]

## 5. Cartan specialization

For

\[
V(\alpha,\beta,\gamma)
=
\exp[-i(\alpha XX+\beta YY+\gamma ZZ)],
\]

let

\[
A=\sin^2(2\alpha),\qquad
B=\sin^2(2\beta),\qquad
C=\sin^2(2\gamma).
\]

Then

\[
e_p
=
\frac23(A+B+C-AB-AC-BC),
\qquad
g_t=\frac13(A+B+C).
\]

The probes used in Checkpoint 04 have the exact coefficients

| Probe ensemble | \((c_I,c_a,c_b,c_{ab})\) |
|---|---|
| Haar \(U(4)\), or a two-qubit unitary 2-design | \((2/5,0,0,2/5)\) |
| \(e^{-i\pi(XX+YY)/8}\) with local input dressing | \((1/3,1/4,-1/12,1/3)\) |
| \(e^{-i\pi XX/4}\) with local input dressing | \((4/9,1/9,-2/9,4/9)\) |

The Haar neighboring-cut identity is therefore one point in a larger exact
four-purity response family.

## 6. Fixed-spectrum gate-space criterion

Compare two state ensembles with identical central Schmidt spectrum. Define the
high-monitoring minus low-monitoring shifts

\[
A_\partial=\Delta(P_L+P_R),
\qquad
B_\times=\Delta P_{L\cup b}.
\]

Because \(\Delta P_{La}=0\), substitution of the invariant coefficients gives

\[
\boxed{
\Delta\chi_V
=-\frac{d}{d-1}
\left[
 g_t B_\times
+\frac{e_p}{6}(4A_\partial-5B_\times)
\right].
}
\]

Since \(e_p\ge0\) and \(g_t\ge0\), the sufficient conditions

\[
B_\times\ge0,
\qquad
4A_\partial-5B_\times\ge0
\]

imply \(\Delta\chi_V\le0\) for every locally dressed two-qubit probe. These
conditions are sufficient, not necessary.

In the extreme-rate Checkpoint 04 comparison, both point inequalities hold in
all five rank-4 dynamics. Bootstrap support for the second inequality is
complete in three of five primary rank-4 families and all five post-hoc rank-2
families. The full gate-space statement is therefore retained as a post-hoc
extension, not as the locked primary claim.

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

\[
S_j=S(1,\ldots,j)
\]

be the bipartite von Neumann entropy in bits across the cut after site `j`, and
let the central cut be `m=n/2`. Define

\[
\delta_L=S_m-S_{m-1},\qquad
\delta_R=S_m-S_{m+1}.
\]

The ordered pair

\[
B=(\delta_L,\delta_R)
\]

is called the **boundary code**. It records how the central cut sits relative
to the two immediately neighboring cuts.

For a fresh Haar-random two-qubit gate, or a uniformly random two-qubit
Clifford gate, crossing the central bond, define the exact normalized
linear-entropy susceptibility

\[
\chi_2
=
\frac{d}{d-1}
\left[
P_m-\frac25(P_{m-1}+P_{m+1})
\right],
\qquad d=2^m,
\]

where `P_j=Tr rho_j^2` is the purity at cut `j`. Define the relative response

\[
\chi_{\rm rel}=\frac{\chi_2}{P_m}.
\]

The two-copy response theorem from Checkpoint 04 proves the first displayed
identity for every pure input state.

## 2. Flat-spectrum lemma

For a pure stabilizer state, the nonzero eigenvalues of every reduced density
matrix are equal. If the entropy across a cut is `S_j`, then the Schmidt rank is
`2^{S_j}` and

\[
P_j=2^{-S_j}.
\]

Consequently, fixing `S_m` fixes the **complete** central Schmidt spectrum, not
only its entropy or purity.

## 3. Finite-alphabet theorem

For adjacent cuts,

\[
|S_m-S_{m\pm1}|\le 1.
\]

The bound follows from the fact that adding or removing one qubit changes the
entropy by at most one bit. Stabilizer entropies are integers, so

\[
\delta_L,\delta_R\in\{-1,0,1\}.
\]

Substituting `P_j=2^{-S_j}` into the exact response gives

\[
\boxed{
\chi_{\rm rel}
=
\frac{d}{d-1}
\left[
1-\frac25\left(2^{\delta_L}+2^{\delta_R}\right)
\right].
}
\]

Thus the relative susceptibility belongs to a finite alphabet determined by
the boundary code:

| Boundary code | `chi_rel / [d/(d-1)]` |
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

\[
q_p(b\mid S_m,\tau,n)
\]

be the boundary-code distribution at monitoring rate `p`, conditional on the
complete central stabilizer spectrum through `S_m`, probe time `tau`, and size
`n`. Then

\[
\mathbb E[\chi_{\rm rel}\mid S_m,\tau,n,p]
=
\sum_b q_p(b\mid S_m,\tau,n)\,r_n(b),
\]

where `r_n(b)` is the table value above including the finite-size factor
`d/(d-1)`.

Therefore every fixed-spectrum monitoring effect is exactly a redistribution
of boundary-code probabilities. In differential notation,

\[
\partial_p\mathbb E[\chi_{\rm rel}]
=
-\frac{2d}{5(d-1)}
\sum_b
\left(2^{\delta_L(b)}+2^{\delta_R(b)}\right)
\partial_p q_p(b).
\]

Checkpoint 05 finds that stronger monitoring shifts probability away from
codes containing `-1` increments and toward codes containing `+1` increments.
At fixed central rank, the central cut therefore becomes more likely to be a
local entanglement maximum. The exact response formula converts that spatial
reshaping into reduced entangling susceptibility.

## 5. One-measurement corollary

A projective Pauli measurement on one side of a stabilizer bipartition changes
the stabilizer entropy across that cut by either zero or minus one:

\[
\Delta S_m\in\{0,-1\}.
\]

For a random measurement outcome, the two signs have the same phase-free
stabilizer support and hence the same entropy. Local operations cannot increase
the average bipartite entanglement, while replacing one stabilizer generator
changes the relevant binary ranks by at most one. Deterministic measurements
leave the stabilizer support unchanged.

On the principal stratum `Delta S_m=0`, the complete central Schmidt spectrum
is exactly unchanged. Nevertheless, the measurement may change
`(delta_L,delta_R)` and therefore changes `chi_rel` exactly through the boxed
finite-alphabet formula. This is the mathematical basis of the paired
measurement-location intervention in Checkpoint 05.

## 6. Scope

The theorem establishes exact sufficiency of the three adjacent stabilizer
entropies for the Haar/Clifford second-Renyi response. It does not say that a
small physical window of qubits determines those entropies, nor that the new
susceptibility is an order parameter. The empirical claims concern how the
boundary-code distribution changes in the monitored circuit ensemble.
