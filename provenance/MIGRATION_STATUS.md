# Migration status

**Repository:** `GoGoKo699/Boundary-Entangling-Susceptibility`

## Complete on the default branch

- [x] Reader-facing README explaining the complete surviving story.
- [x] Exact theory and notation documentation.
- [x] Numerical methods, run chronology, scope, limitations, and related-work audit.
- [x] Canonical data for Figures 1–4 (six Python panels).
- [x] Reproducible plotting scripts for all six panels.
- [x] Browser-visible SVG exports of all six panels.
- [x] Reusable exact-identity package and unit tests.
- [x] Repository-level verifier and GitHub Actions workflow.
- [x] Selected load-bearing scripts, design locks, validation source, and derived tables from Checkpoints 04 and 05.
- [x] Explicit exclusion of TeX and TikZ.
- [x] Author-reviewed PDF filenames and SHA-256 identities recorded without broken in-repository paths.

## Deliberately outside ordinary Git history

- The exact six author-reviewed PDF binaries. They are reproducible from tracked inputs and scripts; their immutable hashes are recorded in `provenance/figure_sha256.csv`.
- Complete compressed Checkpoint 04 and Checkpoint 05 trajectory/state archives. Their hashes are recorded in `docs/DATA_POLICY.md` pending a release or research-data deposit.

## Pending before public release

- [ ] Select code, data, and figure licenses.
- [ ] Upload complete checkpoint archives and the frozen PDF set as release/data-deposit assets.
- [ ] Add immutable download URLs to `docs/DATA_POLICY.md`.
- [ ] Complete an external specialist audit of the exact theorems.
- [ ] Replace the provisional citation record with the preprint DOI/arXiv entry.
- [ ] Add repository description and topics in GitHub settings.
- [ ] Decide whether to protect `main` and require the test workflow before merging.
- [ ] Remove temporary migration branches after explicit author approval.
- [ ] Decide when to change repository visibility from private to public.

## Archived scientific directions

The following are documented only as research history and are not part of the active workflow:

- generic entanglement-trajectory fingerprints;
- cumulative spectral-flow cancellation as a transition mechanism;
- a spectral-flow balance ratio as an order parameter;
- Aubry–André field-versus-transport competition.
