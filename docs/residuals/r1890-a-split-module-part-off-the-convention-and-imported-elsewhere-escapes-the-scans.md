---
title: A split module's part named off the glob, imported from elsewhere and holding no accessor, falls out of every scan
found: at review round one of #952, R-1890, 2026-11-23.
issue: no
---

**The mechanism.** `tests/_split_modules.py` finds each split module's parts
by the glob of its file name, and `tests/test_split_modules.py` fails on a
part the glob misses when the `docs/DEVELOPING.md` table names it, when only
its module and its parts import it by an absolute import, or when it holds
an accessor back to its module in the parts' spelling (a module level
function returning a name `from cratekit.core import X` bound; round two
drove `import cratekit.core.restore as r; return r` and an accessor nested
under `if True:`, both passing). A part named off the convention that some
other module also imports, or only a relative import reaches, holds no
accessor in that spelling, and is missing from the table matches none of the three,
so every scan reading the module through the helper skips it. `rb_tables`
and `session_analysis` already hold no accessor, so that half is the house's
shape.

**Measured cost.** None today: all thirteen parts follow the convention and
the import graph derives exactly the glob's sets. A part breaking the
`DEVELOPING.md` rule that a part is imported from nowhere else would be needed
first.

**Closes when:** a part declares its module (a module level marker every part
carries, held by a test), so the scope no longer rests on naming. Ledger only.
