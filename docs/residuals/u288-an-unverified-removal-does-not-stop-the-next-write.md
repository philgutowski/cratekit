---
title: A removal whose read back disagrees refuses as unverified, and the next write to the library proceeds
found: at the review of #839, U288, round one, 2026-11-21.
issue: no
---

**The mechanism.** `apply_removed` refuses `session-committed-unverified` when
the database read back after the commit is not what it planned, and the
session record then closes abandoned with its source committed, which the
write session gate does not refuse on. So a following `intake land` writes the
library the removal could not vouch for.

**Measured cost.** Driven by round one with the read back patched to report
one difference: exit 25, then `intake land` exited OK. No real producer of a
disagreeing read back was found.

**Closes when:** an unverified removal leaves the session unresolved, as the
landing's committed unverified state does, so the next write refuses until a
person reads it. Ledger only.
