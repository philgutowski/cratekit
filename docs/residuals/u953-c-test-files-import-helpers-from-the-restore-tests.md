---
title: Eight test files import private helpers from tests/test_restore.py rather than from a helper module
found: at the review of #953, U953, 2026-11-23.
issue: no
---

**The mechanism.** U953 folded each `pytest.raises` block that makes one call
into `_refusal`, `_refused` and `_raised`, defined once in
`tests/test_restore.py`. `test_snapshot.py`, `test_snapshot_flush_u272.py`,
`test_snapshot_wal_r1665.py`, `test_snapshot_check_room_r1677.py`,
`test_rb_writer_db.py`, `test_tombstones.py`, `test_tree_registry.py` and
`test_write_session.py` import them from there, and `test_snapshot_flush_u272.py`
imports its `cfg` fixture from `test_snapshot.py`. `tests/_containers.py` calls
such a cross module private import an undeclared coupling and keeps shared
helpers in a helper module. The card's files did not include a new helper
module, so none was added.

**Measured cost.** None to a person: collection is 22,479 cases on base and
branch alike, no autouse fixture travels with the import, and no assertion
was weakened. A maintainer moving `test_restore.py` breaks eight files.

**Closes when:** the helpers move to a module such as `tests/_raises.py`,
by the suite card (#869) or a later one. Ledger only.
