# Simulator and gate audit

Verdict: no scientific simulator defect was found in the audited domain.
The phase-free tableau is appropriate for these pure-stabilizer observables,
the gate maps have the required distribution, and selected original trajectories
regenerate. These conclusions combine code inspection, separate physical/kernel
oracles, and bounded original-generation replay. They do not assert that every
original trajectory was regenerated or that a numerical sample proves a theorem.

## Independent checks actually executed

`code/simulator_independent.py`, seed 2026090819, produced
`results/simulator_independent.json` in 11.84 seconds with one BLAS thread.
All assertions passed at tolerance 2e-12 (except the explicitly looser 1e-10
Pauli-identification bound).

| Check | Independent construction | Result |
|---|---|---|
| Packed entropy/rank | Integer row masks; highest-pivot elimination; compute entropy by counting stabilizers supported in the region through the complementary restriction | 135 subset checks at n=4,8,63,64,65,127,128,129,256 pass; includes empty, full, central, and noncontiguous regions |
| Pauli measurement support | Row update chooses the final anticommuting row, unlike the production first pivot; compare spans, not generator identity | 99 random updates and their 99 deterministic repeat measurements pass, including 64-bit boundaries |
| Dense local gate action | Construct every embedded matrix entry from basis-bit indices | All tested adjacent placements at n=2,4,6 pass in three state-vector implementations; maximum error 6.21e-17 |
| Born-rule and weak measurements | Explicit dense projectors (I±P)/2 and square-root POVM Kraus matrices, both outcomes and eta=0,.6,1 | 432 cases in three implementations; maximum state-vector error 5.98e-16, probability error 4.45e-16 |
| Clifford table | Remove global phase; conjugate four independent Pauli generators; independently generate support group by H,S,CNOT closure | 11,520 distinct projective unitaries, 720 maps, multiplicity exactly 16; maximum unitary error 8.89e-16 |
| Stored masks and ordering | Apply all 720 stored masks to all 16 two-site Pauli supports, compare with conjugation labels | All 11,520 cases agree |
| Clifford class sampler | Exhaustive two-sided local-support orbits and weights 1:9:9:1 | Orbit sizes 36,324,324,36, equal weighted probability 1/720 for every support map |

The full projective table is a Clifford group because every unitary maps the
Pauli generators to signed Paulis, is distinct modulo scalar phase, and all
11,520 elements occur. The sampler's independent local Clifford factors also
randomize Pauli cosets: uniform local-support sampling and the orbit weights
are consistent with full uniform Clifford sampling, not only matching a few
response moments. Ordinary finite-precision pseudorandom sampling is understood;
the unsigned-word modulo implementation has at most one-word count imbalance,
which has no meaningful numerical consequence here.

The first audit-harness attempt failed on Numba cache import resolution because
the audit dynamically renamed the production module. It performed no successful
scientific comparison. The retained `results/simulator_independent_attempt1.log`
documents this. Importing the unchanged module by its original name resolved
the harness issue; the successful second run is logged separately. This was not
a baseline defect or an alteration of source calculations.

## Bounded original-generation replay

The prospective rationale and 27-trajectory budget are saved in
`SIMULATOR_REPLAY_PLAN.md`. `code/simulator_archive_replay.py` completed in 8.61
seconds and wrote `results/simulator_archive_replay.json`.

* Primary: first p=.20 and final p=.34 trajectory, both protocols, all four sizes.
* Replication: final p=.26 trajectory, both protocols, all four sizes.
* Location arm: final p=.26 trajectory at each of n=64,128,256.

All 75 archived probe records agree, including central/neighboring entropies,
purities/responses, measurement counts, every stored window feature, and late
quarter-partition information. All 42 corresponding paired intervention rows
agree. Differences in response fields are only CSV floating-point rounding
(below 2e-12). The independent BLAKE2b seed derivation agrees with the production
function and yields no collisions among all 84,600 primary, replication, and
location trajectories.

This replay shares the production simulator and stored map inputs. It validates
the connection between the archived observations and the stated generation
recipe; it is not another independently implemented large-size simulation.
The separate integer-row and dense-projector checks address different risks.

## Scientific conventions and implementation findings

1. **Phase omission is justified.** `studies/checkpoint_05/scripts/stabilizer_tableau.py:4–14,100–145`
   omits signs but preserves the pure Lagrangian support space. A random Pauli
   projection changes the support identically for both nonzero outcomes; a
   deterministic projection leaves it unchanged. All implemented entropy and
   response observables depend only on this space. This does not justify using
   the simulator for outcome records, mixed states, non-Pauli measurements, or
   non-Clifford state evolution.
2. **Entropy computation is correct for pure states.** The production
   restricted-column rank formula at `stabilizer_tableau.py:215–264` is
   equivalent to S(A)=|A|−dim(stabilizers supported in A). The independent
   oracle deliberately uses the latter identity on the complementary restriction.
3. **Gate/endian conventions agree.** The stored order is
   `(x_low,z_low,x_high,z_high)` (`build_symplectic_maps.py:23–56`); the simulator
   maps these to its separated X/Z columns (`stabilizer_tableau.py:79–97`).
   Dense state-vector pair bases are `|high,low>` and fresh cross-cut gates
   target low site m−1. Exhaustive mask tests and independent embedded matrices
   resolve the possible reversal ambiguity.
4. **Architecture differences are real and retained.** The large physical arm
   randomly orders the two sublayers each cycle (`stabilizer_tableau.py:165–200`).
   The Figure 1 state-vector arm alternates their order by cycle and starts with
   Haar-product states, including the `clifford_z` family
   (`cross_architecture_simulation.py:396–430`). Its physical-stabilizer extension
   explicitly requests stabilizer-product inputs
   (`run_physical_stabilizer_arm.py:57–62`). These distinct arms should not be
   described as one identical circuit ensemble.
5. **Probe normalization is consistent.** Central observables divide the
   normalized linear response by the input purity
   (`stabilizer_tableau.py:268–283`), not by output purity. At the largest
   audited size n=256, purity down to 2^-128 is comfortably representable.
   Floating arithmetic implements the mathematically exact identity; the rank
   and entropy calculations themselves are binary/integer.
6. **Seed independence is scoped correctly.** Seeds include run label, protocol,
   size, probability and trajectory (`run_tableau_scaling.py:33–41`); probe times
   are saved on a common trajectory, not reseeded observations. The 84,600-seed
   check establishes no collisions in the included CP05 campaigns, not statistical
   independence of arbitrary PRNG streams or an external replication.

## What existing verification does and does not establish

The documented 256-case tableau/state-vector validator and 100-gate invariant
validator also passed in the root audit; see `reproduced_records/`. The former
imports production state-vector gate kernels (`validate_tableau_against_statevector.py:13`)
and repeats the analytic response formula. It is a useful independent state
representation, not complete implementation independence. The new dense
projector/embedding oracle removes that shared gate-kernel dependency; the
mathematical audit supplies separate response derivations.

`verify.py:49–119` mainly checks fixed formula examples and expected signs/tables;
`tests/test_identities.py` has three point checks. Those cannot by themselves
validate physical evolution or an asymptotic model. Hash tests protect provenance,
and plotting tests protect scientific coordinates and interval endpoints, but
cannot show an inherited estimator or model is appropriate. The synthetic
fixed-effect and paired-bootstrap tests in `tests/test_evidence_pipeline.py`
do test meaningful estimator behavior. The documentation mostly states these
distinctions correctly (`docs/VALIDATION.md`, `docs/REPRODUCTION.md:67–71`).

## Coverage and limits

The manual source coverage is enumerated in `results/simulator_source_coverage.csv`.
All baseline Python files were additionally parsed for imports by
`code/navigation_inventory.py`; AST parsing is not counted as scientific review.
Statistical estimators and uncertainty implementations are audited in the
figure-specific reports. Remaining exclusions are full original simulation
campaign regeneration, another large-size independent simulator, live GitHub
math rendering, and recovery of original execution logs/manifests. The last
is a provenance gap discussed in `COMPLETENESS.md`; it did not prevent the
bounded original-trajectory replay.

Commands actually executed, from repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /workspace/scratch/0174ee249694/audit-venv/bin/python audits/full-sanity-01/code/simulator_independent.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /workspace/scratch/0174ee249694/audit-venv/bin/python audits/full-sanity-01/code/simulator_archive_replay.py
/workspace/scratch/0174ee249694/audit-venv/bin/python audits/full-sanity-01/code/navigation_inventory.py
```

The root environment record supplies exact package versions. Only audit
additions were written. No scientific repair is proposed for the tested kernels.
