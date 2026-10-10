---
title: A backfill names the playlist for the day it runs, not the day the set landed
found: by the author of U121, 2026-10-09, planning the Vonking backfill.
issue: no
---

**The mechanism.** The form's first word is the naming day,
`batch_name.today()`, and the brief says today. A playlist this product
wrote for a job is named on the landing's session record, and every later
landing and backfill for that job reads the record, checks the row live under
the folder and adds to it under its first name, so a set landed in two parts
on two days is one playlist (the watcher's review of U121). What the record
cannot name is a playlist a PERSON made: the Vonking playlist the author made
by hand on 2026-10-09 is `10_09_26 Public Service NYC Live at Vonking 5-26`,
and a backfill run that day with `--dj "Public Service NYC" --set-name "Live
at Vonking" --set-date 2026-05` finds it live by name and adds only what it
lacks, while a backfill run any later day makes a second playlist beside it.
No flag names the day.

**Measured cost.** For a set whose playlist a person made, or for a set
backfilled after the day it landed with no record of a playlist, a first
word that says when the playlist was made rather than when the set came in,
and for the Vonking set a twin unless run on 2026-10-09. The hand made
playlist is the author's to keep or remove. Driven:
`test_two_landings_of_one_set_on_two_days_make_one_playlist`.

**Closes when:** the author decides whether the first word is the naming
day, the brief's form, or the landing day read off the landing's record, in
which case the backfill gains that read. Ledger only.
