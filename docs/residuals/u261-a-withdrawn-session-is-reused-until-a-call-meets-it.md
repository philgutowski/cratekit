---
title: A session the provider withdraws in the middle of a process is handed to the next resolve without a request, and the label crawl's discovery search reads its 401 as no credited artists
found: at the review of #690, U261, 2026-11-12, round one.
issue: no
---

**The mechanism.** Since U261 a later resolve of the catalogue or the
account reuses the process's held session after asking the gate and the
keychain, never the provider, as the card chose. A session the provider
withdraws between two resolves, with no call made in between, is handed out
again; the first call over it is answered 401, which `provider_session._watch`
reads and drops the hold, so the resolve after that refuses. The cost lands
on that first call: `tidal_catalogue._credited_by` catches every exception
but the gate's and the client's own authentication error as "one query, not
the session", and the client raises a 401 as its HTTP error, so the
discovery search answers no credited artists. The same swallow meets a
revocation between login and the first search on `main` too.

**Measured cost.** Driven by the review with the real client library over
a fake provider (probes P4 and P5): on the branch one resolve's discovery
searches read a withdrawn session as no credits, where `main` refused that
resolve with `credential-missing`. The producer, the provider withdrawing a
session in the middle of a process, was not driven against the live
account, so its reachability is unmeasured.

**Closes when:** `_credited_by` reads a 401 or 403 as the session and
raises, as the account's `provider_failure` does, so a withdrawn session
refuses the run on its first call whichever resolve handed it out. Ledger
only until the producer is driven.
