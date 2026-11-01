---
title: inbox refill asks the account's bare name beside a dated name an intake file recorded, so a bare named playlist another pass's intake file gave the account makes the refill two found
found: at the review of #356, U175, 2026-11-01.
issue: no
---

**The mechanism.** `refill.locate`'s fallback asks the account's bare name and,
since U175, the first dated name an intake file of this pass recorded for this
account. `others` holds only playlists a record names by identifier, so a bare
named playlist an intake file of another pass or account landed (before U175)
still answers beside the dated one, and the account playlist is refused as two
found.

**Measured cost.** Driven by Fable's round 2 on records built by hand (S1,
S1b): the gate lists the account playlist unfound, two answering, and nothing
is written. On `main` the same input filled the other record's playlist, so
the branch is safer. Reaching it needs a bridge landing before U175 and one
after it of the same account, then a cutover; the live library is native, so
the producer was not driven.

**Closes when:** a recorded dated name, when there is one, is asked alone, or
`others` also excludes names intake files recorded for another pass or account.
