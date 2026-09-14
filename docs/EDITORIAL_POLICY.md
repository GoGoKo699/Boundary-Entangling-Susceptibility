# Editorial policy

The repository uses GitHub's default Markdown presentation. Navigation should connect the scientific question to the result, proof, data, and reproducible calculation without a separate themed website.

Use GitHub's documented `$...$`, ``$`...`$``, `$$...$$`, or fenced `math` blocks for equations. Keep inline math on one source line. Avoid custom macros and package-dependent commands. Named operators use `\mathop{\mathrm{Tr}}\nolimits` (and the same form for other names), preserving operator spacing and side subscripts without `\operatorname`. Run `python scripts/check_markdown_math.py --self-test` for all Markdown, including historical notes. The check enforces a reviewed command inventory and source syntax; live rendering remains a separate check. See [GitHub's math syntax](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions) and the [reported operator-name rendering issue](https://github.com/github/markup/issues/1688).

Write concrete reader questions, explain quantities before using them, and keep notation consistent. The My-tone repository-mode guidance informed the earlier reader routes; its private corpus is not copied here or needed to use this repository. New prose avoids em dashes.

Style editing must not change scientific meaning. Preserve signs, quantifiers, reference populations, confidence-interval definitions, causal qualifications, and attribution. Keep diagnostic spectrum replacement, physical conditional matching, and paired measurement interventions distinct.

The approved [Irises palette](../figures/PALETTE.md) is for figures only. All scientific source pages remain ordinary Markdown. The manuscript is the final step, after the repository's source and attribution obligations are complete.
