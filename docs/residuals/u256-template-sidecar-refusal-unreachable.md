---
title: The fixture template's refusal of a build that left a sidecar has no input that reaches it, so it kills no test
found: at the review of #685, U256, 2026-11-12.
issue: no
---

**The mechanism.** `tests/test_rb_writer_db.py::_template` refuses when the
build from nothing leaves anything beside `master.db` in its directory, so a
copy of the one file could never be half a database. A WAL build closes its
last connection and SQLite folds the log into the main file, so nothing is
left, and every probe build in both review rounds left only `master.db`.

**Measured cost.** None to a person. Round one replaced the check with
`if False:` and all ten tests of the new file passed; it is mutation row T6.
A maintainer facing backstop for a change in SQLite or in the binding's
close.

**Closes when:** an input that leaves a sidecar is found and a test drives
it, or the check is accepted as a backstop no current build reaches. Ledger
only.
