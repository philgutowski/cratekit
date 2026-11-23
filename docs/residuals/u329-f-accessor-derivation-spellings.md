---
title: The split module scan derives a part from its imported accessor in one spelling, and its fixture covers the writer's family alone
found: at review round two of #978, U329, 2026-11-23.
issue: no
---

**The mechanism.** U329's fix round taught `tests/test_split_modules.py`'s
`_accessor_parts` to derive a part from an accessor it imports as well as one
it defines, reading `from cratekit.core.<home> import <accessor>` at level
zero. Round two drove four other spellings of a part off the glob holding the
accessor, each passing the suite: from a sibling part, by a relative import,
module then attribute, and a dotted alias; the whole producer in the sibling
and relative spellings, imported by `rb_writer` and by `core.tags`, passed 143
of 143 over five structural files, and that part raising a bare
`RuntimeError` passed the writer scans. The branch's own
`tests/_source_guards.py` `_writer_accessors` accepts
`from .rb_call_time import writer`, so two readers of one accessor disagree on
the relative spelling. The fixture test plants the writer's family in one
spelling, so limiting the derivation to `rb_writer`, counting any name
imported from a home, or reading top level imports only each kill nothing.

**Measured cost.** None today: 399 files read, 10 accessor imports, all in the
absolute spelling, no relative import anywhere, so 10 candidates were driven
and none produces it. A part named off the glob that took the accessor
another way would escape every scan that reads through
`tests/_split_modules.py`.

**Closes when:** the derivation resolves an imported accessor by value (the
function it binds, however reached), with a fixture per family and spelling;
or a test holds every accessor import to the absolute spelling. Ledger only.
