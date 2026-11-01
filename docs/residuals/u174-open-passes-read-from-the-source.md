---
title: The crate-sync skill's open passes field is checked by reading the source, not by a pass that stops there
found: at the Fable review of #355, U174, 2026-11-01.
issue: no
---

**The mechanism.** The skill tells the session to read
`data.summary.open_passes` when `crate sync land` stops because several earlier
passes hold open intake jobs. `tests/test_crate_sync_skill.py` holds every
other summary field it names to a field the verb writes, and for this one it
reads the source of `src/cratekit/cli/sync_land.py` for the assignment, since
no test drives `sync land` into its choice between passes and reads the field
off the envelope.

**Measured cost.** None today: the field is set in `_choose` and the skill
names it correctly. A rename there would leave the skill naming a field the
envelope no longer carries, and the skill test would still pass on any text
that kept the old name.

**Closes when:** a test drives `crate sync land` over two passes with open
intake jobs and reads `data.summary.open_passes` off its envelope. Ledger only,
a maintainer facing coverage gap.
