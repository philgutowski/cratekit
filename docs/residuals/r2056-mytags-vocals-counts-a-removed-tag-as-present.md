---
title: metadata mytags-vocals counts a vox association marked removed as already present, so it never tags that row again
found: at the review of #1061, R-2056, 2026-11-24.
issue: no
---

**The mechanism.** `rb_nodes.add_my_tag` asks `get_my_tag_songs(MyTagID, ContentID).first()` and reads no soft delete marker, so an association marked `rb_local_deleted` counts as present and `apply_mytags` reports the row `already`. `write.vox_tag.vox_tagged`, the reader every vocal filing path now asks, reads the marker and calls that row untagged (R-758). So a row whose file clears the cut and whose association is marked removed is named `untagged` by `converge` and is never tagged by the write that settles the rest.

**Measured cost.** Driven by the review on a disposable database: a row tagged, its association marked removed, then `apply_mytags` over it wrote 0, already 1, and the next rebuild still read `untagged`. R-2056's remedy text was reworded to send such a row to rekordbox. Whether rekordbox itself leaves a removed association as a soft delete is unmeasured (as R-843 says for the category), so whether a live row reaches this is not known.

**Closes when:** an attended read says whether rekordbox soft deletes a My Tag association it takes off; if it does, the writer reads the marker as the reader does. Ledger only: it closes at an attended sitting, and the product's text no longer claims the write settles it.
