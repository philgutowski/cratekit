---
title: A pair's row held as two releases keys on the lowest numbered release ever linked, so a remove and re-add cycle brings back the release the person dropped, and releases already held ignore the heart
found: at the review of #498, U208, 2026-11-05, round two.
issue: no
---

**The mechanism.** `sync/pair_cli.plan_pair` reads every account release
linked to one rekordbox row as that row's one key, the lowest numbered linked
release's (`by_row`, `_lower`). Links are kept while the row lives in the
collection, so the canonical release is the lowest of every link ever made,
with no memory of which release the person kept or hearted. The same rule
chooses among two or more unlinked releases the account already holds
(`held_there`), and it never asks whether one is hearted.

**Measured cost.** Driven by the review: links to 101 and 202, the person
drops 101 and keeps 202, later the row leaves rekordbox and both leave the
account, then the row is put back in rekordbox: the account gains 101, not
202. Same with a heart: hearted 202 linked first, 101 added by hand, after a
remove and re-add cycle the account gets 101. Both releases agree with the
row; nothing is lost and nothing false is said. Which held release is taken
is unpinned by the suite (the add loop links the other release either way).

**Closes when:** the canonical release prefers a linked release the account
still holds, and then a hearted one, before the number, or a link the account
lost is dropped once the row's other release stays; and a test pins which of
two held releases is taken. Ledger only: a preference between agreeing
releases, reachable only through a remove and re-add cycle.
