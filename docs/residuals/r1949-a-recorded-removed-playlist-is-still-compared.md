---
title: A playlist rekordbox removed is still compared when a rebuild recorded it, while one nothing recorded is not
found: at the review of #999, R-1949, 2026-11-23.
issue: no
---

**The mechanism.** R-1949's fix leaves a playlist rekordbox removed out of
the playlists the check compares through their names (`node.removed`), but a
destination a rebuild recorded resolves to its node by identifier whether or
not that node is removed, so a removed recorded playlist with live
memberships still reads `unexpected`. The two paths answer differently for
one state.

**Measured cost.** Driven at round two: a rebuild recorded playlist marked
removed with its memberships live read `unexpected:tech_house/high:1` on the
branch and on the base; with its memberships marked removed too it read
converged on both. The repository's own measurement (the solutions note on
the first removal being a soft delete) found removed memberships inside
removed playlists, so the live state may be the second shape; the first was
not produced by rekordbox here.

**Closes when:** the check treats a removed node the same on both paths, or a
measurement on the live library shows rekordbox never leaves live
memberships in a removed playlist. Ledger only: unmeasured reachability, and
the base's behaviour.
