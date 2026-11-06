---
title: A mirror download driven to its end outside a pass is taken by no pass, and its track is never listed or downloaded
found: at the plan of #579, U227, 2026-11-06.
issue: no
---

**The mechanism.** A sync pass takes a download `crate organize` queued for an
account edit only while the job is QUEUED and carries no run
(`cli.sync_land._take_mirror_downloads`). Until U227 the left open row told
the person to drive such a job by hand with `crate intake playlist ... --job`.
A job driven that way ends SUCCEEDED with no run. `intake missing --run`
lists only the jobs of a run, so no pass lists its missing track. The
downloads step keeps naming the track as awaiting its landing.

**Measured cost.** Not driven. Since U227 the left open row names the next
new pass as the way on, so no new job reaches the state through the product's
own advice. A job driven by hand before U227 may still be in it. Sitting 85's
job `2026-11-06T15:02:36Z-40b0` was left queued, so it is not in that state.

**Closes when:** a pass also takes a succeeded mirror job with no run whose
tracks the library still lacks, listing them afresh, or the downloads step
names such a job with the command that frees it (`crate job retry`). Ledger
only.
