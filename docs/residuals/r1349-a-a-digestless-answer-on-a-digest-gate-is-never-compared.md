---
title: A recorded answer with no digest on a digest bound gate is never compared, so a run record from before R-1349 still applies its early answer unshown
found: at the review of #574, R-1349, 2026-11-06.
issue: no
---

**The mechanism.** R-1349 closed the door that wrote such an answer:
`gates.record` now refuses a digest bound gate its run has not reached. The
checking side is unchanged: `Gates.require` compares a recorded digest only
when it is not `None`, so an answer already holding no digest passes whatever
plan the gate reads. Three inputs hold one. A run record written by the verb
installed before R-1349 with an answer given ahead of its gate; that answer
also stays re answerable, since `record` admits a gate that already holds an
answer, and the new answer still binds no offer. And a gate reached with no
digest and left open, or answered, which `record` admits as the brief asks;
an AST walk of the 64 `require` calls in `src` found four that pass neither a
plan nor a digest, all on gates that declare no digest source, so no shipped
verb produces this one today.

**Measured cost.** Driven by round one's review on the organize suite's world
with the account decision written into the run record as the earlier verb
wrote it (no offer, no digest): `run decide` on it again exits 0 with the
digest still `None`, and after the rekordbox answer the resume applied the
account area with no account gate shown, five playlists created, three folders
and six moves. Reachability on the installed copy is unmeasured: it needs a
run left at its first gate with an early answer from before the install.

**Closes when:** `require` treats a recorded answer with no digest on a gate
that declares a digest source, reached with a digest, as stale, showing the
plan the offer was just taken over, so the next decide binds it. Ledger only:
no verb shipped after R-1349 writes the input, and the remaining records age
out under `run retire`.
