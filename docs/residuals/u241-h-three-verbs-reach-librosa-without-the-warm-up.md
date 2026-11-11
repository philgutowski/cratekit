---
title: Restamp and calibrate reach librosa without the warm up and compile a kernel of their own, so two of them started together can still damage the cache
found: at the review of #649, U241, 2026-11-11.
issue: no
---

**The mechanism.** Two processes filling numba's kernel cache at once crash
and leave the cache damaged (the review of U241 drove it through two light
workers, five runs in seven). U241 makes every process warm alone under a
lock before its first head, at `detect.analyse_file`. `analyze restamp` and
`analyze calibrate` measure through `energy.features_from_path` instead,
which never asks for the warm up, and that path compiles something the warm
up does not: round two measured eleven cache files written by it on an empty
cache, one of them a second specialisation of `utils._cabs2` that a warmed
cache does not hold. So the two verbs write to the cache even after
`analyze run` has filled it. `analyze vocals` also decodes without the
detector and was measured to write no cache file, so it is not part of this.

**Measured cost.** Not driven: each verb is one process, and no pair of them
was started together. The crash and the damaged cache such a pair could
produce were driven on the `analyze run` path, where the fix now stands.

**Closes when:** the energy extractor asks `analysis.warm.kernels()` before
its first librosa call and the warm up measures energy from a file as well
as from samples, with the coverage test widened to that path. Ledger only.
