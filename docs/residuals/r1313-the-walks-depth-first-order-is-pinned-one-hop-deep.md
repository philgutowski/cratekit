---
title: The walk's depth first order off the declared chain is pinned one hop deep only
found: at round two of #561's review, R-1313, 2026-11-06.
issue: no
---

**The mechanism.** Round one's fix made `core.cause.failure_links` take a
context reached link's own cause before what it was raised while handling,
depth first, so `nearest_status` reads what a wrapper says it is first. Depth
first also takes that cause's own context before the wrapper's context: a
wrapper raised from a status-less error, itself raised while handling a 404
page, while the wrapper was handling a 503 page, reads the 404 three hops out
before the 503 two hops out.

**Measured cost.** Driven by the review: that shape reads `nearest_status`
404, and a breadth first walk patched into every copy reads 503 and passes all
89 tests of the two body files, so the order past one hop is unpinned. No
producer: it needs a status-less failure raised while handling a provider
answer, and the handler grep of round one found none.

**Closes when:** a test pins which of the two the walk takes, with the order
chosen on a reason the docstring gives. Ledger only: no producer.
