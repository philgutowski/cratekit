---
title: After a stale refusal, run decide records an answer over the moved plan's digest, which no screen showed
found: at the review of #552, U222, 2026-11-05.
issue: yes
---

**The mechanism.** `gates.Gates.require` records the digest it is offered in
`offers` before it compares a recorded answer, and the dispatcher saves the
run on a `decision-stale` refusal. So after a stale refusal, `crate run decide
RUN GATE OPTION` is accepted over the new digest, and the next resume applies
that plan, although the stale refusal showed no items and the person never saw
it. Pre-existing on `main` for every gate; U222's version bump makes every
open organize run gated on v0.8.0 a producer, since its frozen mirror plan is
no longer read and the resume plans afresh.

**Measured cost.** Driven through `crate organize --only mirror` at the review
of U222: a playlist made under a mirrored folder between the acts, a stale
refusal, `run decide` again, and the resume created the playlist on the
account. A person did type the second decide, against a refusal that told
them to replan (`REPLAN_THEN_DECIDE`) and showed nothing. Meets the board bar
(b): a write is applied that no gate screen declared.

**Closes when:** a decision recorded after a stale refusal is refused until
the moved plan has been shown (a resume that leaves the gate open over it), or
the stale refusal carries the moved plan's items as an open gate does, and a
test drives the two acts with a second decide.
