---
title: a job a chain drives in under a second never reports running under --progress json
found: at the review of #1082, U963, 2026-11-25.
issue: no
---

**The mechanism.** Under `--progress json` the job watch in
`src/cratekit/cli/progress.py` reads the job off the queue once as the drive
starts, then every `WATCH_SECONDS` (one second) and once after the drive. A
job whose whole drive is shorter than the interval goes from `queued` to its
settled state between two readings, so the stream says `queued` then
`succeeded` and never `running`. The brief asks for at least one event per
state change while a chain waits on a job.

**Measured cost.** Driven by the review at the shipped interval, two items of
0.2 seconds each: `queued`, then `succeeded`. No one is told anything false:
the job's last event is its settled state as the queue holds it, and a job
long enough for an app to show it running (a download, an analysis of a real
pass) is read while it runs. A shorter interval reads the queue more often
for every driven job.

**Closes when:** the engine announces each transition it makes, rather than
the watch sampling it, or the sampling is judged enough. Ledger only:
maintainer facing, nothing is lost or misreported.
