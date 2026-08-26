# Data policy

## Tracked in ordinary Git history

The repository tracks:

- every canonical CSV or JSON input used by the six core Python panels;
- the exact plotting scripts;
- selected load-bearing derived tables from Checkpoints 04 and 05;
- design locks, timestamps, simulation and analysis source, theorem checks, and
  validation source needed to audit the final scientific chain;
- browser-visible SVG exports of the accepted panels.

These files are small, reviewable, and sufficient to reproduce the displayed
core figures and verify the headline numerical statements.

## Kept outside ordinary Git history

The complete Checkpoint 04 and Checkpoint 05 packages contain additional
compressed raw arrays, state tables, bootstrap arrays, and duplicated generated
artifacts. They are intentionally not committed as opaque binary archives.
Before public release they should be attached to a versioned GitHub Release or
deposited in a research archive, with download locations and SHA-256 values
recorded here.

## Why this split is deliberate

A reader should not have to download a large archive to understand the result,
inspect the central evidence, or regenerate the paper panels. At the same time,
full trajectory-level provenance should remain available as a release asset for
specialist reanalysis.

## Pending release action

- choose the public data archive or GitHub Release;
- upload the two complete checkpoint packages;
- record their immutable hashes and URLs;
- specify the final data license.
