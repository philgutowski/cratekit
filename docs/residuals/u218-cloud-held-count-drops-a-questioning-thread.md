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

**Measured cost.** Driven on the live board on 2026-11-05: four threads
held #526, #532, #533 and #536, #533 having posted a question while it kept
building, and `board.py cloud` printed `Held, 3 of 5` and offered #537. The
same reader also reads such a card `answered` once Phillip's answer lands,
while its thread is still building, and step 1 of the cloud-unit skill would
hand it to a second thread; the skill now says to pass over an `answered`
card whose thread is still writing. No user of the shipped verbs pays: the building project's coordinator counts lanes by
its own running threads (METHOD's cloud lane section, written by U218), and
`CLOUD_LANES` is five against the building project's cap of four, so one
uncounted question still leaves the cap within the lane count.

**Closes when:** the reader keeps a card held while a session that posted a
question is still writing under it, for example a `Progress` comment after the
question read as a hold, with a test, or the coordinator's own count is the
documented source and `board.py cloud` says its held count excludes
questioning threads. Ledger only: maintainer facing.
