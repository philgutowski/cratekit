---
title: A file whose first genre value is empty reads as carrying none, so a guess replaces the genre it holds second
found: at the review of #353, U172, 2026-11-01.
issue: no
---

**The mechanism.** `tagging.rows._file_word` answers the first non empty value of the joined text on ID3 but the first value as it came on a FLAC whose genre list is `["", "Deep House"]`, so `tag guess` reads the file as blank, makes it a candidate, and `tags.write_genre` replaces the whole list with the guessed word. `tag folder` reads the same way through `read_genre_from_file`, so the behaviour is inherited from it and not new.

**Measured cost.** Driven by the round 1 review with a list written by mutagen directly: the second value is lost. The producer is unmeasured: zero candidates in this repository were driven that write an empty first genre value, and nothing in Cratekit does.

**Closes when:** the readers take the first non empty value on every container, or a file whose genre list holds a word anywhere is read as carrying one. Ledger only: no shipped verb produces the input.
