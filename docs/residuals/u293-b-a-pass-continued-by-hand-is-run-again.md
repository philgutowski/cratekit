---
title: A night pass continued by hand to its gate is run again by the next night
found: at the review of #850, U293, 2026-11-21, round one finding 5.
issue: no
---

**The mechanism.** A firing the night's budget stopped records `continue_pass`, and the next firing runs `crate sync land --pass-run` on it. When the session at the Mac has already continued that pass by hand to its gate, the record still names the continue (`settle` reads only waits, not continues), so the next night runs the tail and `name apply` again and plans a second landing run on the same pass.

**Measured cost.** Driven by the reviewer: a second open gate run on the same pass and a night with no `sync all`. Nothing is lost or landed twice: the second plan is over the same files and waits at its own gate.

**Closes when:** the night settles a continue too, by the pass's land record or its open gate, or the crate-sync skill clears the night's record when it continues a night pass by hand.
