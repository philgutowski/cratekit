---
title: The provider-session-not-stored warning reaches only a download that finished, and a parked or failed one drops it
found: at U274's review round two, 2026-11-13.
issue: no
---

**The mechanism.** The drive's close puts `provider-session-not-stored` on
the drive's result, and `Context.run_job` hands it to the verb with the drift
warnings. `acquire.cli.drive_queued` then calls `jobs.raise_for_state`, which
raises the job's own cause for a parked or failed job, and the warnings go
with the raise, as `label/go._drive` already says of its own.

**Measured cost.** Driven by the review: a refresh, a keychain that refuses
it, then a withdrawal (exit 40) or a track the tool broke on (exit 41); the
envelope carries the job's cause and no word that the refreshed session was
not stored. Nothing is lost: the stored session is left as it was and its
refresh token still logs in. `docs/GUIDE.md` says only a finished run carries
the warning.

**Closes when:** a refusal raised for a job's state carries the drive's
warnings onto the envelope it becomes. Ledger only: maintainer facing, nothing
is lost.
