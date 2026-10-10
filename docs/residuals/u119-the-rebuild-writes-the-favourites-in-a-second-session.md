---
title: The rebuild writes the genre Favorites in a second membership session, after the bands and the vocal sub
found: at the review of #276, U119, 2026-10-10, reading where the favourites are derived.
issue: no
---

**The mechanism.** The favourites are derived from the tree, not from the
files, so a favourite the rebuild moves to another folder is in that folder's
Favorites only once the first write has moved it. The rebuild therefore
writes its derived placements first, derives the favourites off the tree it
left, and writes them through the same writer in a second session of their
own, each with its own capture, record and commit.

**Measured cost.** Two captures and two records per rebuilt routing tree
rather than one, driven by `test_the_rebuild_files_a_favourite_into_the_folder_it_moves_it_to`.
A run stopped between the two leaves the bands and the vocal sub written and
the favourites not, which the next rebuild finishes, and the convergence
check reports the gap in between as missing memberships rather than as a
converged tree.

**Closes when:** the membership writer takes two plans in one session, which
R29's one source per run rule does not offer today. Ledger only.
