---
title: A set's account playlist is tied to its job by name alone, so one made under a name neither the landing nor the job recorded is not found by the rename
found: at the review of #323, R-1017, 2026-10-14.
issue: no
---

**The mechanism.** The outbound ledger keys a set's account playlist by its
name and records no job and no INSPIRATION playlist identifier.
`export set --rename` therefore finds it only under a name it can spell: the
frozen name, a name a landing recorded, or a name the job's page words give.
The backfill makes the account playlist under the INSPIRATION playlist's name
as listed on the day it runs, so a person who renamed the INSPIRATION playlist
between the landing and the backfill, and again later, leaves it under a name
nothing records, and the rename refuses `export-set-rename-unresolved`.

**Measured cost.** Not driven. No such set is known on the live library; the
Signal set was under the landing's name, which R-1017 reads. The refusal
writes nothing and names the hand rename as its remedy.

**Closes when:** the backfill and a named export record the job, or the
INSPIRATION playlist's identifier, on the ledger entry they create, and the
rename resolves by that before any name. Ledger only until a set is found in
this shape.
