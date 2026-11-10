---
title: A saved label sync question's figure past the window has edges no test pins, and an unreadable figure says nothing past the window
found: at the second review round of #646, U238, 2026-11-10.
issue: no
---

**The mechanism.** `sync_cli.Question.from_json` reads `beyond` with
`_count(...) or 0`, so a saved figure that cannot be read (null, a string, a
float) reads as zero and takes a readable split down with it, and the
question then says nothing about releases past the window. The line
predates U238. Beside it, three guards kill nothing alone: the lower clamp
in `sync_cli._past_window`, `_count` refusing a float, and the walk's
`_nothing_check` call carrying the listing (the `--next` path's twin is
pinned).

**Measured cost.** None reachable: round two drove three producers of a
saved question (the branch's `Question.to_json`, `origin/main`'s, and the
record's write and read back) and none writes an unreadable figure. The
walk's nothing new line was driven and says the right count.

**Closes when:** an unreadable saved `beyond` is refused or said as
unread rather than read as zero, and tests pin the lower clamp, a float
split and the walk's nothing new line. Ledger only.
