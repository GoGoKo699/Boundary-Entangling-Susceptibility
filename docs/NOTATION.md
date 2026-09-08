# Notation

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
