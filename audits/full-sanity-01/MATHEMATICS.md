# Independent mathematical audit

Target: `GoGoKo699/Boundary-Entangling-Susceptibility`, commit `00009cf7cc02104e4c776863b3ea551bd38e00f4`. This report audits that mathematical baseline; it does not amend it. It is a component of the full audit, not a statistical or novelty verdict.

**Verdict:** the current core response identities, complete-spectrum insufficiency, stabilizer alphabet, and carefully restricted one-measurement corollary are correct. Independent derivations and finite-dimensional computations agree. No mathematical scientific blocker was found. Three small terminology/definition issues are listed below. The counterexamples here demonstrate why the current exclusions matter; they are not counterexamples to the retained scoped claims.

## 1. Authority, coverage and independence

Read in full: `docs/THEORY.md`, `docs/NOTATION.md`, `docs/SCIENTIFIC_STORY.md`, `docs/SCOPE_AND_LIMITATIONS.md`, `docs/CLAIM_EVIDENCE_MAP.md`, `results/core_claims.csv`, `src/boundary_susceptibility/response.py`, `src/boundary_susceptibility/boundary_codes.py`, `tests/test_identities.py`, `studies/checkpoint_04/scripts/validate_gate_invariant_formula.py`, `studies/checkpoint_04/scripts/validate_response_operator.py`, and `studies/checkpoint_05/scripts/stabilizer_tableau.py`.

Focused source reads: `docs/NUMERICAL_METHODS.md:1–105`; `studies/checkpoint_04/scripts/cross_architecture_simulation.py:1–125,249–348`; `studies/checkpoint_05/scripts/cp04_common.py:210–304`; the mathematical and intervention references found in the study design/notes and current claim ledger. Current documents take precedence over historical figure specifications. The statistical audit separately covers original-row regressions, probability reconstruction, support and sampling.

The new `code/math_independent.py` imports no repository scientific module, archived row, Clifford matrix or symplectic map. It uses big-endian tensor positions, whereas the historical simulator uses little-endian qubit indices. Purities come from dense state-vector SVD, not tableau rank or the response formula. Two-qubit Clifford representatives are freshly generated using dense H, S and CNOT generators and their Pauli actions. Local twirls are independently evaluated by finite gate averages, in addition to a Gram-system reconstruction and invariant formulas. All these approaches share standard swap mathematics and NumPy linear algebra. The Haar unitary sampler uses standard Gaussian QR, an algorithm also used by the baseline; random-gate tests are therefore not an independent test of QR's Haar theorem. The 720-element exact Clifford operator average supplies an additional test without a Haar sampler.

The initial audit plan explicitly authorized these identities, special states, gate limits, stabilizer checks and counterexample searches before results. The illustrative equal-invariant gate pair substantiates a wording issue identified during that planned check. It is not an extension of the monitored-state experiment. No large simulation was run for this mathematical component.

## 2. Observable and general two-copy identity

Write $A=La$, $B=bR$, and $D=2^{n/2}$. From the definition alone,

$$
S_{\mathrm{lin}}^{\mathrm{norm}}(\rho_A)=\frac{D}{D-1}(1-P_A),\qquad
\chi_2=\frac{D}{D-1}(P_A-\mathbb E_U P'_A),\qquad
\chi_{\mathrm{rel}}=\frac{\chi_2}{P_A}.
$$

The denominator is the **input** central purity; it is outside the gate average. The dimension is the full left-half dimension, not the dimension of the probe pair. Substitution of the swap identity $P_A=\mathrm{Tr}(\rho^{\otimes2}F_A)$ and cyclicity gives

$$
\mathbb E P'_A=\mathrm{Tr}\bigl[\rho^{\otimes2}F_L\Omega_{\mathcal E}\bigr],
\quad
\Omega_{\mathcal E}=\mathbb E_U (U^\dagger)^{\otimes2}F_aU^{\otimes2}.
$$

This algebra works for mixed as well as pure inputs. The later complementary-purity substitutions require a pure global state. The tensor identities on spectators in `THEORY.md:44–75` are implicit in this expression. Twelve independent dense four-qubit evaluations agree to $4.45\times10^{-16}$.

This response is neither $\mathbb E[-\log_2P'_A+\log_2P_A]$ nor $-\log_2\mathbb E P'_A+\log_2P_A$. On the four-qubit product state with a uniform two-qubit Clifford probe, the fresh exact group calculation gives respectively

| Quantity | Value |
|---|---:|
| Mean post-gate purity | $4/5$ |
| $\chi_{\mathrm{rel}}$ | $4/15$ |
| Mean finite logarithmic Rényi-2 increment | $2/5$ bits |
| Negative logarithm of mean post-gate purity | $\log_2(5/4)=0.321928\ldots$ bits |

Thus the distinction made in `THEORY.md:5,121–143,340–344` and `NOTATION.md:13–14` is substantive. The implementation at `response.py:7` and `cross_architecture_simulation.py:343–348` has the correct normalization.

## 3. Local dressing, four purities and invariants

For $U=(u_a\otimes u_b)V(v_a\otimes v_b)$, local output unitaries commute with the appropriate replica swap and cancel. Independent local input Haar twirls project onto $B=(I,F_a,F_b,F_aF_b)$. This gives four coefficients, determined by the Gram matrix

$$
G_{ij}=\mathrm{Tr}(B_iB_j)=
\begin{pmatrix}
16&8&8&4\\8&16&4&8\\8&4&16&8\\4&8&8&16
\end{pmatrix}.
$$

Define the realignment explicitly by $(V^R)_{(i,k),(j,l)}=V_{(i,j),(k,l)}$ and set $E=E_{\mathrm{op}}(V)$, $E_s=E_{\mathrm{op}}(V\,\mathrm{SWAP})$. Direct contraction of the four overlaps yields

$$
b=(8,16(1-E),16(1-E_s),8),\qquad c=G^{-1}b.
$$

This is a derivation of the coefficients from four indexed swap contractions, rather than an assumption of the claimed final formula. With the repository's definitions

$$
e_p=\frac{E+E_s-3/4}{3/4},\qquad
g_t=\frac{E-E_s+3/4}{3/2},
$$

solving the displayed linear system gives exactly

$$
c=\left(\frac23e_p,\;1-g_t-\frac56e_p,\;g_t-\frac56e_p,\;\frac23e_p\right).
$$

The operator-Schmidt coefficients of $V/2$ have squared sum one, explaining the factor $1/16$ in `THEORY.md:152–177`. Under this convention, the product-input average **unnormalized** one-qubit linear-entropy production is $e_p/3$. It would be incorrect to replace $e_p$ by that unnormalized entangling power while retaining these coefficients. The repository defines its convention consistently; this is a normalization clarification, not a numerical defect.

Contraction with the pure input gives

$$
\mathbb E P'_{La}=c_IP_L+c_aP_{La}+c_bP_{L\cup b}+c_{ab}P_{Lab}
=c_IP_L+c_aP_{La}+c_bP_{L\cup b}+c_{ab}P_R.
$$

The noncontiguous $L\cup b$ is essential. For four qubits, $|\Phi^+\rangle_{Lb}|\Phi^+\rangle_{aR}$ and $|\Phi^+\rangle_{LR}|\Phi^+\rangle_{ab}$ both have $(P_L,P_{La},P_R)=(1/2,1/4,1/2)$ but $P_{L\cup b}=1$ and $1/4$. A SWAP on $ab$ gives those two post-purities, respectively. The Haar probe is special because its $c_b$ vanishes. Likewise, for the mixed input $I_{16}/16$, $P_L=P_R=1/2$ but $P_{Lab}=1/8$. Replacing $P_{Lab}$ by $P_R$ would incorrectly predict Haar post-purity $2/5$ instead of $1/4$. The source states the required purity assumption at `THEORY.md:117–119`.

Exact limiting coefficients and the two study probes agree:

| Gate/ensemble | $(c_I,c_a,c_b,c_{ab})$ |
|---|---|
| Identity or locally dressed identity | $(0,1,0,0)$ |
| SWAP with local dressing | $(0,0,1,0)$ |
| Haar/uniform Clifford | $(2/5,0,0,2/5)$ |
| $\exp[-i\pi(XX+YY)/8]$, locally dressed | $(1/3,1/4,-1/12,1/3)$ |
| $\exp[-i\pi XX/4]$, locally dressed | $(4/9,1/9,-2/9,4/9)$ |

For the Cartan gate, commuting $XX,YY,ZZ$ allow its Pauli expansion to be multiplied directly. Inserting its four operator-Schmidt weights and those after SWAP gives $e_p=2(A+B+C-AB-AC-BC)/3$ and $g_t=(A+B+C)/3$, with $A=\sin^2(2\alpha)$ and similarly for $B,C$. A separate 100-gate calculation agrees. Since $A,B,C\in[0,1]$, the multilinear expression $A+B+C-AB-AC-BC$ attains its extrema at cube vertices, where it is zero or one. Hence $e_p\ge0$, and $g_t\ge0$ is immediate. Subtracting the four-purity expression for equal central spectra gives the source's fixed-spectrum gate-space criterion (`THEORY.md:248–279`) without a sign error. The two inequalities are sufficient; their validity in particular monitored ensembles is empirical and is not proved here.

Independent numerical results: maximum coefficient discrepancy on 104 gates $2.00\times10^{-15}$; maximum overlap discrepancy $1.07\times10^{-14}$; Cartan identity discrepancy $1.48\times10^{-15}$; exact $24^2$ local-Clifford twirls on eight gates discrepancy $1.27\times10^{-14}$; direct averaged state-purity versus stencil discrepancy $5.94\times10^{-15}$. These finite computations check the derivation and conventions; they are not a proof for all inputs.

## 4. Haar/uniform-Clifford rule and complete-spectrum insufficiency

The two-qubit Haar twirl has commutant $\mathrm{span}(I,F_{ab})$. The traces of the initial $F_a$ against those two operators are both 8, while the Gram matrix is $\bigl(\begin{smallmatrix}16&4\\4&16\end{smallmatrix}\bigr)$. Thus both coefficients are $2/5$. For a pure global input $P_{Lab}=P_R=P_{m+1}$,

$$
\mathbb E P'_m=\frac25(P_{m-1}+P_{m+1}),\qquad
\chi_{\mathrm{rel}}=\frac{D}{D-1}\left[1-\frac25\frac{P_{m-1}+P_{m+1}}{P_m}\right].
$$

The freshly generated 720 symplectic actions have one representative per left-Pauli coset. Every one of the 16 left-Pauli factors cancels from the response operator, so this is exactly the average over all 11,520 projective two-qubit Cliffords, not a 720-gate sample. Its operator agrees with the Haar result to $2.67\times10^{-15}$. This establishes the finite group's property for this operator independently of the archived gate bank; the universal 2-design statement is established literature, assessed in the literature component.

The four-qubit states $|0000\rangle$ and $|\Phi^+\rangle_{La}|\Phi^+\rangle_{bR}$ have exactly the same full central spectrum $(1,0,0,0)$, but relative responses $4/15$ and $4/5$. This verifies the elementary insufficiency claim, including the values in `SCIENTIFIC_STORY.md:7`. It does not prove the direction of a monitoring-associated contrast.

## 5. Stabilizer spectra, alphabet and exact decomposition

Let $\mathcal S$ be a pure $n$-qubit stabilizer group and let $r_A$ be the number of independent generators supported entirely in $A$. Partial trace of $\rho=2^{-n}\sum_{g\in\mathcal S}g$ gives

$$
\rho_A=2^{-|A|}\sum_{g\in\mathcal S_A}g_A
=2^{r_A-|A|}\Pi_A.
$$

Here $\Pi_A$ is a projector of rank $2^{|A|-r_A}$. Consequently every nonzero eigenvalue is $2^{-(|A|-r_A)}$, $S_A=|A|-r_A$ is an integer, and $P_A=2^{-S_A}$. Fixing $S_m$ at fixed $n$ fixes all nonzero eigenvalues and the zero multiplicity, not merely purity. The binary-rank implementation `stabilizer_tableau.py:249–267` uses the equivalent pure-state formula $S_A=\mathrm{rank}(G|_A)-|A|$; this is valid because $\dim\mathcal S_{\bar A}=n-\mathrm{rank}(G|_A)$ and the two complementary entropies coincide.

Adding/removing a qubit bounds the entropy difference by one bit. Therefore the defined increments $\delta_L=S_m-S_{m-1}$ and $\delta_R=S_m-S_{m+1}$ lie in $\{-1,0,1\}$. Substitution gives

$$
\frac{\chi_{\mathrm{rel}}}{D/(D-1)}=1-\frac25(2^{\delta_L}+2^{\delta_R}).
$$

There are nine codes and six distinct response values. In row/column order $(-1,0,1)$ the response matrix is

$$
\begin{pmatrix}3/5&2/5&0\\2/5&1/5&-1/5\\0&-1/5&-3/5\end{pmatrix}.
$$

This matches `THEORY.md:362–403` and `boundary_codes.py:3–8`. The alphabet states the possible response map; it does not require all codes to occur at every fixed size/entropy. Three adjacent entropies suffice for the stated averaged response. They are entropies of extended cuts, not observables reconstructible from an asserted fixed-width local reduced state.

Since each row's response is a fixed linear combination of its nine indicator variables, applying a common linear estimator on identical rows and weights gives the identical linear combination of indicator coefficients. This is exact for the fixed-effects coefficient as well as a simple mean. It is not an independent observation. The distinction is correctly explicit in `THEORY.md:438` and `CLAIM_EVIDENCE_MAP.md`. The differential expression in `THEORY.md:428–438` requires differentiable conditional probabilities and fixed conditioning; the finite-grid regression is not automatically a local derivative or unconditional causal effect. The empirical probability shifts remain a separate statistical question.

## 6. Single-measurement sign, equality and outcome assumptions

An independent stabilizer-group proof avoids relying only on average entanglement monotonicity. For a projective Pauli $M$ supported on one side of a cut, every stabilizer supported wholly on the opposite side commutes with $M$ and remains in the conditional postmeasurement stabilizer group. Thus the opposite-side local stabilizer subgroup cannot shrink. A nondeterministic measurement replaces one independent stabilizer after choosing a commuting basis, so its dimension can increase by at most one. Hence $\Delta_M S\in\{0,-1\}$ for each nonzero outcome. A deterministic measurement leaves the state unchanged. The two nondeterministic outcome groups have identical support and different signs; alternatively, an anticommuting input stabilizer maps the two outcomes by a product of local Paulis. Their Schmidt spectra across every cut coincide.

A single-site measurement lies wholly on one side of each of the three relevant cuts. If the central spectrum is preserved, $\Delta_M P_m=0$, whereas $\Delta_M P_{m-1},\Delta_M P_{m+1}\ge0$. Subtracting the identity gives exactly

$$
\Delta_M\chi_{\mathrm{rel}}=
-\frac{2D}{5(D-1)P_m}(\Delta_M P_{m-1}+\Delta_M P_{m+1})\le0.
$$

Equality holds if and only if both neighboring purities are unchanged. Strictness is equivalent to at least one neighboring entropy dropping. Determinism is sufficient for equality, but is not necessary. This agrees with `THEORY.md:448–492`; it is a deduction from existing identities, not another empirical endpoint.

The support-only measurement update at `stabilizer_tableau.py:101–142` follows the required algebra: locate an anticommuting pivot, multiply every other anticommuter by it, remove the pivot, and insert the measured Pauli. Dropping outcome signs is valid for the present entropies and responses. It would not suffice for phase-sensitive observables, which are outside the present calculation.

Independent dense H/S/CNOT states at $n=4,6,8$ tested all three single-site Pauli axes and both nonzero outcomes: 300 input states, 9,820 nonzero outcomes, and 4,602 central-preserving outcomes. Of the latter, 2,832 saturate and 1,770 strictly suppress. No entropy-increment, outcome-spectrum, sign or equality failure occurred. All nine boundary codes appeared. Maximum positive response change was roundoff $3.00\times10^{-15}$; maximum corollary residual $7.39\times10^{-15}$; maximum opposite-outcome purity difference $3.11\times10^{-15}$. These generated states are not uniform over all stabilizer states, and this is not an exhaustive enumeration or substitute for the proof.

### Explicit restrictions checked by counterexamples

Bits below are listed in increasing site order, starting at site zero. The audit tests implement each state directly.

1. **Generic inputs:** on six qubits take $\sqrt{1/2}|000000\rangle+\frac12|101000\rangle+\frac12|110000\rangle$. A Z measurement of site 0 with outcome $-1$ has probability $1/2$ and leaves a Bell pair inside the left half. The central spectrum remains rank one, but neighboring purity drops from $5/8$ to $1/2$ and $\Delta_M\chi_{\mathrm{rel}}=2/35>0$. Thus the stabilizer-input restriction is real.
2. **A particular gate/arbitrary probe:** on four qubits take $|\Phi^+\rangle_{01}|00\rangle_{23}$. Measuring $X_2$ with outcome $+1$ preserves the central spectrum. The response to the fixed CNOT with control 2 and target 1 rises from 0 to $2/3$. Its Haar-averaged response remains $8/15$, so the exact corollary is saturated. The corollary cannot be stated for every individual gate.
3. **Spatial ordering:** on six qubits take $H_0H_2(|000000\rangle+|101100\rangle)/\sqrt2$. Both the near $Z_2$ and far $Z_0$ positive outcomes preserve central purity $1/2$. The initial, near-postmeasurement and far-postmeasurement relative responses are $-8/35,-8/35,-24/35$. Thus near-minus-far is $+16/35$, even under strict same-side joint preservation. Each individual change obeys the corollary. The negative location contrast in the monitored population is additional empirical content, not an algebraic consequence of the sign theorem.

Nothing here derives a long-run monitoring-rate trend, thermodynamic limit, fixed localization length, or individual-gate sign. The current source explicitly avoids those inferences. Weak measurements were not given a separate sign theorem or exhaustive counterexample search; the retained claim excludes them.

## 7. Minor mathematical documentation findings

| ID | Evidence | Diagnosis and consequence | Certainty / minimum repair |
|---|---|---|---|
| MATH-D1 | `src/boundary_susceptibility/response.py:4` | Docstring says “Relative Renyi-2 response,” inconsistent with the precise current observable. Formula itself is correct. | High. Rename only the docstring to input-purity-normalized linear-entropy response. |
| MATH-D2 | `docs/THEORY.md:195–197` | “same two local-unitary invariants used to classify the nonlocal content” can suggest a complete classification. These two invariants determine this averaged response, but do not determine all nonlocal gate data. | High that completeness would be false; wording ambiguity is minor. Say “determined by these two established local-unitary invariants.” |
| MATH-D3 | `docs/THEORY.md:152–177` | The realignment $V^R$ is used without its index convention being defined in the theory or notation. Readers must infer it from source code. | High, documentation only. Add the one-line realignment definition given in section 3. |

For MATH-D2, an explicit pair has squared-sine Cartan coordinates $(1/2,1/2,0)$ and $(2/3,1/6,1/6)$. Both give $e_p=1/2,g_t=1/3$, yet their normalized operator-Schmidt spectra differ (saved in the JSON). Operator-Schmidt spectra are invariant under local input/output unitaries, so these gates are not locally equivalent. The test `test_response_invariants_are_not_complete_gate_invariants` verifies the stated equal invariants and distinct spectra. No correction to the four-purity coefficients is implied.

The baseline's three small assertions in `tests/test_identities.py:5–11` only check chosen formula values. By themselves they cannot detect an incorrect physical definition or a shared erroneous stencil. Existing archived validations also import scientific baseline functions and gate banks. The new dense group averages, alternative purity computation and explicit states provide additional independence; their use of the same standard mathematical definitions is disclosed rather than treated as a separate physical replication.

## 8. Commands, tolerances, outputs and limits

Executed from the repository root using the clean pinned environment:

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /workspace/scratch/0174ee249694/audit-venv/bin/python audits/full-sanity-01/code/math_independent.py > audits/full-sanity-01/results/math_independent_run.log 2>&1
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /workspace/scratch/0174ee249694/audit-venv/bin/python -m pytest -q audits/full-sanity-01/code/math_independent.py > audits/full-sanity-01/results/math_pytest.log 2>&1
```

Python 3.12.13; NumPy 2.3.5; seed `202609080101`; float64/complex128; absolute assertion tolerance $2\times10^{-10}$; eigenvalue support threshold $10^{-10}$; zero-outcome probability threshold $10^{-13}$. The final full diagnostic took 6.56 seconds on one numerical thread, with dense states up to dimension 256 and full two-copy matrices up to $256\times256$. Exact runtime is in `results/math_independent.json`. The first version passed two tests; after adding the explicit invariant-wording example, the full script was rerun and the final suite passed **three tests**. No warnings or failures occurred. All earlier reported random checks remain unchanged because the added example is deterministic.

Saved outputs: `results/math_independent.json`, `results/math_independent_run.log`, `results/math_pytest.log`; independent source and targeted regression tests: `code/math_independent.py`. The JSON and log intentionally contain the same final numerical report for machine and human replay. These tests confirm scope exclusions and correct identities, rather than silently changing baseline science or marking an invalid universal claim as accepted.

Unchecked here: empirical monitoring redistribution, regressions, bootstrap coverage, full trajectory campaigns, literature priority and remote repository state. Those belong to other components of the full audit. Within this component, all planned mathematical claims were analytically checked and received targeted numerical coverage. The retained M1 elementary insufficiency, M2 identity/alphabet, and T1 restricted corollary survive; empirical portions of M1–M5 require their separate statistical evidence.

## 9. Final source-coverage closure

The closing read completed **all 345 lines** of `studies/checkpoint_05/scripts/cp04_common.py`, beyond the focused range listed in section 1. Both `studies/checkpoint_04/scripts/validate_response_operator.py` (138 lines) and `validate_gate_invariant_formula.py` (32 lines) were read in full. No numerical calculation or test was repeated for this closure.

The shared common module uses the declared little-endian adjacent-gate order, restores the measurement basis after X/Y/Z projections, and implements the weak-Z square-root Kraus operators for its stated POVM. In particular, its Y-basis transformation $H S^\dagger$ has the correct sign. Its gate sampling, subsystem contraction and cycle order are consistent with their documented definitions. The zero-probability guard and clipping are floating-point safeguards; the exact-sign corollary does not depend on these approximate state-vector steps.

`validate_response_operator.py:8–20,70–104` imports the common module's gate sampler, Clifford bank loader, state updates, purity and response functions. Its direct state-gate averaging is a useful check, but cannot be described as an independently implemented simulator. The explicit swap matrices at lines 23–51 offer a partially separate operator contraction. `validate_gate_invariant_formula.py:7,19–23` similarly imports the production QR sampler, SWAP and commutant projection. The final independent audit tests avoid those module imports, as detailed above.

**MATH-C1, minor validation-enforcement defect, high certainty:** `validate_gate_invariant_formula.py:27` computes a `passes` boolean, but lines 28–32 only write/print it and return normally. `.github/workflows/tests.yml:41` runs this script directly, and the workflow contains no following assertion of its JSON flag. Therefore an excessive coefficient error can still produce a successful command exit and green status for this step. This diagnosis follows directly from the unconditional return path; no fault-injection calculation was performed in this closing read. It does **not** indicate that the present formula or fresh numerical result failed. The smallest later repair is to raise a nonzero exit after writing the report when `passes` is false, as `validate_response_operator.py:135–136` already does, and add a targeted failure-path regression. This belongs to verification reliability, not mathematical validity.

### Prospective follow-up for MATH-C1, recorded before execution

To provide an executable minimal counterexample to the exit-code behavior, `code/validator_confirmed_defect.py` will run the unchanged validator in a subprocess with an audit-only in-memory monkeypatch: add $1/8$ to its imported commutant routine's first coefficient. It will use **one sampled gate**, seed 123, and require the report to say `passes=false` before asserting a nonzero exit. This is controlled fault injection into the validator dependency, not a claim of a naturally occurring coefficient error. No baseline file is edited. The small sampled calculation is expected to take less than one second, excluding process/import overhead. The test is marked strict expected failure and will be run once normally and once with `--runxfail` to expose the actual failing assertion. Logs will be retained under `results/`. This follow-up is motivated by the static defect finding, rather than a new scientific test planned before the original results.

**Executed follow-up:** the strict-xfail invocation returned exit 0 with `1 xfailed in 1.01s`; the unmasked invocation returned exit 1 with `1 failed in 1.03s`. Both used one gate at seed 123. The deliberately offset coefficient produced maximum error `0.12500000000000083`, the validator report said `passes=false`, and its subprocess exit code was **0**. The final assertion that failed was `assert completed.returncode != 0`. This experimentally confirms MATH-C1's enforcement defect; it is an expected defect demonstration, not a failed clean calculation of the gate identity.

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /workspace/scratch/0174ee249694/audit-venv/bin/python -m pytest -q -rx audits/full-sanity-01/code/validator_confirmed_defect.py > audits/full-sanity-01/results/validator_confirmed_defect_xfail.log 2>&1
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /workspace/scratch/0174ee249694/audit-venv/bin/python -m pytest -q --runxfail audits/full-sanity-01/code/validator_confirmed_defect.py > audits/full-sanity-01/results/validator_confirmed_defect_runxfail.log 2>&1
```

The test deliberately imports the baseline validator and its production coefficient function because its target is their failure-reporting contract. The alternative implementation consists of the subprocess harness, controlled in-memory fault and independent JSON/exit-code assertions. Unexpected import errors, absent output, or failure to trigger the intended numerical discrepancy are raised as runtime errors and therefore cannot be hidden by the strict expected-failure mark. No scientific baseline source or archived result was altered.
