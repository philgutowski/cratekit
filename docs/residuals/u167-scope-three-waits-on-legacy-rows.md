---
title: analyze check with no landing named waits on every never analysed row in the library
found: at the review of #348, U167, 2026-10-31.
issue: no
---

**The mechanism.** With no `--pass` or `--session` and INBOX / Analyze empty
(after `crate inbox analyzed` cleared it, or on a tree not cut over), the scope
is every live row rekordbox has not analysed, the brief's third scope. Every
row in it is waiting by construction, so the verb can only answer waiting or
nothing, and a library holding any old row rekordbox never analysed answers 12
however many visits follow.

**Measured cost.** Driven by the review on the fixture's two seeded rows: 12,
and the same after a clear. A skill that ran the check after the clear would
wait for ever; U173's skill should run it before the clear, or name the pass.

**Closes when:** U173 settles the order the skill runs the check and the
clear in, or the third scope narrows to rows a landing made. Ledger only.
