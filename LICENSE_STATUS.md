# License decision pending

**The following is a proposal for owner review, not an adopted license or a grant of reuse rights.** The repository remains private. Making it public and licensing its contents are separate decisions.

## Proposed scope

Use the unmodified [MIT License](https://opensource.org/license/mit) for original software and [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode.en) for original research documentation, data and figures, to the extent the author holds the relevant rights. These terms apply to different materials; they are not a choice of either license for every file.

| Material | Proposed license and boundary |
|---|---|
| Original Python programs, tests and scripts, wherever located; build, dependency and CI configuration | MIT. Includes source comments, docstrings and executable examples embedded in documentation. |
| Original explanatory Markdown, mathematical exposition, captions, citation metadata and historical prose records | CC BY 4.0, with the code-example exception above. Scientific references retain their attribution. |
| Original numerical tables, spectra, record arrays, manifests and figure artwork, including historical versions present in the approved release tree | CC BY 4.0 for copyright and applicable database rights held by the author. This does not create exclusive rights over mathematical facts or unprotected individual numbers. |
| Members of `entanglement-data.zip` | Apply the same material-based rules to each member. The two Python members under `takeover_review/` are software; the archive is not uniformly CC BY 4.0. Its [member manifest](data/record_bundle_manifest.json) identifies the contents. |
| Third-party components, external papers, dependencies, and embedded font components | Their existing terms continue to apply. See [third-party notices](THIRD_PARTY_NOTICES.md). A repository license does not relicense them. |
| Untracked external schematic or manuscript sources; other branches and content outside the approved release tree | Outside this proposed grant. Availability and ownership cannot be inferred from a reference or a historical filename. |

MIT allows use, modification and redistribution, including commercial use, while requiring retention of its copyright and permission notice. CC BY 4.0 also allows commercial reuse and adaptation; its terms include attribution, a license link and identification of changes. Compliant recipients retain the CC permissions once granted. Neither proposal requires downstream work to use the same license.

The citation in [CITATION.cff](CITATION.cff) supports scholarly credit and reproducibility. Do not add a mandatory paper-citation clause to MIT or require a particular paper citation as an extra CC restriction. Keep research attribution and the licenses' actual notice requirements distinct.

## Owner decision and adoption

The proposed copyright attribution is **Ruge Lin, 2026**, based on the existing author record. Before adoption, confirm that this identifies the appropriate rights holder and that any collaborator, employer, funder or publisher permissions needed for the included material are in place. Git authorship and stored file hashes do not establish that authority.

If approved, place the complete unmodified MIT text with the confirmed copyright notice in root `LICENSE`; add the complete CC BY 4.0 legal text under `LICENSES/CC-BY-4.0.txt`; replace this proposal with an adopted scope notice; and update README, the data-policy license paragraph and software package metadata consistently. Keep the member exceptions and third-party notices. Record the first licensed commit or release so this notice does not imply that every historical branch has been licensed.

The software package should declare its MIT license; the separate research-content scope belongs in this notice. Do not label every repository file with `MIT OR CC-BY-4.0`. Do not add a release date, tag, preprint identifier or DOI until it exists.

[Creative Commons' guidance](https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software) supports using a software license for code and a separate content license for documentation. The standard license texts linked above control once adopted; this explanation does not modify them.

[Next: public-release preparation](docs/PUBLIC_RELEASE.md) · [Return to README](README.md)
