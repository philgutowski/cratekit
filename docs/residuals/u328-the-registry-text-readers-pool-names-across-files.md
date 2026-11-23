---
title: The two text readers of the verb table pool tuple and constant names across its files, and the board's reads every registry file on disk
found: at the review of #977, U328, round one, 2026-11-23.
issue: no
---

**The mechanism.** `scripts/refactor_measure.py` `verbs_from` and
`scripts/board.py` `planned_units` read the verb table as text, the registry
and its `registry_*.py` parts together since U328. Both keep one mapping of
names for all the files, the last file read winning, where Python binds a
name per module. And `planned_units` reads every `registry*.py` under
`src/cratekit/cli` whether `cli/registry.py` assembles it or not.

**Measured cost.** None on the tree: no part binds a string constant, each
part holds one tuple under its own name, and a test holds each reading to the
live registry. Driven by the reviewer on fixtures: a constant bound in two
parts gave `{2: ['m.a', 'm.b']}` where Python gives units 1 and 2; a second
`ENTRIES` tuple in a `registry_tools.py` replaced the table with no refusal;
a tuple that stars itself ends in `RecursionError` where the base raised
`ValueError` (Python cannot import that source either); a `registry_old.py`
nobody imports, holding a marker, was read as owing a unit; and a half
written `registry_wip.py` ended `planned_units` in an uncaught `SyntaxError`,
as a half written `registry.py` did at the base. The producer of each is a
file nobody has written.

One file over, and the same at the base: `planned_units` has no refusal for
a tree with no `cli/registry.py` and returns no unit owed, so `board.py
closing` would pass a trailer over a register it could not read. The live
table holds no `planned_in` marker today, so the test that holds that reader
to the live registry compares empty with empty; U328's fixture test is what
reads a marker.

**Closes when:** both readers resolve a name in the file that uses it and
refuse a name two files bind, and `planned_units` reads the parts
`registry.py` stars and no other file and refuses a tree with no registry.
`refactor_measure.py` has three lines left under its 1,500 and the seventeen
scripts of #979's bar thirteen under 7,374 (`board.py` 26 under its own
1,500), so it waits on room there. Ledger only.
