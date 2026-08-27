# Public release checklist

The scientific and reader-facing migration is complete. The following administrative, archival, and external-audit steps remain before making the repository public.

## Licensing and citation

- [ ] Choose a code license.
- [ ] Choose compatible data and figure licenses.
- [ ] Replace the provisional `CITATION.cff` metadata with the preprint DOI or arXiv identifier.

## Immutable research assets

- [ ] Upload the complete Checkpoint 04 and Checkpoint 05 archives to a versioned GitHub Release or research-data repository.
- [ ] Upload the six exact author-reviewed PDF panels, or a frozen figure bundle, to the same versioned release.
- [ ] Record immutable asset URLs alongside the existing SHA-256 hashes in `docs/DATA_POLICY.md` and `provenance/figure_sha256.csv`.

## Scientific audit

- [ ] Complete an independent specialist audit of the response-operator and stabilizer boundary-code theorems.
- [ ] Recheck the final novelty language against the literature immediately before preprint release.

## GitHub administration

- [ ] Add the repository description and scientific topics in GitHub settings.
- [ ] Decide whether `main` should require the test workflow before merging.
- [ ] Remove temporary migration branches after explicit author approval.
- [ ] Confirm all README equations and SVGs render correctly after the repository becomes public.
- [ ] Run the full clean-clone workflow against the final public-release commit.
- [ ] Change visibility only after the preceding items are complete.

No manuscript TeX or TikZ should be added during release preparation.
