---
title: analyze check's three sigma key floor does not flag sitting 47's 98 of 212
found: at the review of #348, U167, 2026-10-31.
issue: no
---

**The mechanism.** `rekordbox_check.key_floor` puts the floor at the recorded
equal rate (158 of 299) less three standard errors of the sample. For 212
compared keys the floor is 42.6 percent equal, and sitting 47's 98 of 212 is
46.2 percent, so the brief's motivating key number reads as ordinary.

**Measured cost.** Nothing false is said: the counts, the rate and the floor
are all on the check. The cost is a threshold choice, three sigma, that calls
a library agreeing at the recorded rate suspect about once in seven hundred
checks and lets a rate several points below it through.

**Closes when:** a sitting measures what agreement a good visit actually
gives, and `KEY_AGREEMENT_SIGMAS` or the reference rate is set from it. Ledger
only.
