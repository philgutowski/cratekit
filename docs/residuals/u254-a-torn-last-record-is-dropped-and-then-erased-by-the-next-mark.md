---
title: A journal's damaged last line is read as a torn mark and erased by the next mark, even when it was a whole record
found: at the review of #683, U254, 2026-11-12.
issue: no
---

**The mechanism.** `apply._read_journal` reads an unterminated last line, or
a terminated last line that is not JSON, as the mark that did not finish, and
the next mark rewrites the file without it. That is the decision U254's card
asked for and its tests hold: a mark is the last act of an entry, so a mark
that did not land re-applies the entry, which the module's crash table shows
is safe. Two inputs are dropped with it that were not torn writes: a whole
valid record that only lacks its newline, and a last line damaged by anything
other than a kill.

**Measured cost.** The documented re-apply: the entry is placed again (a no
op for the membership writer) and marked again, so its record's actor, digest
and applied time become the second run's. `organize/mirror_downloads.py` reads
the digest and the applied time to tell an adoption from a person's filing.
Neither producer (partial page persistence after a power loss, a hand edit)
was driven.

**Closes when:** the cost is accepted, or a whole record lacking only its
newline is kept and repaired with its newline rather than dropped. Ledger
only.
