---
title: delete review offers nothing from a session record it cannot read and says nothing on its envelope
found: at the review of #839, U288, round one, 2026-11-21.
issue: no
---

**The mechanism.** `deletion.run._recorded_details` reads the log with
`scan_log` and only logs how many records it could not read, so a removal
whose record is torn or written by a later build is not offered and the gate
shows `offered: 0` with no warning.

**Measured cost.** Driven by round one with a record truncated by hand: offered
0 and no warning; repaired, offered 1. It keeps the file, the safe side. Not
driven: a later readable removal advancing the watermark past the unread one,
which would then never be offered.

**Closes when:** the plan carries the unread count and the gate screen and the
envelope name it. Ledger only.
