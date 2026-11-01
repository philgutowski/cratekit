---
title: A batch an unreadable landing record names is left out of the INBOX mirror with nothing said, when it was never mirrored before
found: at the second review of #331, U150, 2026-11-01.
issue: no
---

**The mechanism.** A batch recognised only by its landing record (`run record`
or `recorded name`) is not a batch when that record cannot be read, so
`live_batches` leaves it out. One already mirrored is left on the account and
named, because its title is still under INBOX. One never mirrored is simply
absent from the plan, and under `--only mirror` the rotation's own warning
about unreadable records is not on the screen either.

**Measured cost.** Driven by the review on a hand corrupted record: the batch
is missing from the account's INBOX folder with no line saying why. No verb
that writes an unreadable record was driven, so reachability is unmeasured.

**Closes when:** the mirror's plan states the unreadable record count, as the
rotation's step does. Ledger only.
