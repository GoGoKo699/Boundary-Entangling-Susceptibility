# Data policy

## Tracked in ordinary Git history

The repository tracks:

- every canonical CSV or JSON input used by the six core Python panels;
- the exact plotting scripts;
- selected load-bearing derived tables from Checkpoints 04 and 05;
- design locks, timestamps, simulation and analysis source, theorem checks, and validation source needed to audit the final scientific chain;
- browser-visible SVG exports of the accepted panels.

These files are small, reviewable, and sufficient to regenerate the displayed data panels and verify the headline numerical statements.

## Frozen author-reviewed figure binaries

The six PDF panels approved in the manuscript-layout workflow are identified by filename, SHA-256 hash, and byte count in `provenance/figure_sha256.csv`. They are not tracked as ordinary branch files. The canonical values and plotting scripts regenerate equivalent vector PDFs locally, while an immutable copy of the exact frozen PDF set should be attached to a future versioned release.

## Kept outside ordinary Git history

The complete Checkpoint 04 and Checkpoint 05 packages contain additional compressed raw arrays, state tables, bootstrap arrays, and duplicated generated artifacts. They are intentionally not committed as opaque binary archives. Before public release they should be attached to a versioned GitHub Release or deposited in a research archive, with download locations and SHA-256 values recorded here.

Current local archive identities retained for migration provenance:

| Archive | Bytes | SHA-256 |
|---|---:|---|
| `entanglement_project_checkpoint_04.zip` | 8,874,243 | `690722855b37c5ba1aab96720e03d0f36e7b2b0b86447827f9eeecda0a973023` |
| `entanglement_project_checkpoint_05.zip` | 10,718,474 | `284a92bfac08af6194cd576ce07c4be90e1e760fcc7b0fc7951eaacd1fa975ce` |
| `Overleaf.zip` frozen figure source | 56,910 | `888103c5c63a5b8ebb203e73c8cea79c4f43b4d8828caf59d8a6f4518ce44977` |

## Why this split is deliberate

A reader should not have to download a binary archive to understand the result, inspect the central evidence, or regenerate the paper panels. At the same time, full trajectory-level provenance should remain available as a release asset for specialist reanalysis.

## Pending release action

- choose the public data archive or GitHub Release;
- upload the two complete checkpoint packages and frozen figure set;
- record their immutable URLs alongside the hashes above;
- specify the final data and figure licenses.
