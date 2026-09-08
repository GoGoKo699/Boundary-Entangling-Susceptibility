# Repository completeness and reader experience

Verdict: the frozen checkout is a usable, self-contained resource for the
documented four-figure recorded-data workflows. It is not yet complete under
its own stated criterion for eventual manuscript preparation. Two acknowledged
completion obligations remain, and several small provenance statements need
correction. No general redesign is necessary or authorized.

## Confirmed findings and smallest adequate changes

| ID | Severity and certainty | Exact evidence | Consequence and minimum repair |
|---|---|---|---|
| C1 | Known completion requirement, high confidence | `docs/PROJECT_GUIDE.md:19–23`; all 207 baseline tracked paths and figure source inventory | Editable external composite schematics are not tracked. All six numerical panels have editable Python source, which does not supply the external composites. Obtain the author's actual editable schematic sources and a mapping to the intended composites. Do not recreate an unseen layout or claim it was checked. |
| C2 | Attribution completion requirement, high confidence | `docs/PROJECT_GUIDE.md:23`; authoritative `docs/RELATED_WORK.md` | Equation-level entanglement-feature antecedent integration is explicitly unfinished. The literature audit supplies the scientific comparison; integrate the smallest accurate citation/notation mapping in a later authorized repair. This is distinct from the valid empirical findings. |
| C3 | Minor source-navigation defect, certain | `docs/DIALOGUE_REPORT.md:508`, versus `provenance/SOURCE_MIGRATION.md:7` and complete archive member list | S8 says the full CP04 archive is preserved, but the checkout contains selected original members in a new 172-member bundle. Replace this with exact bundle namespaces and the already recorded source-archive identity. This does not require obtaining the old ZIP to reproduce current figures. |
| C4 | Provenance documentation gap, certain | `docs/RUN_HISTORY.md:35,57–60`; `data/record_bundle_manifest.json`; `run_tableau_scaling.py:125–142` | Original simulation manifests and the claimed preserved preflight failure log are absent from the tracked tree and bundle. The run-history timing/failure narrative cannot be independently checked against those records here. Supply original records if available, or clearly label these details as historical narrative and the log unavailable. Do not invent recovered logs. |
| C5 | Campaign reproduction recipe gap, high confidence | `docs/REPRODUCTION.md:65`; `run_tableau_scaling.py:108–117`; `analyze_checkpoint05.py:191–195,225–228`; `analyze_measurement_location.py:127–130,151–153` | `--help` gives configurable defaults, not exact archived commands. Analysis summaries omit the actual bootstrap seed. Add an explicit run-specific generation/analysis recipe and distinguish verified seeds from defaults or unrecovered history. The audit regenerated 27 original trajectories and all current documented analyses already work; this is not an observed calculation failure. |

C1 and C2 block the assertion that everything needed for the eventual paper is
already contained in the repository. C3–C5 are limited provenance/reader defects,
not grounds to discard the four-figure observations. Missing original bootstrap
execution seeds for Figures 3–4 are distinct from missing input data: the actual
archived resample arrays are included and their intervals replay. A later
independently declared fresh bootstrap can be reproducible without pretending
to recover undocumented historical RNG settings.

One residual language inconsistency should follow the Figure 4 report:
`docs/RUN_HISTORY.md:97–98` recommends an unqualified “within a principal stratum”
description, whereas `docs/NUMERICAL_METHODS.md:215` and the current caption
carefully distinguish side-varying original eligibility from strict same-side
joint preservation. Update that summary to the exact selected intervention
estimand already defined in the current methods. This does not change data.

## Navigation, definitions, figures and source access

`code/navigation_inventory.py` examined the pinned Git tree, not generated audit
files. Its ledger records all 221 local links/image sources across 64 Markdown
files. Every destination and tested Markdown fragment resolves. It parses all
50 Python files and inventories their imports. The only third-party runtime
dependencies are the declared scientific/plotting/testing stack; local helper
imports found in different source directories were manually resolved. No
manuscript `.tex` or editable composite-specific source was found. Results are
saved in `results/navigation_links.csv`, `results/navigation_imports.csv`, and
`results/navigation_summary.json`.

The README offers a coherent entry route through the four figures, exact
definitions, evidence qualifications and reproduction commands. The guide
separates reading, checking, and reproduction. The notation table defines n,m,D,
the distance d, response normalization, the regression scale, and the two
different Figure 4 quantities before detailed inference. The dialogue explains
that family labels in Figure 1 describe state generation rather than fresh
probe choice, and it separates a negative contrast from a negative response.
These are useful protections against common misreadings.

Ordinary Markdown mathematical syntax, symbol usage and references were checked
in source. The six regenerated numerical panels were visually checked by the
root audit (`FIGURE_RENDERING.md`) and separately tied to their data/code.
This audit did not open a live GitHub-rendered page or inspect an unavailable
Overleaf composite. Thus it does not certify every live math-renderer behavior
or any external panel arrangement. No observed source-level rendering defect
requires a redesign.

Current sources are identified adequately: `docs/FIGURE_BASELINE.md` and
`provenance/current_baseline_sha256.json` identify the active plots;
`results/historical_figure1/` holds the superseded intervals and figures;
`results/historical_fit/` preserves the rejected distance fit; historical study
notes contain explicit supersession banners. The original design/source paths
retain their identities. The active Figure 4 generator does not read the old
fit, and the primary narrative rejects a recovered localization length or a
proven thermodynamic coefficient. The known small provenance inconsistencies
above should be corrected without altering historical source records.

## Data completeness versus provenance completeness

The root bundle contains the raw observations, reference/physical spectra,
Clifford matrices and support maps, archived Figures 3–4 resamples, design locks,
and supporting tables used by the documented commands. `RecordBundle` requires
the full ZIP identity and exact member set, checks each member hash, prevents
unsafe paths, and refuses to overwrite different materialized files
(`src/boundary_susceptibility/records.py:15–74`). The root audit actually ran
materialization, record replay, reassessment and the complete Figure 1 sampler
and verifier from this checkout. No old chat, expired CI download, private
working directory or separate channel project was needed.

Hashes authenticate continuity against the manifest, not an externally witnessed
history. The dated locks and SHA files are internally preserved records, not
public preregistration. The missing manifests and preflight log prevent full
verification of certain historical execution details. The 27 regenerated
trajectories materially strengthen practical generation reproducibility while
leaving this distinction intact.

No license change is recommended as a scientific correction. The README and
`LICENSE_STATUS.md` honestly disclose that a reuse license is undecided, and
`CITATION.cff` is provisional. Those are author release choices, separate from
scientific validity. No unrelated project material, website, manuscript source,
or redesign has been added.
