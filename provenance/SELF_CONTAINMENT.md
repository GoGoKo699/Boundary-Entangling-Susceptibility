# Self-containment contract

The checkout is complete only when the root `entanglement-data.zip` has the identity specified by `data/record_bundle_manifest.json`. `python verify.py` enforces this; it does not silently skip missing data.

All current artwork and canonical numerical values are frozen to the accepted `d693b9dda41891d046157f3569b79c3b0d90d2e5` baseline. The only original-fit input relocation is to `results/historical_fit/`. No scientific estimate is replaced during cleanup.

The data container consolidates unchanged source members; it does not regenerate missing observations, substitute rounded tables for raw data, or include manuscript source. Reproduction does not need any old checkpoint ZIP or access to a previous chat.

A local package, a staged pull request, and the merged remote repository are different objects. Completion of one does not establish completion of the others. Remote readiness requires the binary bundle to be present and the repository checks to pass on that exact commit.

See [precise reproducibility limits](../docs/REPRODUCIBILITY_LIMITS.md). Preserved original intervals and fully regenerated intervals are not interchangeable.
