# Data policy

The repository tracks all canonical data needed to regenerate the six core Python panels, the complete analysis scripts from the final two checkpoints, and the load-bearing derived tables.

The two complete checkpoint packages contain roughly 20 MB of additional compressed raw arrays and state tables. They are preserved in the handover package but are not placed in the first ordinary Git commit. Before public release they should be attached to a versioned GitHub Release or deposited in a research archive, with hashes recorded here.

This avoids hiding the scientific story inside binary archives while keeping ordinary Git history reviewable.