---
title: The deferred off interface core imports cannot be settled without a source change or a wider interface
found: at the build of #869, U312, 2026-11-23.
issue: no
---

**The mechanism.** Area cards left their off interface core imports in
`tests/ratchets/imports/` for U312 to settle in `tests/test_import_rules.py`
(#868 named `core.processes` from `modules.tools` and `session`, and
`core.restore` from `session`). `CORE_INTERFACE` is at its cap of 25, and
every module on it is reached by at least one feature package (`snapshot` by
one, five others by three), so no listed module can give up its place
without moving an allowance line to another package. Fifteen reaches by ten
modules stay off the list. Settling them takes either a re-export from an
interface module (#868's alternative: `core.session` re-exporting the five
process names and the restore entry points), which is a source change U312's
brief rules out, or raising `CORE_INTERFACE_LIMIT`, which relaxes U296's
measure.

**Measured cost.** Maintainer facing: the allowance files keep fifteen
`off-interface` lines; nothing a person runs changes.

**Closes when:** a card that may edit `src/` adds the re-exports and empties
the allowance lines, or Phillip raises the limit.
