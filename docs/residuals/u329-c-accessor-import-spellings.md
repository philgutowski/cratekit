---
title: The soft delete guard reads the writer's shared accessor in one import spelling, so a permissive read through any other passes
found: at review round one of #978, U329, 2026-11-23.
issue: no
---

**The mechanism.** Since U329 the writer's parts bind `_writer` with
`from cratekit.core.rb_call_time import writer as _writer`, and
`tests/_source_guards.py` (`_writer_accessors`) recognises that import and
`from .rb_call_time import writer` inside `core`. The review drove five
other spellings through the guard and each names nothing:
`from ..core.rb_call_time import writer`, `rb_call_time.writer()` after a
module import, `import cratekit.core.rb_call_time as ct` with `ct.writer()`,
`from . import rb_call_time`, and `_writer = writer` after the import. A
permissive read appended to `write/row_defaults.py` through the level two
relative import passed the beat grid suites and the parts guard (271
passed). It extends R-1901, which records the same limit for the accessor
defined in a file.

**Measured cost.** None today: the five imports of the accessor in `src`
all use the recognised spelling, so none of them produces it. A part written
in another spelling with a falsey default would read a removed row as active
and pass the guard.

**Closes when:** the guard resolves the writer by value rather than by
spelling, as R-1901 asks, or a test holds every import of the accessor to
the recognised spelling. Ledger only: a maintainer facing gap with no
producer in the tree.
