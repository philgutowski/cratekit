---
title: A held card has no release, and only its board status knows it is held
found: at the review of #280, U122, 2026-10-10.
issue: no
---

**The mechanism.** U122 made `derive_status` keep In Progress and In review
for any open card, so a hold is now read from the card's own status and
nothing else. Four things follow, each raised by the review and each older
than the unit or asked for by the brief. Nothing in this repository releases
a stale hold. The runner's closeout does, in the normal flow: a landed task's
issue is closed before its card is set Done, and a blocked or halted one is
moved back to the status it read before the run. A card the closeout never
reaches, a run that dies first or a closeout that fails its write, keeps In
review, and now `sync` no longer moves it back, `audit` no longer reports it,
and `next` lists it as underway and never offers it, the same treatment In
Progress always had. `board.py start` checks closure and dependencies but not the hold,
so it will branch and overwrite a card the runner or a lane holds. The
`ready` and `blocked` labels ignore the hold, and the feeder's ready source
reads labels only, so a lane held unit still reads ready to the feeder;
the lane deny set is what keeps it out today. The audit's summary line counts
a held unit among the ready ones, so it can say more are ready than `next`
offers.

**Measured cost.** Not driven against a live board. A stale hold costs a card
that sits unoffered until somebody moves it by hand. `start` on a held card
costs two builders on one card, and it needs a person to type the number of a
card `next` did not offer. The review also raised a landed card reading Done
on an open issue; the runner's closeout closes the issue first, so that
window was read from its code and not found, and nothing here records it.

**Closes when:** a hold carries something that can age, such as the runner's
cycle or the lane's branch, so `audit` can tell a live hold from an abandoned
one; `start` refuses a card held by anyone else; and either the labels or the
feeder's ready source read the hold. Ledger only, it is operator tooling.
