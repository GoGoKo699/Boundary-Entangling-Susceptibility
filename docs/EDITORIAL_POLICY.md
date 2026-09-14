# Editorial policy

The repository uses GitHub's default Markdown presentation. Navigation should connect the scientific question to the result, proof, data, and reproducible calculation without a separate themed website.

Write concrete reader questions, explain quantities before using them, and keep notation consistent. The My-tone repository-mode guidance informed the earlier reader routes; its private corpus is not copied here or needed to use this repository. New prose avoids em dashes.

Style editing must not change scientific meaning. Preserve signs, quantifiers, reference populations, confidence-interval definitions, causal qualifications, and attribution. Keep diagnostic spectrum replacement, physical conditional matching, and paired measurement interventions distinct.

Use [GitHub's supported math delimiters](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions). For named operators, write `\mathop{\mathrm{Tr}}\nolimits` (and similarly for other names) to retain upright letters, operator spacing and side subscripts. Avoid `\operatorname`, which GitHub can reject even when a local TeX renderer accepts it; see [github/markup#1688](https://github.com/github/markup/issues/1688). Run `python scripts/check_reader_docs.py --self-test` before submitting reader documentation. CI runs this check; its static macro check does not replace inspection of rendered pages.

The approved [Irises palette](../figures/PALETTE.md) is for figures only. All scientific source pages remain ordinary Markdown. The manuscript is the final step, after the repository's source and attribution obligations are complete.
