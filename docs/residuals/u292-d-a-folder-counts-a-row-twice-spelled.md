---
title: The needs genre backlog's folder answer counts a row whose row carries the word while tag rows would write another case of it
found: at round two of the review of #849, U292, 2026-11-21.
issue: no
---

**The mechanism.** `word_of` in `tagging/backlog.py` counts a row as filed by a folder of the word's name when its row carries that spelling exactly, even when `tag rows` would write its file's other case of the word over it. Round two drove a library with genre entries for both `Indie Tech` and `indie tech`: the folder claimed 3 rows and filed 2.

**Measured cost.** A folder's row count over by such rows, and the projection with it. Whether rekordbox keeps two genre entries that differ only in case was not measured, so reachability on a real library is unmeasured.

**Closes when:** the count reads the word `tag rows` would write before the row's own word. Ledger only.
