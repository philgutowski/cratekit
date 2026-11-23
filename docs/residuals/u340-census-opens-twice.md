---
title: Every adoption census now opens each routed file twice
found: at the review of #989, U340, 2026-11-23.
issue: no
---

**The mechanism.** `adopt/scan.py`'s `scan_rows` opens a routed file's
container once for its energy and once more for its second genre, where
`rebuild.read_truth` reads both in one open (U250).

**Measured cost.** Measured at round one: 300 routed rows over one FLAC on the
local disk, five repeats each, 0.069 to 0.087 s with the second genre read
against 0.037 to 0.040 s without. Not measured on an external volume, where an
open costs more.

**Closes when:** the census reads energy and second genre in one open. Ledger
only.
