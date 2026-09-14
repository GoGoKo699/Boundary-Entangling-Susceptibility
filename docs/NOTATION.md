# Notation

[Previous: project guide](PROJECT_GUIDE.md#check) · [Return to README](../README.md) · [Next: theory](THEORY.md)

The current scientific account uses these conventions. Historical study source, file fields, and artwork retain their original identifiers; no code or data are renamed.

| Symbol | Meaning |
|---|---|
| $n$, $m=n/2$ | Even chain length and central cut position |
| $D=2^m$ | Half-chain Hilbert-space dimension |
| $d$ | Measurement distance from the central cut in sites; $d=0$ is adjacent to the cut |
| $La\mid bR$ | Bipartition with probe qubits $a,b$ and interiors $L,R$ |
| $P_j$ | Purity of the reduced state on sites $1,\ldots,j$ |
| $S_j$ | Von Neumann entropy in bits; integer for the pure stabilizer states used in the physical matching arm |
| $\chi_2$ | Expected normalized linear-entropy increment under the fresh probe |
| $\chi_{\rm rel}=\chi_2/P_m$ | Purity-normalized response; not an average finite increment of $-\log_2P_m$ |
| $(\delta_L,\delta_R)$ | Boundary code, with $\delta_L=S_m-S_{m-1}$ and $\delta_R=S_m-S_{m+1}$ |
| $p$, $\tau$ | Monitoring probability per site per complete two-sublayer cycle; probe time in cycles divided by $n$ |
| $\Delta\chi_{\rm rel}$ in Figure 1 | Equal-cell high-minus-low contrast between $p=0.24$ and $p=0.08$, at fixed run-specific references and common support |
| $\beta_n$ | Within-spectrum regression coefficient per $\Delta p=0.02$, at fixed size and within $(\tau,S_m)$ strata; not a pointwise derivative |
| $\Delta_M\chi_{\rm rel}(d)$ | Change in the averaged response caused by one measurement at distance $d$; the plotted $\Delta\chi_{\rm rel}(d)$ in Figure 4 |
| $D_{\rm rel}$ | Paired near-minus-far difference of measurement-induced changes; not the dimension $D$ |
| $\xi$ | Historical single-exponential fit parameter, not an established physical localization length |

Original source functions using an argument `d` for dimension mean the present $D$, not measurement distance. The [theory](THEORY.md), [methods](NUMERICAL_METHODS.md), and [dialogue](DIALOGUE_REPORT.md) use the notation above. The [claim map](CLAIM_EVIDENCE_MAP.md) separates exact identities, conditional empirical effects, and model-dependent extrapolation.

## Translation from the selected review

These comparisons use Fisher et al., [arXiv:2207.14280v1](https://arxiv.org/abs/2207.14280v1), with **PDF/preprint pages**, not journal pagination. The review supplies the general concepts; the project keeps its existing conventions and code identifiers.

| In the review | Here | Reading consequence |
|---|---|---|
| Natural logarithms, Eq.1 and Rényi definition, p.5 | $S_j$ in bits: $-\mathop{\mathrm{Tr}}\nolimits\rho_{[1:j]}\log_2\rho_{[1:j]}$ | Divide the review entropy by $\ln2$ to express it in bits. For stabilizers, $P_j=2^{-S_j}$. |
| $n$ as Rényi order; $L$ (or $N$ in §2.1) as site count | $n$ is the even number of qubits | The subscript 2 in $\chi_2$ refers to its purity-based definition, not chain length. |
| $q$ as local Hilbert-space dimension, p.9; $D=\min(D_A,D_{\bar A})$, p.6 | Qubits have $q=2$; central half-chain $D=2^{n/2}$ | The probe is on a four-dimensional two-qubit space. $D$ is not its dimension. |
| General subsystem $A$ and complement; bond label $x$ | Prefix cut $j$: sites $1,\ldots,j$; central $m=n/2$ | Neighboring cuts $m\pm1$ still define extended bipartitions. |
| Outcome record $\mathbf m$, §§2.4 and 4.1 | Scalar $m$ is the central cut; the bridge uses $\omega$ for a trajectory | The same letter in the review is not a cut index. |
| One alternating odd/even layer per timestep, Eqs.9–10, p.9 | One cycle includes both sublayers, then monitoring; $\tau=\text{cycles}/n$ | Compare probabilities only with the actual monitoring schedule stated. |
| Gate averages in §3.1.3; outcome averages in §4.1.1 | $\mathbb E_U$ for a fixed state's fresh probe; preparation averages over trajectories; conditional averages within spectrum/time strata | Neither state averaging nor spectrum selection is part of the fixed-input probe twirl. |
| $S_{2A}$ and $e^{-S_{2A}}=\mathop{\mathrm{Tr}}\nolimits\rho_A^2$, Eq.13, p.16 | $P_j$ for purity; $L_m=D(1-P_m)/(D-1)$ for normalized linear entropy | $\chi_2=\mathbb E_U[L'_m-L_m]$ and $\chi_{\rm rel}=\chi_2/P_m$ are finite purity responses, not finite logarithmic entropy increments. |
| Replica-pairing labels $\sigma=\pm$, §3.1.3, p.17 | $(\delta_L,\delta_R)$ label entropy increments of one physical stabilizer state | These are different discrete descriptions. The boundary code is not a replica spin or itself an error-correcting code. |

An unqualified average of $\chi_{\rm rel}$ in a statistical comparison means the specified average of statewise ratios. It is not permission to replace it by a ratio of ensemble-mean purities. The [bridge](TUTORIAL_BRIDGE.md#what-is-the-experiment-and-what-is-random) explains the three operations before using them.

[Next: complete technical derivations](THEORY.md) · [Return to README](../README.md)
