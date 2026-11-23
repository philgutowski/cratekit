---
title: The soft delete guard resolves the writer's accessor in one spelling, so a permissive read through any other passes
found: at review round one of #952, R-1890, 2026-11-23.
issue: no
---

**The mechanism.** `tests/_source_guards.py` now resolves
`_writer().SOFT_DELETE_COLUMN` when `_writer` is a function of the same file
that imports `cratekit.core.rb_writer` and returns the name it bound. The
review drove other spellings through the beat grid suite's two package wide
tests and each passed: `getattr(row, _restore().rb_writer.SOFT_DELETE_COLUMN,
0)` in `restore_perform.py`, the `_session()` twin in `session_ack.py`,
`getattr(row, getattr(_writer(), "SOFT_DELETE_COLUMN"), 0)`, and
`writer = writer or _writer()` in `rb_copies.py`; on fixtures an accessor
reached through `importlib` or `sys.modules`, a lambda, a method, or one
imported from a sibling part is not recognized either. Round two drove five
more that return nothing: a module level import returned by `def _writer():
return rb_writer`, `w = rb_writer; return w`, `return rb_writer if True else
None`, `from cratekit import core; return core.rb_writer`, and `(w :=
_writer()).SOFT_DELETE_COLUMN` at the call. And reading an accessor at any
depth makes an outer function wrapping one, or a method named like a free
function, read as the writer too: `outer().SOFT_DELETE_COLUMN` fires though
`outer()` returns `object()`, a false firing on shapes not in the tree (366
files, five accessors, all module level `_writer`). The fix rounds added the
dotted return and an accessor at any depth; the rest are named in the guard's
known limits.

**Measured cost.** None today: every accessor in `src` uses the one recognized
spelling, and no `_restore().rb_writer` or `_session().rb_writer` exists. A
part written in one of the other spellings with a falsey default would read
a removed row as active and pass the guard.

**Closes when:** the guard resolves the writer by value rather than by
spelling (a call whose result is the writer module however reached), or the
parts' accessors are held to the one spelling by a guard of their own.
Ledger only: a maintainer facing gap with no producer in the tree.
