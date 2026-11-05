---
title: A copy run made by hand saves its ISRC lookups only if it exports CRATEKIT_ISRC_CACHE_DIR, and the sitting steps do not say so yet
found: at the review of #496, U206, 2026-11-05.
issue: no
---

**The mechanism.** Every copy run since sitting 39 copies the installation
state and redirects `CRATEKIT_STATE_DIR`, which puts the ISRC cache in the
scratch area. `core.rehearsal.redirected` keeps it live by itself; a copy run
by hand keeps it live only by exporting `CRATEKIT_ISRC_CACHE_DIR` to the live
state folder first. `docs/GUIDE.md` and the solutions entry on it say so;
`docs/cutover.md`'s sitting steps and the `crate-sync` skill do not.

**Measured cost.** Driven in process: without the variable a redirected copy
run asks again, with it the copy run asks nothing. Whether the next sitting
exports it is not measurable here. A hand rehearsal of `sync pair` that follows
the old steps pays its lookups twice, the cost #496 was filed for.

**Closes when:** the next attended sitting that rehearses a lookup heavy verb by
hand exports the variable and records its live run's `isrc-lookups` line, and
the sitting steps carry it. Ledger only, since it closes at an attended sitting.
