---
title: Two rows recording one file, both named to tag set, end refused as if the file had changed by another hand
found: at the review of #988, U339, round one, 2026-11-23.
issue: no
---

**The mechanism.** `write_files` in `tagging/genre_set.py` reads each file again before writing it and leaves one no longer carrying the word the plan read. Two rows recording one file both plan the same file; the first write changes it, so the second row is listed as moved and the run ends `tag-set-unwritten`, "no longer carry the genre the plan read", when the verb's own first write is the cause.

**Measured cost.** Driven with two rows seeded on one file: the file and the first row carry the genre, the second row keeps its old one, and the refusal's reason names the wrong cause. A second run writes the second row. Two rows on one file is a duplicate the collection should not hold.

**Closes when:** the plan lists a second row on a file already named as `file-shared` (or writes the file once for both), with the seeded pair as its test.
