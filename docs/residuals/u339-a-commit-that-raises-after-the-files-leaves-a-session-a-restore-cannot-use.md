---
title: A tag set commit that raises after the files were written leaves the files' old genre in a session the next run's answer does not name
found: at the review of #988, U339, round one, 2026-11-23.
issue: no
---

**The mechanism.** `tagging/genre_set.py` `apply_set` writes the files inside the session, then the rows' commit. When `rb_writer.commit_guarded` raises, the run ends `internal-error` naming no session, the files carry the new genre and the rows the old one. The next run plans the row only (its file already agrees), keeps no file in its record, and its answer says a restore of its session puts each file's old genre back, which it cannot: the old values are in the first, abandoned session's record.

**Measured cost.** Driven with the commit made to raise: restoring the second session leaves row Melodic House and file Deep House (`planned: 0`); restoring the first puts the files back (`read_back: 2`). The producer was injected; a real commit refusing after files is the guard's own refusal or a disk failure.

**Closes when:** a refusal after the files names the session whose record keeps them and the restore that undoes them, and the success message says "each file's old genre" only when the record kept one, with the injected failure as its test.
