# Review-guided reader route 01

## Starting point and plan

Repository: `GoGoKo699/Boundary-Entangling-Susceptibility`, GitHub ID 1347195921 (private).
Baseline and remote `main` verified on 12 September 2026: `20954b2ae96e8a5ea95749475fd6b0724b2d5e6b`.
Tree: `dacf187350003e43329e3000957e911ba9455519`. Starting checkout clean; no repository AGENTS.md or additional instruction file found. Read `docs/EDITORIAL_POLICY.md`.
Branch `docs/review-guided-reader-route-01` did not exist in the local or remote branch inventory. Created a separate worktree directly from the baseline. Remote main has no newer changes to reconcile. Terminal HTTPS Git has no credential; authenticated GitHub connector is available for publishing.

Before explanatory edits, [BASELINE_SHA256.json](BASELINE_SHA256.json) records SHA-256 for every baseline tracked file. Preserve every baseline file except the explicitly reviewed current explanatory Markdown. Protect all scientific code, data, tables, figure assets, adopted caption text, plans, audits, repairs and provenance records. No science or historical files will be edited.

1. Read the pinned review in full enough to verify the chosen sections, current four-figure account, exact theory, methods, attribution, and repaired status.
2. Adapt README and PROJECT_GUIDE into LEARN, CHECK and REPRODUCE routes. Add one focused TUTORIAL_BRIDGE and a notation translation. Keep the nine main and 32 appendix question destinations.
3. Align the dialogue and figure gallery; give existing summaries distinct roles. Keep proofs, methods, captions and commands in their authoritative homes.
4. Add a small static navigation check, run existing verification/tests, compare protected hashes, and record three author-side reader walkthroughs. Inspect rendered pages only if authenticated tools permit.
5. Make incremental commits, publish the working branch and open an unmerged review PR. No manuscript or new campaign.

## Presentation and sources

My-tone v0.6.1, commit `005873301782c06f21b1c6e73a5ce3b08c630cc4`, read-only repository mode: README, SKILL.md and docs/MODES.md. Presentation guidance only; no corpus copied or dependency introduced. New prose avoids em dashes.

Review: Fisher, Khemani, Nahum and Vijay, *Random Quantum Circuits*, arXiv:2207.14280v1. Full 56-page PDF downloaded from the versioned arXiv URL; web-reader fetch failed but direct PDF retrieval succeeded. PDF section/page checks are in progress. No review PDF, text extraction or figures will be committed.

## Initial checkpoint

The plan and baseline hashes above were saved before reader-facing edits. Implementation and verification are recorded below.

## Implemented route and content ownership

| Page(s) | Role / change |
|---|---|
| [README](../../README.md) | Single entrance: question, bounded answer, LEARN/CHECK/REPRODUCE and four figure jobs. Former figure-by-figure detail remains in the dialogue/gallery rather than a second long entrance. Legacy section anchors retained. |
| [PROJECT_GUIDE](../PROJECT_GUIDE.md) | Review-to-project map, findings versus derivation reading, three source categories, specialist/reproducer routes and current asset readiness. |
| [TUTORIAL_BRIDGE](../TUTORIAL_BRIDGE.md) | One new substantial teaching page, approximately 2,100 words including worked self-checks. Defines the experiment, three averages/selections, response, short Haar specialization, existing four-qubit example, physical matching and empirical boundary. |
| [NOTATION](../NOTATION.md) | Existing conventions retained; one compact review-translation table added. |
| [DIALOGUE_REPORT](../DIALOGUE_REPORT.md), [question map](../DIALOGUE_QUESTION_MAP.md) | Complete four-figure account retained; clearer definitions/transitions, evidence links, 41 direct question links, original headings/anchors and caption paragraphs preserved. Paired panels stack in first/second order for narrow reading. |
| [Figure gallery](../../figures/README.md) | Each figure's question, controlled/varied quantities, endpoint, answer, limit, table, script and caption destination. All six assets unchanged. |
| [REPRODUCTION](../REPRODUCTION.md) | Environment → integrity/tests → redraw → record replay → uncertainty, with optional reassessment/campaign instructions. Existing scientific command flags unchanged; old section anchors preserved. |
| [RELATED_WORK](../RELATED_WORK.md) | Single tutorial reference added and separated from primary attribution. Existing equation-level dictionary, primary references and bounded priority assessment retained. |
| [THEORY](../THEORY.md), [NUMERICAL_METHODS](../NUMERICAL_METHODS.md), [CLAIM_EVIDENCE_MAP](../CLAIM_EVIDENCE_MAP.md) | Authoritative proofs, estimators and claim status retained; route navigation added only. |
| [EVIDENCE_REASSESSMENT](../EVIDENCE_REASSESSMENT.md), [SCOPE_AND_LIMITATIONS](../SCOPE_AND_LIMITATIONS.md), [REPRODUCIBILITY_LIMITS](../REPRODUCIBILITY_LIMITS.md), [FIGURE_BASELINE](../FIGURE_BASELINE.md), [CODE_MAP](../CODE_MAP.md) | Existing substantive content retained; previous/next/return links added. |
| [00_START_HERE](../00_START_HERE.md), [SCIENTIFIC_STORY](../SCIENTIFIC_STORY.md), [RESULTS_AT_A_GLANCE](../RESULTS_AT_A_GLANCE.md), [FAQ](../FAQ.md) | Respectively a redirect, result-chain recap, numerical lookup and short-answer index. Their roles point back to the authoritative routes. |
| [DATA_POLICY](../DATA_POLICY.md), [figure-script README](../../scripts/figures/README.md) | Clarify which archived resamples exist; correct the stale claim that current Figure 4 still contains an exponential. No asset or historical record changed. |
| [check_reader_docs.py](../../scripts/check_reader_docs.py) | Standard-library static link/anchor/image/delimiter and question-destination check, with deliberate failure fixtures. No Git history dependency or site platform. |

Proofs remain in THEORY; comparison and estimator rules in NUMERICAL_METHODS and the adopted Figure 1 recipe; claim status in CLAIM_EVIDENCE_MAP/core_claims.csv; numerical values in canonical tables. Caption authority: FIGURE1_CAPTION for Figure 1, the unchanged dialogue caption paragraphs for Figures 2–3, and FIGURE_BASELINE for Figure 4. Summaries link to these homes. No numerical or statistical item was relocated.

## Verified review source

Full v1 PDF SHA-256: `96f25aef97c564be923d6f78982ff982636dfc8fa3f5ea022419029d153458f5` (56 pages). The root editor and a separate read-only source reviewer inspected the relevant sections and surrounding text, not only the abstract or contents. Verified findings route: §§2.1–2.4, PDF pp.5–11; Clifford part of §3.3.4, pp.27–28; opening of §4.1, p.30; §4.1.1, pp.31–32. Derivation addition: purity/Haar portion of §3.1.3, pp.16–18. Optional motivation only: the deep-measurement paragraph immediately before §4.1.1 on p.31.

Equation checks: Eq.1 p.5 uses natural logarithms; Eqs.9–10 p.9 use alternating single-layer timesteps; Eq.13 p.16 relates purity to Rényi-2 entropy; Eq.14 p.17 is schematic and single-site, not the exact two-site 2/5 update; Eq.27 p.30 describes normalized trajectories. The pairing brackets on p.17 were visually checked because text extraction loses them. The review's replica labels are not our entropy-increment codes. No journal-page references are substituted for v1 PDF pages.

The map separates (a) review background, (b) established primary-attributed machinery explained locally, and (c) project definitions, analysis designs and empirical observations. No susceptibility, code label, estimator, confidence interval or empirical effect is attributed to the review. The primary entanglement-feature attribution repaired before this baseline remains intact.

## Checks actually performed

Environment: Linux, Python 3.12.14; task virtual environment uses preinstalled runtime packages plus the pinned requirements. NumPy 2.3.5, pandas 2.2.3, Matplotlib 3.10.8, SciPy 1.17.0, numba 0.65.1 and statsmodels 0.14.6. Installed `requirements-reproducible.txt` and the editable package. This was not presented as a new clean-environment scientific replication.

| Check | Actual result |
|---|---|
| `python verify.py` | Passed: 172 source-data members and all current panels/inputs verified; full Figure 1 resample output was not checked by this command. |
| `python -m pytest -q` | 63 passed in 12.70 seconds. Existing suite unchanged. |
| `python reproduce.py --core-figures` | Passed: 18 PDF/PNG/SVG files validated in scratch output. Accepted tracked assets untouched. |
| `python scripts/check_reader_docs.py --self-test` | Passed: 25 active pages, 484 local links/images and all 41 baseline question destinations; missing-target, bad-anchor and delimiter fixtures rejected. |
| Snapshot without `.git`; deliberate question-heading mutation | Checker passed without history and rejected the changed heading. Its expected heading/slug fingerprint comes from the actual frozen baseline. |
| Baseline SHA-256 comparison | 588 of 610 baseline files unchanged; the 22 changed baseline files are current explanatory Markdown only. No change under data, results, src, studies, audits, repairs, provenance or analysis_plans. All pre-existing executable code and all accepted figure assets unchanged. |
| Caption/equation comparison | Four dialogue caption paragraphs and all existing dialogue display equations byte-identical. Figure 1 caption file unchanged; Figure 4 adopted caption text unchanged. |
| Semantic source-to-revision review | Root editor and separate read-only reviewers checked definitions, response normalization, complete versus entropy matching, preparation/probe equality, conditioning, coefficient interpretation, seed independence, sign corollary and spatial/size limits. Two scheduling/protocol ambiguities clarified; no new mathematical or evidential inconsistency found in changed passages. |
| `git diff --check` | Passed. New prose contains no em dashes. |
| GitHub browser attempt | Browser was signed out and returned the private repository's 404 page. Rendered GitHub equations/pages/figures and mobile layout were not verified. No visibility or authentication changes made. |

The static checker covers local targets and fragments plus basic delimiters. It is not a TeX renderer, external citation crawler, browser or accessibility validator. Narrow reading was considered through stacked panels and prose/navigation review only. External review-source references were checked against the retrieved PDF; existing scientific citations were retained without a new literature audit.

Local runs did not repeat the full historical simulations, large uncertainty campaigns or prior audit. Existing remote CI may run its normal numerical regression jobs; their commit-specific status is reported in the PR/final handover, not assumed from local results.

## Three author-side walkthroughs

1. **Review-prepared newcomer:** README → PROJECT_GUIDE → bridge → dialogue M1–M9 → gallery. The reader can explain why central eigenvalues fix P_m but not neighboring purities; calculate the existing 4/15 versus 4/5 example; explain nine codes/six values, physical matching and the distinct jobs of all four figures. The derivation's original papers are not extra tutorial prerequisites.
2. **Specialist:** NOTATION → THEORY → CLAIM_EVIDENCE_MAP → NUMERICAL_METHODS → EVIDENCE_REASSESSMENT → REPRODUCIBILITY_LIMITS. Each claim reaches its proof or empirical table, estimator/eligibility rules and limitation. Exact reconstruction is not independent evidence; the conditional rate coefficient and selected paired intervention remain different estimands.
3. **Reproducer:** REPRODUCTION environment/checks → redraw → record replay → current uncertainty → optional campaign recipes. The gallery's five numerical tables and four plotting entry points agree with actual source. The included root bundle supplies required observations and archived arrays; output directories and operation meanings are explicit. No old chat, separate project, My-tone corpus or missing checkpoint ZIP is required.

These are author-side semantic/static walkthroughs, not external user testing or measured comprehension results.

## Remaining genuine gaps and handover

The actual tracked tree and archive member inventory still contain no editable external composite-schematic sources. Six accepted numerical panels and their generators are present. External Overleaf material has not been checked, and no missing schematic was fabricated. Current workflows do not recover historical Figure 1 resamples, historical invocation seeds or every execution manifest. These availability limits remain in their existing authoritative records.

The manuscript remains the final step. No new scientific campaign, manuscript, palette change, hosting, license/visibility change or merge is part of this pass.

Published milestone commits: plan `b369b5c44adcc7611e327ec59bc2002d835c8bad`; reader routes `e25159f0d8d3f77005d364ca4acfdd4aaa31c732`. Authenticated connector publication uses its own commit metadata; each published Git tree was compared exactly with the corresponding local implementation tree. Final checks and this record are a third incremental commit. The review PR is the stopping point.
