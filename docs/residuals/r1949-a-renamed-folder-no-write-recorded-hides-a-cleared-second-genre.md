---
title: A cleared second genre left under a folder renamed in rekordbox reads as matching when no rebuild or resort ever recorded that folder
found: at the review of #999, R-1949, 2026-11-23.
issue: yes
---

**The mechanism.** The convergence check reads a playlist that nothing
derives into by its folder's declared name, or, when the folder's name
declares no bucket, by the bucket a previous write recorded for it. Adoption's
writer (`trees.write_tree_membership` under `adopt apply`) records no node, so
a tree filed only by adoption has no record. A genre folder renamed in
rekordbox there declares no bucket and has none recorded, so a cleared second
genre's track left alone in a playlist under it falls into `foreign`, and
`converge` says `matching`: R-1949's own state, under a rename.

**Measured cost.** Driven at round two with the folder renamed by a row
write standing in for rekordbox: the verb said `matching`, "1 declared
placement(s) all present", left behind empty, `foreign: Loud! Room/High`.
Once a rebuild or resort recorded a playlist in that folder it said
`differing` and named the leftover. The rename itself was not made in
rekordbox, which no cloud session may open.

**Closes when:** the check can tell which bucket an unrecorded renamed folder
under the governed root is (for instance by a record adoption writes, or the
bucket its declared playlists' tracks derive into) and compares its playlists,
or names such a folder as not compared rather than reading matching. An issue:
a clean report over a membership no genre files (the bar's b).
