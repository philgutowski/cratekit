---
title: A rotation approved in the same organize run moves an edited INBOX batch into Old and refuses the whole mirror-edits step
found: at the review of #494, U204, 2026-11-05.
issue: no
---

**The mechanism.** The rekordbox area applies `rotate` before `mirror-edits`
(`organize/rekordbox.py` STEPS). An INBOX batch a person edited on the account
that the rotation moves into Old in the same run is no longer a live batch
when `mirror-edits` plans again on its write handle, so the plan the gate
showed differs and `_stale` refuses the step, with every other edit of the run.
Old is never touched.

**Measured cost.** Driven by review round one: nothing written that run; the
next organize takes the other edits again, while the edit to that batch goes
with its retired mirrored playlist. Round two's drive did not reach the
refusal, so its producer is not always met.

**Closes when:** the step plans an INBOX edit only for a batch the rotation
will not move this run, or drops a moved batch's change alone rather than
refusing the step. Ledger only: an honest refusal that heals on the next run.
