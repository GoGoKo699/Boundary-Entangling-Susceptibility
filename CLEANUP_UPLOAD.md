# Original-study cleanup: transfer pending

**Do not merge this branch yet.** The scientifically checked replacement files and original data are in the author-side transfer archive. This branch currently contains only the temporary, hash-locked import setup. Main remains unchanged.

## One required upload

Upload **`entanglement-cleanup-transfer.zip`**, without unzipping or renaming it, to the repository root on branch:

`cleanup/entanglement-only-2026-09-08`

Expected ZIP size: 17,373,459 bytes.

SHA-256: `a14638afdf3fbe8a8d71f36f1a61a7a68bea2e85a64f7c89a228b8099f97dd15`.

The branch-only importer checks the complete package hash, every old/new file hash, and all protected panels before applying it. It runs the source tests, figure exports, raw-record point-estimate replay, September reassessment, and small simulator/theorem cross-checks. Only after success does it commit to this branch. It refuses concurrent changes and never force-pushes or writes main.

The final tree retains the indexed root `entanglement-data.zip` (172 original data members) but removes the temporary transfer ZIP, this instruction file, and the one-time import/export helpers. Normal CI remains read-only. No repository is renamed or created, no history is rewritten, and no license or visibility changes are made.

## What the cleanup preserves

All 18 accepted PDF/PNG/SVG files and five canonical CSV tables remain byte-identical. The Figure 4 exponential curve remains removed. All recovered records, maps, design inputs, and necessary old-study scripts are included. No later channel-capacity project source or result is included.

## A limitation that must not be hidden

All ten accepted Figure 1 point estimates reproduce from the original states on the common cross-run support. The accepted interval table and its source manifest are preserved. However, its exact bootstrap seed/resample arrays were not saved in the recovered hybrid figure package. The earlier figure-design resamples differ, including a different primary Clifford support. The cleanup does not relabel those as the accepted resamples or replace the accepted intervals. This limitation remains explicit in `docs/REPRODUCIBILITY_LIMITS.md` and the record-replay output.

Local validation passed 13 tests, 152 core-record comparisons, all 256 tableau/state-vector comparisons, and 100 gate-invariant checks. These are local results, not proof that the remote data transfer is complete. Remote completion requires the upload, successful import, and review of the resulting branch before merge.
