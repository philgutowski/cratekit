---
title: A capture that cannot be flushed exits as an internal error while its remedy says to check the library drive
found: at the review of #701, U272, 2026-11-13.
issue: no
---

**The mechanism.** A flush failure refuses with `snapshot-integrity-failed`,
the slug the commit gate already refuses an unverified capture with, so the
two refusals of one capture read alike. `cause.REASONS` maps that slug to the
internal band ("an unexpected failure"), while the flush refusal's remedy is
`mount-library-volume`, so a pulled drive mid capture reports as an internal
error that tells the person to mount the volume.

**Measured cost.** The message names the file and the operating system's
error, and the remedy is right; only the exit code's band is off. Chosen on
purpose in U272 so the gate's refusal class did not grow a second slug.

**Closes when:** a library band slug for a capture the drive would not take
is declared and used here, or the pairing is recorded as intended. Ledger only.
