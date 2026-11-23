---
title: The behaviour capture's clock pin misses a clock bound as a default argument, so two captures of one commit differ
found: at the build of #861, U304, 2026-11-22.
issue: no
---

**The mechanism.** `tests/behaviour/__init__.pin` replaces `time.time` and the other clocks wherever a module holds them by name, but `acquire/isrc_cache.py` (`clock: Callable[[], float] = time.time`) and `core/provider_gate.py` (`clock=time.time`) bound the real function as a default when they were imported, which no patch of a name reaches. Measured: two captures of `c9192091` differed in `isrc_cache.json`'s `asked_at` for every scenario that asks the provider for an ISRC (a tie), and in `provider_gate.json`'s `last_call` and hour buckets for a ceiling stop. Four `sync mark` plans' digests also differed between the two captures, by an input not traced. U304 left those scenarios out of `tests/behaviour/sync_*.py` and says so in their docstrings.

**Measured cost.** None to a person. A card cannot compare a tie, a ceiling stop or those four mark plans base against branch.

**Closes when:** the pin also reaches a clock held as a default (for example by patching the two classes' defaults while the pins are on), the mark digest's moving input is found, and the left out scenarios are added back. The harness is U297's, now #869's or #870's to change. Ledger only.
