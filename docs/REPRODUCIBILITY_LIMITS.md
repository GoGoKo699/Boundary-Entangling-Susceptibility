# Reproducibility limits

The repository must distinguish preserved scientific records from exact regeneration of every historical calculation.

## Figure 1 accepted confidence intervals

The accepted hybrid-panel table and source manifest are preserved unchanged in the indexed record bundle under `accepted_figure1/`. Its ten point estimates are recovered from original state records by matching the supported family/size/time cells across the primary and independent runs. This uses six cells per family except Clifford, which uses four, and agrees with every accepted point estimate.

However, the accepted panel's bootstrap RNG seed and resample arrays were not saved in the recovered hybrid package. The preceding figure-design package contains a different 10,000-draw bootstrap. Its primary Clifford point estimate also uses a different support (six cells rather than four). Those earlier resamples must not be mislabeled as the accepted figure's resamples. The later source manifest identifies the raw records and bootstrap count, but not the missing seed or full analysis routine.

The accepted confidence intervals are source-traced and redraw exactly; they are NOT claimed to be regenerated from raw data by the cleanup. `reproduce_core_records.py` exposes `figure1_exact_accepted_interval_replay: false`. No interval was silently replaced, no random seed was reverse-engineered to match desired answers, and no claim of independent validation is based on the plotting table alone.

A future explicitly approved statistical revision could supply a complete deterministic recipe and new intervals. Such a revision is outside this repository cleanup. Until then, do not describe the original Figure 1 uncertainty calculation as fully replayable.

## Other intervals and simulation generation

Figures 3 and 4 use preserved original bootstrap arrays to reconstruct their original intervals; this is not a fresh full bootstrap campaign. The September reassessment does perform its separately specified post-hoc resampling. Its numerical estimands and seeds are retained.

All restored circuit code and original records belong to the susceptibility study. Small simulator cross-validation and stored-row reanalysis do not establish a fresh end-to-end repeat of every original simulation campaign. Software dependencies must be installed; no inference requires another research repository or an old chat.
