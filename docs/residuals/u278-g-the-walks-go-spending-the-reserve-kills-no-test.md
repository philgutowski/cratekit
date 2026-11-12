---
title: The go a label sync walk ends at spends the reserve, and no test kills its removal
found: at the review of #741, U278, 2026-11-12.
issue: no
---

**The mechanism.** `label sync`'s walk is held to the read line by
`provider_gate.reading`, and the go its last gate leads to widens back to the
verb's declared class through `provider_gate.spending` in `sync_cli._go`.
Removing that `with` leaves the suite green: no test drives a walk whose go
meets an hour already past the read line.

**Measured cost.** Driven by the round one review as a mutation, zero kills.
With it removed, a walk's go would stop at 1,125 rather than 1,500 in an hour
the reads had used, which is the case the reserve exists for. The code is
present and correct at the merge; only its guard is unpinned.

**Closes when:** a test walks every label to the go with the account's hour
at its read line and the download still runs. Ledger only, maintainer facing.
