---
title: When sync removed gives the deletion pass its first position, landed rows already gone are numbered at the first review and offered, not taken as history
found: at the review of #913, R-1037, round one, a hypothesis the review named and did not drive, 2026-11-21.
issue: no
---

**The mechanism.** `sync.removed` gives the deletion pass its first position
when it has none, so a removal it records is not baselined away (U288). That
position records no sightings, so a landed row removed in rekordbox before it
is first seen by the next `delete review`, at a count past the position, and
offered. R35 takes the removals before a library's first position as history,
and a review that baselines does take them so; a position `sync removed` gave
does not.

**Measured cost.** Not driven. Each such row is a real removal of a Cratekit
landed track, offered at the explicit gate with its proofs, so a person is
asked about a removal older than the position rather than not asked; nothing
is moved without the trash answer.

**Closes when:** `sync removed`'s first position also numbers every absent
landed row as history, or R35 is read as allowing it and GUIDE says so.
Ledger only.
