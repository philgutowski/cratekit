---
title: The wiring of tag set's outside root sentence is pinned by no test through the verb, and the backlog's docstrings still call its walk adoption's census
found: at the review of #1020, U956, 2026-11-23.
issue: no
---

**The mechanism.** `cratekit.tagging.genre_set_cli._written` takes the library
root and names a written row whose file is outside it; its tests call it
directly with stand ins and their own root. The verb's call passes
`cfg.library.root`, and a mutant passing `"/"` there killed 0 of 77 tests; so
did dropping the `item.path and` guard and `sorted`. The new sentence joins raw
content ids uncapped, where the file's other sentences name rows by title
through `named()`. And `src/cratekit/tagging/backlog.py` (its module docstring
and two others) and `genre_set.py` still describe the tag verbs' walk as
adoption's census, which since U956 is confined to the root while theirs is not.

**Measured cost.** None today: round two drove the verb with rows inside and
outside the root and the wiring is right. A later change to the call would ship
green. The docstrings are not help text.

**Closes when:** a test drives `tag set` through the verb over a row mapped
outside the root and asserts its answer, the sentence names rows by title, and
the docstrings say the walk is not confined. Ledger only.
