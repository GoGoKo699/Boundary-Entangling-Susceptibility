# Frequently asked questions

## What is fixed when two states are called “same-spectrum”?

The complete Schmidt eigenvalue list across the central cut is fixed, including its rank. In the counterfactual intervention this is imposed directly while retaining the original Schmidt vectors. In the physical stabilizer arm, no state is modified: matching the stabilizer entropy `S_m` fixes the complete flat nonzero spectrum exactly.

## Why is the central Schmidt spectrum insufficient?

It determines every bipartite quantity that depends only on the central reduced-state eigenvalues, but it does not determine how the corresponding Schmidt vectors are embedded in the sites adjacent to the cut. A fresh local gate interacts with that spatial embedding.

For the Haar/uniform-Clifford Rényi-2 response, the missing information is identified exactly by the two neighboring-cut purities.

## Is the spectrum-replacement operation supposed to be experimentally physical?

No. It is a diagnostic intervention used to separate eigenvalue effects from Schmidt-vector and spatial-embedding effects. The physical stabilizer comparison later reproduces the result without replacing coefficients or modifying states.

## Why use the response to a fresh gate?

A fresh independent probe tests a property of the state rather than reusing correlations with the circuit gate that generated it. The endpoint is local, non-telescoping, and admits an exact two-copy response formula.

## Why use relative Rényi-2 susceptibility?

Purity gives direct access to swap-operator identities and exact Haar/Clifford two-copy averages. Dividing by the central purity removes a trivial multiplicative scale that can become exponentially small with stabilizer rank. The unnormalized response is retained as a secondary check.

## Is the result merely a restatement that local gates depend on local correlations?

The broad principle is not new. The contribution is the fixed-complete-spectrum question, the exact neighboring-cut response specialization, the monitored-state redistribution that it exposes, physical large-size matching, independent replication, and the paired location intervention.

## Is this a new order parameter for the measurement-induced transition?

No. The response remains nonzero and of the same sign on both sides of the independently located transition. Its monitoring dependence changes across the transition, so it is transition-sensitive but not an order parameter.

## What exactly is causal in the paired intervention?

For each sampled premeasurement state, copies are subjected to measurements at different locations. Measurement location is therefore controlled on the same pre-state. The causal statement is conditional on the branch where the complete central spectrum remains unchanged. It is not a causal claim about assigning the long-run monitoring probability `p`.

## Are the thermodynamic conclusions universal?

The data remain negative through `n=256` in monitored Clifford circuits and are consistent with a nonzero large-size limit under several fixed correction models. This does not establish a universal exponent or generic non-Clifford thermodynamic law.

## What non-Clifford evidence is included?

Checkpoint 04 includes finite state-vector tests with Haar and fixed non-Clifford Floquet-Cartan dynamics, weak measurements, random-Pauli measurements, and several fresh-probe ensembles. The large-size physical exact-spectrum arm is stabilizer/Clifford based.

## Why are the full checkpoint ZIP files not committed?

They contain compressed raw arrays, state tables, bootstrap arrays, and duplicated generated artifacts that are unsuitable for ordinary reviewable Git history. The canonical plotted data, source, design locks, selected result tables, and browser figures are tracked. Complete archives are reserved for a versioned release or research-data deposit.

## How do I reproduce the core figures?

Run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
python verify.py
python reproduce.py --core-figures
```

The generated PDFs and PNGs appear in `reproduced_figures/`.
