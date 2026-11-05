---
title: crate organize's mirror downloads reads an expired provider session as one playlist that could not be listed
found: at the review of #547, R-1289, 2026-11-05.
issue: no
---

**The mechanism.** `organize/mirror_downloads.py` `plan` catches every
`CratekitError` from its listing, so a refusal that is not about one playlist,
an expired session (`credential-missing`), names each wanted track "the
provider could not list the playlist: ..." and plans the rest, where `crate
sync all`'s sweep re raises any reason outside `PER_PLAYLIST_REASONS` and
stops. The catch is the same on `main`; R-1289 changed only the reader.

**Measured cost.** Driven by the review's round one: `listed` raising
`credential-missing` left the queue empty and named both wanted tracks with
the session's message. The step reports nothing planned with the tracks named
and the reason given, so the report is not clean, but it is not the refusal
that would send a person to log in again.

**Closes when:** the step re raises a refusal outside the per playlist reasons,
as the sweep does, so the step refuses with the session's own cause. Ledger
only: the words a person reads carry the true reason.
