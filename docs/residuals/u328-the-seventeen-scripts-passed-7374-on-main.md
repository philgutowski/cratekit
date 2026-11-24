---
title: The seventeen scripts of U330 passed 7,374 lines on main, by the privacy scan's host forms
found: at the last merge of main into #977, U328, 2026-11-24.
issue: no
---

**The mechanism.** Point 6 of #847, U290, holds `scripts/` to the standard
U330 (#979) set: the seventeen scripts its brief names total at most 7,374
lines. U330 left them at 7,360. U957 (#1025) landed `scripts/scan_repo.py`'s
host and path forms for an ordinary word, 164 lines, and nothing in the
battery holds the total, so it passed the bar under a green suite.

**Measured cost.** `wc -l` over the seventeen files the brief of #979 lists:
7,327 at `e0573a66` and 7,443 at `c5fb1015`, both on 2026-11-24, 69 over.
U328 adds 1, in `scripts/board.py`, so its merged head reads 7,444. No file
in `scripts/` is over 1,500 lines. None to a person using a verb.

**Closes when:** the audit card of #847, #987 (U338), measures point 6 again
and files a further card for the total, or Phillip moves the bar for the
scan's new forms. Ledger only: a maintainer facing count.
