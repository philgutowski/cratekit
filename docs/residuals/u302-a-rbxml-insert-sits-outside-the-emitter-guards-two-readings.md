---
title: The new rbxml_insert.py sits outside both readings of the emitter guard, which read rbxml.py alone
found: at the review of #859, U302, 2026-11-22.
issue: no
---

**The mechanism.** `tests/test_tree_registry.py` finds the XML byte writers
two ways: `_public_functions` keeps only functions whose `__module__` is
`cratekit.write.rbxml`, and `_byte_writers_by_source` parses `rbxml.py` alone.
U302 moved the read only placement helpers into `write/rbxml_insert.py` and
imports them back into `rbxml`, so a byte writer added to `rbxml_insert.py`
later, and imported back the same way, is checked by neither reading. The
review planted one there on a scratch copy: both conformance tests stayed
green, while the same function in `rbxml.py` failed both.

**Measured cost.** None today: no function in `rbxml_insert.py` changes a
buffer (read by grep and by syntax tree). The producer is a future edit, not
driven.

**Closes when:** the guard reads every module under `write/` whose name
starts `rbxml`, or `rbxml_insert.py` is folded back. `tests/test_tree_registry.py`
is on no area card's list, so it is the suite card's, #869 (U312). Ledger only.
