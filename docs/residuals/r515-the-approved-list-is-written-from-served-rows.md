---
title: The approved list document is written from the served rows of a short release
found: at the review of #284, R-515, 2026-10-10.
issue: no
---

**The mechanism.** `approved_cli.py` writes the list document from the
rows the provider served, so an accepted release of 12 with 3 withheld
produces a 9 row document that reads as the whole release.

**Measured cost.** Not driven. The document undercounts a short release with
nothing in it saying so.

**Closes when:** the document carries the shortfall beside the rows, or
`label approved` warns over a short release. Ledger only; out of scope per the
watcher's answer on #264.
