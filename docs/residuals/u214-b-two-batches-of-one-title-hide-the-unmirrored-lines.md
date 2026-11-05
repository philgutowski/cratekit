---
title: An INBOX step refused for two batches of one title shows the refusal only, and none of the nodes it would leave off
found: at the plan and the review of #512, U214, 2026-11-05.
issue: no
---

**The mechanism.** `account_mirror._inbox` returns the `_twice` refusal when
two live batches take one account title, before the unmirrored lines are
built, so the refused INBOX step names neither the batches it would mirror
nor the nodes it would leave off.

**Measured cost.** The brief's "never dropped without a line" does not hold
while the step is refused. Nothing is mirrored and nothing is skipped
silently: the refusal names the title to fix, and once it is fixed the next
refresh names every node. Driven on a disposable database with two
`2026-09-23 Tidal playlists` batches and a label playlist beside them. The
author's call at the plan, the conservative one, since the refusal stops the
step whole.

**Closes when:** the refusal's detail carries the unmirrored lines too.
Ledger only.
