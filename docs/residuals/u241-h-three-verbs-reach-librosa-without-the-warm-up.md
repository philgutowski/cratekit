---
title: Restamp, calibrate and the vocal rescore reach librosa without the warm up, so two of them started together on a cold cache can still damage it
found: at the review of #649, U241, 2026-11-11.
issue: no
---

**The mechanism.** Two processes filling numba's kernel cache at once crash
and leave the cache damaged (the review of U241 drove it through two light
workers, five runs in seven). U241 makes every process warm alone under a
lock before its first head, at `detect.analyse_file`. Three verbs measure
without going through the detector: `analyze restamp` and `analyze calibrate`
call `energy.features_from_path`, and `analyze vocals` decodes for the model.
Each is one process, so within one command nothing races. Two such commands
started together on a cache that has never been filled are not held apart.

**Measured cost.** Not driven: it needs two commands started within seconds
of each other on a fresh install, before any `analyze run` has filled the
cache. The crash and the damaged cache it would produce were driven on the
`analyze run` path, where the fix now stands.

**Closes when:** the energy extractor and the vocal decoder ask
`analysis.warm.kernels()` before their first librosa call, with the coverage
test widened to their paths. Ledger only.
