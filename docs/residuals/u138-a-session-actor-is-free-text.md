---
title: The session actor that lifts the terminal check on the backup acknowledgment is a free text answer any process can give
found: at the review of #315, U138, 2026-10-12.
issue: no
---

**The mechanism.** Since U138 `crate session ack` mints with no controlling
terminal when the run record holds the gate's answer under the actor
`session`, and only while every backup portion is under five days old. The
actor comes from `crate run decide RUN session.ack.backup acknowledged
--actor session`, and `--actor` is free text: a Relay task, a queued job or a
script can type it as readily as the author's session. Nothing establishes
that the answer came from a session the author is running. The engine's
`decided_by` selector is likewise trusted as given by any caller of
`record_acknowledgment`, as its `terminal` seam always was.

**Measured cost.** Driven by reading, not by a run: the three invocations
above, with no terminal and backups under five days, mint a twelve hour
acknowledgment every destructive verb accepts. This is the author's decision
(2026-10-09, five days since 2026-10-10), and before U138 the same session
satisfied the terminal check with `script -q /dev/null`, which any process
can also run and which checked no age. U138 narrows that route to young
backups; it does not close it. Not on the board bar: the guard is the one
the author chose, and it kills its tests.

**Closes when:** the author decides a session's answer needs an identity a
detached process cannot claim, or decides the free text actor is enough.
