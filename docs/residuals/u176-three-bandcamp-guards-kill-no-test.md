---
title: Three Bandcamp guards kill no test, the session asked before the library walk, the library view reused, and the stat request trust check
found: at the second review of #357, U176, 2026-10-28.
issue: no
---

**The mechanism.** Mutated alone in memory by the second review, each of these
survives the unit's tests: `_planned` asking the keychain before the library
walk, the queue path seeding `_LIBRARIES` so its worker walks the library
once, and `_prepared` declining to ask the stat endpoint for an untrusted
link. Each is a cost guard or is covered by `fetch` refusing the same link.

**Measured cost.** None measured: the order and the reuse save a library walk,
and the trust check is covered by the one in `fetch`. Maintainer facing.

**Closes when:** a test counts the library walks of one fetch and asserts the
order. Ledger only.
