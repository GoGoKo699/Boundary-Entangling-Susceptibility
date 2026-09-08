# Website editorial policy

## Scientific authority

The scientific source is the consolidated repository at commit `1059662eb7a8ad8bb3262ff4feddd9d95da71d00`, tree `4157908c3aa8f216c8ad7ffa0764c8a7928cb542`. The preview does not amend that source. Its 200 tracked files are protected by `scientific_baseline.json` and supplied unchanged in the generated source downloads.

The nine main questions and eight appendix groups are taken verbatim from `docs/DIALOGUE_REPORT.md`. The original 32 appendix questions, four captions, mathematical expressions, source-register references, and figure assignments remain. Each extracted block has a source hash in `BUILD.json`.

The scientific claim map distinguishes the finite-system spectrum-replacement diagnostic, conditional comparisons of physical stabilizer states, and paired measurement-location interventions. Those comparisons must not become a single causal estimator through editing.

## Voice source and limits

The reference is My-tone v0.6.1, `GoGoKo699/My-tone`, commit `005873301782c06f21b1c6e73a5ce3b08c630cc4`, file `SKILL.md`, Git blob `7ea3baf71c94ba4943d029787b5ecd82697228a6`. The repository mode emphasizes concrete questions, visible dependencies, operational explanations, readable commands, and file-to-purpose maps. No em dash is introduced in new authored prose.

The style guidance does not authorize changing evidence strength, signs, quantifiers, reference populations, confidence intervals, causality, or attribution. Its private corpus is neither copied nor needed to build this website. Its preservation-check script has not been run in this pass. Instead, canonical scientific documents remain byte-identical, and extracted source text is hash-checked. These mechanical checks do not prove that newly written summaries preserve every nuance.

## New and generated text

| Presentation material | Scientific basis or purpose |
|---|---|
| `content/index.md` | `docs/SCIENTIFIC_STORY.md`, `docs/CLAIM_EVIDENCE_MAP.md`, and their stated boundaries |
| `content/resources.md` | Existing source and reproduction paths; explicitly unfinished editorial and release decisions |
| `figures.json` and generated figure pages | Canonical figure inputs, dialogue questions, methods, figure baseline, and plotting scripts |
| `content/design.md` and `palette.json` | User-requested painting reference and proposed presentation choices, not new scientific conclusions |
| Navigation, search, source details, and file indexes | Build-time views of the included source tree |

The new summaries were checked against the supplied scientific account during preparation. This is author-side editorial work, not an independent scientific or human-editor review. Related-work attribution identified in the prior publication discussion still needs explicit integration into the authoritative source before declaring the project presentation complete.

## Mathematical rendering

MathML is compiled during the build. Only legacy brace-delimited `\\rm` font declarations in mathematical AST nodes are converted into `\\mathrm{...}`. All such transformations are logged in `BUILD.json`; the original TeX expression remains available in the unchanged Markdown download. This is a rendering adjustment, not a regrouping of mathematical terms.

## Figure preview

The accepted figures remain the default in the scientific reading route. The Irises palette appears on a separate review page. Color literals and the default plotting color cycle are changed only in memory. Matrix-label text colors can change to preserve contrast against the new cell colors. Numeric values, normalization, color-scale direction, markers, lines, text, and artist geometry are compared exactly between baseline and preview executions. No new confidence interval, fit, or simulated state is generated.

The original composite layouts include external schematic elements not tracked as Python panels. A complete manuscript-source repository must also resolve those schematic sources without silently recreating or importing an unseen Overleaf layout.

## Before publication

Review the integrated reader route, approve or revise the palette, resolve the remaining schematic-source and attribution items, and decide the reuse license and hosting visibility. A `noindex` instruction is not access control. A public deployment is a separate action and is not enabled by this preview.
