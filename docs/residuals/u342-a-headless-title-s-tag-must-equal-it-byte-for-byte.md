---
title: analyze adopt stamps a headless row only when its title tag equals the row's title byte for byte, so three near misses are left as title-tag-differs
found: at review round one of #994, U342, 2026-11-23.
issue: no
---

**The mechanism.** `analysis/head_adopt.py`, `_tag_after`: a title with no
head is stamped only when the file's title tag reads exactly as the row's
title, or already as the stamped title. Anything else is `title-tag-differs`.

**Measured cost.** Driven at review round one, through the landing and the
plan on the suite's disposable library: a file with no title tag lands as
Title `Lima` and is left `title-tag-differs` naming an empty tag; a tag
`[MP3]Tango` lands as Title `[MP3] Tango`, since `intake/ingest.py` renders
the marker again, and is left the same; a stamp stopped after the files and
before the rows (a `KeyboardInterrupt` at the row write) is continued while
rekordbox's answer stands, and left on every later run once the BPM column
moves, where a corrected head would splice the tag's own. Each row is named
and nothing is written or lost; the row keeps having no head until a person
fixes the tag. No producer of a tagless or off spaced marker file upstream of
staging was driven, and the stopped stamp needs a reanalysis between two runs.

**Closes when:** a stamped row compares the tag by its body as a corrected
head does, with a tagless file given the row's title. The trap: a blank
before title tag makes `core/restore_tags.py` `kept_by` refuse the session's
record, so a tagless file must keep a non blank before value or the restore
must learn to clear it. Ledger only.
