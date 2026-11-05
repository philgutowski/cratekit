---
title: How INBOX is released after a restore marks it is a conservative call that waits on Phillip
found: by U219, by its author, 2026-11-05.
issue: no
---

**The mechanism.** A restore marks every database native tree unconverged,
INBOX among them, and every landing into a marked tree refuses. The routing
tree is repaired by `crate rebuild`; INBOX holds the batches the landings
wrote and cannot be derived, and U219 stopped the rebuild that used to
derive it wrongly (R-789). So U219 built the conservative way out: `crate
rebuild --tree inbox` asks the explicit gate `rebuild.accept`, and a named
person's answer records a disposition on INBOX and a fresh fingerprint, so
landings resume while `crate converge` still reports it unconverged and
accepted. The next restore marks it again. The question went on #537 as a
Question for Phillip with two other ways: never mark INBOX at a restore, or
keep it blocked until a later card rebuilds its batches from the landing
records.

**Measured cost.** Not driven live. Whatever a restore took out of INBOX
stays out unless it is landed again, and only the person accepting is told.

**Closes when:** Phillip answers the question on #537. Option 1 closes it as
built; option 2 or 3 is a new card. Ledger only: it closes at a decision,
not at a verb a person pays for.
