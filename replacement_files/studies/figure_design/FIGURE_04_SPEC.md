> Historical figure-design record. The current accepted artwork is defined in `docs/FIGURE_BASELINE.md` at repository root; the original Figure 4 fit is not endorsed. The earlier Figure 1 statistics differ from the accepted hybrid-panel table.

# Figure 4 Specification — Paired Causal Localization

## Main-text question

**Can one local measurement change the susceptibility without changing the complete central spectrum, and over what distance from the cut does that influence extend?**

## Claim

On the branch where the complete central stabilizer Schmidt spectrum is unchanged, moving one projective-Z measurement toward the central cut causally suppresses the subsequent fresh-gate response. The influence is short-ranged, with a fitted decay length of approximately 2.37 sites.

## Final geometry

- Two-column figure, target size approximately **7.08 in × 3.05 in**.
- Two panels only.
- Panel (a): approximately 68% of the width.
- Panel (b): approximately 32% of the width.

## Panel (a): paired protocol and distance decay

The main plot shows

`Delta chi_rel(d)`

relative to a far measurement for distances

`d = 0, 1, 2, 4, 8, 16`.

Use:

- filled navy circles with 95% trajectory-cluster bootstrap intervals;
- teal fit `-A exp(-d/xi)`;
- annotation `xi = 2.37 [2.25, 2.50]` sites;
- distance axis with explicit ticks `0, 1, 2, 4, 8, 16`.

Add a compact inset showing:

1. copies of the same premeasurement stabilizer state;
2. one projective-Z measurement placed at different distances;
3. selection of branches with `Delta S_m = 0`;
4. the same fresh cross-cut probe applied afterward.

Required logic label:

`Delta S_m = 0  =>  complete central spectrum unchanged`.

Sources:

- `analysis/intervention/fixed_spectrum_distance_decay.csv`;
- `analysis/intervention/fixed_spectrum_distance_decay_fit.json`.

## Panel (b): why spectrum conditioning reverses the sign

Use two bars with 95% intervals:

- unconditional near-minus-far effect: `+0.071407 [0.065481, 0.077315]`;
- unchanged-spectrum effect: `-0.047429 [-0.049435, -0.045452]`.

Source:

- `analysis/intervention/paired_near_far_effects.csv`;
- filter `scope == equal_cell_pooled`, `outcome == D_relative`.

Labels:

- unconditional: “rank reduction adds headroom”;
- unchanged spectrum: “embedding suppresses response”.

Use muted orange for the unconditional positive bar and navy for the fixed-spectrum negative bar. Print both signed values so the conclusion does not depend on color.

## Caption draft

**FIG. 4. A paired location intervention reveals a short-ranged causal mechanism.** (a) Copies of the same premeasurement stabilizer state are measured at different distances from the central cut. On branches with `Delta S_m = 0`, the complete central Schmidt spectrum is unchanged; moving the measurement toward the cut suppresses the subsequent fresh-gate response, with an exponential decay length `xi = 2.37 [2.25, 2.50]` sites. (b) Without spectrum conditioning, a near-cut measurement can lower the central rank and create additional entanglement headroom, producing the opposite sign. The intervention is causal for measurement location on the same pre-state, not for assignment of the long-run monitoring probability.

## Material excluded from Figure 4

- every individual `(n, p)` cell;
- all outcome probabilities;
- branch-frequency tables;
- alternative decay models;
- size-resolved decay lengths;
- transition data.

## Acceptance criteria

- The paired nature of the intervention is visually explicit.
- The unchanged-spectrum implication is stated inside the schematic.
- The distance dependence is legible without a logarithmic-axis explanation.
- The unconditional and fixed-spectrum signs are printed.
- The causal qualification appears in the caption.
