---
title: tag set records no folder a row holds only through with vox, Favorites or a genre sub, so adopt move never asks it
found: at the review of #1007, R-1965, round one, 2026-11-23.
issue: no
---

**The mechanism.** `tagging/genre_set.py` `_leaves` records a genre folder as left only when the row holds a competing sub there (`Placements.holds`), while the move across genre folders (`adopt/move.py` `leaving_moved`) now also leaves the places beside the band, `with vox`, Favorites and a genre sub. A row whose band in its old folder was taken out by hand, but which still sits in that folder's `with vox` or Favorites, is never recorded by `tag set`, so `adopt move` plans and lists nothing for it.

**Measured cost.** Driven in review round one with the band removed by `rb_writer.remove_memberships` by hand, not by a verb, before `tag set`: the row ended in both folders' `with vox` and Favorites, `adopt move` planned and listed nothing, and `converge` read matching. No verb was driven that produces the state, so reachability is unmeasured. When the band goes after `tag set` recorded the entry, the move is correct (driven).

**Closes when:** `_leaves` asks the same places the move leaves (`holds` and `holds_alongside`, through one predicate the move shares), with a test that records and moves such a row.
