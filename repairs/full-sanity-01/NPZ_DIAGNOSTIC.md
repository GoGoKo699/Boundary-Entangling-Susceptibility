# Figure 1 output-file diagnostic

Two fresh generation attempts returned zero but left incomplete NPZ files.
Their subsequent independent replay and fixed-reference adoption checks
correctly failed. These failures are preserved, not counted as passes. A
third fresh generation followed immediately by both unchanged verification
commands succeeded. No generator, estimator, RNG, observation, canonical
expected hash, or frozen audit file was modified to obtain that result.

## Established observations

The first output directory is `reproduced_figure1_uncertainty/`; the second
is `reproduced_figure1_uncertainty_retry/`, both relative to this directory.
The corresponding logs are `logs/figure1_full.*`, `logs/figure1_replay.*`,
`logs/figure1_replay_final.*`, `logs/figure1_adoption.*`, and the retry logs.

| Attempt | Incomplete NPZ stem | Observed bytes | Complete expected bytes |
|---|---|---:|---:|
| Initial | `eligible_union__independent__haar_z` | 786,728 | 1,499,577 |
| Initial | `all_confirmatory__primary__haar_random_pauli` | 1,488,201 | 1,860,447 |
| Retry | `eligible_union__primary__floquet_cartan_z` | 1,140,198 | 1,859,094 |

Each affected file is an exact proper prefix of its valid counterpart in
the frozen audit's `reproduced_figure1_uncertainty/resamples/` directory.
The incomplete files lack the ZIP end record. Both `numpy.load(path)` and
`numpy.load(io.BytesIO(path.read_bytes()))` raise `BadZipFile`; this is not a
Path-versus-memory parsing difference.

There are two distinct digest records in the unchanged generator:

1. `ANALYSIS_STATUS.json` records each file's digest immediately after its
   `save_arrays` call. For all three affected files, this digest equals the
   complete canonical file's digest.
2. `OUTPUT_SHA256.json` records files again at the end of the entire run. Its
   affected entries equal the incomplete files' later digests.

Thus the run-end self-hash scan passes because it is checking the same
incomplete bytes that its manifest describes. The separately locked expected
hashes and the actual NPZ reader expose the failure. Self-consistency of a
newly written checksum manifest alone does not prove completeness.

Inspection found an ordinary closing `ZipFile` context in `save_arrays`, and
no later generator write to an already completed NPZ path. The files were
not sparse and the filesystem reported approximately 27 GiB free. Process
listing was unavailable in this environment (`ps` reported `fatal library
error, lookup self`), so absence of other processes was not established.
The observations establish changed/truncated file contents between reads,
but do not identify the underlying cause or demonstrate that concurrency,
storage, or the execution interface was responsible.

## Successful fresh verification

`code/verify_figure1_sequence.py` invokes the same three existing commands
sequentially in one job, with a new empty output directory:

- Generation: `reproduced_figure1_uncertainty_sequential/`.
- Independent replay: `figure1_review_verification/independent_replay_sequential.json`.
- Adoption check against the existing locked expected hashes.

`logs/figure1_sequential.json` records exit zero and 29.314854 seconds for the
whole sequence. The replay checked 1,009,814 proposed multiplicity vectors,
1,000,000 retained contrasts, and 1,280 explicit row expansions. Maximum
vector and explicit-expansion error were both 2.220446049250313e-16. The
adoption check also passed.

After that job finished, a separate read-only inspection loaded every array
from all 20 NPZs both by filesystem path and by `BytesIO`: 560 arrays with
each access method. All 20 files were byte-identical to the valid canonical
audit copies, and their immediate, run-end, and fixed-reference digests
agreed. These sequential outputs, not the earlier incomplete outputs, are
the successful repair resampling evidence. The successful retry does not
retroactively erase the earlier failures or establish their root cause.

An additional disposable diagnostic under
`/tmp/figure1_read_diagnostic_eqysjfea` was deliberately interrupted with
exit 130 after learning another fresh sequence had already started. It
completed neither generation nor replay and is not scientific evidence or
an accepted output. No repository file was written by that interrupted run.

## Consequence and scope

The independent reader and fixed expected-output comparison remain necessary
acceptance steps. The complete sequential output reproduces the adopted
calculation without any scientific-source repair. The earlier outputs remain
forensic records only. This diagnosis does not certify the execution
environment against future output-file failures, recover the unknown
historical seed, or add physical trajectories.
