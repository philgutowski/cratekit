---
title: Two label and favourites inconsistencies a person can see, left as they are by the refactor that froze behaviour
found: at the build of #865, U308, 2026-11-22.
issue: no
---

**The mechanism.** U308 changed no behaviour, so it left two differences its
workers saw. `crate label registry remove <unknown>` exits OK reporting
`removed: false`, where `set` and `rename` refuse an unknown label with
`label-unknown`. And `crate favorites backfill` and `crate favorites refresh` open
their approval gate even when the plan writes nothing, where `favorites split`
and `favorites order` end NO_OP without asking; `favorites.spine.run` keeps the
difference as its `gate_first` flag, and tests pin both orders.

**Measured cost.** A person removing a misspelt label is told nothing was
removed rather than that no such label exists; a person running backfill or
refresh with nothing to do is asked to approve nothing.

**Closes when:** Phillip decides each as a UX cleanup under #847's rule, posted
on #847 first. Ledger only.
