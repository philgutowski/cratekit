---
title: A restamp told a run's job decides what it leaves out at its queue, and a calibration refit before its drive does not reopen those files
found: at the review of #996, U344, round one, 2026-11-23.
issue: no
---

**The mechanism.** `scored_in_pass` compares each run report's calibration
fingerprint with the calibration active when the restamp is queued, and the
left out files are frozen on the payload. The worker reads the calibration
again when the job is driven. A refit saved between the queue and the drive
restamps the queued files under the new calibration and leaves the left out
ones at the level the old one gave, with no warning.

**Measured cost.** Driven by the review by hand: `analyze restamp
--scored-by RUN --queue-only`, a refit saved through
`energy.save_calibration`, then the job's `--job` command: the queued file
stamped 1 under the refit, the left out file still 6 where the refit gives
1. The tail queues and drives back to back and replaces a stale tail job, so
only a hand sequence of three steps reaches it; the refit was not made
through `analyze calibrate`.

**Closes when:** the drive compares the calibration it reads with the one
the queue left files out under, and restamps them, or refuses, when they
differ. Ledger only.
