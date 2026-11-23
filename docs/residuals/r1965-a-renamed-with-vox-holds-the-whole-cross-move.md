---
title: A renamed with vox or Favorites in the old genre folder now lists the whole move across folders instead of moving the band
found: at the review of #1007, R-1965, round one, 2026-11-23.
issue: no
---

**The mechanism.** `adopt/move.py` `moved_out_of` folds a place beside the band held under another name only (`holds_alongside_unnamed`) into the move's `unnamed`, so the whole move is listed under `held-under-another-name` with the band in `holds`, where main moved the band and left the renamed playlist unmentioned. The writer finds a playlist by its declared name, so it could not remove the renamed one; listing says so rather than moving half.

**Measured cost.** At the engine only (`test_a_derived_class_held_under_another_name_only_is_listed_never_moved`); the reader path through a renamed playlist with a recorded node was not driven end to end. The row stays in both folders' bands until the playlist's name is put back, and the gate names it with its reason; GUIDE says so.

**Closes when:** a renamed place beside the band is either found through its recorded node by the writer, or left behind with the band moved and the leftover named, with a dispatcher drive as its test.
