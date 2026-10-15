---
title: A heart the product made and the author un-hearted on the account is never hearted again, while All Favorites keeps it
found: at the build of #325, U146, 2026-10-15.
issue: no
---

**The mechanism.** The 2026-10-14 plan's R6 says an un-hearted track still in
All Favorites is hearted again by the next outbound pass. `hearts.heart_back`
counts a remote identifier as already hearted when the outbound ledger holds
it (`remote in known or account.has_heart(remote)`), so a heart this product
made once, then taken back by the author on the account, reads as already
there and is never sent again. A heart the author made on the account is in
no ledger and is hearted again, which
`test_a_favourite_un_hearted_on_the_account_is_hearted_again_and_nothing_is_removed`
drives. `hearts.py` was read only in this unit, so the ledger rule stands.

**Measured cost.** Read from the source, not driven against the account. The
two sides then disagree for the one class of track the product hearted: in
All Favorites in rekordbox and not hearted on the account, until the author
hearts it by hand or takes it out of All Favorites.

**Closes when:** the author decides whether the ledger should yield to a
listing that lacks the heart (R6 as written) or whether a heart the product
made and the author took back stays taken back on the account; ledger only
until then.
