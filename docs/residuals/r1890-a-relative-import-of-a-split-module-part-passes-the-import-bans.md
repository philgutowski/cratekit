---
title: A relative import of a split module's part passes the night job's and the heard path's import bans
found: at review round one of #952, R-1890, 2026-11-23.
issue: no
---

**The mechanism.** `tests/test_sync_night.py` and `tests/test_label_heard.py`
read imports by their absolute dotted names, and R-1890 widened both bans to
the parts' names. A relative import is read as its written module, so
`from ..core import session_holders` appended to `cli/sync_night.py`, and
`from ..core import rb_nodes` appended to `label/heard_cli.py`, each passed
(driven by the review). The same was true of `from ..core import session`
before R-1890. Round two drove the same class in
`tests/test_split_modules.py`: its import graph drops every import with a
level, so a part off the convention imported only by `from . import x` in its
module has no importer and is not derived; with `Kind.UNCONVERGED_TREE` and a
typed suffix in such a part, 102 tests passed across the restore scans.

**Measured cost.** None today: `src` holds no relative import, measured, though
the lint selection does not ban one. The night job taking the library lock
through a relative import of the session would pass the ban written to stop
it.

**Closes when:** the bans resolve a relative import against the module's
package (`tests/_source_guards.py` has `_absolute_module` for this), or a lint
rule bans relative imports in `src`. Ledger only.
