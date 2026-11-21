---
title: killset.py list piped into head ends in a BrokenPipeError traceback after the lines asked for
found: at the last battery of #854, U297, 2026-11-21, after both review rounds were spent.
issue: no
---

**The mechanism.** `scripts/killset.py list` prints its counts and then one
line per source file, 326 of them on the merged tree, with plain `print`.
When the reader closes the pipe early, `list | head -12`, the next `print`
raises `BrokenPipeError`, nothing in `main` catches it, and Python prints a
traceback on standard error and exits 1. `list --rows`, which prints every
row, does the same. The lines that were asked for are printed whole and
correct before it.

**Measured cost.** Driven once: `scripts/killset.py list | head -12` printed
its count lines and the head of the per file table, then the traceback. Maintainer facing and cosmetic: no count is wrong and no file is
written. A reader who sees the traceback may take the counts for
unreliable, and a shell running under `pipefail` reads the pipeline as
failed. `rows` and `check` print a handful of lines and were not seen to do
it.

**Closes when:** `main` in `scripts/killset.py` ends quietly when its output
is closed, as a filter does, with a test that closes the pipe after one
line. Ledger only.
