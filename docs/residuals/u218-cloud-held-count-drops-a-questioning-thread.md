---
title: board.py cloud stops counting a card as held once its thread posts a question for Phillip, though the thread keeps building
found: at the build of #536, U218, 2026-11-05.
issue: no
---

**The mechanism.** `cloud_state` in `scripts/board.py` reads a card whose
session's last stated comment is `Question for Phillip` (or `Brainstorm`) as
`waiting-on-phillip`, and `cmd_cloud` counts only `underway` cards against
`CLOUD_LANES`. Since Phillip's rules of 2026-11-04 a question does not stop
the build: the thread makes the conservative call and keeps going, posting
`Progress` notes that the reader skips when it picks the stated heading. So
the queue prints one lane fewer held than there are threads building, and a
session reading the queue alone would start a thread the cap has no room for.

**Measured cost.** Read from the code, not driven on the board. No user of
the shipped verbs pays: the building project's coordinator counts lanes by
its own running threads (METHOD's cloud lane section, written by U218), and
`CLOUD_LANES` is five against the building project's cap of four, so one
uncounted question still leaves the cap within the lane count.

**Closes when:** the reader keeps a card held while a session that posted a
question is still writing under it, for example a `Progress` comment after the
question read as a hold, with a test, or the coordinator's own count is the
documented source and `board.py cloud` says its held count excludes
questioning threads. Ledger only: maintainer facing.
