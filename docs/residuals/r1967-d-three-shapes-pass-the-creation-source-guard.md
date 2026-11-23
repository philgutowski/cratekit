---
title: Three source shapes still pass the creation guard, an alias of commit_guarded, an argument in parentheses before creations, and a keyword splat in another module
found: at the review of #1008, R-1967, round one, 2026-11-23.
issue: no
---

**The mechanism.** `tests/test_rb_writer_guard.py::test_every_other_writer_in_the_package_asks_for_no_creation` finds askers by the regular expression `commit_guarded\([^)]*creations=`, which stops at the first closing parenthesis, and holds `tag set` to `djmdGenre` by an AST walk that finds calls by the name `commit_guarded`. Driven by the reviewer over 19 planted variants: `commit = rb_writer.commit_guarded` then `commit(db, creations=(rb_writer.CONTENT_TABLE,))` inside `genre_set.py`; another module with a parenthesised argument before `creations=`; another module passing a `**kwargs` splat. All three pass; all three shapes placed in another module also pass the guard at `c84dc4ac`, so R-1967 did not open them.

**Measured cost.** None today: no module has any of the shapes, and the runtime whitelist still refuses a creation in a table nobody asked for. A future writer could ask for a creation the source guard does not see.

**Closes when:** the guard finds askers by an AST walk of every module (any call whose keywords hold `creations` or a splat, and any name bound to `commit_guarded`), which is outside the scoped exception Phillip granted for R-1967, so it needs his leave to edit that suite. Ledger only.
