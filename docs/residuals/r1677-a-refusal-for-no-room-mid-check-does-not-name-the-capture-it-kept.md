---
title: A capture refused because its check's copy found no room keeps an unverified capture the refusal does not name
found: at the review of #813, R-1677, 2026-11-13.
issue: no
---

**The mechanism.** When the throwaway copy runs out of room after the measure
passed, `snapshot.capture` writes the capture's manifest unverified and
refuses as `snapshot-check-temp-full`, naming the temporary directory. The
capture directory, its copy of the database and its unverified manifest stay
in the store, as a capture that failed its check always has. The refusal does
not name it, and on a volume the store shares with the temporary directory
that capture holds part of the room the step asks the person to free.

**Measured cost.** Driven by the review on a 256 KiB tmpfs with the measure
bypassed: the stamp directory with `capture.json` saying not verified and
`master.db` stays, the throwaway is removed. Not a regression: the same
capture was kept, unverified, before this card. Pruning reaches it as any
unverified capture.

**Closes when:** the refusal's detail and message name the capture it kept
and say pruning frees it. Ledger only.
