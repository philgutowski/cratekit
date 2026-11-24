---
title: A record binding a destination to a node that is gone stops adopt apply recording the node it just filed into
found: at the review of #1022, R-1991, 2026-11-23.
issue: no
---

**The mechanism.** `convergence.record_nodes(keep_recorded=True)` never moves
a destination the record already binds, so when that binding names a
playlist rekordbox deleted, the node `adopt apply` files into instead is not
recorded. After a rename of that folder the check cannot tie it to a genre.

**Measured cost.** Driven at round one with a record naming a missing node:
`converge` says `not-compared:Loud! Room/High` over a folder `adopt apply`
filed into. Honest, and giving the folder back its name ends it.

**Closes when:** keep recorded replaces a binding whose node no longer
exists under the root. Ledger only.
