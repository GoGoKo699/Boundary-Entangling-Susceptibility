# Public-release preparation

**Status: licenses adopted on the working branch; public release remains pending.** The repository remains private and the PR is unmerged. This page records the release decisions and checks. The owner's licensing approval does not authorize a visibility change or certify security or scientific priority.

The adopted licenses and material scope are in [LICENSE_STATUS.md](../LICENSE_STATUS.md), component boundaries in [third-party notices](../THIRD_PARTY_NOTICES.md), and correction guidance in [CONTRIBUTING.md](../CONTRIBUTING.md). [CITATION.cff](../CITATION.cff) supports citation of the repository and the actual commit used. Its optional personal-email field is omitted; that does not remove email addresses from Git history.

## Decisions before public visibility

| Item | Prepared result and remaining decision |
|---|---|
| License | Completed on the working branch: the owner approved MIT for original software and CC BY 4.0 for original documentation, data and figures, and confirmed authority under Ruge Lin's name. Both permit commercial reuse. See the [adoption record](#license-adoption). |
| What becomes public | Review the history, other branches, pull-request discussions and Actions logs/artifacts as well as the intended main tree. Current-file cleanup alone does not clear these surfaces. See the inventory below. |
| Author identity | Ruge Lin is the confirmed copyright attribution. Review contact information already present in commit metadata for public suitability. Removing an optional CFF email is not history scrubbing. |
| Review and stability | Review the reader-route PR and this preparation separately. Before release, require the existing `test`, `recorded-evidence` and `figure1-uncertainty` checks on the selected commit. The branch endpoint currently reports `main` as unprotected; consider a pull-request/check requirement before accepting public contributions. No settings were changed. |
| Citation and version | Keep the repository citation usable now. Choose a release tag only for an approved commit. Add the real release date and version, and a DOI or preprint reference only after one has actually been issued. No GitHub releases were present at inspection. |
| Figure assets | The owner's authority confirmation covers the included original numerical panels. Disclose the unavailable external editable composite sources and leave those assets out of the release. Their absence does not prevent release of the existing self-contained numerical workflows. |

Licensing consent is a decision to grant reuse rights. Public visibility is a later, separate action after the release scope is approved. If historical material should stay private, first choose a specific preservation and publication approach. Do not assume deleting a branch or removing a current file erases its commits, pull requests or other copies.

## Exposure inventory and limits

Inspected on 2026-09-12: repository identity `GoGoKo699/Boundary-Entangling-Susceptibility`, private; main `20954b2ae96e8a5ea95749475fd6b0724b2d5e6b`; reader-route PR #11 open and unmerged, head `1b262318d244cd2f44536647fd4d94861a7d2b05`, tree `aadcdb9d62900dabf9595172c50172b318d6cfbc`. This preparation starts from that reader-route tree on `docs/public-release-prep-01` and preserves the separate review.

The remote inventory contained 22 branches before this preparation branch, with 19 unique heads. All 22 head trees were listed without truncation. The local checkout is shallow and contained eight reachable commits when inspected. This is not a complete history scan.

In particular, `presentation/repository-preview-2026-09-08` retains 46 paths outside the current main tree, including website/build files, alternative figure exports, screenshots and a preview workflow. Other older branches retain superseded fit/caption paths and migration status records. These remain part of the release-scope decision; their historical labels should not be confused with accepted current results.

GitHub listed 11 pull requests, no standalone issues, five issue comments and 157 workflow runs at the start of preparation. The first 100 run metadata records were retrieved; old logs, artifacts, review comments and the full commit ancestry were not content-reviewed. The repository settings' secret-scanning status and account security settings were not inspected. A clean current-tree screen cannot clear those unreviewed surfaces.

A bounded pattern screen covered the 614 starting tracked files, root ZIP members, their 21 inflated gzip records, readable NPZ members and the eight locally reachable commits. It found no matches for the checked credential patterns (private keys, common service-token formats, credential-bearing URLs and quoted secret assignments). This is not a full secret-scanning or security audit. Path references occur in 76 file/member records, chiefly workspace and temporary paths in provenance and historical logs. The existing author email remains in historical citation and commit metadata. Review their public suitability rather than treating them as newly removed.

Three historical repair-attempt NPZ files could not be opened as ZIP containers and were screened only as raw bytes. Their compressed contents are outside this screen; these protected attempt outputs were left untouched:

<details>
<summary>Historical files with limited content-screen coverage</summary>

- `repairs/full-sanity-01/reproduced_figure1_uncertainty/resamples/all_confirmatory__primary__haar_random_pauli.npz`
- `repairs/full-sanity-01/reproduced_figure1_uncertainty/resamples/eligible_union__independent__haar_z.npz`
- `repairs/full-sanity-01/reproduced_figure1_uncertainty_retry/resamples/eligible_union__primary__floquet_cartan_z.npz`

</details>

GitHub's [visibility documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility#making-a-repository-public) explicitly states that Actions history and logs become public. Review the relevant stored material before changing visibility. Nothing in this preparation deletes history, branches, workflow runs or artifacts.

## Initial preparation checks

The implementation sequence is: inventory the current files and remote release surfaces; prepare the license scope, citation and contribution guidance; validate metadata, navigation and preserved assets; submit a private review PR. Initial SHA-256 hashes of all 614 tracked files were saved before editing. The starting Git tree above is the durable source for comparison.

The root archive has 172 indexed members, including two Python programs. Its bytes and member manifest remain unchanged. All 19 tracked PDFs were inspected for font names with `pdffonts`; only embedded STIXGeneral Regular/Italic subsets were reported. No standalone font files, copied tutorial PDF or manuscript source were identified in this current-tree inventory. These observations establish neither original authorship nor permission.

Validation passed: `CITATION.cff` against the [official CFF 1.2.0 schema](https://github.com/citation-file-format/citation-file-format/blob/1.2.0/schema.json), using Draft 7 validation with format checks; `python scripts/check_reader_docs.py --self-test` for 29 active pages, 515 local links/images and 41 preserved question destinations; `python verify.py` for all 172 source-data members and current panels/inputs; and `git diff --check`. The CFF validator was used in the task environment and is not a new project dependency.

At preparation head `bc8104496cd90380045f0cda1f80cd03b0045e0a`, 610 of the 614 starting tracked files retained their SHA-256 hashes. The four changed files were `CITATION.cff`, `LICENSE_STATUS.md`, README and the documentation check's page list. Three new Markdown pages provided contribution guidance, third-party notices and this record. Scientific code, data, accepted figures, plans and historical records were unchanged. That preparation created no license grant, repository setting, release or DOI. All three existing CI jobs passed at that head. These were static metadata/link and existing integrity checks, not browser, mobile, accessibility or scientific validation. The [reader-route implementation record](reader-route-01/IMPLEMENTATION.md) retains its previous checks.

<a id="license-adoption"></a>
## License adoption

On 2026-09-12 the owner approved the proposed material split and confirmed authority to license the included original material under Ruge Lin's name. The adoption adds root `LICENSE` and `LICENSES/CC-BY-4.0.txt`, updates the current scope, README, contribution and data notices, and declares MIT for software package metadata. It applies on this private working branch; merge and public visibility remain separate actions.

The MIT text comes from the [SPDX license-list-data v3.27.0 template](https://github.com/spdx/license-list-data/blob/v3.27.0/text/MIT.txt), with only its copyright placeholders filled as `2026 Ruge Lin`. The CC BY 4.0 text was downloaded unchanged from [Creative Commons](https://creativecommons.org/licenses/by/4.0/legalcode.txt). The web reader timed out for that URL; direct HTTPS retrieval succeeded. No legal terms were rewritten.

The package retains the existing `setuptools>=68` build floor and uses its supported file-based license metadata. Its distributions include the scope and both legal texts, preserving the separate terms for any bundled research documentation. This does not add dependencies or modify the science. The first adoption commit and final checks are recorded in PR #12.

<a id="after-the-owner-approves-the-scope"></a>
## Remaining release steps

1. Resolve any unwanted historical exposure through an explicitly approved approach. Preserve research provenance and do not silently rewrite it.
2. Review the intended main commit, its documentation route and successful existing checks. Authorize merges separately from publication.
3. Approve the exact repository visibility change. Then inspect the public README, equations, figure paths and citation panel, and publish a versioned release if desired. Archive that release for a DOI only if an archival service has actually been configured.

[Next: license scope](../LICENSE_STATUS.md) · [Return to README](../README.md)
