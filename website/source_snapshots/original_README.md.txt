# Beyond the Schmidt Spectrum

## Boundary entangling susceptibility in monitored quantum circuits

Does the complete Schmidt spectrum across a cut determine the average response to the next fresh gate crossing that cut? **No.** The response considered here also depends on neighboring-cut purities. The empirical question is how monitored dynamics reshapes that additional information while the complete central spectrum is held fixed.

Read the [four-figure dialogue report](docs/DIALOGUE_REPORT.md) for the complete argument, with nine main-text questions and 32 appendix questions. The [question map](docs/DIALOGUE_QUESTION_MAP.md) retains the agreed narrative order. The [evidence reassessment](docs/EVIDENCE_REASSESSMENT.md) distinguishes archived-row replay from new post-hoc checks and explains the distance/size-fit limitations.

## 1. Central-spectrum insufficiency

Replacing the central eigenvalues by a shared reference spectrum while retaining the state-dependent Schmidt vectors separates eigenvalue effects from spatial-embedding effects. The plotted stronger-minus-weaker monitoring contrasts are negative across five tested circuit/measurement families and a disjoint-seed replication.

![Fixed-spectrum response](figures/core_svg/figure_01_panel_b.svg)

Filled circles denote the primary run; open squares denote the independent seed. The horizontal bars are the adopted nominal pointwise 95% support-conditioned trajectory-cluster bootstrap intervals (50,000 valid draws per contrast). References and observed support are fixed; see [the uncertainty definition](docs/FIGURE1_UNCERTAINTY.md). The reference spectrum is shared within each family/size/time comparison cell, not across every plotted family and size. This is a finite-system diagnostic intervention, not a physical spectrum-replacement protocol.

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

Finite-size points are direct estimates. Points at infinity and the lines come from the locked $1/n$ model, not a theorem. Filled circles/solid lines are the primary run; open squares/dashed lines are the independent seed. The original 95% intervals describe sampling uncertainty under the stated analysis. Model residuals, changing exact-spectrum support, and alternative fixed-form extrapolations are discussed in the [reassessment](docs/EVIDENCE_REASSESSMENT.md). The negative finite-size evidence is stronger than any precise claim about a limiting coefficient.

## 4. Paired measurement-location intervention

For the stated averaged probe, the nonpositive response change after a spectrum-preserving single-site Pauli measurement is an [exact stabilizer corollary](docs/THEORY.md#5-one-measurement-corollary). Its magnitude and near-minus-far sign are not fixed by that corollary. Copies of the same premeasurement stabilizer state receive one projective-Z measurement at different distances. The retained interventions preserve the central spectrum. The paired near-minus-far contrast is negative, and the response is concentrated near the cut.

<p align="center">
<img src="figures/core_svg/figure_04_distance_decay.svg" width="62%" alt="Observed distance profile with original intervals and no fitted curve">
<img src="figures/core_svg/figure_04_conditioning_contrast.svg" width="28%" alt="Unconditional and spectrum-preserving paired contrasts">
</p>

The distance panel uses the author-approved revision without the exponential curve or length annotation. Its observed means and original intervals are unchanged. The profile supports strong attenuation over the measured distances, not an established single-exponential law or precise physical localization length. A stricter common-eligibility curve retains the near-cut concentration; a same-side comparison requiring spectrum preservation under both interventions gives $-0.04747$, with a fresh pointwise 95% interval $[-0.04934,-0.04547]$. These are explicitly post-hoc checks, not changes to the original primary estimates. See the [approved figure baseline and caption](docs/FIGURE_BASELINE.md) and [full evidence reassessment](docs/EVIDENCE_REASSESSMENT.md).

Causality is restricted to the specified paired location interventions and their unchanged-spectrum eligibility. It does not concern assignment of the long-run monitoring rate. The distance profile is a postmeasurement-minus-premeasurement response change; the contrast panel separately compares near and far interventions.

## Reproduce and inspect

A complete checkout includes **`entanglement-data.zip` at the repository root**. [The data manifest](data/record_bundle_manifest.json) verifies the bundle and every source member. No old checkpoint download or previous chat is needed. `verify.py` fails if the original-data bundle is absent; redrawing summary tables alone is not data completeness.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-reproducible.txt
pip install -e .
python verify.py
pytest -q
python reproduce.py --core-figures
```

The figure command validates six PDF/PNG/SVG triples in a fresh staging directory before copying them into `reproduced_figures/`. The core data are in [data/processed/core_figures](data/processed/core_figures/); source is in [scripts/figures](scripts/figures/). Browser SVGs and publication PDFs use the same plotting code. The current Figure 4 generator does not read a decay-fit file. The [baseline record](docs/FIGURE_BASELINE.md) distinguishes current artwork from the historical external Overleaf hashes.

To replay all four figures from stored observations, run `python scripts/analysis/reproduce_core_records.py`. The post-hoc reassessment has a separate command in [REPRODUCTION.md](docs/REPRODUCTION.md). Redrawing a small canonical table is not the same as recomputing its estimates from raw records. A successful CI run is a software/regression check, not an independent scientific replication.

## Reader routes and scope

| Goal | Page |
|---|---|
| Complete four-figure argument | [Dialogue report](docs/DIALOGUE_REPORT.md) |
| Main-text versus appendix questions | [Question map](docs/DIALOGUE_QUESTION_MAP.md) |
| Short overview | [Scientific story](docs/SCIENTIFIC_STORY.md) |
| Evidence and fit limitations | [Evidence reassessment](docs/EVIDENCE_REASSESSMENT.md) |
| Exact identities | [Theory](docs/THEORY.md) |
| Circuit and estimator definitions | [Numerical methods](docs/NUMERICAL_METHODS.md) |
| Source navigation | [Code map](docs/CODE_MAP.md) |
| Current figure version and caption | [Figure baseline](docs/FIGURE_BASELINE.md) |
| Data availability | [Data policy](docs/DATA_POLICY.md) |

No new order parameter, critical exponent, universal non-Clifford thermodynamic law, or finite-range theorem is claimed. The original trajectory-fingerprint and cumulative flow-balance directions are retained only as [research history](docs/RESEARCH_HISTORY.md). Selected study source is under [studies](studies/); the required original observations and resamples are in the indexed root data bundle. No manuscript TeX or TikZ is tracked.

The [citation record](CITATION.cff) is provisional. No reuse license has been selected; see [license status](LICENSE_STATUS.md).

See [precise reproducibility limits](docs/REPRODUCIBILITY_LIMITS.md). Preserved original intervals and fully regenerated intervals are not interchangeable.
