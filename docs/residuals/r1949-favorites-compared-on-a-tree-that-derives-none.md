---
title: A Favorites playlist is compared on a governed tree whose derivation neither files favourites nor names their dimension as not compared
found: at the review of #999, R-1949, 2026-11-23.
issue: no
---

**The mechanism.** `rebuild.with_favorites` derives the genre Favorites
only for the routing tree, and names the dimension as not compared only
there. On any other tree id the check now compares a playlist bearing a
declared Favorites name with nothing declared there, so its members read
`unexpected` though nothing was derived for them.

**Measured cost.** Driven at round one on the test tree id: a Favorites
playlist by hand read `unexpected:deep_house/favorites:1` with no gap
named. One candidate producer was driven and does not reach it:
`cutover.derivation_source` refuses any tree but the two cutover trees, and
the inbox tree refuses at `assert_derivable`, so no shipped verb checks
another tree. Reachability is unmeasured beyond that one candidate.

**Closes when:** the check leaves a playlist signal class out of the newly
compared playlists on any tree `with_favorites` does not derive. Ledger only:
no producer reached.
