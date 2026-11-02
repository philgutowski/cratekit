---
title: inbox refill takes the first name an intake file of the pass recorded even while that file still awaits an import that never came, so a later landing's live playlist is not found
found: at the review of #356, U175, 2026-11-01.
issue: no
---

**The mechanism.** `refill.bridge_names` reads every standing intake record,
`AWAITING_IMPORT` included, while `rotate.landings` reads an intake record only
once its import is proven. When the first landing of a pass was never imported
and a second one was, the first's name is asked and answers nothing, and the
second's live ` 2` is never asked.

**Measured cost.** Driven by Fable's round 2 on hand built records (S2c): the
screen says no live INBOX playlist answers the account playlist while a record
of this pass names one; nothing is written. `main` gives the same answer for
the undated pair, so it is not new. The producer, a second bridge landing
while the first awaits import followed by a cutover, was not driven.

**Closes when:** the name asked is the first one whose import was proven, the
rule `rotate.landings` keeps.
