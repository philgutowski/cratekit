---
title: A landing record whose start is not a date is read as readable and then skipped, so its batch reads as named by no record with no warning
found: at round two of the review of #512, U214, 2026-11-05.
issue: no
---

**The mechanism.** `SessionRecord.from_json` keeps a `started` that is not a
date as text, so the record counts as read, and `rotate.landings` skips it when
`_local_date` returns nothing. The batch it names then reads "no landing record
names it" and `unreadable_records` stays at 0.

**Measured cost.** A false reason with no warning on the rotation's plan and
the mirror's INBOX step. Driven with a hand edited record; the writer always
writes an ISO date, so no Cratekit verb was found to produce it (1 candidate
driven).

**Closes when:** `landings` counts such a record as unreadable. Ledger only.
