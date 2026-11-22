---
title: The verb registry stays over 1,500 lines because two scripts read its table from that one file
found: at the build of #860, U303, 2026-11-22.
issue: no
---

**The mechanism.** `src/cratekit/cli/registry.py` is 2,459 lines after U303,
over the 1,500 line limit of #847's point 2. Its `ENTRIES` table alone is
about 1,700 code lines, so prose cannot bring it under. #860's brief asked for
the one table split by module group into several files, and that split cannot
land from the shell's card: `scripts/refactor_measure.py` `verbs_from` raises
unless `registry.py` holds `ENTRIES` as one literal tuple of `Entry(...)`
keyword calls, and `scripts/board.py` `planned_units` reads the `planned_in`
markers from that same file by syntax tree. Both are #870's files, and
`tests/test_import_rules.py` holds the first reading equal to the live
registry.

**Measured cost.** None to a person: the table is value for value what it
was, compared by syntax tree and by a dump in the behaviour scenario
`cli/the_registry_value_for_value`. The cost is the audit's: one file over
the limit.

**Closes when:** both readers follow a table assembled from several modules
(for example, reading every `ENTRIES` tuple of the modules `registry.py`
names), and the table is then split by module group. Ledger only; #870 or a
later card under #847 takes it.
