# R-381 mutation notes

Seventeen rows, the author's own, one pass, then a re-measure of two. The
brief's named row, M1, restoring the fold only slug, kills 12.

The first pass left two zeros, both user facing and both a layer that another
layer covers on the tree. M12 drops the display name check when `add` finds an
entry under the old fold. M14 has `marks` follow every recorded move instead of
the live ones, and the writer already drops a move whose old identifier is held.
Each was pinned by a direct test, and `r381-b.md` measures both killed, one
kill each. All seventeen are killed on the final tree, by the author's own
tests; the author found no way to leave one standing.

Dropped: the two fallbacks, `load` returning the stored document when a move
cannot be written and `_follow` answering nothing over an unreadable registry.
Both are maintainer facing and neither has a producer on the tree without a
fault injected into the lock or the file.
