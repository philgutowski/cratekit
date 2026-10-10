---
title: The by name gate lookup and the config load wrapper are retyped in every verb module
found: at the review of issue 291, A32, 2026-10-10.
issue: no
---

**The mechanism.** Every verb module under `write/` and its siblings carries
its own `_confirm_gate`, a loop over the entry's gates by name, and its own
`_load`, the wrapper that turns a configuration failure into a typed cause.
The review counted the probe's copy as the sixth of the first and the thirty
fourth of the second. Each copy hand edits its origin tuple, and the probe's
first draft spelled one origin two ways in one file.

**Measured cost.** None to a person using the verbs. A maintainer adding a
verb retypes twelve lines and may spell an origin wrong, which only a reader
of the cause's `origin` field sees.

**Closes when:** `registry.Entry` grows a `gate(name)` accessor and one shared
config loader takes the origin, and the copies are replaced by calls. Ledger
only: maintainer facing, below the board bar.
