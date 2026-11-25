---
title: crate sync night under --progress json writes only its end, none of its nested pass's steps or jobs
found: at the review of #1082, U963, 2026-11-25.
issue: no
---

**The mechanism.** `sync night` runs its nested `sync land` through
`tail.dispatch`, which calls the dispatcher with `--output json` and no
`--progress`, and keeps the child's standard error in memory. So under
`crate --output json --progress json sync night` the pass's fifteen or so
child commands write no event, and the stream is one `end`. Human output of
`sync night` shows none of the pass's steps either, so the flag matches it.

**Measured cost.** Driven by the review in process over the suite's fakes:
fifteen child commands ran and the only event was `end`. No producer asks
for it: the scheduled night's command, `schedule.py`'s `NIGHT_ARGV`, passes
no flag, and the menu bar app's Sync (U967) runs `sync land`, which streams.
The guide says to follow a pass with `sync land`.

**Closes when:** a card has the app follow a night pass, which hands the
night's writer to its nested pass as `run decide --continue` does, or the
night is judged to need no stream. Ledger only: nothing is misreported, and
no workflow is blocked.
