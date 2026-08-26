# Checkpoint 05 paired measurement-location intervention lock

This file was frozen before the intervention simulation began. The design was
already prespecified in the primary scaling lock; this file records the exact
execution parameters.

## Question

At the same pre-measurement stabilizer state and measurement count, does one
projective Z measurement change the relative boundary susceptibility more when
it is adjacent to the central cut than when it is far from the cut?

## Simulation

- open monitored Clifford chain, projective-Z protocol;
- sizes n = 64, 128, 256;
- monitoring probabilities p = 0.20, 0.26, 0.34;
- 600 independent trajectories per (n,p) cell;
- probe time tau = 10;
- base seed 2026082501;
- one counterfactual projective-Z measurement at distances
  d = 0,1,2,4,8,16,32,64 on both sides where the site exists.

## Primary paired endpoint

For every pre-state, average the left/right interventions at d=0 that leave
S_m unchanged and separately average all valid interventions with d >= n/4
that leave S_m unchanged. Retain a trajectory only when both averages exist.
The primary response is

    D_i = mean(delta chi_rel at d=0 | delta S_m=0)
          - mean(delta chi_rel at d>=n/4 | delta S_m=0).

A negative mean D indicates stronger near-cut suppression. Uncertainty is a
trajectory bootstrap within each (n,p) cell. Pooled estimates use equal cell
weight. Unconditional paired estimates are secondary.

## Reporting rule

This intervention identifies the causal effect of measurement location on the
next-gate response for the sampled pre-states. It does not by itself identify
the effect of assigning a long-run monitoring probability.
