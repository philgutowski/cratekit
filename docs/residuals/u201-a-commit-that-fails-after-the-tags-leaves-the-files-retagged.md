---
title: The mirror-edits write tags each file before the guarded commit, and a commit that then fails leaves the files retagged while the rows and the tree stay as they were
found: at the review of #489, U201, round one, 2026-11-05.
issue: no
---

**The mechanism.** `organize.mirror_edits.write` writes each file's `genre` and
`energylevel`, reads them back, and only then writes the rows and memberships
and calls `rb_writer.commit_guarded`, the order `tag suggest` keeps so the
database never says what a file does not. A commit refused after the tags were
written rolls the database back and leaves the files as written. Routing reads
the file, so the next `route resort` or adoption reads the new genre while
rekordbox still files the track where it was. The next organize plans the same
edit again and writes it whole, since the snapshot was not settled.

**Measured cost.** Driven by the round one reviewer with `commit_guarded`
replaced to raise (scratchpad drive D5): the file reads Tech House at energy 4,
the row and the tree are unchanged, and the next run completes the move. No
product path that fails between the tag write and the commit was driven, so the
reachability is unmeasured.

**Closes when:** the write records each file's previous tags and puts them back
when the commit fails, with a test injecting the failure.
