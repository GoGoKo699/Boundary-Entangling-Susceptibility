# Beyond the Schmidt Spectrum

## Boundary entangling susceptibility in monitored quantum circuits

Does the complete Schmidt spectrum across a cut determine the average response to the next fresh gate crossing that cut? **No.** The response considered here also depends on neighboring-cut purities. The empirical question is how monitored dynamics reshapes that additional information while the complete central spectrum is held fixed.

The four-result chain below separates exact identities, finite-size observations, extrapolation, and paired interventions. The [scientific story](docs/SCIENTIFIC_STORY.md) is self-contained. The [evidence reassessment](docs/EVIDENCE_REASSESSMENT.md) reports the archived-row replay and the limitations of the distance and size fits.

## 1. Central-spectrum insufficiency

Replacing the central eigenvalues by a shared reference spectrum while retaining the state-dependent Schmidt vectors separates eigenvalue effects from spatial-embedding effects. The plotted stronger-minus-weaker monitoring contrasts are negative across five tested circuit/measurement families and a disjoint-seed replication.

![Fixed-spectrum response](figures/core_svg/figure_01_panel_b.svg)

Filled circles denote the primary run; open squares denote the independent seed. The horizontal bars are the archived 95% trajectory-cluster bootstrap intervals. This is a finite-system diagnostic intervention, not a physical spectrum-replacement protocol.

## 2. An exact neighboring-cut mechanism

Let $m=n/2$, $D=2^m$, and $P_j$ be the purity across cut $j$. The purity-normalized linear-entropy response to an independent Haar-random or uniformly random two-qubit Clifford probe is

$$
\chi_{\mathrm{rel}}=\frac{D}{D-1}\left(1-\frac{\mathbb E_U P'_m}{P_m}\right)
=\frac{D}{D-1}\left[1-\frac{2}{5}\frac{P_{m-1}+P_{m+1}}{P_m}\right].
$$

This is not generally the mean finite-gate increment of $-\log_2 P_m$. The central spectrum fixes $P_m$, but not its two neighboring purities. Those purities concern extended bipartitions; the identity does not assert reconstruction from a small local reduced density matrix.

For stabilizer states, define $\delta_L=S_m-S_{m-1}$ and $\delta_R=S_m-S_{m+1}$. Each belongs to $\{-1,0,1\}$, and the response divided by $D/(D-1)$ is $1-\frac25(2^{\delta_L}+2^{\delta_R})$.

<p align="center">
<img src="figures/core_svg/figure_02_response_matrix.svg" width="38%" alt="Exact stabilizer response matrix">
<img src="figures/core_svg/figure_02_redistribution_matrix.svg" width="38%" alt="Conditional boundary-code probability slopes">
</p>

The left matrix gives the exact response alphabet. The right gives the representative fixed-spectrum probability slopes at $n=256$: rows are $\delta_L=+1,0,-1$ and columns are $\delta_R=-1,0,+1$. The weighted redistribution reconstructs the measured response slope. The [theory](docs/THEORY.md) gives the general two-copy and locally dressed gate identities.

## 3. Physical exact-spectrum comparison through 256 qubits

Pure stabilizer states have flat nonzero Schmidt spectra. Matching within $(n,\tau,S_m)$ therefore fixes the complete central spectrum **without modifying the state**. The within-spectrum monitoring coefficients remain negative through $n=256$ under projective-Z and random-Pauli monitoring and a disjoint-seed replication.

![Finite-size coefficients and model-dependent extrapolations](figures/core_svg/figure_03_size_scaling.svg)

Finite-size points are direct estimates. Points at infinity and the lines come from the locked $1/n$ model, not a theorem. Filled circles/solid lines are the primary run; open squares/dashed lines are the independent seed. The archived 95% intervals describe sampling uncertainty under the stated analysis. Model residuals, changing exact-spectrum support, and alternative fixed-form extrapolations are discussed in the [reassessment](docs/EVIDENCE_REASSESSMENT.md). The negative finite-size evidence is stronger than any precise claim about a limiting coefficient.

## 4. Paired measurement-location intervention

Copies of the same premeasurement stabilizer state receive one projective-Z measurement at different distances. The retained interventions preserve the central spectrum. The paired near-minus-far contrast is negative, and the response is concentrated near the cut.

<p align="center">
<img src="figures/core_svg/figure_04_distance_decay.svg" width="62%" alt="Recorded distance profile with historical descriptive exponential">
<img src="figures/core_svg/figure_04_conditioning_contrast.svg" width="28%" alt="Unconditional and spectrum-preserving paired contrasts">
</p>

**Interpretation of the retained artwork:** the exponential curve and `xi=2.37` annotation reproduce the historical accepted figure. The current residual checks do not support a single-exponential law or a precisely identified physical localization length. The observed points and paired sign reversal remain supported. A stricter common-eligibility curve retains the near-cut concentration; a same-side comparison requiring spectrum preservation under both interventions gives $-0.04747$, with a fresh pointwise 95% interval $[-0.04934,-0.04547]$. These are explicitly post-hoc checks, not changes to the frozen primary plot. See [definitions, results, and proposed artwork revision](docs/EVIDENCE_REASSESSMENT.md).

Causality is restricted to the specified paired location interventions and their unchanged-spectrum eligibility. It does not concern assignment of the long-run monitoring rate.

## Reproduce and inspect

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-reproducible.txt
pip install -e .
pytest -q
python verify.py
python reproduce.py --core-figures
```

The figure command validates six PDF/PNG/SVG triples in a fresh staging directory before copying them into `reproduced_figures/`. The core data are in [data/processed/core_figures](data/processed/core_figures/); source is in [scripts/figures](scripts/figures/). Browser SVGs and publication PDFs use the same plotting code. Exact external author-approved PDF hashes remain in [provenance](provenance/figure_sha256.csv); regenerated PDF metadata may differ.

To replay Figures 3 and 4 from stored trajectory records, use the separate archive-based command in [EVIDENCE_REASSESSMENT.md](docs/EVIDENCE_REASSESSMENT.md). Redrawing a small canonical table is not the same as recomputing its estimates from raw records. A successful CI run is a software/regression check, not an independent scientific replication.

## Reader routes and scope

| Goal | Page |
|---|---|
| Full argument | [Scientific story](docs/SCIENTIFIC_STORY.md) |
| Current evidence and fit limitations | [Evidence reassessment](docs/EVIDENCE_REASSESSMENT.md) |
| Exact identities | [Theory](docs/THEORY.md) |
| Circuit and estimator definitions | [Numerical methods](docs/NUMERICAL_METHODS.md) |
| Source navigation | [Code map](docs/CODE_MAP.md) |
| Likely questions | [FAQ](docs/FAQ.md) |
| Data availability | [Data policy](docs/DATA_POLICY.md) |

No new order parameter, critical exponent, universal non-Clifford thermodynamic law, or finite-range theorem is claimed. The original trajectory-fingerprint and cumulative flow-balance directions are retained only as [research history](docs/RESEARCH_HISTORY.md). Selected study source is under [studies](studies/); immutable raw-data deposition remains pending. No manuscript TeX or TikZ is tracked.

The [citation record](CITATION.cff) is provisional. No reuse license has been selected; see [license status](LICENSE_PENDING.md).
