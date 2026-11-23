---
title: The tree registry and the backup facts each read their JSON document with the same shape and different words
found: at the build of #857, U300, 2026-11-22.
issue: no
---

**The mechanism.** #857's brief notes that `core/tree_registry.py`'s path
reader repeats `core/backup_facts.py`'s by shape (read the bytes, absent is
empty, unreadable and not JSON and not an object each refuse). The two differ
in their exception types, their messages, and a permission branch only the
backup facts have, so a shared home would take each message and type as a
parameter. U300 left both where they are rather than fold text a person
reads into arguments.

**Measured cost.** None; a maintainer reads two readers where one shape would do.

**Closes when:** a card that may change these refusals' wording gives them one
reader with the two vocabularies as data. Ledger only.
