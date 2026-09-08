# Attribution and notation repair

Date: 2026-09-08. Implements audit F-02 and the THEORY portions of F-05b/F-05d.
Only `docs/THEORY.md` and `docs/RELATED_WORK.md` were edited for this component;
the frozen audit files were not changed.

## Changes

- Attributed the local four-purity stencil to Kuo et al., arXiv:1910.11351v2,
  Eqs. (19)/(60), and the Haar cut rule to Akhtar and You,
  arXiv:2006.08797v2, Eq. (20).
- Added a feature-basis/subsystem dictionary, explicit coefficient translation,
  local versus half-chain dimension distinction, and input-purity normalization.
  The surrounding monitored dynamics need not satisfy the fresh probe's local
  scrambling assumption.
- Defined realignment indices and the rescaled entangling-power convention.
  Clarified that the two invariants determine this averaged response, not the
  full local-equivalence class of a gate.
- Replaced hypothetical prior-equivalence wording with confirmed specialization;
  separated the established ingredients, elementary deductions, and monitored
  empirical endpoints without asserting priority.
- Added focused comparisons with measurement-distance entropy loss and
  fixed-Schmidt-orbit channel response, and completed the Lunt et al. title.
- Qualified the existing gate-space supporting paragraph using its actual
  historical estimator: pooled raw-purity shifts, omission of empty cells,
  and marginal intervals. These are not dimension-weighted normalized-response
  intervals or a universal simultaneous probe guarantee. No numbers or
  bootstrap draws were changed.

## Verification actually performed

Primary full texts were reopened and the relevant equations inspected:

| Primary source | Material checked |
|---|---|
| [Kuo et al., v2](https://arxiv.org/html/1910.11351v2) | Eqs. (17), (19), (59), (60); feature labels and local-conjugation ensemble |
| [Akhtar and You, v2](https://arxiv.org/html/2006.08797v2) | Eq. (20), including the local-dimension coefficient |
| [Jonnadula et al., v2](https://arxiv.org/html/1909.08139v2) | Eqs. (15), (16), (18), (31); rescaled entangling power and Cartan convention |
| [Fattal et al., v1](https://arxiv.org/html/quant-ph/0406168v1) | Reduced stabilizer projector and entropy, Eqs. (4)-(6) |
| [Fan et al., v1](https://arxiv.org/html/2002.12385v1) | Eqs. (6)-(7), (13); Figure 4 and Appendix E; endpoint and approximation |
| [Rudziński et al., v2](https://arxiv.org/html/2605.26867v2) | Section VI, Eqs. (86)-(97); checked against the audit's v1 comparison |
| [Lunt et al.](https://arxiv.org/abs/2012.03857) | Full title and author metadata |

The Kuo/Akhtar journal references and DOIs were checked against arXiv landing
metadata. The Rudziński bibliography follows the landing-page singular
“diagnostic”; the HTML heading uses “diagnostics”. No PDF conversion timestamp
was treated as a paper publication date.

Executed from the repository root:

```bash
/workspace/scratch/0174ee249694/audit-venv/bin/python audits/full-sanity-01/code/check_literature_translation.py
git diff --check -- docs/THEORY.md docs/RELATED_WORK.md
```

Both commands exited 0. The exact rational translation passed its three
affine-basis checks, six listed gate cases, and Haar local dimensions 2 through
8. It uses the published transfer formulas and invariant definitions, so this
is algebraic verification, not an independent validation of their physical
premises. Its output is printed, not written over the historical audit output.
The repair-wide reproduction log records any later logged replay separately.

Read the historical gate-space estimator before changing its description.
The numerical table reconstruction and full regression suite are separate
repair components. No broader literature census, new simulator campaign,
manuscript work, or priority certification was performed here.
