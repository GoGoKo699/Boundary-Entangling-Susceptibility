# Remote repository audit — 2026-08-27

**Repository:** `GoGoKo699/Boundary-Entangling-Susceptibility`  
**Audit branch:** `repository-audit-2026-08-27`

## Scope

This audit checks the remote repository as a standalone scientific resource rather than as a manuscript supplement. It covers:

- reader-facing scientific structure;
- correspondence among claims, canonical data, plotting scripts, and figures;
- local documentation-link integrity;
- browser-figure validity;
- clean-clone verification and CI configuration;
- provenance of the author-reviewed Python panels;
- repository scope, exclusions, and public-release readiness.

## Findings that pass

### Scientific story

The README presents the surviving project in the correct order:

1. central-spectrum insufficiency;
2. exact neighboring-cut response mechanism;
3. physical large-size persistence and independent replication;
4. paired cut-local measurement intervention.

Rejected historical claims are clearly separated from the active result. The susceptibility is not described as an order parameter or critical exponent.

### Reader routes

The repository has distinct routes for:

- the full scientific argument;
- exact theory;
- numerical methods;
- claim-by-claim evidence;
- extended results;
- reproduction;
- validation;
- research history and limitations.

A reader can reconstruct the scientific logic without consulting the manuscript.

### Figures and data

All six data-backed panels have:

- a browser-visible SVG;
- canonical CSV or JSON inputs;
- a Python plotting script;
- an author-reviewed PDF identity recorded by filename, byte count, and SHA-256 hash.

The exact manuscript-layout PDF binaries are deliberately not claimed to exist at broken in-repository paths. They are reproducible locally and should be attached to a future versioned release.

### Code and verification

The repository contains:

- a reusable exact-identity package;
- unit tests;
- a repository verifier;
- a GitHub Actions test workflow;
- load-bearing Checkpoint 04 and 05 source, design locks, validation source, and selected result tables.

The verifier checks the exact identities, numerical signs and reconstructions, SVG validity, local documentation links, provenance-manifest structure, and the exclusion of TeX/TikZ.

### Scope discipline

The repository contains no manuscript TeX or TikZ. Historical trajectory-fingerprint, cumulative flow-balance, and Aubry–André branches are preserved only as research history rather than active claims.

## Corrections made in this audit

1. Replaced misleading nonexistent `figures/core/*.pdf` and `.png` paths in the figure-hash manifest with an explicit external frozen-baseline manifest.
2. Clarified the distinction among tracked browser SVGs, tracked canonical inputs/scripts, locally regenerated PDFs, and future release assets.
3. Added immutable hashes and byte counts for the two complete checkpoint archives and the frozen Overleaf source bundle.
4. Strengthened `verify.py` with SVG parsing, local Markdown/HTML-image link checking, and figure-provenance validation.
5. Removed a temporary self-committing figure-materialization workflow that was useful only during migration and should not remain in the research repository.
6. Expanded the migration-status and public-release checklists so they do not imply that licensing, raw-data deposit, external theorem audit, or GitHub administration is already complete.

## Remaining manual or external tasks

The repository should remain private until these are resolved:

- select code, data, and figure licenses;
- deposit the complete raw checkpoint archives and frozen PDF set as immutable release assets;
- add repository description and scientific topics in GitHub settings;
- decide whether `main` should be protected and require CI;
- obtain an independent specialist audit of the two exact theorems;
- update the citation record after a preprint exists;
- remove temporary migration branches after explicit author approval;
- make the final visibility decision.

## Audit verdict

**Scientifically and structurally suitable for manuscript construction and external technical review.**

**Not yet ready for public release**, because licensing, immutable raw-data assets, external theorem review, repository settings, and branch cleanup remain open.
