---
title: the Vonking set's job carries no upload_date, so U136's posted day naming cannot rename it
found: at sitting 39, 2026-10-13, reading the two set jobs for U136's attended rename.
issue: no
---

**The mechanism.** U136 reads a set's posted day from the page fields frozen on its job.
The Signal job (`2026-10-10T14:59:24Z-a4b0`) carries `upload_date 20260325` and was
renamed; the Vonking job (`2026-10-09T03:01:03Z-6ad9`, `intake.set`, payload 13,319
bytes) carries no `upload_date` at all, so `naming_day` falls back to the landing day and
nothing names the posted one. U136's brief said the Vonking job "carries the page too";
its payload does not.

**Measured cost.** One INSPIRATION playlist, `10_09_26 Public Service NYC Live at
Vonking 5-26`, keeps the landing day in its name.

**Closes when:** the page is fetched again for that job (or `--posted` names the day) and
the rename runs through U140's verb for the account and by hand in rekordbox.
