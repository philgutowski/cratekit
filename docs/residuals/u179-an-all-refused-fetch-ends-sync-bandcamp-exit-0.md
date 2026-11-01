---
title: A sync bandcamp whose every release the fetch refused ends exit 0, no_op, where the fetch alone exits non zero
found: at the first Fable review of #360, U179, 2026-11-01.
issue: no
---

**The mechanism.** `crate sync bandcamp` reads a fetch that failed only by refusals for good (a lossy only release under the strict policy above all) as settled, the way `sync land` skips a lossy download, and goes on with what was staged. When nothing was staged it ends `no_op` with exit 0. `crate acquire bandcamp-fetch` alone ends the same job with its failed state's refusal.

**Measured cost.** Driven by `test_a_release_refused_for_good_is_recorded_and_nothing_is_landed_over_none`: the envelope names each refused release in `fetch_refused`, in a `sync-bandcamp-fetch-refused` warning and on a `fail` check row, so nothing false is said, but a caller reading only the exit code is not told. `sync land` over an all refused download carries the same shape (U152's residual).

**Closes when:** the verb ends with the fetch's own refusal when every release it attempted was refused and nothing was staged, or the record states exit 0 as the contract. Ledger only.
