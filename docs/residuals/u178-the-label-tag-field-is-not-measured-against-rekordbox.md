---
title: The label tag tag folder reads is the one Picard writes, not one measured against rekordbox
found: at the plan of #358, U178, 2026-10-31.
issue: no
---

**The mechanism.** U178 added `label` to `core/tags.FIELDS` on the keys
MusicBrainz Picard writes, the Vorbis `label` comment, the ID3 `TPUB` frame
and a freeform MP4 `LABEL` atom, because nothing in the product wrote a label
tag yet. Which field rekordbox shows in its Label column was not measured, so
a file another tagger labelled under `organization` or `publisher` reads as
carrying no label tag.

**Measured cost.** Not driven. A file read as carrying no label is tagged as
before, or by `--label`, so the cost is a label genre not applied, never a
wrong one.

**Closes when:** U177, which writes the label tag, measures rekordbox's Label
column on a copy as its brief already says, and moves the entry in the field
table if it differs, for the reader and the writer at once. Ledger only, since
U177's brief owns the measurement.
