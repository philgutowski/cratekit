---
title: Runs waiting on a pending action with no open gate are not in the status glance
found: at the plan of #1079, U960, 2026-11-25.
issue: no
---

**The mechanism.** The glance's `gates` lists runs with an open gate, each
with the gate's options, as the brief's shape asks. A run that waits on a
pending human action and no gate has nothing to answer through
`crate run decide`, so it is left out; `crate status`'s own check lines still
list it as awaiting that action.

**Measured cost.** Driven only as a run saved with no gate, which reads
`gates` empty; a run carrying a pending action was read, not driven. An app
reading the glance alone does not see such a run.

**Closes when:** the menu bar app's card decides whether a pending action is
shown, and the glance gains a key for it with a schema version bump. Ledger
only.
