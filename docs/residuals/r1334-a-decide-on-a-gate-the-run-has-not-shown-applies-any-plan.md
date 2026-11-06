---
title: A decide on a gate the run has not yet shown records no digest, and the resume applies whatever plan it then reads
found: while building #567, R-1334, 2026-11-06.
issue: yes
---

**The mechanism.** `gates.record` takes the answer's digest from the run's
`offers`, which `Gates.require` fills only when the gate is reached. A `crate
run decide RUN GATE OPTION` on a gate the run has not reached yet, the second
of two gates for one, records a decision whose digest is `None`, and
`require` compares a recorded digest only when it is not `None`. So the
resume applies the plan it reads at that gate without its screen ever being
shown, and no later move of that plan can make the answer stale. The same
class as R-1334, an answer bound to a plan no screen showed, one door over:
R-1334's door was the stale refusal, this one is the gate never reached.

**Measured cost.** Driven through `crate organize` on the organize suite's
world: the rekordbox gate open, `run decide RUN organize.account.apply
apply` before the account gate was ever shown, then the rekordbox gate
answered, and the resume applied the whole account area with no account
gate: three folders created on the account, the label folder, the
downloaded sets folder and the INBOX mirror. Meets the board bar (b) and
(d): writes applied that no gate screen declared, past a digest guard the
early answer is never compared by.

**Why it was not closed with R-1334.** The fix is a new refusal on `crate run
decide` (refuse a digest bound gate the run holds no offer for and has not
left open), which changes what `run decide` accepts rather than what a stale
refusal shows, and it needs its own reason and screen: the gate screen
`decision-required` prints invites the very decide it would refuse. Whether
anything decides a gate ahead on purpose was not surveyed.

**Closes when:** a decide on a digest bound gate the run has neither offered
nor left open is refused, naming the run to continue to reach the gate, and a
test drives organize's two gates with the account answered first.
