---
title: A run planned again under its own run reports only the last plan's provider calls
found: at the review of #499, U209, 2026-11-05.
issue: no
---

**The mechanism.** `sync_pair` holds the plan with the calls its plan took,
and the write reports that count under `totals.calls.plan`. When a later
command of the run cannot use the held plan (unreadable, older than thirty
days, made for other pairs) it plans again and holds the new plan with the
new count, so the first plan's calls are in no answer. The reason for the
replan is on that command's gate screen, under `planned again`, and not on
the write's answer when the write was a later command still.

**Measured cost.** Round one drove it with a held file made unreadable before
the second command: the fake counted four plan calls across the run and the
answer said two. The live producer at the person's level, another playlist
named under the same run, was not driven.

**Closes when:** the held document carries the run's running plan count, added
to by each command that plans again. Ledger only: a count in an answer, no
write.
