---
title: The first position a removal gives the deletion pass can sit above its own commit, or replace one of another identity over an earlier removal, and its file is then never offered
found: at the review of #839, U288, round two, 2026-11-21.
issue: no
---

**The mechanism.** With no position, `sync removed` gives the deletion pass
the greater of the update count before its commit and the highest marked
removal, the pass's own rule. A marked row whose `rb_local_usn` sits above the
counter puts the position above the removal's commit, so its recorded row is
filtered as history. And a position stored for another database identity is
replaced, as the pass itself replaces one, which drops an earlier removal still
waiting under the old position.

**Measured cost.** Driven by round two on copies whose rows were written by
SQL: a marked row at the counter plus 1000 left the removed file never
offered; an identity rewritten by hand between two removals left the first
one's file never offered. Neither producer was driven: no real marked row
above the counter, and a rehearsal copy carries the live `DBID`. Both keep the
file, the safe side, and Phillip's library holds a position since 2026-09-23.

**Closes when:** the first position is the lower of the pass's rule and the
earliest recorded removal less one, with a test of each corner. Ledger only.
