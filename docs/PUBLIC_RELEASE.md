# Public-release preparation

**Status: release preparation and the available-history exposure review are complete. No blocking disclosure was identified in the reviewed material.** Licenses are adopted on the working branch. The repository remains private, with the reader-route and release PRs awaiting author review and merge. This page records the scope, findings and remaining publication actions.

The adopted licenses and material scope are in [LICENSE_STATUS.md](../LICENSE_STATUS.md), component boundaries in [third-party notices](../THIRD_PARTY_NOTICES.md), and correction guidance in [CONTRIBUTING.md](../CONTRIBUTING.md). [CITATION.cff](../CITATION.cff) supports citation of the repository and the actual commit used. Its optional personal-email field is omitted; that does not remove email addresses from Git history.

## Decisions before public visibility

| Item | Prepared result and remaining decision |
|---|---|
| License | Completed on the working branch: the owner approved MIT for original software and CC BY 4.0 for original documentation, data and figures, and confirmed authority under Ruge Lin's name. Both permit commercial reuse. See the [adoption record](#license-adoption). |
| What becomes public | Reviewed the available Git ancestry and other branches, all current pull-request discussions, and all retained Actions logs/artifacts in the pinned snapshot below. Historical previews and superseded development records remain visible as history. |
| Author identity | Ruge Lin is the confirmed copyright attribution. The existing author email remains in historical citation files, Git author/committer metadata, Actions run metadata and copies of old source files in artifacts. It was not removed from history. |
| Review and stability | Review the reader-route PR and this preparation separately. Before release, require the existing `test`, `recorded-evidence` and `figure1-uncertainty` checks on the selected commit. The branch endpoint currently reports `main` as unprotected; consider a pull-request/check requirement before accepting public contributions. No settings were changed. |
| Citation and version | Keep the repository citation usable now. Choose a release tag only for an approved commit. Add the real release date and version, and a DOI or preprint reference only after one has actually been issued. No GitHub releases were present at inspection. |
| Figure assets | The owner's authority confirmation covers the included original numerical panels. Disclose the unavailable external editable composite sources and leave those assets out of the release. Their absence does not prevent release of the existing self-contained numerical workflows. |

Licensing consent grants reuse rights. The author reserved review of the reading route and the later publication decision. No history, branch, discussion, workflow run or artifact was deleted during preparation.

## Exposure inventory and limits

Inspected on 2026-09-12: repository `GoGoKo699/Boundary-Entangling-Susceptibility`, private; main `20954b2ae96e8a5ea95749475fd6b0724b2d5e6b`; reader-route PR #11 head `1b262318d244cd2f44536647fd4d94861a7d2b05`; release-preparation PR #12 head `69e3670fe197ebf23c8a9cbee844ce2b3058416a`, tree `f0fff20658467618edf08c5585d8866567888aeb`. Both PRs were open and unmerged. The compact [coverage record](release-prep-01/EXPOSURE_REVIEW.json) pins the refs, inventory digests and retrieval limits.

The initial current-tree check below was limited by a shallow checkout. The follow-up used GitHub's complete reachable commit graph and retrieved every distinct blob, closing that ancestry and content-coverage gap without rewriting the checkout's history.

| Surface | Completed coverage at the snapshot |
|---|---|
| Git history | All 37 listed refs: 23 branches, 12 PR heads and two PR merge refs; no tags. Their ancestry contains 122 distinct commits, 106 distinct commit-root trees (recursively listed) and 742 blobs. All parents were accounted for, no tree listing was truncated, and every blob's Git hash and size were verified. All commit messages and author/committer entries were read. |
| Historical file contents | Credential/contact/path screening of all blobs, recursive ZIP/gzip content and 21 PDF text extractions, with contextual reading of flagged text and historical presentation/provenance changes. Three encoded transfer payloads were decoded and hash-checked without executing their programs. |
| Discussions | All 12 PR bodies and five issue comments were read. There were no standalone issues, review submissions or inline review comments. Collection pagination was exhausted. |
| Actions logs | All 165 runs through run `34679287903`, including 166 attempts and 265 jobs. All 265 job logs were retrieved and screened, with relevant context inspected: 115,967 lines and 11,359,977 characters. No log was unavailable. |
| Actions artifacts | All 175 retained artifacts across those runs were downloaded: 1,587,247,013 bytes. Every size and GitHub SHA-256 digest matched. Recursive inspection covered 33,171 member occurrences and 1,135 distinct payloads, including nested source TARs, numeric arrays, PDF text/fonts and image metadata. No artifact or nested-container parse errors remained. |
| Stored screenshots | Three distinct historical website screenshots, also present in five preview artifacts, were visually inspected. They showed project pages without visible private content. This is inspection of stored history, not validation of today's GitHub rendering. |

No unmasked credential, credential-bearing download URL, private conversation payload or copied private style corpus was identified in the covered material. Masked Actions authentication entries remained masked. The existing author email and ordinary workspace paths remain in historical metadata and source/provenance copies. The scope is a bounded pattern screen and contextual inspection, not a security certification or a new scientific audit.

The branch `presentation/repository-preview-2026-09-08` retains 46 paths absent from current main, including website/build files, alternative figure exports and screenshots. Those files and the retained preview artifacts were inspected. They are historical presentation material; the current README and accepted figure gallery remain the scientific entrance. Older fit labels, captions and failed repair attempts likewise remain historical records.

Three historical repair-attempt NPZ files lack their ZIP central directories. The follow-up read their 58 existing local numeric-array streams, checked stream completion and CRCs, and accounted for all bytes. This closes the earlier compressed-content inspection gap. It does not repair the files, recover missing historical resamples or change their scientific status. Their original bytes remain unchanged; paths and coverage are recorded in the JSON above.

The review covers available material at the pinned snapshot. Deleted/unreachable commits, deleted or earlier edited discussion versions, expired/deleted artifacts, account security settings and secret values were not available or queried. Numerical images received text/metadata/raw-byte checks as applicable, not OCR or a new visual scientific audit. These limits do not leave a known blocking disclosure unresolved in the reviewed material.

GitHub's [visibility documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility#making-a-repository-public) explains that Actions history and logs become public. This review therefore included those retained surfaces as well as the intended main tree.

For this follow-up, hashes of all 619 starting tracked files were saved before editing. Only this readiness page changed, and one compact coverage JSON was added. All 618 other files, including scientific code, tables, accepted figures, analysis plans and historical records, retain their hashes. The reader/navigation self-test, existing data-integrity verification and whitespace check were rerun; the updated PR carries the actual CI status. No archived program was executed for exposure inspection.

## Initial preparation checks

The implementation sequence is: inventory the current files and remote release surfaces; prepare the license scope, citation and contribution guidance; validate metadata, navigation and preserved assets; submit a private review PR. Initial SHA-256 hashes of all 614 tracked files were saved before editing. The initial reader-route commit `1b262318d244cd2f44536647fd4d94861a7d2b05`, tree `aadcdb9d62900dabf9595172c50172b318d6cfbc`, is the durable source for that comparison.

The root archive has 172 indexed members, including two Python programs. Its bytes and member manifest remain unchanged. All 19 tracked PDFs were inspected for font names with `pdffonts`; only embedded STIXGeneral Regular/Italic subsets were reported. No standalone font files, copied tutorial PDF or manuscript source were identified in this current-tree inventory. These observations establish neither original authorship nor permission.

Validation passed: `CITATION.cff` against the [official CFF 1.2.0 schema](https://github.com/citation-file-format/citation-file-format/blob/1.2.0/schema.json), using Draft 7 validation with format checks; `python scripts/check_reader_docs.py --self-test` for 29 active pages, 515 local links/images and 41 preserved question destinations; `python verify.py` for all 172 source-data members and current panels/inputs; and `git diff --check`. The CFF validator was used in the task environment and is not a new project dependency.

At preparation head `bc8104496cd90380045f0cda1f80cd03b0045e0a`, 610 of the 614 starting tracked files retained their SHA-256 hashes. The four changed files were `CITATION.cff`, `LICENSE_STATUS.md`, README and the documentation check's page list. Three new Markdown pages provided contribution guidance, third-party notices and this record. Scientific code, data, accepted figures, plans and historical records were unchanged. That preparation created no license grant, repository setting, release or DOI. All three existing CI jobs passed at that head. These were static metadata/link and existing integrity checks, not browser, mobile, accessibility or scientific validation. The [reader-route implementation record](reader-route-01/IMPLEMENTATION.md) retains its previous checks.

<a id="license-adoption"></a>
## License adoption

On 2026-09-12 the owner approved the proposed material split and confirmed authority to license the included original material under Ruge Lin's name. The adoption adds root `LICENSE` and `LICENSES/CC-BY-4.0.txt`, updates the current scope, README, contribution and data notices, and declares MIT for software package metadata. It applies on this private working branch; merge and public visibility remain separate actions.

The MIT text comes from the [SPDX license-list-data v3.27.0 template](https://github.com/spdx/license-list-data/blob/v3.27.0/text/MIT.txt), with only its copyright placeholders filled as `2026 Ruge Lin`. The CC BY 4.0 text was downloaded unchanged from [Creative Commons](https://creativecommons.org/licenses/by/4.0/legalcode.txt). The web reader timed out for that URL; direct HTTPS retrieval succeeded. No legal terms were rewritten.

The first licensed snapshot is [8a042014cbfea55ef8cc7781181f451a06455e47](https://github.com/GoGoKo699/Boundary-Entangling-Susceptibility/commit/8a042014cbfea55ef8cc7781181f451a06455e47), a direct child of preparation head `bc8104496cd90380045f0cda1f80cd03b0045e0a`. It is available in [PR #12](https://github.com/GoGoKo699/Boundary-Entangling-Susceptibility/pull/12). The remote adoption tree exactly matched the locally validated tree.

The package retains the existing `setuptools>=68` build floor and uses its supported file-based license metadata. A wheel and source distribution were built in a temporary source copy with setuptools 84.0.0. Both contain byte-identical copies of the MIT and CC texts, scope and third-party notices; the source distribution's included README retains the separate content license. No package was published and no dependency was added.

Adoption checks passed: MIT matches the SPDX template with only the copyright placeholders filled; CC text matches the 18,657-byte direct download (SHA-256 `9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411`); the reader check covers 29 pages, 523 local links/images and 41 original question destinations; `verify.py` validates 172 data members and the current panels/inputs; and `git diff --check` is clean. Of 617 files at the preparation head, 610 retain their hashes. Seven current notice/documentation/package-metadata files changed and two license texts were added. Scientific code, data, accepted figures and historical records remain unchanged. The existing CI jobs run on the updated PR; their current status is reported there.

<a id="after-the-owner-approves-the-scope"></a>
## Remaining release steps

1. Review and approve [reader-route PR #11](https://github.com/GoGoKo699/Boundary-Entangling-Susceptibility/pull/11), then [release-preparation PR #12](https://github.com/GoGoKo699/Boundary-Entangling-Susceptibility/pull/12), which is stacked on it. Check the existing CI results on the commit selected for main before merging.
2. Approve the repository visibility change, with the known author-email and historical-preview exposure described above. The available-history review found no additional blocking cleanup to perform.
3. After publication, inspect the public README, equations, figure paths and citation panel. A versioned release and archival DOI are optional later actions. The unavailable external editable composite sources remain an explicitly excluded asset-completion gap; the included numerical workflows do not depend on them.

[Next: license scope](../LICENSE_STATUS.md) · [Return to README](../README.md)
