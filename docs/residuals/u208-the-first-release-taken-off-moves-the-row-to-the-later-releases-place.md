---
title: Taking a pair's first release of a row off the account while a later release stays moves the row in rekordbox to the later release's place
found: at the review of #498, U208, 2026-11-05, round two.
issue: no
---

**The mechanism.** A row held on the account as two releases is one key in
the merge, and a key's place on the account side is its first occurrence.
When the earlier release is taken off and the later stays, the key's place
moves to the later release's, and rekordbox follows the account's order.

**Measured cost.** Driven: rekordbox (1, 2, 3), account [101, 92, 93, 202];
the person removes 101; the sync reorders rekordbox to [2, 3, 1], then stays.
No track is lost and the account's visible order is mirrored faithfully;
whether the row should keep its place is a judgment the brief does not make.
`test_the_first_release_taken_off_while_a_later_one_stays_keeps_the_row`
pins that the row stays, not its place.

**Closes when:** the brief says whether a row's place survives the removal of
one of its releases; if it should, the key's place is the place of the
release the base held first. Ledger only.
