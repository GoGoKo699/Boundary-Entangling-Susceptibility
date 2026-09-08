# Bounded archived-trajectory replay, recorded before execution

This follows initial PLAN item 6 (targeted simulator checks), with a concrete
budget of 27 trajectories, at most n=256 and tau=10. Motivation: the source
bundle contains original state records but omits simulation_manifest.json and
campaign command logs. A known base seed and a configurable simulator alone
do not demonstrate that the recorded trajectories can be regenerated.

Replay 16 primary trajectories (both protocols, four sizes, first trajectory
at p=.20 and final trajectory at p=.34), eight replication trajectories (both
protocols, four sizes, final trajectory at p=.26), and three intervention
pre-states (three sizes, final trajectory at p=.26). Compare all archived cut
entropies, central response fields, measurement counts, window features, late
tripartite features, and the corresponding paired interventions. Also derive
all 84,600 primary/replication/intervention seeds from the documented base
seeds and archived run labels and check collisions.

Expected resource use: a few minutes of one numerical thread, below 500 MB.
If the replay disagrees, preserve the mismatch and do not repair the simulator.
This is source-code replay, sharing the production simulator and gate maps; it
does not replace the separate independent row-space and dense-projector tests.
It does not rerun an entire original campaign or recover missing manifests.
