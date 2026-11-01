---
title: crate tag retag reports a genre written onto a file that would not take it
found: at the review of #358, U178, 2026-10-31.
issue: yes
---

**The mechanism.** `tagging/retag.py`, in `retag_one`, calls `tags.write_genre`
and reports the answer as written without reading the writer's return.
`write_genre` answers False rather than raising for a file it could not save, a
locked file or one on a read only volume, so the retag reports the new genre
and the file keeps the old one. U178 found the same shape in `tag folder` and
fixed it there with `tag-folder-unwritten`; `remap.py` and `suggest.py` already
check the return. `retag.py` is the one caller left.

**Measured cost.** Read at the review, not driven. A `crate tag retag` over a
locked file would say the file was retagged while it still carries the coarse
genre, the clean report over a write never performed that the board bar names.

**Closes when:** `retag_one` checks the writer's return and the file's item
fails or is reported unwritten with the file named, with a test that drives a
file refusing the write. Earns an issue: the product says something false
about a write.
