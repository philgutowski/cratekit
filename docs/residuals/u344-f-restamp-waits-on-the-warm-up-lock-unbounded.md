---
title: analyze restamp and analyze calibrate now wait on the warm up lock with no bound
found: at round two of the review of #996, U344, 2026-11-23.
issue: no
---

**The mechanism.** Since U344 the energy measure asks `warm.kernels()`
before its first decode, so a restamp or a calibrate takes the warm up's
file lock as `analyze run` already did. `warm.py` says the run's wait is
unbounded; U344 extends that wait to the two verbs.

**Measured cost.** With another process holding the lock for 20 seconds, a
fresh process's first measure took 23.49 s against 4.42 to 4.95 s unheld.
A sleeping holder stood in for a suspended one; a holder that never lets go
would hold the restamp as long.

**Closes when:** the warm up lock is taken with a bound, after which a
process measures unwarmed and says so. Ledger only.
