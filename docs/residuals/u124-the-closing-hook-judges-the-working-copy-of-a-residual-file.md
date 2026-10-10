---
title: The closing hook judges the working copy of a residual file, not the staged one
found: at the review of #287, U124, 2026-10-09.
issue: no
---

**The mechanism.** `board.py closing` reads every residual file git knows
from the working tree. In the commit-msg hook the commit is made from the
index, so a malformed file staged with a fixed working copy passes the hook,
and a good staged file with a broken working copy is refused.

**Measured cost.** Not driven past the review's reading. CI runs the same
check over the pushed range on a clean checkout, where the working tree is
the commit, so a malformed file that slips the hook is refused there before
anything numbers it, and `residuals --land` validates every file before it
writes.

**Closes when:** the hook path reads each file's staged blob with `git show
:<path>` and the range path keeps the working tree. Ledger only,
maintainer facing.
