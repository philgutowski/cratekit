---
title: A kill between analyze run's name claim and its rename leaves a zero byte stub the resume then fails on for good
found: at the review of #555, U223, 2026-11-05.
issue: no
---

**The mechanism.** `_finalize` in `src/cratekit/analysis/cli.py` claims the
headed name with `naming.claim_target`, an exclusive create of a zero byte
file, and then renames the source onto it. A process death between the two
leaves the stub. The resume finds the source still a file, analyses it again,
and fails the item `analysis-write-failed`, "that name is already taken",
against the job's own stub, a permanent cause. Present on main before U223.

**Measured cost.** Driven by the round one reviewer with a kill after
`claim_target`: resume exit 1, the cause not retryable, the stub at 0 bytes
under an audio name. The producer is a hard kill in a window of
microseconds; a Ctrl-C is deferred to the engine's checkpoint and does not
land there.

**Closes when:** the claim is recorded with the intent so a resume can tell
its own stub from another file, or the rename replaces a zero byte stub the
intent names. Ledger only: a SIGKILL in a microsecond window.
