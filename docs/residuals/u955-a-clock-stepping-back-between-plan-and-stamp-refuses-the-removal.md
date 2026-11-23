---
title: A clock stepping back between a removal's plan and its stamp refuses the removal as an unplanned write
found: at review round one of #1002, U955, 2026-11-23.
issue: no
---

**The mechanism.** `DatabaseReading.read_at` is the plan's time, read when
`CollectionRemoval.prepare` reads the database, and the renumbering's
`updated_at` stamp is read from the same clock at the commit.
`_stamp_after_plan` refuses a stamp earlier than the plan, so a system clock
stepped back between the two (an NTP correction, a manual change) refuses
the whole removal with `whitelist-violation`, "reached rows it did not plan",
nothing written, and a remedy of changing policy or input where waiting and
running again is the answer.

**Measured cost.** Driven by the reviewer with `rb_removal._now` patched to
run 5 ms backward per call: exit 42, nothing written, the message above. The
producer, a real clock step inside one apply, was not driven. Nothing is
lost: the verb can be run again.

**Closes when:** the refusal names the clock and is retryable, or the check
is dropped in favour of the row moving to the stamp's text alone. Ledger
only: a misleading refusal over nothing lost, on an input not driven.
