---
title: The genre row tag set made is named only in its answer's sentence, not in the answer's data or the session record
found: at the review of #1008, R-1967, round one, 2026-11-23.
issue: no
---

**The mechanism.** After an apply that made the genre row, `data.totals` still says `genre_row: "mint"` and gains only `written` and `read_back`; the made id reaches the `set-genre-written` warning's prose and nothing else. The session record's change is `content.genre` with no creation counted, and its detail holds only each file's old genre, so `restore list` and a restore's summary say the session created nothing.

**Measured cost.** Driven by the reviewer through two acts and a restore: the row does go back with the capture, so nothing is lost, and the native landing records no lookup mint either. A session reading the JSON must parse a sentence for the id, and a person reading a restore's summary is not told a lookup row goes with it.

**Closes when:** the applied answer's totals carry the made id (`genre_row` the id, or a `minted` field) and the session record names the creation, with a test reading both. Ledger only.
