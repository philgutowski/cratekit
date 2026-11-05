---
title: A resort whose shown add was made by hand before the drive fails the job and says the library moved
found: at the review of #537, U219, round one, 2026-11-05.
issue: no
---

**The mechanism.** `rebuild.assert_as_approved` asks the before check's adds
to equal the approved adds exactly. A person who approves a resort and then
files one of its shown tracks by hand in rekordbox before the job is driven
leaves the worker one add short of the plan, and the job fails with
`resort-plan-stale`, "the library or its taxonomy moved after the gate". The
same refusal would meet a job whose item committed and whose driver was
killed before the item was marked done, when the respawn claims it again.

**Measured cost.** Driven for the hand add: approve and queue, add track 1 to
`Minimal / Deep Tech / Med Energy` by hand, drive; the job fails, planned 3
against approved 4, nothing written. Running the resort again plans the rest
and files it, so nothing is lost; the cost is a failed job and a sentence
that blames a move rather than a subset. The killed driver window was not
driven, so that producer is unmeasured.

**Closes when:** the worker accepts a before check whose adds are a subset of
the approved adds, writing only those, and names the shown adds that were
already present, or the refusal says which approved adds are already there.
