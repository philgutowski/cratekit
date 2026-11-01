---
title: A landing that plans nothing after a download and its tail ends the verb OK, with no way on named
found: at the review of #401, U190, 2026-11-01.
issue: no
---

**The mechanism.** `cratekit.cli.tail.land` reads a succeeded `intake land`
as a landing with nothing to plan and raises `Done`, and both verbs that run
the chain then end OK: `crate sync land` with NO_OP, and since U190 `crate
label sync --go` with the go's own outcome. The only words are the check
"intake land planned nothing to land", over a folder the download had just
filled and the tail had just run on.

**Measured cost.** Driven at the stand in: a three track go whose landing
answered NO_OP exited 0 with no pending action and no command named. The real
`intake land` answering NO_OP over a staging folder the tail had just run on
was not reached, so the producer is unmeasured. The shape is U152's, moved
here unchanged.

**Closes when:** a landing that plans nothing after a download that landed
tracks is a failing check naming the folder and what `intake land` read, or
the producer is driven and shown not to exist. Ledger only, since the producer
was not driven.
