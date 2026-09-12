# From random quantum circuits to a fixed-spectrum response question

[Previous: review reading map](PROJECT_GUIDE.md#learn) · [Return to README](../README.md) · [Next: four-figure account](DIALOGUE_REPORT.md)

This bridge starts from the entanglement, circuit and trajectory concepts in Fisher, Khemani, Nahum and Vijay's *Random Quantum Circuits*, [arXiv:2207.14280v1](https://arxiv.org/abs/2207.14280v1). The [reading map](PROJECT_GUIDE.md#review-to-project-map) identifies the relevant passages. Here we define the project's experiment and explain the specific calculation it needs. The review supplies background; the primary references attached to the local derivation supply attribution, without becoming further required reading.

## What changes after the review?

The review explains how gates and measurements shape entanglement in individual quantum trajectories. A central question there is whether typical trajectories have volume-law or area-law entanglement. This study asks a different question about a prepared state: **if its complete central Schmidt spectrum is specified, is its average response to a fresh boundary gate also specified?**

The answer is no for the response defined below. Eigenvalues determine entanglement quantities at that cut, but they leave freedom in the Schmidt vectors within each half. A gate acting on designated boundary sites can distinguish that freedom. The empirical question is whether monitoring systematically changes this response-relevant structure after spectrum control. Locating a measurement-induced transition is background context, not the primary task.

## What is the experiment and what is random?

Take a pure state of an open chain of an even number $n$ of qubits. Label sites $1,\ldots,n$, put $m=n/2$, and place the central cut between sites $m$ and $m+1$. Write the partition as $La\mid bR$: $a=m$ and $b=m+1$ are the probe qubits; $L$ and $R$ are the remaining interiors. The neighboring cuts are after sites $m-1$ and $m+1$.

First, circuit evolution and monitoring prepare the state. Then an **independent fresh** two-qubit unitary $U$ acts only on $ab$. We compare the central reduced state before and after this probe. The probe is a specified extra operation, not whichever gate happened to occur next in the recorded preparation.

In the large-size physical arm, preparation begins with independent single-qubit stabilizer product states. Each cycle applies both nearest-neighbor brickwork sublayers, in randomly chosen order, with fresh uniform Clifford gates, then monitors each site independently with probability $p$. Two separate monitoring protocols are used: projective Z, or random Pauli with X, Y and Z chosen independently with equal probability at each selected site. The probe time is $\tau=\text{cycles}/n$. Thus $p$ is per site per **complete two-sublayer cycle**, not per sublayer.

The finite-system arm uses random product inputs and five recorded preparation families: Haar/Z, Clifford/Z, Floquet-Cartan/Z, Haar/random Pauli and Haar/weak Z. It also monitors once after the complete pair of sublayers, but alternates their order deterministically between cycles; its Floquet gates are fixed in time for a run. Its weak Z measurements have strength $\eta=0.6$. These preparation details differ from the physical stabilizer arm. The main fresh probe is the same Haar/two-design probe across all five families. See [methods](NUMERICAL_METHODS.md) and the [finite-arm source](../studies/checkpoint_04/scripts/cross_architecture_simulation.py) for the exact definitions.

Three operations must remain separate:

| Operation | What is averaged or selected? | What stays fixed? |
|---|---|---|
| Fresh-probe average $\mathbb E_U$ | The independent probe gate | One prepared input state |
| Preparation/trajectory average | Prepared states from random inputs, gates, measurement locations/bases and outcomes under the specified design | Run, size, protocol, monitoring rate and observation time as appropriate |
| Spectrum conditioning | Only states in a declared central-spectrum stratum | That spectrum and the other matching variables; the remaining states still vary |

The last operation changes the comparison population. It is not another gate average. In the physical arm the stratum is $(n,\tau,S_m)$, with $S_m$ defined below. It need not contain every monitoring rate.

A recorded trajectory remains pure after each outcome-conditioned measurement. Discarding the outcomes instead gives a mixture $\bar\rho=\sum_\omega w_\omega\rho_\omega$, where $\omega$ labels trajectories and $w_\omega$ their probabilities. Purity and response are nonlinear in the state: averaging their trajectory values generally differs from computing them on $\bar\rho$. This is the distinction in review §2.4 and §4.1.1. The simulation's phase-free stabilizer representation can omit outcome signs because these particular entropy observables do not depend on them; it does not replace pure trajectories by a mixture.

## What response is measured?

For cut $j$, reduce to the first $j$ sites and define its purity

$$
\rho_{[1:j]}=\operatorname{Tr}_{j+1,\ldots,n}|\psi\rangle\langle\psi|,
\qquad P_j=\operatorname{Tr}\rho_{[1:j]}^2.
$$

The central half has dimension $D=2^m$. Its normalized linear entropy is

$$
L_m=\frac{D}{D-1}(1-P_m).
$$

It is zero for a pure reduced state and one for a maximally mixed reduced state. A prime denotes the state after the fresh probe. Define

$$
\chi_2=\mathbb E_U[L'_m-L_m]
=\frac{D}{D-1}(P_m-\mathbb E_U P'_m),
\qquad \chi_{\mathrm{rel}}=\frac{\chi_2}{P_m}.
$$

The denominator is the **input** central purity, fixed during the gate average. Dividing by it removes the multiplicative purity scale, useful when the matched rank grows with system size. Across trajectories the ratio is evaluated on each state before statistical aggregation. A ratio of ensemble-mean purities is generally a different estimator.

Positive response means the probe increases normalized linear entropy on average; negative response means it decreases it. “Susceptibility” here denotes a finite-gate response, not automatically an infinitesimal derivative. It is not a derivative with respect to $p$, and it is not $\mathbb E_U[-\log_2P'_m+\log_2P_m]$. The review's discussion of purity versus entropy averaging in §3.1.3, p.18, helps explain this distinction.

### The short two-copy calculation

Let $\rho=|\psi\rangle\langle\psi|$ and let $F_X$ exchange subsystem $X$ between two copies. Contracting indices gives $P_X=\operatorname{Tr}(\rho^{\otimes2}F_X)$. Since the probe touches only $ab$, it changes the central swap $F_LF_a$ only through $F_a$.

Haar averaging over $U(4)$ projects that operator onto the span of the identity and the full two-copy swap $F_{ab}$:

$$
\Omega=\mathbb E_U U^{\dagger\otimes2}F_aU^{\otimes2}
=\alpha I+\beta F_{ab}.
$$

This is an average on the two-qubit probe space, whose two-copy dimension is 16. Both $\operatorname{Tr}F_a$ and $\operatorname{Tr}(F_aF_{ab})$ equal 8, while $\operatorname{Tr}I=16$ and $\operatorname{Tr}F_{ab}=4$. Preserving these two overlaps gives

$$
16\alpha+4\beta=8,\qquad 4\alpha+16\beta=8,
\qquad \alpha=\beta=\frac25.
$$

Multiplication by $F_L$ leaves swaps on $L$ and $Lab$, respectively. Their purities are $P_{m-1}$ and $P_{m+1}$. Hence

$$
\mathbb E_U[P'_m]=\frac25(P_{m-1}+P_{m+1}),
$$

$$
\chi_{\mathrm{rel}}=\frac{D}{D-1}
\left[1-\frac25\frac{P_{m-1}+P_{m+1}}{P_m}\right].
$$

This is the qubit specialization of established entanglement-feature transfer machinery: [Akhtar and You, Eq.20](https://arxiv.org/abs/2006.08797v2), with the broader local transfer formulation in [Kuo et al., Eqs.19 and 60](https://arxiv.org/abs/1910.11351v2). The [full theory and dictionary](THEORY.md#entanglement-feature-dictionary) retain the precise translation and locally dressed extensions. The review's schematic pairing discussion motivates the method; it does not explicitly derive this formula in our notation.

A uniform two-qubit Clifford probe gives the same result because it has the required two-copy Haar moment; see the design attribution to [Webb and Zhu](RELATED_WORK.md#clifford-designs). No stabilizer input assumption was needed. Equality of these probe averages does **not** make Haar and Clifford monitored-state ensembles identical.

## Same central spectrum, different response

Across $A\mid B$, write $|\psi\rangle=\sum_\alpha\sqrt{\lambda_\alpha}|u_\alpha\rangle_A|v_\alpha\rangle_B$. The complete list of reduced-state eigenvalues $\lambda_\alpha$, including zeros, fixes $P_m$ and every eigenvalue-based central entropy. It does not fix either neighboring purity. Those cuts describe extended bipartitions, not a small physical window surrounding the gate.

The repository's four-qubit example makes the distinction explicit. Use the central cut $12\mid34$ and probe sites 2 and 3. Compare $|0000\rangle$ with $|\Phi^+\rangle_{12}\otimes|\Phi^+\rangle_{34}$, where $|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2$. Both are products across the central cut and have spectrum $(1,0,0,0)$, so $P_2=1$ and $D=4$.

| Input | $P_1$ | $P_2$ | $P_3$ | $\mathbb E_U P'_2$ | $\chi_{\mathrm{rel}}=\chi_2$ |
|---|---:|---:|---:|---:|---:|
| Four-qubit product | $1$ | $1$ | $1$ | $4/5$ | $(4/3)(1-4/5)=4/15$ |
| Two internal Bell pairs | $1/2$ | $1$ | $1/2$ | $2/5$ | $(4/3)(1-2/5)=4/5$ |

For the second state, tracing out site 2 leaves site 1 maximally mixed; similarly, global purity makes $P_3$ equal the purity of site 4. Entanglement inside each half changes the boundary response while leaving the central spectrum untouched. This checked illustration is neither a new discovery nor evidence about a monitored ensemble's typical behavior.

## Why stabilizers permit physical spectrum matching

Generic equal entropies do not fix equal spectra. Pure stabilizer states form a restricted class where the reduced density matrix is proportional to a projector. If its entropy in **bits** is $S_j$, it has rank $2^{S_j}$, with that many eigenvalues $2^{-S_j}$ and all remaining eigenvalues zero. Therefore

$$
P_j=2^{S_j}(2^{-S_j})^2=2^{-S_j}.
$$

This established stabilizer property is attributed to [Fattal et al.](RELATED_WORK.md#stabilizer-entanglement-structure); the [flat-spectrum lemma](THEORY.md#2-flat-spectrum-lemma) supplies the local statement. At fixed $n$, matching $S_m$ fixes the entire central spectrum. Time $\tau$ is also matched to define the comparison. The states themselves are unmodified.

Define the two entropy increments

$$
\delta_L=S_m-S_{m-1},\qquad \delta_R=S_m-S_{m+1}.
$$

Adding or removing one qubit changes a bipartite entropy by at most one bit, by subadditivity and the corresponding difference bound. Stabilizer entropies are integers, so each increment lies in $\{-1,0,+1\}$. The ordered pair has nine possible codes in the overall description, although individual ranks or small geometries can restrict which occur. Here **boundary code** means this pair of entropy increments; it is not itself a quantum error-correcting code or a replica-pairing variable.

Since $P_{m\pm1}/P_m=2^{\delta_{L,R}}$, define the response with its dimension factor removed,

$$
r(\delta_L,\delta_R)=\frac{\chi_{\mathrm{rel}}}{D/(D-1)}
=1-\frac25(2^{\delta_L}+2^{\delta_R}).
$$

The nine ordered pairs yield six distinct values:

| Boundary code | $r$ |
|---|---:|
| $(-1,-1)$ | $3/5$ |
| $(-1,0)$ or $(0,-1)$ | $2/5$ |
| $(0,0)$ | $1/5$ |
| $(-1,+1)$ or $(+1,-1)$ | $0$ |
| $(0,+1)$ or $(+1,0)$ | $-1/5$ |
| $(+1,+1)$ | $-3/5$ |

A local entropy minimum at the central cut has the highest response in this alphabet; a local maximum has the lowest. If $q_p(b\mid n,\tau,S_m)$ is the conditional probability of code $b$, the conditional mean response is exactly $\sum_b q_p(b\mid n,\tau,S_m)[D/(D-1)]r(b)$. Applying the same linear estimator to these probabilities and to the response preserves the identity. Figure 2's reconstruction is consequently a consistency check, not another independent statistical observation.

## What remains empirical?

The formula specifies a state's response, but it does not specify how monitored preparation populates the nine codes. Figure 1 tests diagnostic spectrum replacement in finite-system states; Figures 2–3 use conditional comparisons of physical stabilizer states. Their sampling and spectrum controls are different.

For Figure 3, the fitted within-spectrum coefficient $\beta_n$ multiplies $(p-0.26)/0.02$ after controlling $(\tau,S_m)$. It summarizes observed rate overlap within eligible strata. The recorded coefficients remain negative through $n=256$ under both protocols and disjoint seeds; the limiting extrapolation is model-dependent. A negative coefficient means a lower response with increasing monitoring within those comparisons; it need not mean every state's response is negative. Because the matched spectrum is produced by the dynamics, conditioning on it does not identify the unconditional causal effect of assigning $p$. Eligibility, trajectory clustering and the limiting fit are specified in [methods](NUMERICAL_METHODS.md#6-exact-spectrum-fixed-effect-estimator).

Figure 4 asks another question. Apply alternative single-site measurements to copies of one pre-state, and compare the resulting changes in the later probe response. Under the pure-stabilizer, single-site Pauli and unchanged-central-spectrum assumptions, each individual change is nonpositive by the [measurement corollary](THEORY.md#5-one-measurement-corollary). Two nonpositive numbers need not have a negative difference. The observed near-minus-far ordering and its spatial concentration therefore remain empirical, within the specified eligible populations. They neither derive the long-run coefficient nor establish an exponential localization length.

You can now read the [four-figure account](DIALOGUE_REPORT.md): diagnostic contrast, exact code interpretation, physical size/seed comparison, then paired location intervention. Its [claim map](CLAIM_EVIDENCE_MAP.md) and [gallery](../figures/README.md) lead to the evidence without further background reading.

## Self-checks

These are worked teaching questions, not external comprehension testing.

<details>
<summary>Does equal central entropy imply equal complete spectra?</summary>

Generally no. One entropy is one function of the eigenvalue list. For pure stabilizer states at fixed size, the flat-spectrum property makes the implication valid. Even then, equal central spectra leave neighboring purities free.

</details>

<details>
<summary>Can we average trajectory density matrices first and then calculate their response?</summary>

That computes a different quantity in general. A known-outcome trajectory is pure; forgetting outcomes creates a mixture. Purity is quadratic, and the relative response also divides by input purity. Evaluate each trajectory's response before the specified statistical average.

</details>

<details>
<summary>What do the three cut purities determine, and what do they not determine?</summary>

They determine the Haar/uniform-Clifford averaged response exactly. They do not determine the response to every individual gate or describe the entire state. Their sufficiency also does not prove sufficiency of a small local reduced density matrix.

</details>

<details>
<summary>What is controlled by physical stabilizer matching?</summary>

At fixed size, matching central entropy fixes all central eigenvalues, their rank and multiplicities; matching time also controls the observation time. It does not fix neighboring cuts or make populations at different monitoring rates interchangeable under causal rate assignment.

</details>

<details>
<summary>Why are the monitoring coefficient and paired location contrast different questions?</summary>

The coefficient compares different prepared trajectories within spectrum/time strata across rates. The location experiment compares alternative measurements on copies of the same pre-state under declared preservation eligibility. The exact individual-measurement sign orders neither two locations nor long-run rate-conditioned ensembles.

</details>

[Next: the four figures and their evidence](DIALOGUE_REPORT.md) · [Notation reference](NOTATION.md) · [Return to README](../README.md)
