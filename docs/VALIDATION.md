# Validation

Validation has four distinct layers.

1. `verify.py` checks exact identity examples, frozen numerical expectations, all current figure/input hashes, local document references, allowed source types, and every member of the recorded-data bundle. These are regression and integrity checks, not proof of an extrapolation model.
2. `reproduce_core_records.py` recalculates core point estimates from the original observations, verifies the separately preserved historical Figure 1 table against its original hybrid source, and reconstructs Figures 3/4 intervals from their preserved bootstrap arrays. It does not claim that the missing accepted Figure 1 resamples were recovered. The output labels those distinctions.
3. `reassess_evidence.py` repeats the independently written, post-hoc analysis of size-model and paired-selection sensitivity. Its historical exponential diagnostics do not restore the abandoned length claim.
4. The study source provides tableau/state-vector and gate-invariant checks. The full large-system campaigns and external peer review are not implied by a green CI run.

The measurement data, simulator source, group maps, and needed design records are all available through the root bundle and readable study directories. No inaccessible checkpoint or another project is needed. See [reproduction commands](REPRODUCTION.md).

See [precise reproducibility limits](REPRODUCIBILITY_LIMITS.md). Preserved original intervals and fully regenerated intervals are not interchangeable.

## Current Figure 1 uncertainty

The dedicated read-only CI job reruns the unchanged locked sampler and the separately written multiplicity verifier, then checks every numerical output hash and all current endpoints against the adopted table. The new calculation is reproducible, while the superseded historical bootstrap remains unrecovered. See [the precise recipe](FIGURE1_UNCERTAINTY.md).
