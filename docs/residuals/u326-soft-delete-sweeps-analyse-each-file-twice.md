---
title: The two soft delete sweeps analyse every file twice, and the guard module's own pins refuse the memo that would share them
found: at the plan of #932, U326, 2026-11-22.
issue: no
---

**The mechanism.** `test_no_module_in_the_package_reads_the_soft_delete_marker_permissively`
and `test_only_the_declared_modules_read_the_soft_delete_marker_at_all`, in
`tests/test_rb_writer_guard.py`, each ask `tests/_source_guards.py` one
question of the same 788 files, and both questions are functions of the text
alone. A memo keyed on the text, or on a digest of it, would let the second
sweep in a worker read the first one's answers. U326 drafted one and dropped
it, because `tests/test_reserved_causes.py` pins the guard module's imports to
`__future__`, `ast` and `re` (so no `hashlib`) and reports any use of a
`source: str` parameter other than as the one argument of `ast.parse` (so no
dictionary keyed on the text). Both pins exist so that no comment can reach a
rule, and a memo keyed on the text lets none reach one, but widening them is a
decision for the card that owns that file.

**Measured cost.** On a four core Linux container on 2026-11-22, after U326's
walk: 13.7 and 10.1 seconds for the two sweeps in one process. The second
sweep would cost close to nothing in a worker that ran the first.

**Closes when:** #869 (U312), which owns `tests/test_reserved_causes.py`,
either admits a memo keyed on the text (a digest import, and a named exception
in the raw text rule for a key that is never read as text) and adds it, or
records that the pins stay and the cost is kept. Ledger only.
