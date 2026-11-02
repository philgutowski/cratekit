---
title: A landing planned before midnight and answered after it goes stale on the account playlists' date, and the refusal does not say the date moved
found: at the review of #356, U175, 2026-11-01.
issue: no
---

**The mechanism.** Since U175 each account playlist's INBOX name carries the
landing's date, read from `batch_name.today` when the plan is built. The
landing's two acts each build the plan, so a gate asked before midnight and
answered after it plans names with the next day's date, the digest moves, and
the second act refuses `decision-stale` with nothing written. A batch named
by `--name` used to survive midnight, since only the default batch name was
dated; now the account playlists move it too.

**Measured cost.** Driven by Fable's round 1 on both media, with and without
`--name`: exit 11, nothing written, INBOX empty. The person answers the gate
once more, and the refusal says the plan changed without saying it was the
date. No data is at risk.

**Closes when:** the date is frozen on the run with the plan (as the account
mirror freezes its plan, R-1031), or the stale refusal names a date that
moved. Ledger only: a repeated gate is a wording and convenience cost.
