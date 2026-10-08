# Editorial policy

The repository uses GitHub's default Markdown presentation. Navigation should connect the scientific question to the result, proof, data, and reproducible calculation without a separate themed website.

Write concrete reader questions, explain quantities before using them, and keep notation consistent. Present the scientific question, definitions, results, evidence and reproduction instructions directly. Keep development chronology in the historical records. State assumptions and limitations where they affect interpretation; avoid repeated inventories of work outside the study. New prose avoids em dashes.

Style editing must not change scientific meaning. Preserve signs, quantifiers, reference populations, confidence-interval definitions, causal qualifications, and attribution. Keep diagnostic spectrum replacement, physical conditional matching, and paired measurement interventions distinct.

Use [GitHub's supported math delimiters](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions). For named operators, write `\mathop{\mathrm{Tr}}\nolimits` (and similarly for other names) to retain upright letters, operator spacing and side subscripts. Avoid `\operatorname`, which GitHub can reject even when a local TeX renderer accepts it; see [github/markup#1688](https://github.com/github/markup/issues/1688). Run `python scripts/check_reader_docs.py --self-test` and `python scripts/check_markdown_math.py --self-test` before submitting reader documentation. The second check covers all tracked Markdown, including historical notes, and flags commands outside the reviewed inventory, legacy delimiters, and unbalanced math/grouping. Use GitHub's protected inline form, for example ``$`S_m`$`` so Markdown preserves TeX underscores and escaped braces. Keep each inline expression on one source line. CI runs both checks; source checks do not replace inspection of rendered pages.

Use fenced `math` blocks for display equations in current reader pages. An equals sign on its own line inside a `$$` block can be interpreted as a [Markdown heading underline](https://github.github.com/gfm/#setext-headings), so a valid equation can appear as a broken title. A `math` fence protects the equation from Markdown parsing and needs no `$$` inside it. Keep intentional section headings and their stable anchors separate from display equations. The documentation check includes a regression for this collision.

The approved [Irises palette](../figures/PALETTE.md) is for figures only. All scientific source pages remain ordinary Markdown.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
