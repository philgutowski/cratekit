---
title: A stale batch is mirrored by the same organize run that rotates it into Old, and removed from the account at the next
found: at the review of #331, U150, 2026-11-01.
issue: no
---

**The mechanism.** `rotate.live_batches` reads a batch as live while it sits
under INBOX, whatever its age, and `crate organize` plans both areas before it
applies either. So a batch past `reports.intake_stale_days` that was never
mirrored is planned into the account's INBOX folder in the run whose
rekordbox area moves it into Old, and the next refresh removes that playlist.
The first fix round skipped a batch the rotation would move, and the second
review drove what that cost: under `--as-of`, under `--only mirror`, or with
the rekordbox gate declined or refused, the batch stays in rekordbox's INBOX
and was silently missing from the account's. That skip was reverted.

**Measured cost.** Driven at the function seam by the review: one playlist
created and filled, then removed at the next refresh, per stale batch never
mirrored before. No track leaves the library or any other playlist.

**Closes when:** the account area learns, after the rekordbox apply, which
batches the rotation actually moved (a second account gate, or the mirror
planned after the database area writes, the lag the U147 solution names).
Ledger only.
