---
title: A file that will not take its genre now stops a sync land at the tag step
found: at the review of #358, U178, 2026-10-31.
issue: no
---

**The mechanism.** Since U178 a file `tag folder` cannot write fails its item
with `tag-folder-unwritten`, so the tagging job ends failed, its resume exits
with the item's cause and no tagging summary, and `crate sync land`'s tail,
which reads the job state, stops at the tag step with the file named. Before
U178 the same file was reported tagged and landed carrying no genre.

**Measured cost.** Driven at the review as far as the job state and the
resume's envelope; the land pass itself was not driven. A person running a
sync pass over a staging folder holding one locked file is stopped at tagging
rather than landing it untagged under a false report. That is the intended
behaviour, the shape `source-missing` already has, and it is recorded so the
stop is not read as a regression.

**Closes when:** nothing to close unless a person wants a pass to land the
rest of the batch past one unwritable file, which would be a card of its own.
Ledger only.
